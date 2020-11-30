/** @license flask-state
 * flask-state.js
 *
 * Copyright (c) 2020, yoobool
 *
 * This source code is licensed under the BSD-3 license found in the
 * LICENSE file in the root directory of this source tree.
 */

'use strict';


(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports) :
        typeof define === 'function' && define.amd ? define(factory) :
            (factory((global.flaskState = {})));
}(this, (function (exports) {
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
            document.getElementById('fs-background').style.display = 'block';
            document.getElementById('fs-info-container').style.display = 'block';
            document.getElementsByTagName('body')[0].style.overflowX = 'hidden';
            document.getElementsByTagName('body')[0].style.overflowY = 'hidden';
            document.getElementById('fs-select-days').value = '1';
            this.setCharts('1');
        }

        /* Insert window element */
        initFlaskStateContainer() {
            let _chart = this.mobile ? `<hr id="console-info-line" class="console-info-line-style"><ul id="fs-info-tab" class="fs-ul-tabs"><li class="active"><a data-toggle="tab"> <strong>Memory</strong></a></li> <li><a data-toggle="tab"><strong>CPU</strong></a></li><li><a data-toggle="tab"><strong>Disk Usage</strong></a></li><li><a data-toggle="tab"><strong>Load Avg</strong></a></li></ul><div id="fs-info-tab-memory" class="fs-mChart-box fs-show"><div id="fs-info-memory-chart" class="fs-chart-style"></div></div><div id="fs-info-tab-cpu" class="fs-mChart-box"><div id="fs-info-cpu-chart" class="fs-chart-style"></div></div><div id="fs-info-tab-disk-usage" class="fs-mChart-box"><div id="fs-info-diskusage-chart" class="fs-chart-style"></div></div><div id="fs-info-tab-loadavg" class="fs-mChart-box"><div id="fs-info-loadavg-chart" class="fs-chart-style"></div></div>`
                : `<div class='fs-chart-content'><div class='fs-charts-width fs-charts-box fs-border'><div id='fs-info-memory-chart' class='fs-chart-style'></div></div><div class='fs-charts-width fs-charts-box'><div id='fs-info-cpu-chart' class='fs-chart-style'></div></div><div class='fs-charts-width fs-charts-box fs-border'><div id='fs-info-diskusage-chart' class='fs-chart-style'></div></div><div class='fs-charts-width fs-charts-box'><div id='fs-info-loadavg-chart' class='fs-chart-style'></div></div></div>`;
            let _content = `<div class="flask-state-elem fs-background" id="fs-background"><div class="fs-container-width fs-container" id="fs-info-container"><div class="fs-select-container"><svg class="fs-select-arrow" viewBox="0 0 1024 1024" version="1.1" width="29" height="17"><path d="M524.736 548.256l181.248-181.248a51.264 51.264 0 1 1 72.48 72.512l-217.472 217.472a51.264 51.264 0 0 1-72.512 0L271.04 439.52a51.264 51.264 0 1 1 72.512-72.512l181.216 181.248z" fill="#161e2e"></path></svg><select id="fs-select-days" class="fs-select-days"><option value="1">1</option><option value="3">3</option><option value="7">7</option><option value="30">30</option></select><p id="fs-days" class="fs-days"> days</p></div><button type="button" class="fs-close" id="fs-info-close"><svg viewBox="0 0 1024 1024" version="1.1" width="24" height="24"><path d="M572.16 512l183.466667-183.04a42.666667 42.666667 0 1 0-60.586667-60.586667L512 451.84l-183.04-183.466667a42.666667 42.666667 0 0 0-60.586667 60.586667l183.466667 183.04-183.466667 183.04a42.666667 42.666667 0 0 0 0 60.586667 42.666667 42.666667 0 0 0 60.586667 0l183.04-183.466667 183.04 183.466667a42.666667 42.666667 0 0 0 60.586667 0 42.666667 42.666667 0 0 0 0-60.586667z" fill="#161e2e"></path></svg></button><h4 id="fs-host-status-title" class="fs-h4-style">Host Status</h4><div id="fs-host-status"><div><span id="fs-memory" class="b-0079cc fs-badge-intro">Memory</span><span class="fs-badge-content background-green"></span></div><div><span id="fs-cpu" class="b-0079cc fs-badge-intro">CPU</span><span class="fs-badge-content background-green"></span></div><div><span id="fs-disk-usage" class="b-0079cc fs-badge-intro">Disk Usage</span><span class="fs-badge-content background-green"></span></div><div><span id="fs-load-avg" class="b-007dc8 fs-badge-intro">Load Avg</span><span class="fs-badge-content background-green"></span></div><div><span id="fs-boot-seconds" class="b-0051b9 fs-badge-intro">Uptime</span><span class="fs-badge-content background-green"></span></div></div><h4 id="fs-redis-status-title" class="fs-h4-style">Redis Status</h4><div id="fs-redis-status"><div><span id="fs-used-memory" class="b-99cb3d fs-badge-intro">Used Mem</span><span class="fs-badge-content background-green"></span></div><div><span id="fs-used-memory-rss" class="b-99cb3d fs-badge-intro">Used Mem Rss</span><span class="fs-badge-content background-green"></span></div><div><span id="fs-mem-fragmentation-ratio" class="b-534c6d fs-badge-intro">Mem Fragmentation Ratio</span><span class="fs-badge-content background-green"></span></div><div><span id="fs-hits-ratio" class="b-0079cc fs-badge-intro">Cache Hits Ratio</span><span class="fs-badge-content background-green"></span></div><div><span id="fs-delta-hits-ratio" class="b-0079cc fs-badge-intro">24h Hits Ratio</span><span class="fs-badge-content background-green"></span></div><div><span id="fs-uptime-in-seconds" class="b-0051b9 fs-badge-intro">Uptime</span><span class="fs-badge-content background-green"></span></div><div><span id="fs-connected-clients" class="b-534c6d fs-badge-intro">Connections</span><span class="fs-badge-content background-green"></span></div></div>` + _chart + `</div></div>`;
            document.getElementsByTagName('body')[0].insertAdjacentHTML('beforeend', _content);
        }

        // add EventListener
        setEventListener() {
            if (window.addEventListener) {
                document.getElementById('fs-info-close').addEventListener('click', function clickClose() {
                    document.getElementById('fs-background').style.display = 'none';
                    document.getElementById('fs-info-container').style.display = 'none';
                    document.getElementsByTagName('body')[0].style.overflowX = 'auto';
                    document.getElementsByTagName('body')[0].style.overflowY = 'auto';
                    if (document.getElementById('fs-state-circular')) {
                        document.getElementById('fs-state-circular').classList.remove('fs-circular-out');
                    }
                });

                document.getElementById('fs-background').addEventListener('click', function clickBack(e) {
                    if (String(e.target.id) === 'fs-background') {
                        document.getElementById('fs-background').style.display = 'none';
                        document.getElementById('fs-info-container').style.display = 'none';
                        document.getElementsByTagName('body')[0].style.overflowX = 'auto';
                        document.getElementsByTagName('body')[0].style.overflowY = 'auto';
                        if (document.getElementById('fs-state-circular')) {
                            document.getElementById('fs-state-circular').classList.remove('fs-circular-out');
                        }
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
            this.cpuOption = MachineStatus.generateChatOption(this.mobile, this.language.cpu || 'CPU', '', this.language.today || 'Today');
            this.memoryOption = MachineStatus.generateChatOption(this.mobile, this.language.memory || 'Memory', '', this.language.today || 'Today');
            this.diskUsageOption = MachineStatus.generateChatOption(this.mobile, this.language.disk_usage || 'Disk Usage', '', this.language.today || 'Today');
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
                    if (response.code !== 200) {
                        return;
                    }

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
                        let hostInfoSpan = document.getElementById('fs-host-status').getElementsByClassName('fs-badge-content');
                        hostInfoSpan[0].innerHTML = currentStatistic.memory + '%';
                        hostInfoSpan[1].innerHTML = currentStatistic.cpu + '%';
                        hostInfoSpan[2].innerHTML = currentStatistic.disk_usage + '%';
                        hostInfoSpan[3].innerHTML = currentStatistic.load_avg[0] + "，" + currentStatistic.load_avg[1] + "，" + currentStatistic.load_avg[2];

                        hostInfoSpan[4].innerHTML = MachineStatus.getFormatSeconds(currentStatistic.boot_seconds || 0, this.language.days, this.language.hours, this.language.minutes, this.language.seconds);

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

                        let hostInfoExtendSpan = document.getElementById('fs-redis-status').getElementsByClassName('fs-badge-content');
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
                                        hostInfoExtendSpan[index].innerHTML = Math.ceil(currentStatistic[item] / BIT_TO_MB) + ' M';
                                        break;
                                    case 'used_memory_rss':
                                        hostInfoExtendSpan[index].innerHTML = Math.ceil(currentStatistic[item] / BIT_TO_MB) + ' M';
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
                baseData.legend.data = ['1 ' + lineName, '5 ' + lineName, '15 ' + lineName];
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
                result = Math.floor(minuteTime) + ' ' + minutes;
            }
            if (hourTime > 0) {
                result = Math.floor(hourTime) + ' ' + hours;
            }
            if (dayTime > 0) {
                result = Math.floor(dayTime) + ' ' + days;
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
                    // readyState: 0: init, 1: connect has set up, 2: receive request, 3: request.. , 4: request end, send response
                    if (xhr.readyState === 4) {
                        // status: 200: OK,  401: Verification Failed, 404: Not Found Page
                        if (opt.dataType === 'json') {
                            const data = JSON.parse(xhr.responseText);
                            resolve(data);
                            if (opt.success !== null) {
                                opt.success(data);
                            } else {
                                reject(new Error(String(xhr.status) || 'No callback function.'));
                            }
                        } else {
                            reject(new Error(String(xhr.status) || 'Error data type.'));
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
            let str = "<div id='fs-state-circular' class='fs-circular' style='top:300px;border-radius:100px;opacity:0.3;border:2px solid purple;'></div>";
            let domBody = document.getElementsByTagName('body')[0];
            domBody.insertAdjacentHTML('beforeend', str);
            let triggerCircular = document.getElementById('fs-state-circular');
            triggerCircular.onclick = function () {
                this.classList.add('fs-circular-out');
                FlaskStateInstance(language).setFlaskStateData();
            };

            let mousePosition;

            function circularMove(moveEvent) {
                triggerCircular.style.top = moveEvent.clientY - mousePosition + 300 + 'px';
            }

            triggerCircular.onmousedown = function (downEvent) {
                mousePosition = mousePosition || downEvent.clientY;
                document.addEventListener("mousemove", circularMove);
            };

            document.onmouseup = function () {
                document.removeEventListener("mousemove", circularMove);
                const circularHeight = parseInt(triggerCircular.style.top);
                triggerCircular.classList.add("fs-circular-animation");
                triggerCircular.style.top = Math.min(Math.max(circularHeight, 50), window.screen.height - 200) + 'px';
                setTimeout(() => triggerCircular.classList.remove("fs-circular-animation"), 500);
            };
        }
    }

    exports.init = Init;
})));