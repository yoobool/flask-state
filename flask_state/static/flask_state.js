class MachineStatus {
    showConsoleDetail() {


        MachineStatus.addConsoleInfoContainer();

        if (window.addEventListener) {
            document.getElementById('console_info_close').addEventListener('click', function clickClose() {
                document.getElementById('console_info_back').click();
                document.getElementById('console_info_close').removeEventListener('click', clickClose);
                if (document.getElementById('console_state_circular')) {
                    document.getElementById('console_state_circular').classList.remove('circular-out');
                }
            });

            document.getElementById('console_info_back').addEventListener('click', function clickBack() {
                document.getElementById('console_info_back').style.display = 'none';
                document.getElementById('console_info_container').style.display = 'none';
                document.getElementById('console_info_back').removeEventListener('click', clickBack);
                if (document.getElementById('console_state_circular')) {
                    document.getElementById('console_state_circular').classList.remove('circular-out');
                }
            });

        } else if (window.attachEvent) {
            document.getElementById('console_info_close').attachEvent('onclick', function () {
                document.getElementById('console_info_back').click();
                if (document.getElementById('console_state_circular')) {
                    document.getElementById('console_state_circular').classList.remove('circular-out');
                }
            });

            document.getElementById('console_info_back').attachEvent('onclick', function () {
                document.getElementById('console_info_back').style.display = 'none';
                document.getElementById('console_info_container').style.display = 'none';
                if (document.getElementById('console_state_circular')) {
                    document.getElementById('console_state_circular').classList.remove('circular-out');
                }
            }, false);
        }

        document.getElementById('console_info_back').style.display = 'block';

        let consoleInfo = document.getElementById('console_info_container');
        consoleInfo.style.display = 'block';
        consoleInfo.style.height = 'fit-content';
        consoleInfo.style.top = String(5) + 'rem';

        let ajax = new Ajax();
        ajax.send({
            type: 'POST',
            url: '/v0/state/language',
            success: renderView
        });

        function renderView(data) {
            consoleInfo.getElementsByTagName('h4')[0].innerHTML = data.data.host_status;
            consoleInfo.getElementsByTagName('h4')[1].innerHTML = data.data.redis_status;
            document.getElementById('cpu').innerHTML = data.data.cpu;
            document.getElementById('memory').innerHTML = data.data.memory;
            document.getElementById('disk_usage').innerHTML = data.data.disk_usage;
            document.getElementById('load_avg').innerHTML = data.data.load_avg;
            document.getElementById('boot_seconds').innerHTML = data.data.boot_seconds;
            document.getElementById('used_memory').innerHTML = data.data.used_memory;
            document.getElementById('used_memory_rss').innerHTML = data.data.used_memory_rss;
            document.getElementById('mem_fragmentation_ratio').innerHTML = data.data.mem_fragmentation_ratio;
            document.getElementById('hits_ratio').innerHTML = data.data.hits_ratio;
            document.getElementById('delta_hits_ratio').innerHTML = data.data.delta_hits_ratio;
            document.getElementById('uptime_in_seconds').innerHTML = data.data.uptime_in_seconds;
            document.getElementById('connected_clients').innerHTML = data.data.connected_clients;
            document.getElementById('days').innerHTML = data.data.days;

            let hostInfoSpan = consoleInfo.getElementsByTagName('div')[0].getElementsByClassName('badge-style');
            let hostInfoExtendSpan = consoleInfo.getElementsByTagName('div')[1].getElementsByClassName('badge-style');
            for (let item of hostInfoSpan) {
                item.innerText = '';
            }
            for (let item of hostInfoExtendSpan) {
                item.innerText = '';
            }

            let consoleCpuChart = echarts.init(document.getElementById('console_info_cpu_chart'), null, {renderer: 'svg'});
            let consoleMemoryChart = echarts.init(document.getElementById('console_info_memory_chart'), null, {renderer: 'svg'});
            let consoleLoadavgChart = echarts.init(document.getElementById('console_info_loadavg_chart'), null, {renderer: 'svg'});
            let consoleDiskusageChart = echarts.init(document.getElementById('console_info_diskusage_chart'), null, {renderer: 'svg'});

            let cpuOption = MachineStatus.generateChatOption(data.data.cpu, '', data.data.today);
            let memoryOption = MachineStatus.generateChatOption(data.data.memory, '', data.data.today);
            let diskusageOption = MachineStatus.generateChatOption(data.data.disk_usage, '', data.data.today);
            let loadavgOption = MachineStatus.generateChatOption('Load Avg', 'loadavg', data.data.minutes, data.data.language);

            consoleCpuChart.showLoading();
            consoleMemoryChart.showLoading();
            consoleLoadavgChart.showLoading();
            consoleDiskusageChart.showLoading();
            let viewData = data.data;
            ajax = new Ajax();
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
                            node.classList.remove('show');
                            now.classList.add('show');
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
        let str = '<div class="all-elem layer div-style" id="console_info_back" disabled="disabled" xmlns="http://www.w3.org/1999/html">' +
            '</div>' +
            '<div class="all-elem div-style">' +
            '<div class="all-elem console_info_container_style console_info_container_box box-style div-style" id="console_info_container">' +
            '<button type="button" class="all-elem console_info_close_style" id="console_info_close"><span>&times;</span></button>' +
            '<h4 class="all-elem font_box box-style no-padding margin-top-10 h4-style">host_status</h4>' +
            '<div class="all-elem font_box box-style no-padding div-style">' +
            '<span id="memory">memory</span>:&nbsp;<span class="all-elem badge-style background-green margin-top-m3"></span>&nbsp;&nbsp;' +
            '<span id="cpu">cpu</span>:&nbsp;<span class="all-elem badge-style background-green margin-top-m3"></span>&nbsp;&nbsp;' +
            '<span id="disk_usage">disk_usage</span>:&nbsp;<span class="all-elem badge-style background-green margin-top-m3"></span>&nbsp;&nbsp;' +
            '<span id="load_avg">LoadAvg</span>:&nbsp;<span class="all-elem badge-style background-green margin-top-m3"></span>&nbsp;&nbsp;' +
            '<span id="boot_seconds">boot_seconds</span>:&nbsp;<span class="all-elem badge-style background-green margin-top-m3"></span>' +
            '</div>' +
            '<h4 class="all-elem font_box box-style no-padding h4-style">redis_status</h4>' +
            '<div class="all-elem font_box box-style no-padding margin-bottom-10 div-style">' +
            '<span id="used_memory">used_memory</span>:&nbsp;<span class="all-elem badge-style margin-top-m3 no-padding fontsize-18 console-info-memory-text"></span>&nbsp;&nbsp;' +
            '<span id="used_memory_rss">used_memory_rss</span>:&nbsp;<span class="all-elem badge-style margin-top-m3 no-padding fontsize-18 console-info-memory-text"></span>&nbsp;&nbsp;' +
            '<span id="mem_fragmentation_ratio">mem_fragmentation_ratio</span>:&nbsp;<span class="all-elem badge-style background-green margin-top-m3"></span>&nbsp;&nbsp;' +
            '<span id="hits_ratio">hits_ratio</span>:&nbsp;<span class="all-elem badge-style background-green margin-top-m3"></span>&nbsp;&nbsp;' +
            '<span id="delta_hits_ratio">24h_hits_ratio</span>:&nbsp;<span class="all-elem badge-style background-green margin-top-m3"></span>&nbsp;&nbsp;' +
            '<span id="uptime_in_seconds">uptime_in_seconds</span>:&nbsp;<span class="all-elem badge-style background-green margin-top-m3"></span>&nbsp;&nbsp;' +
            '<span id="connected_clients">connected_clients</span>:&nbsp;<span class="all-elem badge-style background-green margin-top-m3"></span>&nbsp;&nbsp;' +
            '<div class="all-elem select_container div-style"><select id="select_days">' +
            '<option value="1">1</option><option value="3">3</option><option value="7">7</option><option value="30">30</option></select><span id="days">days</span></div>' +
            '</div>';
        if (MachineStatus.checkMobile()) {
            str += '<hr width="109%" size="1" align="center" noshade="" id="console_info_line">' +
                '<div class="all-elem ul-tabs-box no-margin div-style">' +
                '<ul id="console_info_tab" class="all-elem ul-tabs">' +
                '<li class="all-elem active"><a href="#console_info_tab_memory" data-toggle="tab">' +
                '<strong>memory</strong></a></li>' +
                '<li class="all-elem "><a href="#console_info_tab_cpu" data-toggle="tab">' +
                '<strong>cpu</strong></a></li>' +
                '<li class="all-elem "><a href="#console_info_tab_diskusage" data-toggle="tab">' +
                '<strong>disk_usage</strong></a></li>' +
                '<li class="all-elem "><a href="#console_info_tab_loadavg" data-toggle="tab">' +
                '<strong>LoadAvg</strong></a></li>' +
                '</ul>' +
                '<div class="all-elem form-group no-margin div-style">' +
                '<div class="all-elem state-tab-content div-style">' +
                '<div class="all-elem state-tab-pane show div-style" id="console_info_tab_memory">' +
                '<div>' +
                '<div id="console_info_memory_chart" class="all-elem margin-top-10 div-style"></div>' +
                '</div>' +
                '</div>' +
                '<div class="all-elem state-tab-pane div-style" id="console_info_tab_cpu">' +
                '<div>' +
                '<div id="console_info_cpu_chart" class="all-elem margin-top-10 div-style"></div>' +
                '</div>' +
                '</div>' +
                '<div class="all-elem state-tab-pane div-style" id="console_info_tab_diskusage">' +
                '<div>' +
                '<div id="console_info_diskusage_chart" class="all-elem margin-top-10 div-style"></div>' +
                '</div>' +
                '</div>' +
                '<div class="all-elem state-tab-pane div-style" id="console_info_tab_loadavg">' +
                '<div>' +
                '<div id="console_info_loadavg_chart" class="all-elem margin-top-10 div-style"></div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>';
        } else {
            str += '<div class="all-elem charts_box box-style  no-padding console-info-border-r div-style">' +
                '<div class="all-elem charts-box-info div-style">' +
                '<div id="console_info_memory_chart" class="all-elem margin-top-10 div-style"></div>' +
                '</div>' +
                '</div>' +
                '<div class="all-elem charts_box box-style no-padding div-style">' +
                '<div class="all-elem charts-box-info div-style">' +
                '<div id="console_info_cpu_chart" class="all-elem margin-top-10 div-style"></div>' +
                '</div>' +
                '</div>' +
                '<div class="all-elem charts_box box-style no-padding console-info-border-r div-style">' +
                '<div class="all-elem charts-box-info div-style">' +
                '<div id="console_info_diskusage_chart" class="all-elem margin-top-10 div-style"></div>' +
                '</div>' +
                '</div>' +
                '<div class="all-elem charts_box box-style no-padding div-style">' +
                '<div class="all-elem charts-box-info div-style">' +
                '<div id="console_info_loadavg_chart" class="all-elem margin-top-10 div-style"></div>' +
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



let whenReady = (function () {
    let funcs = [];
    let ready = false;

    function handler(e) {
        if (ready) return;


        if (e.type === 'onreadystatechange' && document.readyState !== 'complete') {
            return;
        }


        for (let i = 0; i < funcs.length; i++) {
            funcs[i].call(document);
        }
        ready = true;
        funcs = null;
    }

    if (document.addEventListener) {
        document.addEventListener('DOMContentLoaded', handler, false);
        document.addEventListener('readystatechange', handler, false);
        window.addEventListener('load', handler, false);
    } else if (document.attachEvent) {
        document.attachEvent('onreadystatechange', handler);
        window.attachEvent('onload', handler);
    }

    return function whenReady(fn) {
        if (ready) {
            fn.call(document);
        } else {
            funcs.push(fn);
        }
    }
})();



function fn() {
    let ajax = new Ajax();
    ajax.send({
        type: 'POST',
        url: '/v0/state/bindid',
        success: bindId
    });

    function bindId(data) {
        if (!data.data.circular) {
            if (!document.getElementById(data.data.id_name)) {
                alert('Binding element ID does not exist');
                let obj = new MachineStatus();
                obj.showConsoleDetail();
            } else {
                document.getElementById(data.data.id_name).addEventListener('click', function () {
                    window.scroll(0, 0);
                    let obj = new MachineStatus();
                    obj.showConsoleDetail();
                })
            }
        } else if (data.data.circular) {
            let str = "<div id='console_state_circular' class='circular circular-animation' style='border-radius:100px;opacity:0.3;border:2px solid purple;'></div>";
            let bodyObj = document.getElementsByTagName('body')[0];
            bodyObj.insertAdjacentHTML('afterbegin', str);
            let circularObj = document.getElementById('console_state_circular');
            circularObj.onclick = function () {
                this.classList.add('circular-out');
                window.scroll(0, 0);
                let obj = new MachineStatus();
                obj.showConsoleDetail();
            };
            let timeOutId;
            let mousePosition;
            circularObj.onmousedown = function (downEvent) {
                mousePosition = mousePosition || downEvent.clientY;
                circularObj.classList.remove('circular-animation');
                timeOutId = setTimeout(function () {
                    circularObj.style.cursor = 'move';
                    bodyObj.style.cursor = 'move';
                    bodyObj.onmousemove = function (moveEvent) {
                        circularObj.style.top = Math.max(moveEvent.clientY - mousePosition + 300, 20) + 'px';
                    }
                }, 1500)
            };
            bodyObj.onmouseup = function () {
                circularObj.style.cursor = 'pointer';
                circularObj.classList.add('circular-animation');
                bodyObj.onmousemove = null;
                this.style.cursor = 'default';
                clearTimeout(timeOutId);
            };
            circularObj.ontouchstart = function (downEvent) {
                mousePosition = mousePosition || downEvent.clientY;
                circularObj.classList.remove('circular-animation');
                timeOutId = setTimeout(function () {
                    circularObj.style.cursor = 'move';
                    bodyObj.style.cursor = 'move';
                    bodyObj.ontouchmove = function (moveEvent) {
                        circularObj.style.top = Math.max(moveEvent.clientY - mousePosition + 300, 20) + 'px';
                    }
                }, 1500)
            };
            bodyObj.ontouchend = function () {
                circularObj.style.cursor = 'pointer';
                circularObj.classList.add('circular-animation');
                bodyObj.ontouchmove = null;
                this.style.cursor = 'default';
                clearTimeout(timeOutId);
            };
        }

    }
}

whenReady(fn);

