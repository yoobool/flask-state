/** @license flask-state
 * flask-state.js
 *
 * Copyright (c) 2020, yoobool
 *
 * This source code is licensed under the BSD-3 license found in the
 * LICENSE file in the root directory of this source tree.
 */

'use strict';



(function () {
    'use strict';

    const ONE_MIN_SECONDS = 60;
    const ONE_DAY_HOURS = 24;
    const MACHINE_VALUE = {
        DANGER: 85,
        WARNING: 75,
    };
    const LOADAVG_VALUE = {
        DANGER: 10,
        WARNING: 5,
    };

    const BIT_TO_MB = 1048576;
    const SECONDS_TO_MILLISECONDS = 1000;

    class MachineStatus {
        constructor(language) {
            this.language = language;
            this.mobile = MachineStatus.isMobile();
            this.index = 0;
            this.ajax = new Ajax();
            this.initFlaskStateContainer(this.mobile);
            this.setEventListener();
            this.initFlaskStateLanguage(this.language);
            this.setInitParams();
            if (this.mobile) {
                this.setTagChangeEventListener(this.consoleCpuChart, this.consoleMemoryChart, this.consoleLoadavgChart, this.consoleDiskusageChart);
            }
            // Bind window resizing redraw event
            window.addEventListener('resize', () => {
                MachineStatus.resizeChartTimer([this.consoleMemoryChart, this.consoleCpuChart, this.consoleLoadavgChart, this.consoleDiskusageChart]);
            })
        };

        setFlaskStateData() {
            document.getElementById('fs-info-back').style.display = 'block';
            document.getElementById('fs-info-container').style.display = 'block';
            document.getElementsByTagName('body')[0].style.overflowX = 'hidden';
            document.getElementsByTagName('body')[0].style.overflowY = 'hidden';
            document.getElementById('fs-select-days').value = '1';
            this.setCharts('1');
        }

        /* Insert window element */
        initFlaskStateContainer() {
            let str = '<div class="flask-state-elem layer console-info-back-style" id="fs-info-back" disabled="disabled" xmlns="http://www.w3.org/1999/html">' +
                '</div>' +
                '<div class="flask-state-elem ">' +
                '<div class="flask-state-elem console-info-container-style console-info-container-box box-style " id="fs-info-container">' +
                '<div class="flask-state-elem fs-select-container">' +
                '<svg t="1604570316831" class="icon fs-select-arrow" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3994" width="16" height="16" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><style type="text/css"></style></defs><path d="M524.736 548.256l181.248-181.248a51.264 51.264 0 1 1 72.48 72.512l-217.472 217.472a51.264 51.264 0 0 1-72.512 0L271.04 439.52a51.264 51.264 0 1 1 72.512-72.512l181.216 181.248z" fill="#161e2e" p-id="3995"></path></svg>' +
                '<select id="fs-select-days" class="margin-right-5 fs-select-days">' +
                '<option value="1">1</option><option value="3">3</option><option value="7">7</option><option value="30">30</option></select><span id="fs-days">days</span></div>' +
                '<button type="button" class="flask-state-elem console-info-close-style" id="fs-info-close">' +
                '<svg t="1604544405227" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3278" width="32" height="32" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><style type="text/css"></style></defs><path d="M572.16 512l183.466667-183.04a42.666667 42.666667 0 1 0-60.586667-60.586667L512 451.84l-183.04-183.466667a42.666667 42.666667 0 0 0-60.586667 60.586667l183.466667 183.04-183.466667 183.04a42.666667 42.666667 0 0 0 0 60.586667 42.666667 42.666667 0 0 0 60.586667 0l183.04-183.466667 183.04 183.466667a42.666667 42.666667 0 0 0 60.586667 0 42.666667 42.666667 0 0 0 0-60.586667z" p-id="3279" fill="#161e2e"></path></svg>' +
                '</button>' +
                '<h4 id="fs-host-status-title" class="flask-state-elem fs-font-box box-style no-padding margin-top-10 fs-h4-style">host status</h4>' +
                '<div id="fs-host-status" class="flask-state-elem fs-font-box box-style no-padding">' +
                '<div class="inline-block"><div id="fs-memory" class="b-0079cc fs-state-right-badge">memory:</div><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-18"></span></div>' +
                '<div class="inline-block"><div id="fs-cpu" class="b-0079cc fs-state-right-badge">cpu:</div><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-18"></span></div>' +
                '<div class="inline-block"><div id="fs-disk-usage" class="b-0079cc fs-state-right-badge">disk usage:</div><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-18"></span></div>' +
                '<div class="inline-block"><div id="fs-load-avg" class="b-007dc8 fs-state-right-badge">LoadAvg:</div><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-18"></span></div>' +
                '<div class="inline-block"><div id="fs-boot-seconds" class="b-0051b9 fs-state-right-badge">boot seconds:</div><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-18"></span></div>' +
                '</div>' +
                '<h4 id="fs-redis-status-title" class="flask-state-elem fs-font-box box-style no-padding fs-h4-style">redis status</h4>' +
                '<div id="fs-redis-status" class="flask-state-elem fs-font-box box-style no-padding margin-bottom-10 ">' +
                '<div class="inline-block"><div id="fs-used-memory" class="b-99cb3d fs-state-right-badge">used memory:</div><span class="flask-state-elem background-green fs-badge-style margin-top-m3 console-info-memory-text margin-right-18"></span></div>' +
                '<div class="inline-block"><div id="fs-used-memory-rss" class="b-99cb3d fs-state-right-badge">used memory rss:</div><span class="flask-state-elem background-green fs-badge-style margin-top-m3 console-info-memory-text margin-right-18"></span></div>' +
                '<div class="inline-block"><div id="fs-mem-fragmentation-ratio" class="b-534c6d fs-state-right-badge">mem fragmentation ratio:</div><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-18"></span></div>' +
                '<div class="inline-block"><div id="fs-hits-ratio" class="b-0079cc fs-state-right-badge">hits ratio:</div><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-18"></span></div>' +
                '<div class="inline-block"><div id="fs-delta-hits-ratio" class="b-0079cc fs-state-right-badge">24h hits ratio:</div><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-18"></span></div>' +
                '<div class="inline-block"><div id="fs-uptime-in-seconds" class="b-0051b9 fs-state-right-badge">uptime in seconds:</div><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-18"></span></div>' +
                '<div class="inline-block"><div id="fs-connected-clients" class="b-534c6d fs-state-right-badge">connected clients:</div><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-18"></span></div>' +
                '</div>';
            if (this.mobile) {
                str += '<hr id="console-info-line" class="console-info-line-style">' +
                    '<div class="flask-state-elem fs-ul-tabs-box no-margin ">' +
                    '<ul id="fs-info-tab" class="flask-state-elem fs-ul-tabs">' +
                    '<li class="flask-state-elem active"><a href="#console_info_tab_memory" data-toggle="tab">' +
                    '<strong>memory</strong></a></li>' +
                    '<li class="flask-state-elem"><a href="#console_info_tab_cpu" data-toggle="tab">' +
                    '<strong>cpu</strong></a></li>' +
                    '<li class="flask-state-elem"><a href="#console_info_tab_diskusage" data-toggle="tab">' +
                    '<strong>disk usage</strong></a></li>' +
                    '<li class="flask-state-elem"><a href="#console_info_tab_loadavg" data-toggle="tab">' +
                    '<strong>LoadAvg</strong></a></li>' +
                    '</ul>' +
                    '<div class="flask-state-elem form-group no-margin ">' +
                    '<div class="flask-state-elem state-tab-content ">' +
                    '<div id="fs-info-tab-memory" class="flask-state-elem state-tab-pane fs-show">' +
                    '<div class="fs-mobile-chart-container">' +
                    '<div id="fs-info-memory-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                    '</div>' +
                    '</div>' +
                    '<div id="fs-info-tab-cpu" class="flask-state-elem state-tab-pane ">' +
                    '<div class="fs-mobile-chart-container">' +
                    '<div id="fs-info-cpu-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                    '</div>' +
                    '</div>' +
                    '<div id="fs-info-tab-disk-usage" class="flask-state-elem state-tab-pane ">' +
                    '<div class="fs-mobile-chart-container">' +
                    '<div id="fs-info-diskusage-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                    '</div>' +
                    '</div>' +
                    '<div id="fs-info-tab-loadavg" class="flask-state-elem state-tab-pane">' +
                    '<div class="fs-mobile-chart-container">' +
                    '<div id="fs-info-loadavg-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>';
            } else {
                str += "<div class='fs-chart-content'><div class='flask-state-elem fs-charts-box box-style no-padding console-info-border-r'><div class='flask-state-elem charts-box-info'>" +
                    "<div id='fs-info-memory-chart' class='flask-state-elem margin-top-10 fs-chart-style'></div>" +
                    "</div>" +
                    "</div>" +
                    "<div class='flask-state-elem fs-charts-box box-style no-padding '>" +
                    "<div class='flask-state-elem charts-box-info'>" +
                    "<div id='fs-info-cpu-chart' class='flask-state-elem margin-top-10 fs-chart-style'></div>" +
                    "</div>" +
                    "</div>" +
                    "<div class='flask-state-elem fs-charts-box box-style no-padding console-info-border-r '>" +
                    "<div class='flask-state-elem charts-box-info'>" +
                    "<div id='fs-info-diskusage-chart' class='flask-state-elem margin-top-10 fs-chart-style'></div>" +
                    "</div>" +
                    "</div>" +
                    "<div class='flask-state-elem fs-charts-box box-style no-padding'>" +
                    "<div class='flask-state-elem charts-box-info'>" +
                    "<div id='fs-info-loadavg-chart' class='flask-state-elem margin-top-10 fs-chart-style'></div>" +
                    "</div>" +
                    "</div>" +
                    "</div>" +
                    "</div></div>";
            }
            document.getElementsByTagName('body')[0].insertAdjacentHTML('beforeend', str);
        }

        // add EventListener
        setEventListener() {
            if (window.addEventListener) {
                document.getElementById('fs-info-close').addEventListener('click', function clickClose() {
                    document.getElementById('fs-info-back').style.display = 'none';
                    document.getElementById('fs-info-container').style.display = 'none';
                    document.getElementsByTagName('body')[0].style.overflowX = 'auto';
                    document.getElementsByTagName('body')[0].style.overflowY = 'auto';
                    if (document.getElementById('fs-state-circular')) {
                        document.getElementById('fs-state-circular').classList.remove('fs-circular-out');
                    }
                });

                document.getElementById('fs-info-back').addEventListener('click', function clickBack() {
                    document.getElementById('fs-info-back').style.display = 'none';
                    document.getElementById('fs-info-container').style.display = 'none';
                    document.getElementsByTagName('body')[0].style.overflowX = 'auto';
                    document.getElementsByTagName('body')[0].style.overflowY = 'auto';
                    if (document.getElementById('fs-state-circular')) {
                        document.getElementById('fs-state-circular').classList.remove('fs-circular-out');
                    }
                });

                // Pull the local state again when switching days
                let selectContainer = document.getElementById('fs-select-days');
                selectContainer.addEventListener('change', () => {
                    this.setCharts(selectContainer.value);
                })

            }
        }

        /* add mobile changeTag EventListener */
        setTagChangeEventListener(...chartList) {
            // Bind mobile phone to switch to display charts event
            if (document.getElementById('fs-info-tab')) {
                let liArr = document.getElementById('fs-info-tab').getElementsByTagName('li');
                let preNode = document.getElementById('fs-info-tab-memory');
                let node_li = liArr[0];
                let index = 0;
                const elemDict = {
                    0: 'fs-info-tab-memory',
                    1: 'fs-info-tab-cpu',
                    2: 'fs-info-tab-disk-usage',
                    3: 'fs-info-tab-loadavg'
                };
                for (let item of liArr) {
                    let nowNode = document.getElementById(elemDict[index]);
                    item.children[0].addEventListener('click', () => {
                        item.classList.add('active');
                        node_li.classList.remove('active');
                        preNode.classList.remove('fs-show');
                        nowNode.classList.add('fs-show');
                        MachineStatus.resizeChart(chartList);
                        preNode = nowNode;
                        node_li = item;
                    });
                    index++;
                }
            }
        }

        /* set flask-state show language */
        initFlaskStateLanguage() {
            // Modify parameter display language
            if (Object.keys(this.language).length !== 0) {
                document.getElementById('fs-host-status-title').innerHTML = this.language.host_status;
                document.getElementById('fs-redis-status-title').innerHTML = this.language.redis_status;
                document.getElementById('fs-cpu').innerHTML = this.language.cpu;
                document.getElementById('fs-memory').innerHTML = this.language.memory;
                document.getElementById('fs-disk-usage').innerHTML = this.language.disk_usage;
                document.getElementById('fs-load-avg').innerHTML = this.language.load_avg;
                document.getElementById('fs-boot-seconds').innerHTML = this.language.boot_seconds;
                document.getElementById('fs-used-memory').innerHTML = this.language.used_memory;
                document.getElementById('fs-used-memory-rss').innerHTML = this.language.used_memory_rss;
                document.getElementById('fs-mem-fragmentation-ratio').innerHTML = this.language.mem_fragmentation_ratio;
                document.getElementById('fs-hits-ratio').innerHTML = this.language.hits_ratio;
                document.getElementById('fs-delta-hits-ratio').innerHTML = this.language.delta_hits_ratio;
                document.getElementById('fs-uptime-in-seconds').innerHTML = this.language.uptime_in_seconds;
                document.getElementById('fs-connected-clients').innerHTML = this.language.connected_clients;
                document.getElementById('fs-days').innerHTML = this.language.days;
            }
        }

        /* set flask-state init params */
        setInitParams() {
            this.consoleCpuChart = echarts.init(document.getElementById('fs-info-cpu-chart'), null, {renderer: 'svg'});
            this.consoleMemoryChart = echarts.init(document.getElementById('fs-info-memory-chart'), null, {renderer: 'svg'});
            this.consoleLoadavgChart = echarts.init(document.getElementById('fs-info-loadavg-chart'), null, {renderer: 'svg'});
            this.consoleDiskusageChart = echarts.init(document.getElementById('fs-info-diskusage-chart'), null, {renderer: 'svg'});
            this.cpuOption = MachineStatus.generateChatOption(this.mobile, this.language.cpu || 'CPU', '', this.language.today || 'today');
            this.memoryOption = MachineStatus.generateChatOption(this.mobile, this.language.memory || 'Memory', '', this.language.today || 'today');
            this.diskUsageOption = MachineStatus.generateChatOption(this.mobile, this.language.disk_usage || 'DiskUsage', '', this.language.today || 'today');
            this.loadavgOption = MachineStatus.generateChatOption(this.mobile, 'Load Avg', 'loadavg', this.language.minutes || 'min');
        }

        /* Define functions that access native state and plot */
        setCharts(days) {
            this.consoleCpuChart.showLoading();
            this.consoleMemoryChart.showLoading();
            this.consoleLoadavgChart.showLoading();
            this.consoleDiskusageChart.showLoading();
            this.ajax.send({
                type: 'POST',
                url: '/v0/state/hoststatus',
                data: {'timeQuantum': days},
                success: response => {
                    const fields = ["ts", "cpu", "memory", "load_avg", "disk_usage"];
                    const data = response.data;
                    data.items = data.items.map(item => {
                        let element = {};
                        fields.forEach((field, index) => {
                            if (field === "ts") return element[field] = SECONDS_TO_MILLISECONDS * item[index];
                            element[field] = item[index];
                        });
                        return element;
                    });
                    let currentStatistic = data.currentStatistic;
                    if (Object.keys(currentStatistic).length) {
                        let hostInfoSpan = document.getElementById('fs-host-status').getElementsByClassName('fs-badge-style');
                        hostInfoSpan[0].innerHTML = currentStatistic.memory + '%';
                        hostInfoSpan[1].innerHTML = currentStatistic.cpu + '%';
                        hostInfoSpan[2].innerHTML = currentStatistic.disk_usage + '%';
                        hostInfoSpan[3].innerHTML = currentStatistic.load_avg[0] + "，" + currentStatistic.load_avg[1] + "，" + currentStatistic.load_avg[2];
                        if (currentStatistic.boot_seconds)
                            hostInfoSpan[4].innerHTML = MachineStatus.getFormatSeconds(currentStatistic.boot_seconds, this.language.days, this.language.hours, this.language.minutes, this.language.seconds);

                        const machineIndex = ['memory', 'cpu', 'disk_usage', 'load_avg'];
                        machineIndex.forEach(function (item, index) {
                            let paramClass = '';
                            if (item === 'load_avg') {
                                let loadavgAvg = (currentStatistic.load_avg[0] + currentStatistic.load_avg[1] + currentStatistic.load_avg[2]) / 3;
                                paramClass = loadavgAvg >= LOADAVG_VALUE.WARNING ? loadavgAvg >= LOADAVG_VALUE.DANGER ? 'background-red' : 'background-orange' : 'background-green';
                            } else {
                                paramClass = currentStatistic[item] >= MACHINE_VALUE.WARNING ? currentStatistic.memory >= MACHINE_VALUE.DANGER ? 'background-red' : 'background-orange' : 'background-green';
                            }
                            let param = hostInfoSpan[index].classList;
                            param.remove('background-green', 'background-orange', 'background-red');
                            param.add(paramClass);
                        });

                        let hostInfoExtendSpan = document.getElementById('fs-redis-status').getElementsByClassName('fs-badge-style');
                        let hostInfoKeysList = ['used_memory', 'used_memory_rss', 'mem_fragmentation_ratio', 'hits_ratio', 'delta_hits_ratio', 'uptime_in_seconds', 'connected_clients'];
                        let hideRedis = true
                        for (let item of hostInfoKeysList) {
                            if (currentStatistic[item]) {
                                hideRedis = false
                                break
                            }
                        }
                        if (hideRedis) {
                            document.getElementById('fs-redis-status-title').innerHTML = '';
                            document.getElementById('fs-redis-status-title').style.marginTop = '0';
                            document.getElementById('fs-redis-status').style.display = 'none';
                        } else {
                            hostInfoKeysList.forEach((item, index) => {
                                switch (item) {
                                    case 'used_memory':
                                        hostInfoExtendSpan[index].innerHTML = Math.ceil(currentStatistic[item] / BIT_TO_MB) + 'M';
                                        break;
                                    case 'used_memory_rss':
                                        hostInfoExtendSpan[index].innerHTML = Math.ceil(currentStatistic[item] / BIT_TO_MB) + 'M';
                                        break;
                                    case 'mem_fragmentation_ratio':
                                        let ratio = currentStatistic[item];
                                        hostInfoExtendSpan[index].innerHTML = currentStatistic[item];
                                        if (ratio !== null && ratio !== undefined && ratio > 1) {
                                            let hostInfoExtendSpanClass = hostInfoExtendSpan[index].classList;
                                            hostInfoExtendSpanClass.remove('background-green');
                                            hostInfoExtendSpanClass.add('background-red');
                                        }
                                        break;
                                    case 'hits_ratio':
                                        hostInfoExtendSpan[index].innerHTML = currentStatistic[item] + '%';
                                        break;
                                    case 'delta_hits_ratio':
                                        hostInfoExtendSpan[index].innerHTML = currentStatistic[item] + '%';
                                        break;
                                    case 'uptime_in_seconds':
                                        hostInfoExtendSpan[index].innerHTML = MachineStatus.getFormatSeconds(currentStatistic[item], this.language.days, this.language.hours, this.language.minutes, this.language.seconds);
                                        break;
                                    case 'connected_clients':
                                        hostInfoExtendSpan[index].innerHTML = currentStatistic[item];
                                }
                            });
                        }
                    }

                    data.items.reverse();
                    let dataMap = MachineStatus.getChartsData(data.items);

                    let tsList = dataMap.ts_list;
                    let cpuList = dataMap.cpu_list;
                    let memoryList = dataMap.memory_list;
                    let loadavgList = dataMap.load_avg_list[0];
                    let loadavg5MinList = dataMap.load_avg_list[1];
                    let loadavg15MinList = dataMap.load_avg_list[2];
                    let diskUsageList = dataMap.disk_usage_list;

                    this.memoryOption.xAxis.data = tsList;
                    this.cpuOption.xAxis.data = tsList;
                    this.loadavgOption.xAxis.data = tsList;
                    this.diskUsageOption.xAxis.data = tsList;

                    this.memoryOption.series[0].data = memoryList;
                    this.cpuOption.series[0].data = cpuList;
                    this.diskUsageOption.series[0].data = diskUsageList;
                    this.loadavgOption.series[0].data = loadavgList;
                    this.loadavgOption.series[1].data = loadavg5MinList;
                    this.loadavgOption.series[2].data = loadavg15MinList;

                    this.consoleMemoryChart.setOption(this.memoryOption);
                    this.consoleCpuChart.setOption(this.cpuOption);
                    this.consoleLoadavgChart.setOption(this.loadavgOption);
                    this.consoleDiskusageChart.setOption(this.diskUsageOption);
                    MachineStatus.resizeChart([this.consoleMemoryChart, this.consoleCpuChart, this.consoleLoadavgChart, this.consoleDiskusageChart]);
                },
                complete: () => {
                    this.consoleMemoryChart.hideLoading();
                    this.consoleCpuChart.hideLoading();
                    this.consoleLoadavgChart.hideLoading();
                    this.consoleDiskusageChart.hideLoading();
                },
            }).then();
        };

        /* Check if the device is a mobile phone */
        static isMobile() {
            let u = navigator.userAgent;
            let deviceBrowser = function () {
                return {
                    trident: u.indexOf('Trident') > -1,
                    presto: u.indexOf('Presto') > -1,
                    webKit: u.indexOf('AppleWebKit') > -1,
                    gecko: u.indexOf('Gecko') > -1 && u.indexOf('KHTML') === -1,
                    mobile: u.match(/AppleWebKit.*Mobile.*/) && true,
                    ios: u.match(/\(i[^;]+;( U;)? CPU.Mac OS X/) && true,
                    android: u.indexOf('Android') > -1 || u.indexOf('Linux') > -1,
                    iPhone: u.indexOf('iPhone') > -1,
                    iPad: u.indexOf('iPad') > -1,
                    webApp: u.indexOf('Safari') === -1,
                    wechat: u.indexOf('MicroMessenger') > -1,
                    qq: u.match(/\sQQ/i) && u.match(/\sQQ/i)[0] === " qq",
                }
            }();
            return deviceBrowser.iPhone || deviceBrowser.iPad || deviceBrowser.webApp || deviceBrowser.wechat
                || deviceBrowser.qq || deviceBrowser.ios || deviceBrowser.mobile || false;

        };

        /* Redraw chart events timer */
        static resizeChartTimer(myChart, timeout) {
            clearTimeout(this.clearId);
            this.clearId = setTimeout(function () {
                MachineStatus.resizeChart(myChart);
            }, timeout || 200)
        }

        /* Redraw chart events */
        static resizeChart(chartList) {
            chartList.forEach(chart => chart.resize());
        }

        /* Initialize echart */
        static generateChatOption(isMobile, titleText, tableName = '', lineName = '') {
            let baseData = {
                color: tableName === 'loadavg' ? ['#ffa726', '#42a5f5', '#66bb6a'] : ['#42a5f5'],
                title: {
                    show: !isMobile,
                    text: titleText
                },
                tooltip: {
                    trigger: 'axis',
                    formatter: (params) => {
                        let value = echarts.format.formatTime('yyyy-MM-dd hh:mm:ss', new Date(parseInt(params[0].axisValue)), false) + '<br />';
                        for (let i = 0; i < params.length; i++) {
                            value += (params[i].marker + params[i].seriesName + ': ' + params[i].value +
                                (tableName === 'loadavg' ? '' : '%') + '<br />')
                        }
                        return value;
                    }
                },
                legend: {
                    data: [lineName],
                    textStyle: {
                        fontSize: 14
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    top: isMobile ? 30 : 60,
                    containLabel: true
                },
                toolbox: {
                    show: !isMobile,
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    axisLabel: {
                        formatter: function (value) {
                            return echarts.format.formatTime('hh:mm', new Date(parseInt(value)), false);
                        }
                    }
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: lineName,
                        type: 'line',
                        symbol: 'none',
                        hoverAnimation: false
                    }
                ]
            };
            if (tableName === 'loadavg') {
                baseData.legend.data = ['1' + lineName, '5' + lineName, '15' + lineName];
                baseData.series = [];
                baseData.legend.data.forEach((name) => {
                    baseData.series.push({
                        name: name,
                        type: 'line',
                        symbol: 'none',
                        hoverAnimation: false
                    });
                });
            }
            return baseData;
        }

        /* Get Echarts data */
        static getChartsData(rawData) {
            let cpuList = [];
            let diskUsageList = [];
            let loadAvgList = [];
            let loadAvg5minList = [];
            let loadAvg15minList = [];
            let memoryList = [];
            let tsList = [];
            for (let i = 0; i < rawData.length; i++) {
                let item = rawData[i];
                cpuList.push(item.cpu);
                diskUsageList.push(item.disk_usage);
                loadAvgList.push(item.load_avg[0]);
                loadAvg5minList.push(item.load_avg[1]);
                loadAvg15minList.push(item.load_avg[2]);
                memoryList.push(item.memory);
                tsList.push(item.ts);
            }
            return {
                'cpu_list': cpuList, 'disk_usage_list': diskUsageList,
                'load_avg_list': [loadAvgList, loadAvg5minList, loadAvg15minList],
                'memory_list': memoryList, 'ts_list': tsList
            };
        };

        /* Get format time */
        static getFormatSeconds(value, days = 'days', hours = 'hours', minutes = 'min', seconds = 'seconds') {
            let secondTime = parseInt(value);
            let minuteTime = 0;
            let hourTime = 0;
            let dayTime = 0;
            let result = "";
            if (secondTime >= ONE_MIN_SECONDS) {
                minuteTime = secondTime / ONE_MIN_SECONDS;
                if (minuteTime >= ONE_MIN_SECONDS) {
                    hourTime = minuteTime / ONE_MIN_SECONDS;
                    minuteTime = minuteTime % ONE_MIN_SECONDS;
                }
                if (hourTime >= ONE_DAY_HOURS) {
                    dayTime = hourTime / ONE_DAY_HOURS;
                    hourTime = hourTime % ONE_DAY_HOURS;
                }
            } else {
                result = secondTime + seconds;
            }
            if (minuteTime > 0) {
                result = Math.floor(minuteTime) + minutes;
            }
            if (hourTime > 0) {
                result = Math.floor(hourTime) + hours;
            }
            if (dayTime > 0) {
                result = Math.floor(dayTime) + days;
            }
            return result;
        };
    }

    /* Native Ajax classes */
    class Ajax {
        constructor(xhr) {
            xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
            this.xhr = xhr;
        }

        send(options) {

            let xhr = this.xhr;

            let opt = {
                type: options.type || 'get',
                url: options.url || '',
                async: options.async || true,
                data: JSON.stringify(options.data),
                dataType: options.dataType || 'json',
                contentType: 'application/json',
                success: options.success || null,
                complete: options.complete || null
            };


            return new Promise((resolve, reject) => {
                xhr.open(opt.type, opt.url, opt.async);
                xhr.onreadystatechange = () => {
                    // readyState: 0: init, 1: connect has set up, 2: recive request, 3: request.. , 4: request end, send response
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            // status: 200: OK,  404: Not Found Page
                            if (opt.dataType === 'json') {
                                const data = JSON.parse(xhr.responseText);
                                resolve(data);
                                if (opt.success !== null) {
                                    opt.success(data);
                                } else {
                                    reject(new Error(String(xhr.status) || 'No callback function.'));
                                }
                            }
                        } else {
                            reject(new Error(String(xhr.status) || 'Server is fail.'));
                        }
                    }
                };

                xhr.onerror = () => {
                    reject(new Error(String(xhr.status) || 'Server is fail.'));
                };

                xhr.setRequestHeader("Content-type", opt.contentType);
                xhr.send(opt.data);
                xhr.onloadend = () => {
                    if (opt.complete != null) {
                        opt.complete();
                    }
                };
            });
        }
    }

    /* singleton */
    const FlaskStateInstance = (function () {
        let instance = null;
        return function (language) {
            return instance || (instance = new MachineStatus(language))
        }
    })();

    /* Trigger window event */
    function Init(initMap) {
        let targetDom = null;
        let language = {};
        if (initMap !== null && typeof initMap === 'object') {
            targetDom = initMap.hasOwnProperty('dom') ? initMap.dom : null;
            language = initMap.hasOwnProperty('lang') ? initMap['lang'].hasOwnProperty('language') ? initMap['lang'] : {} : {};
        }

        if (targetDom instanceof HTMLElement) {
            if (targetDom.getAttribute('flaskState')) return;
            targetDom.setAttribute('flaskState', "true");
            targetDom.addEventListener('click', () => FlaskStateInstance(language).setFlaskStateData());
        } else {
            if (document.getElementById('fs-state-circular')) return;
            let str = "<div id='fs-state-circular' class='fs-circular fs-circular-animation' style='border-radius:100px;opacity:0.3;border:2px solid purple;'></div>";
            let domBody = document.getElementsByTagName('body')[0];
            domBody.insertAdjacentHTML('beforeend', str);
            let triggerCircular = document.getElementById('fs-state-circular');
            triggerCircular.onclick = function () {
                this.classList.add('fs-circular-out');
                FlaskStateInstance(language).setFlaskStateData();
            };
            let timeOutId;
            let mousePosition;
            triggerCircular.onmousedown = function (downEvent) {
                mousePosition = mousePosition || downEvent.clientY;
                triggerCircular.classList.remove('fs-circular-animation');
                timeOutId = setTimeout(function () {
                    triggerCircular.style.cursor = 'move';
                    domBody.style.cursor = 'move';
                    domBody.onmousemove = function (moveEvent) {
                        triggerCircular.style.top = Math.max(moveEvent.clientY - mousePosition + 300, 20) + 'px';
                    }
                }, 1500)
            };
            domBody.onmouseup = function () {
                triggerCircular.style.cursor = 'pointer';
                triggerCircular.classList.add('fs-circular-animation');
                domBody.onmousemove = null;
                this.style.cursor = 'default';
                clearTimeout(timeOutId);
            };
            triggerCircular.ontouchstart = function (downEvent) {
                mousePosition = mousePosition || downEvent.clientY;
                triggerCircular.classList.remove('fs-circular-animation');
                timeOutId = setTimeout(function () {
                    triggerCircular.style.cursor = 'move';
                    domBody.style.cursor = 'move';
                    domBody.ontouchmove = function (moveEvent) {
                        triggerCircular.style.top = Math.max(moveEvent.clientY - mousePosition + 300, 20) + 'px';
                    }
                }, 1500)
            };
            domBody.ontouchend = function () {
                triggerCircular.style.cursor = 'pointer';
                triggerCircular.classList.add('fs-circular-animation');
                domBody.ontouchmove = null;
                this.style.cursor = 'default';
                clearTimeout(timeOutId);
            };
        }
    }

    exports.init = Init;
})();