'use strict';

class MachineStatus {
    constructor(language) {
        this.language = language;
    };

    showConsoleDetail() {

        MachineStatus.addConsoleInfoContainer();

        if (window.addEventListener) {
            document.getElementById('console-info-close').addEventListener('click', function clickClose() {
                document.getElementById('console-info-back').click();
                document.getElementById('console-info-close').removeEventListener('click', clickClose);
                if (document.getElementById('console-state-circular')) {
                    document.getElementById('console-state-circular').classList.remove('fs-circular-out');
                }
            });

            document.getElementById('console-info-back').addEventListener('click', function clickBack() {
                document.getElementById('console-info-back').style.display = 'none';
                document.getElementById('console-info-container').style.display = 'none';
                document.getElementById('console-info-back').removeEventListener('click', clickBack);
                if (document.getElementById('console-state-circular')) {
                    document.getElementById('console-state-circular').classList.remove('fs-circular-out');
                }
            });

        } else if (window.attachEvent) {
            document.getElementById('console-info-close').attachEvent('onclick', function () {
                document.getElementById('console-info-back').click();
                if (document.getElementById('console-state-circular')) {
                    document.getElementById('console-state-circular').classList.remove('fs-circular-out');
                }
            });

            document.getElementById('console-info-back').attachEvent('onclick', function () {
                document.getElementById('console-info-back').style.display = 'none';
                document.getElementById('console-info-container').style.display = 'none';
                if (document.getElementById('console-state-circular')) {
                    document.getElementById('console-state-circular').classList.remove('fs-circular-out');
                }
            }, false);
        }

        document.getElementById('console-info-back').style.display = 'block';

        let consoleInfo = document.getElementById('console-info-container');
        consoleInfo.style.display = 'block';
        consoleInfo.style.height = 'fit-content';
        consoleInfo.style.top = String(5) + 'rem';

        consoleInfo.getElementsByTagName('h4')[0].innerHTML = this.language.host_status + ':'
        consoleInfo.getElementsByTagName('h4')[1].innerHTML = this.language.redis_status + ':'
        document.getElementById('cpu').innerHTML = this.language.cpu + ':';
        document.getElementById('memory').innerHTML = this.language.memory + ':'
        document.getElementById('disk_usage').innerHTML = this.language.disk_usage + ':'
        document.getElementById('load_avg').innerHTML = this.language.load_avg + ':'
        document.getElementById('boot_seconds').innerHTML = this.language.boot_seconds + ':'
        document.getElementById('used_memory').innerHTML = this.language.used_memory + ':'
        document.getElementById('used_memory_rss').innerHTML = this.language.used_memory_rss + ':'
        document.getElementById('mem_fragmentation_ratio').innerHTML = this.language.mem_fragmentation_ratio + ':'
        document.getElementById('hits_ratio').innerHTML = this.language.hits_ratio + ':'
        document.getElementById('delta_hits_ratio').innerHTML = this.language.delta_hits_ratio + ':'
        document.getElementById('uptime_in_seconds').innerHTML = this.language.uptime_in_seconds + ':'
        document.getElementById('connected_clients').innerHTML = this.language.connected_clients + ':'
        document.getElementById('days').innerHTML = this.language.days;

        let hostInfoSpan = document.getElementById('fs-host-status').getElementsByClassName('fs-badge-style');
        let hostInfoExtendSpan = document.getElementById('fs-redis-status').getElementsByClassName('fs-badge-style');
        for (let item of hostInfoSpan) {
            item.innerText = '';
        }
        for (let item of hostInfoExtendSpan) {
            item.innerText = '';
        }

        let consoleCpuChart = echarts.init(document.getElementById('console-info-cpu-chart'), null, {renderer: 'svg'});
        let consoleMemoryChart = echarts.init(document.getElementById('console-info-memory-chart'), null, {renderer: 'svg'});
        let consoleLoadavgChart = echarts.init(document.getElementById('console-info-loadavg-chart'), null, {renderer: 'svg'});
        let consoleDiskusageChart = echarts.init(document.getElementById('console-info-diskusage-chart'), null, {renderer: 'svg'});

        let cpuOption = MachineStatus.generateChatOption(this.language.cpu, '', this.language.today);
        let memoryOption = MachineStatus.generateChatOption(this.language.memory, '', this.language.today);
        let diskusageOption = MachineStatus.generateChatOption(this.language.disk_usage, '', this.language.today);
        let loadavgOption = MachineStatus.generateChatOption('Load Avg', 'loadavg', this.language.minutes, this.language.language);

        consoleCpuChart.showLoading();
        consoleMemoryChart.showLoading();
        consoleLoadavgChart.showLoading();
        consoleDiskusageChart.showLoading();
        let viewData = this.language;
        let ajax = new Ajax();
        ajax.send({
            type: 'POST',
            url: '/v0/state/hoststatus',
            data: {'timeQuantum': '1'},
            success: ajaxSuccess,
            complete: ajaxComplete,
        });

        function ajaxSuccess(data) {
            const fields = ["ts", "cpu", "memory", "load_avg", "disk_usage"];

            data.data.items = data.data.items.map(item => {
                let element = {};
                fields.forEach((field, index) => {
                    if (field === "ts") return element[field] = 1000 * item[index];
                    element[field] = item[index];
                });
                return element;
            });

            let currentStatistic = data.data.currentStatistic;
            if (Object.keys(currentStatistic).length) {
                hostInfoSpan[0].innerHTML = currentStatistic.memory + '%';
                hostInfoSpan[1].innerHTML = currentStatistic.cpu + '%';
                hostInfoSpan[2].innerHTML = currentStatistic.disk_usage + '%';
                let loadavgStr = currentStatistic.load_avg[0] + "，" + currentStatistic.load_avg[1] + "，" + currentStatistic.load_avg[2];
                hostInfoSpan[3].innerHTML = loadavgStr;
                if (currentStatistic.boot_seconds)
                    hostInfoSpan[4].innerHTML = MachineStatus.consoleFormatSeconds(currentStatistic.boot_seconds, viewData.days, viewData.hours, viewData.minutes, viewData.seconds);

                if (currentStatistic.memory >= 85) {
                    let hostInfoSpanClass = hostInfoSpan[0].classList;
                    hostInfoSpanClass.remove('bg-orange', 'background-green');
                    hostInfoSpanClass.add('background-red');
                } else if (currentStatistic.memory >= 75 && currentStatistic.memory < 85) {
                    let hostInfoSpanClass = hostInfoSpan[0].classList;
                    hostInfoSpanClass.remove('background-green', 'background-red');
                    hostInfoSpanClass.add('bg-orange');
                } else {
                    let hostInfoSpanClass = hostInfoSpan[0].classList;
                    hostInfoSpanClass.remove('bg-orange', 'background-red');
                    hostInfoSpanClass.add('background-green');
                }
                if (currentStatistic.cpu >= 85) {
                    let hostInfoSpanClass = hostInfoSpan[1].classList;
                    hostInfoSpanClass.remove('background-green', 'bg-orange');
                    hostInfoSpanClass.add('background-red');
                } else if (currentStatistic.cpu >= 75 && currentStatistic.cpu < 85) {
                    let hostInfoSpanClass = hostInfoSpan[1].classList;
                    hostInfoSpanClass.remove('background-green', 'background-red');
                    hostInfoSpanClass.add('bg-orange');
                } else {
                    let hostInfoSpanClass = hostInfoSpan[1].classList;
                    hostInfoSpanClass.remove('bg-orange', 'background-red');
                    hostInfoSpanClass.add('background-green');
                }
                if (currentStatistic.disk_usage >= 85) {
                    let hostInfoSpanClass = hostInfoSpan[2].classList;
                    hostInfoSpanClass.remove('background-green', 'bg-orange');
                    hostInfoSpanClass.add('background-red');
                } else if (currentStatistic.disk_usage >= 75 && currentStatistic.disk_usage < 85) {
                    let hostInfoSpanClass = hostInfoSpan[2].classList;
                    hostInfoSpanClass.remove('background-green', 'background-red');
                    hostInfoSpanClass.add('bg-orange');
                } else {
                    let hostInfoSpanClass = hostInfoSpan[2].classList;
                    hostInfoSpanClass.remove('bg-orange', 'background-red');
                    hostInfoSpanClass.add('background-green');
                }
                let loadavgAvg = (currentStatistic.load_avg[0] + currentStatistic.load_avg[1] + currentStatistic.load_avg[2]) / 3;
                if (loadavgAvg >= 10) {
                    let hostInfoSpanClass = hostInfoSpan[3].classList;
                    hostInfoSpanClass.remove('background-green', 'bg-orange');
                    hostInfoSpanClass.add('background-red');
                } else if (loadavgAvg >= 5 && loadavgAvg < 10) {
                    let hostInfoSpanClass = hostInfoSpan[3].classList;
                    hostInfoSpanClass.remove('background-green', 'background-red');
                    hostInfoSpanClass.add('bg-orange');
                } else {
                    let hostInfoSpanClass = hostInfoSpan[3].classList;
                    hostInfoSpanClass.remove('bg-orange', 'background-red');
                    hostInfoSpanClass.add('background-green');
                }

                let hostInfoKeysList = ['used_memory', 'used_memory_rss', 'mem_fragmentation_ratio', 'hits_ratio', 'delta_hits_ratio', 'uptime_in_seconds', 'connected_clients'];
                {
                    let counter = 0;
                    for (let item of hostInfoExtendSpan) {
                        item.innerText = String(currentStatistic[hostInfoKeysList[counter]]);
                        if (counter < 2) {
                            item.innerHTML = Math.ceil(currentStatistic[hostInfoKeysList[counter]] / 1024 / 1024) + 'M';
                        } else if (counter === 2) {
                            let ratio = currentStatistic[hostInfoKeysList[counter]];
                            if (ratio !== null && ratio !== undefined && ratio > 1) {
                                let hostInfoExtendSpanClass = hostInfoExtendSpan[counter].classList;
                                hostInfoExtendSpanClass.remove('background-green');
                                hostInfoExtendSpanClass.add('background-red');
                            }
                            counter++;
                            continue;
                        } else if (counter > 2 && counter < 5) {
                            item.innerHTML = currentStatistic[hostInfoKeysList[counter]] + '%';
                        } else if (counter == 5) {
                            if (currentStatistic[hostInfoKeysList[counter]])
                                item.innerHTML = MachineStatus.consoleFormatSeconds(currentStatistic[hostInfoKeysList[counter]], viewData.days, viewData.hours, viewData.minutes, viewData.seconds);
                        }
                        if (counter >= 2) {
                            item.classList.add('background-green');
                        }
                        counter++;
                    }
                }
            }

            data.data.items.reverse();
            let dataMap = MachineStatus.refactorRawData(data.data.items);

            let ts_list = dataMap.ts_list;
            let cpu_list = dataMap.cpu_list;
            let memory_list = dataMap.memory_list;
            let loadavg_list = dataMap.load_avg_list[0];
            let loadavg_5min_list = dataMap.load_avg_list[1];
            let loadavg_15min_list = dataMap.load_avg_list[2];
            let diskusage_list = dataMap.disk_usage_list;

            memoryOption.xAxis.data = ts_list;
            cpuOption.xAxis.data = ts_list;
            loadavgOption.xAxis.data = ts_list;
            diskusageOption.xAxis.data = ts_list;

            memoryOption.series[0].data = memory_list;
            cpuOption.series[0].data = cpu_list;
            diskusageOption.series[0].data = diskusage_list;
            loadavgOption.series[0].data = loadavg_list;
            loadavgOption.series[1].data = loadavg_5min_list;
            loadavgOption.series[2].data = loadavg_15min_list;

            consoleMemoryChart.setOption(memoryOption);
            consoleCpuChart.setOption(cpuOption);
            consoleLoadavgChart.setOption(loadavgOption);
            consoleDiskusageChart.setOption(diskusageOption);
            consoleMemoryChart.resize();
            consoleCpuChart.resize();
            consoleLoadavgChart.resize();
            consoleDiskusageChart.resize();

            window.onresize = () => MachineStatus.resizeChart([consoleMemoryChart, consoleCpuChart, consoleLoadavgChart, consoleDiskusageChart]);
            if (document.getElementById('console_info_tab')) {
                let liArr = document.getElementById('console_info_tab').getElementsByTagName('li');
                let index = 0;
                let node = document.getElementById('console_info_tab_memory');
                let node_li = liArr[0];
                for (let item of liArr) {
                    let now = null;
                    if (index === 0) {
                        now = document.getElementById('console_info_tab_memory');
                    } else if (index === 1) {
                        now = document.getElementById('console_info_tab_cpu');
                    } else if (index === 2) {
                        now = document.getElementById('console_info_tab_diskusage');
                    } else {
                        now = document.getElementById('console_info_tab_loadavg');
                    }
                    item.children[0].addEventListener('click', function () {
                        item.classList.add('active');
                        node_li.classList.remove('active');
                        node.classList.remove('fs-show');
                        now.classList.add('fs-show');
                        consoleMemoryChart.resize();
                        consoleCpuChart.resize();
                        consoleLoadavgChart.resize();
                        consoleDiskusageChart.resize();
                        node = now;
                        node_li = item;
                    });
                    index++;
                }
            }
        }

        function ajaxComplete() {
            consoleMemoryChart.hideLoading();
            consoleCpuChart.hideLoading();
            consoleLoadavgChart.hideLoading();
            consoleDiskusageChart.hideLoading();
        }

        let selectContainer = document.getElementById('select_days');
        selectContainer.onchange = function () {
            ajax.send({
                type: 'POST',
                url: '/v0/state/hoststatus',
                data: {'timeQuantum': selectContainer.value},
                success: ajaxSuccess,
                complete: ajaxComplete,
            });
        };

    }

    static resizeChart(myChart, timeout) {
        clearTimeout(this.clearId);
        this.clearId = setTimeout(function () {
            myChart.forEach(function (chart) {
                if (chart)
                    chart.resize();
            });
        }, timeout || 200)
    }


    static addConsoleInfoContainer() {
        let str = '<div class="flask-state-elem layer console-info-back-style" id="console-info-back" disabled="disabled" xmlns="http://www.w3.org/1999/html">' +
            '</div>' +
            '<div class="flask-state-elem ">' +
            '<div class="flask-state-elem console-info-container-style console-info-container-box box-style " id="console-info-container">' +
            '<div class="flask-state-elem fs-select-container"><select id="select_days" class="margin-right-3">' +
            '<option value="1">1</option><option value="3">3</option><option value="7">7</option><option value="30">30</option></select><span id="days">days</span></div>' +
            '<button type="button" class="flask-state-elem console-info-close-style" id="console-info-close"><span>&times;</span></button>' +
            '<h4 class="flask-state-elem fs-font-box box-style no-padding margin-top-10 fs-h4-style">host_status</h4>' +
            '<div id="fs-host-status" class="flask-state-elem fs-font-box box-style no-padding">' +
            '<span id="memory" class="margin-right-5">memory:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
            '<span id="cpu" class="margin-right-5">cpu:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
            '<span id="disk_usage" class="margin-right-5">disk_usage:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
            '<span id="load_avg" class="margin-right-5">LoadAvg:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
            '<span id="boot_seconds" class="margin-right-5">boot_seconds:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
            '</div>' +
            '<h4 class="flask-state-elem fs-font-box box-style no-padding fs-h4-style">redis_status</h4>' +
            '<div id="fs-redis-status" class="flask-state-elem fs-font-box box-style no-padding margin-bottom-10 ">' +
            '<span id="used_memory" class="margin-right-5">used_memory:</span><span class="flask-state-elem fs-badge-style margin-top-m3 no-padding fontsize-18 console-info-memory-text margin-right-10"></span>' +
            '<span id="used_memory_rss" class="margin-right-5">used_memory_rss:</span><span class="flask-state-elem fs-badge-style margin-top-m3 no-padding fontsize-18 console-info-memory-text margin-right-10"></span>' +
            '<span id="mem_fragmentation_ratio" class="margin-right-5">mem_fragmentation_ratio:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
            '<span id="hits_ratio" class="margin-right-5">hits_ratio:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
            '<span id="delta_hits_ratio" class="margin-right-5">24h_hits_ratio:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
            '<span id="uptime_in_seconds" class="margin-right-5">uptime_in_seconds:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
            '<span id="connected_clients" class="margin-right-5">connected_clients:</span><span class="flask-state-elem fs-badge-style background-green margin-top-m3 margin-right-10"></span>' +
            '</div>';
        if (MachineStatus.checkMobile()) {
            str += '<hr size="1" align="center" noshade="" id="console-info-line" class="console-info-line-style">' +
                '<div class="flask-state-elem fs-ul-tabs-box no-margin ">' +
                '<ul id="console_info_tab" class="flask-state-elem fs-ul-tabs">' +
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
                '<div class="flask-state-elem state-tab-pane fs-show" id="console_info_tab_memory">' +
                '<div>' +
                '<div id="console-info-memory-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                '</div>' +
                '</div>' +
                '<div class="flask-state-elem state-tab-pane " id="console_info_tab_cpu">' +
                '<div>' +
                '<div id="console-info-cpu-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                '</div>' +
                '</div>' +
                '<div class="flask-state-elem state-tab-pane " id="console_info_tab_diskusage">' +
                '<div>' +
                '<div id="console-info-diskusage-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                '</div>' +
                '</div>' +
                '<div class="flask-state-elem state-tab-pane " id="console_info_tab_loadavg">' +
                '<div>' +
                '<div id="console-info-loadavg-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>';
        } else {
            str += '<div class="flask-state-elem fs-charts-box box-style no-padding console-info-border-r">' +
                '<div class="flask-state-elem charts-box-info ">' +
                '<div id="console-info-memory-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                '</div>' +
                '</div>' +
                '<div class="flask-state-elem fs-charts-box box-style no-padding ">' +
                '<div class="flask-state-elem charts-box-info ">' +
                '<div id="console-info-cpu-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                '</div>' +
                '</div>' +
                '<div class="flask-state-elem fs-charts-box box-style no-padding console-info-border-r ">' +
                '<div class="flask-state-elem charts-box-info ">' +
                '<div id="console-info-diskusage-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                '</div>' +
                '</div>' +
                '<div class="flask-state-elem fs-charts-box box-style no-padding ">' +
                '<div class="flask-state-elem charts-box-info ">' +
                '<div id="console-info-loadavg-chart" class="flask-state-elem margin-top-10 fs-chart-style"></div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>';
        }
        document.getElementsByTagName('body')[0].insertAdjacentHTML('afterbegin', str);
    }


    static refactorRawData(rawData) {
        let cpu_list = [];
        let disk_usage_list = [];
        let load_avg_list = [];
        let load_avg_5min_list = [];
        let load_avg_15min_list = [];
        let memory_list = [];
        let ts_list = [];
        for (let i = 0; i < rawData.length; i++) {
            let item = rawData[i];
            cpu_list.push(item.cpu);
            disk_usage_list.push(item.disk_usage);
            load_avg_list.push(item.load_avg[0]);
            load_avg_5min_list.push(item.load_avg[1]);
            load_avg_15min_list.push(item.load_avg[2]);
            memory_list.push(item.memory);
            ts_list.push(item.ts);
        }
        return {
            'cpu_list': cpu_list, 'disk_usage_list': disk_usage_list,
            'load_avg_list': [load_avg_list, load_avg_5min_list, load_avg_15min_list],
            'memory_list': memory_list, 'ts_list': ts_list
        };
    }


    static generateChatOption(titleText, tableName, lineName, language = '-1') {
        let checkResult = MachineStatus.checkMobile();
        let baseData = {
            color: tableName === 'loadavg' ? ['#ffa726', '#42a5f5', '#66bb6a'] : ['#42a5f5'],
            title: {
                show: !checkResult,
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
                top: checkResult ? 30 : 60,
                containLabel: true
            },
            toolbox: {
                show: !checkResult,
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
            let suffix = (language === '1' ? 1 : 0);
            baseData.legend.data = ['1' + lineName.substring(0, lineName.length - suffix), '5' + lineName, '15' + lineName];
            baseData.series = [];
            for (let i = 0; i < baseData.legend.data.length; i++) {
                let name = baseData.legend.data[i];
                baseData.series.push({
                    name: name,
                    type: 'line',
                    symbol: 'none',
                    hoverAnimation: false
                });
            }
        }
        return baseData;
    }


    static consoleFormatSeconds(value, days, hours, minutes, seconds) {
        let secondTime = parseInt(value);
        let minuteTime = 0;
        let hourTime = 0;
        let dayTime = 0;
        let result = "";
        if (secondTime >= 60) {
            minuteTime = parseInt(secondTime / 60);
            if (minuteTime >= 60) {
                hourTime = parseInt(minuteTime / 60);
                minuteTime = parseInt(minuteTime % 60);
            }
            if (hourTime >= 24) {
                dayTime = parseInt(hourTime / 24);
                hourTime = parseInt(hourTime % 24);
            }
        } else {
            result = secondTime + seconds;
        }
        if (minuteTime > 0) {
            result = "" + parseInt(minuteTime) + minutes;
        }
        if (hourTime > 0) {
            result = "" + parseInt(hourTime) + hours;
        }
        if (dayTime > 0) {
            result = "" + parseInt(dayTime) + days;
        }
        return result;
    }


    static checkMobile() {
        let u = navigator.userAgent;
        let deviceBrowser = function () {
            return {
                trident: u.indexOf('Trident') > -1,
                presto: u.indexOf('Presto') > -1,
                webKit: u.indexOf('AppleWebKit') > -1,
                gecko: u.indexOf('Gecko') > -1 && u.indexOf('KHTML') === -1,
                mobile: !!u.match(/AppleWebKit.*Mobile.*/),
                ios: !!u.match(/\(i[^;]+;( U;)? CPU.Mac OS X/),
                android: u.indexOf('Android') > -1 || u.indexOf('Linux') > -1,
                iPhone: u.indexOf('iPhone') > -1,
                iPad: u.indexOf('iPad') > -1,
                webApp: u.indexOf('Safari') === -1,
                weixin: u.indexOf('MicroMessenger') > -1,
                qq: u.match(/\sQQ/i) === " qq",
            }
        }();
        return deviceBrowser.iPhone || deviceBrowser.iPad || deviceBrowser.webApp || deviceBrowser.weixin
        || deviceBrowser.qq || deviceBrowser.ios || deviceBrowser.mobile ? true : 0;

    };
}


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

function Machine_state(language, floatball = false) {
    const FlaskStateExample = new MachineStatus(language);
    if (floatball) {
        let str = "<div id='console-state-circular' class='fs-circular fs-circular-animation' style='border-radius:100px;opacity:0.3;border:2px solid purple;'></div>";
        let domBody = document.getElementsByTagName('body')[0];
        domBody.insertAdjacentHTML('afterbegin', str);
        let triggerCircular = document.getElementById('console-state-circular');
        triggerCircular.onclick = function () {
            this.classList.add('fs-circular-out');
            window.scroll(0, 0);
            FlaskStateExample.showConsoleDetail();
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
    } else {
        FlaskStateExample.showConsoleDetail();
    }
}


