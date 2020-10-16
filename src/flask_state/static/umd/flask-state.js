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
            this.mobile = isMobile();
            MachineStatus.initFlaskStateContainer(this.mobile);
            MachineStatus.setEventListener();
        };

        setFlaskStateData() {
            document.getElementById('fs-info-back').style.display = 'block';
            document.getElementById('fs-info-container').style.display = 'block';

            // Modify parameter display language
            if (Object.keys(this.language).length !== 0) {
                document.getElementById('fs-host-status-title').innerHTML = this.language.host_status + ':';
                document.getElementById('fs-redis-status-title').innerHTML = this.language.redis_status + ':';
                document.getElementById('fs-cpu').innerHTML = this.language.cpu + ':';
                document.getElementById('fs-memory').innerHTML = this.language.memory + ':';
                document.getElementById('fs-disk-usage').innerHTML = this.language.disk_usage + ':';
                document.getElementById('fs-load-avg').innerHTML = this.language.load_avg + ':';
                document.getElementById('fs-boot-seconds').innerHTML = this.language.boot_seconds + ':';
                document.getElementById('fs-used-memory').innerHTML = this.language.used_memory + ':';
                document.getElementById('fs-used-memory-rss').innerHTML = this.language.used_memory_rss + ':';
                document.getElementById('fs-mem-fragmentation-ratio').innerHTML = this.language.mem_fragmentation_ratio + ':';
                document.getElementById('fs-hits-ratio').innerHTML = this.language.hits_ratio + ':';
                document.getElementById('fs-delta-hits-ratio').innerHTML = this.language.delta_hits_ratio + ':';
                document.getElementById('fs-uptime-in-seconds').innerHTML = this.language.uptime_in_seconds + ':';
                document.getElementById('fs-connected-clients').innerHTML = this.language.connected_clients + ':';
                document.getElementById('fs-days').innerHTML = this.language.days;
            }

            let consoleCpuChart = echarts.init(document.getElementById('fs-info-cpu-chart'), null, {renderer: 'svg'});
            let consoleMemoryChart = echarts.init(document.getElementById('fs-info-memory-chart'), null, {renderer: 'svg'});
            let consoleLoadavgChart = echarts.init(document.getElementById('fs-info-loadavg-chart'), null, {renderer: 'svg'});
            let consoleDiskusageChart = echarts.init(document.getElementById('fs-info-diskusage-chart'), null, {renderer: 'svg'});

            let cpuOption = MachineStatus.generateChatOption(this.mobile, this.language.cpu || 'CPU', '', this.language.today);
            let memoryOption = MachineStatus.generateChatOption(this.mobile, this.language.memory || 'Memory', '', this.language.today);
            let diskUsageOption = MachineStatus.generateChatOption(this.mobile, this.language.disk_usage || 'DiskUsage', '', this.language.today);
            let loadavgOption = MachineStatus.generateChatOption(this.mobile, 'Load Avg', 'loadavg', this.language.minutes);

            let ajax = new Ajax();

            // Define functions that access native state and plot
            const setCharts = days => {
                consoleCpuChart.showLoading();
                consoleMemoryChart.showLoading();
                consoleLoadavgChart.showLoading();
                consoleDiskusageChart.showLoading();
                ajax.send({
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
                                hostInfoSpan[4].innerHTML = getFormatSeconds(currentStatistic.boot_seconds, this.language.days, this.language.hours, this.language.minutes, this.language.seconds);

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
                                        hostInfoExtendSpan[index].innerHTML = getFormatSeconds(currentStatistic[item], this.language.days, this.language.hours, this.language.minutes, this.language.seconds);
                                        break;
                                    case 'connected_clients':
                                        hostInfoExtendSpan[index].innerHTML = currentStatistic[item];
                                }
                            });
                        }

                        data.items.reverse();
                        let dataMap = getChartsData(data.items);

                        let tsList = dataMap.ts_list;
                        let cpuList = dataMap.cpu_list;
                        let memoryList = dataMap.memory_list;
                        let loadavgList = dataMap.load_avg_list[0];
                        let loadavg5MinList = dataMap.load_avg_list[1];
                        let loadavg15MinList = dataMap.load_avg_list[2];
                        let diskUsageList = dataMap.disk_usage_list;

                        memoryOption.xAxis.data = tsList;
                        cpuOption.xAxis.data = tsList;
                        loadavgOption.xAxis.data = tsList;
                        diskUsageOption.xAxis.data = tsList;

                        memoryOption.series[0].data = memoryList;
                        cpuOption.series[0].data = cpuList;
                        diskUsageOption.series[0].data = diskUsageList;
                        loadavgOption.series[0].data = loadavgList;
                        loadavgOption.series[1].data = loadavg5MinList;
                        loadavgOption.series[2].data = loadavg15MinList;

                        consoleMemoryChart.setOption(memoryOption);
                        consoleCpuChart.setOption(cpuOption);
                        consoleLoadavgChart.setOption(loadavgOption);
                        consoleDiskusageChart.setOption(diskUsageOption);
                        MachineStatus.resizeChart([consoleMemoryChart, consoleCpuChart, consoleLoadavgChart, consoleDiskusageChart]);
                    },
                    complete: () => {
                        consoleMemoryChart.hideLoading();
                        consoleCpuChart.hideLoading();
                        consoleLoadavgChart.hideLoading();
                        consoleDiskusageChart.hideLoading();
                    },
                }).then();
            };
            setCharts('1');

            // Bind window resizing redraw event
            window.onresize = () => MachineStatus.resizeChartTimer([consoleMemoryChart, consoleCpuChart, consoleLoadavgChart, consoleDiskusageChart]);
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
                        MachineStatus.resizeChart([consoleMemoryChart, consoleCpuChart, consoleLoadavgChart, consoleDiskusageChart]);
                        preNode = nowNode;
                        node_li = item;
                    });
                    index++;
                }
            }

            // Pull the local state again when switching days
            let selectContainer = document.getElementById('fs-select-days');
            selectContainer.addEventListener('change', () => {
                setCharts(selectContainer.value);
            })
        }

        // Redraw chart events timer
        static resizeChartTimer(myChart, timeout) {
            clearTimeout(this.clearId);
            this.clearId = setTimeout(function () {
                MachineStatus.resizeChart(myChart);
            }, timeout || 200)
        }

        // Redraw chart events
        static resizeChart(chartList) {
            chartList.forEach(chart => chart.resize());
        }

        // Insert window element
        static initFlaskStateContainer(isMobile) {
            let str = '<div class="flask-state-elem layer console-info-back-style" id="fs-info-back" disabled="disabled" xmlns="http://www.w3.org/1999/html">' +
                '</div>' +
                '<div class="flask-state-elem ">' +
                '<div class="flask-state-elem console-info-container-style console-info-container-box box-style " id="fs-info-container">' +
                '<div class="flask-state-elem fs-select-container"><select id="fs-select-days" class="margin-right-3">' +
                '<option value="1">1</option><option value="3">3</option><option value="7">7</option><option value="30">30</option></select><span id="fs-days">days</span></div>' +
                '<button type="button" class="flask-state-elem console-info-close-style" id="fs-info-close"><span>&times;</span></button>' +
                '<h4 id="fs-host-status-title" class="flask-state-elem fs-font-box box-style no-padding margin-top-10 fs-h4-style">host_status</h4>' +
                '<div id="fs-host-status" class="flask-state-elem fs-font-box box-style no-padding">' +
                '<span id="fs-memory" class="margin-right-5">memory:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
                '<span id="fs-cpu" class="margin-right-5">cpu:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
                '<span id="fs-disk-usage" class="margin-right-5">disk_usage:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
                '<span id="fs-load-avg" class="margin-right-5">LoadAvg:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
                '<span id="fs-boot-seconds" class="margin-right-5">boot_seconds:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
                '</div>' +
                '<h4 id="fs-redis-status-title" class="flask-state-elem fs-font-box box-style no-padding fs-h4-style">redis_status</h4>' +
                '<div id="fs-redis-status" class="flask-state-elem fs-font-box box-style no-padding margin-bottom-10 ">' +
                '<span id="fs-used-memory" class="margin-right-5">used_memory:</span><span class="flask-state-elem fs-badge-style margin-top-m3 no-padding fontsize-18 console-info-memory-text margin-right-10"></span>' +
                '<span id="fs-used-memory-rss" class="margin-right-5">used_memory_rss:</span><span class="flask-state-elem fs-badge-style margin-top-m3 no-padding fontsize-18 console-info-memory-text margin-right-10"></span>' +
                '<span id="fs-mem-fragmentation-ratio" class="margin-right-5">mem_fragmentation_ratio:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
                '<span id="fs-hits-ratio" class="margin-right-5">hits_ratio:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
                '<span id="fs-delta-hits-ratio" class="margin-right-5">24h_hits_ratio:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
                '<span id="fs-uptime-in-seconds" class="margin-right-5">uptime_in_seconds:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
                '<span id="fs-connected-clients" class="margin-right-5">connected_clients:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
                '</div>';
            if (isMobile) {
                str += '<hr id="console-info-line" class="console-info-line-style">' +
                    '<div class="flask-state-elem fs-ul-tabs-box no-margin ">' +
                    '<ul id="fs-info-tab" class="flask-state-elem fs-ul-tabs">' +
                    '<li class="flask-state-elem active"><a href="#console_info_tab_memory" data-toggle="tab">' +
                    '<strong>memory</strong></a></li>' +
                    '<li class="flask-state-elem"><a href="#console_info_tab_cpu" data-toggle="tab">' +
                    '<strong>cpu</strong></a></li>' +
                    '<li class="flask-state-elem"><a href="#console_info_tab_diskusage" data-toggle="tab">' +
                    '<strong>disk_usage</strong></a></li>' +
                    '<li class="flask-state-elem"><a href="#console_info_tab_loadavg" data-toggle="tab">' +
                    '<strong>LoadAvg</strong></a></li>' +
                    '</ul>' +
                    '<div class="flask-state-elem form-group no-margin ">' +
                    '<div class="flask-state-elem state-tab-content ">' +
                    '<div id="fs-info-tab-memory" class="flask-state-elem state-tab-pane fs-show">' +
                    '<div>' +
                    '<div id="fs-info-memory-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                    '</div>' +
                    '</div>' +
                    '<div id="fs-info-tab-cpu" class="flask-state-elem state-tab-pane ">' +
                    '<div>' +
                    '<div id="fs-info-cpu-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                    '</div>' +
                    '</div>' +
                    '<div id="fs-info-tab-disk-usage" class="flask-state-elem state-tab-pane ">' +
                    '<div>' +
                    '<div id="fs-info-diskusage-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                    '</div>' +
                    '</div>' +
                    '<div id="fs-info-tab-loadavg" class="flask-state-elem state-tab-pane">' +
                    '<div>' +
                    '<div id="fs-info-loadavg-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>';
            } else {
                str += "<div class='flask-state-elem fs-charts-box box-style no-padding console-info-border-r'><div class='flask-state-elem charts-box-info'>" +
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
                    "</div>";
            }
            document.getElementsByTagName('body')[0].insertAdjacentHTML('beforeend', str);
        }

        // add EventListener
        static setEventListener() {
            if (window.addEventListener) {
                document.getElementById('fs-info-close').addEventListener('click', function clickClose() {
                    document.getElementById('fs-info-back').style.display = 'none';
                    document.getElementById('fs-info-container').style.display = 'none';
                    if (document.getElementById('fs-state-circular')) {
                        document.getElementById('fs-state-circular').classList.remove('fs-circular-out');
                    }
                });

                document.getElementById('fs-info-back').addEventListener('click', function clickBack() {
                    document.getElementById('fs-info-back').style.display = 'none';
                    document.getElementById('fs-info-container').style.display = 'none';
                    if (document.getElementById('fs-state-circular')) {
                        document.getElementById('fs-state-circular').classList.remove('fs-circular-out');
                    }
                });

            }
        }

        // Initialize echart
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
                                    reject(new Error(xhr.status || 'No callback function.'));
                                }
                            }
                        } else {
                            reject(new Error(xhr.status || 'Server is fail.'));
                        }
                    }
                };

                xhr.onerror = () => {
                    reject(new Error(xhr.status || 'Server is fail.'));
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

    /* Get Echarts data */
    const getChartsData = (rawData) => {
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
    const getFormatSeconds = (value, days = 'days', hours = 'hours', minutes = 'minutes', seconds = 'seconds') => {
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

    /* Check if the device is a mobile phone */
    const isMobile = () => {
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

    /* singleton */
    const FlaskStateInstance = (function () {
        let instance = null;
        return function (language) {
            return instance || (instance = new MachineStatus(language))
        }
    })();

    /* Trigger window event */
    function Init(targetDom) {
        const language = arguments.length > 1 && typeof arguments[1] === "object" && arguments[1].hasOwnProperty('language') ? arguments[1] : {};

        if (targetDom instanceof HTMLElement && targetDom.id) {
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
                window.scroll(0, 0);
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
})));