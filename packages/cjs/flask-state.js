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
    var __values = (this && this.__values) || function(o) {
        var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
        if (m) return m.call(o);
        if (o && typeof o.length === "number") return {
            next: function () {
                if (o && i >= o.length) o = void 0;
                return { value: o && o[i++], done: !o };
            }
        };
        throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
    };
    var ONE_MIN_SECONDS = 60;
    var ONE_DAY_HOURS = 24;
    var MACHINE_VALUE = {
        DANGER: 85,
        WARNING: 75,
    };
    var LOADAVG_VALUE = {
        DANGER: 10,
        WARNING: 5,
    };
    var BIT_TO_MB = 1048576;
    var SECONDS_TO_MILLISECONDS = 1000;
    var XML_ELEMENT = {
        svg: "http://www.w3.org/2000/svg",
        path: "http://www.w3.org/2000/svg"
    };
    var XML_PROPS = {
        t: null,
        version: null,
        viewBox: null,
        xmlns: "http://www.w3.org/2000/xmlns/",
        d: null,
        width: null,
        height: null,
        fill: null,
        className: null,
    };
    var MOUSE_POSITION = null;
    var MachineStatus = (function () {
        function MachineStatus(language) {
            var _this = this;
            this.clearId = null;
            this.language = language;
            this.mobile = MachineStatus.isMobile();
            this.index = 0;
            this.initFlaskStateContainer();
            this.setEventListener();
            this.initFlaskStateLanguage();
            this.setInitParams();
            if (this.mobile) {
                this.setTagChangeEventListener(this.consoleCpuChart, this.consoleMemoryChart, this.consoleLoadavgChart, this.consoleDiskUsageChart);
            }
            window.addEventListener('resize', function () {
                _this.resizeChartTimer([_this.consoleMemoryChart, _this.consoleCpuChart, _this.consoleLoadavgChart, _this.consoleDiskUsageChart]);
            });
        }
        ;
        MachineStatus.prototype.setFlaskStateData = function () {
            document.getElementById('fs-background').style.display = 'block';
            document.getElementById('fs-info-container').style.display = 'block';
            document.getElementsByTagName('body')[0].style.overflowX = 'hidden';
            document.getElementsByTagName('body')[0].style.overflowY = 'hidden';
            var selectDays = document.getElementById('fs-select-days');
            selectDays.value = '1';
            this.setCharts(1);
        };
        MachineStatus.prototype.initFlaskStateContainer = function () {
            var _chart = this.mobile ?
                DOMcreateElement("div", null,
                    DOMcreateElement("hr", { id: "console-info-line", className: "console-info-line-style" }),
                    DOMcreateElement("ul", { id: "fs-info-tab", className: "fs-ul-tabs" },
                        DOMcreateElement("li", { className: "active" },
                            DOMcreateElement("a", { "data-toggle": "tab" },
                                " ",
                                DOMcreateElement("strong", null, "Memory"))),
                        DOMcreateElement("li", null,
                            DOMcreateElement("a", { "data-toggle": "tab" },
                                DOMcreateElement("strong", null, "CPU"))),
                        DOMcreateElement("li", null,
                            DOMcreateElement("a", { "data-toggle": "tab" },
                                DOMcreateElement("strong", null, "Disk Usage"))),
                        DOMcreateElement("li", null,
                            DOMcreateElement("a", { "data-toggle": "tab" },
                                DOMcreateElement("strong", null, "Load Avg")))),
                    DOMcreateElement("div", { id: "fs-info-tab-memory", className: "fs-mChart-box fs-show" },
                        DOMcreateElement("div", { id: "fs-info-memory-chart", className: "fs-chart-style" })),
                    DOMcreateElement("div", { id: "fs-info-tab-cpu", className: "fs-mChart-box" },
                        DOMcreateElement("div", { id: "fs-info-cpu-chart", className: "fs-chart-style" })),
                    DOMcreateElement("div", { id: "fs-info-tab-disk-usage", className: "fs-mChart-box" },
                        DOMcreateElement("div", { id: "fs-info-diskusage-chart", className: "fs-chart-style" })),
                    DOMcreateElement("div", { id: "fs-info-tab-loadavg", className: "fs-mChart-box" },
                        DOMcreateElement("div", { id: "fs-info-loadavg-chart", className: "fs-chart-style" })))
                : DOMcreateElement("div", { className: 'fs-chart-content' },
                    DOMcreateElement("div", { className: 'fs-charts-width fs-charts-box fs-border' },
                        DOMcreateElement("div", { id: 'fs-info-memory-chart', className: 'fs-chart-style' })),
                    DOMcreateElement("div", { className: 'fs-charts-width fs-charts-box' },
                        DOMcreateElement("div", { id: 'fs-info-cpu-chart', className: 'fs-chart-style' })),
                    DOMcreateElement("div", { className: 'fs-charts-width fs-charts-box fs-border' },
                        DOMcreateElement("div", { id: 'fs-info-diskusage-chart', className: 'fs-chart-style' })),
                    DOMcreateElement("div", { className: 'fs-charts-width fs-charts-box' },
                        DOMcreateElement("div", { id: 'fs-info-loadavg-chart', className: 'fs-chart-style' })));
            var _content = DOMcreateElement("div", { className: "flask-state-elem fs-background", id: "fs-background" },
                DOMcreateElement("div", { className: "fs-container-width fs-container", id: "fs-info-container" },
                    DOMcreateElement("div", { className: "fs-select-container" },
                        DOMcreateElement("svg", { className: "fs-select-arrow", viewBox: "0 0 1024 1024", version: "1.1", width: "29", height: "17", xmlns: "http://www.w3.org/2000/svg" },
                            DOMcreateElement("path", { d: "M524.736 548.256l181.248-181.248a51.264 51.264 0 1 1 72.48 72.512l-217.472 217.472a51.264 51.264 0 0 1-72.512 0L271.04 439.52a51.264 51.264 0 1 1 72.512-72.512l181.216 181.248z", fill: "#161e2e" })),
                        DOMcreateElement("select", { id: "fs-select-days", className: "fs-select-days" },
                            DOMcreateElement("option", { value: "1" }, "1"),
                            DOMcreateElement("option", { value: "3" }, "3"),
                            DOMcreateElement("option", { value: "7" }, "7"),
                            DOMcreateElement("option", { value: "30" }, "30")),
                        DOMcreateElement("p", { id: "fs-days", className: "fs-days" }, " days")),
                    DOMcreateElement("button", { type: "button", className: "fs-close", id: "fs-info-close" },
                        DOMcreateElement("svg", { viewBox: "0 0 1024 1024", version: "1.1", width: "24", height: "24", xmlns: "http://www.w3.org/2000/svg" },
                            DOMcreateElement("path", { d: "M572.16 512l183.466667-183.04a42.666667 42.666667 0 1 0-60.586667-60.586667L512 451.84l-183.04-183.466667a42.666667 42.666667 0 0 0-60.586667 60.586667l183.466667 183.04-183.466667 183.04a42.666667 42.666667 0 0 0 0 60.586667 42.666667 42.666667 0 0 0 60.586667 0l183.04-183.466667 183.04 183.466667a42.666667 42.666667 0 0 0 60.586667 0 42.666667 42.666667 0 0 0 0-60.586667z", fill: "#161e2e" }))),
                    DOMcreateElement("h4", { id: "fs-host-status-title", className: "fs-h4-style" }, "Host Status"),
                    DOMcreateElement("div", { id: "fs-host-status" },
                        DOMcreateElement("div", null,
                            DOMcreateElement("span", { id: "fs-memory", className: "b-0079cc fs-badge-intro" }, "Memory"),
                            DOMcreateElement("span", { className: "fs-badge-content background-green" })),
                        DOMcreateElement("div", null,
                            DOMcreateElement("span", { id: "fs-cpu", className: "b-0079cc fs-badge-intro" }, "CPU"),
                            DOMcreateElement("span", { className: "fs-badge-content background-green" })),
                        DOMcreateElement("div", null,
                            DOMcreateElement("span", { id: "fs-disk-usage", className: "b-0079cc fs-badge-intro" }, "Disk Usage"),
                            DOMcreateElement("span", { className: "fs-badge-content background-green" })),
                        DOMcreateElement("div", null,
                            DOMcreateElement("span", { id: "fs-load-avg", className: "b-007dc8 fs-badge-intro" }, "Load Avg"),
                            DOMcreateElement("span", { className: "fs-badge-content background-green" })),
                        DOMcreateElement("div", null,
                            DOMcreateElement("span", { id: "fs-boot-seconds", className: "b-0051b9 fs-badge-intro" }, "Uptime"),
                            DOMcreateElement("span", { className: "fs-badge-content background-green" }))),
                    DOMcreateElement("h4", { id: "fs-redis-status-title", className: "fs-h4-style" }, "Redis Status"),
                    DOMcreateElement("div", { id: "fs-redis-status" },
                        DOMcreateElement("div", null,
                            DOMcreateElement("span", { id: "fs-used-memory", className: "b-99cb3d fs-badge-intro" }, "Used Mem"),
                            DOMcreateElement("span", { className: "fs-badge-content background-green" })),
                        DOMcreateElement("div", null,
                            DOMcreateElement("span", { id: "fs-used-memory-rss", className: "b-99cb3d fs-badge-intro" }, "Used Mem Rss"),
                            DOMcreateElement("span", { className: "fs-badge-content background-green" })),
                        DOMcreateElement("div", null,
                            DOMcreateElement("span", { id: "fs-mem-fragmentation-ratio", className: "b-534c6d fs-badge-intro" }, "Mem Fragmentation Ratio"),
                            DOMcreateElement("span", { className: "fs-badge-content background-green" })),
                        DOMcreateElement("div", null,
                            DOMcreateElement("span", { id: "fs-hits-ratio", className: "b-0079cc fs-badge-intro" }, "Cache Hits Ratio"),
                            DOMcreateElement("span", { className: "fs-badge-content background-green" }, "/")),
                        DOMcreateElement("div", null,
                            DOMcreateElement("span", { id: "fs-delta-hits-ratio", className: "b-0079cc fs-badge-intro" }, "24h Hits Ratio"),
                            DOMcreateElement("span", { className: "fs-badge-content background-green" })),
                        DOMcreateElement("div", null,
                            DOMcreateElement("span", { id: "fs-uptime-in-seconds", className: "b-0051b9 fs-badge-intro" }, "Uptime"),
                            DOMcreateElement("span", { className: "fs-badge-content background-green" })),
                        DOMcreateElement("div", null,
                            DOMcreateElement("span", { id: "fs-connected-clients", className: "b-534c6d fs-badge-intro" }, "Connections"),
                            DOMcreateElement("span", { className: "fs-badge-content background-green" }))),
                    _chart));
            document.body.appendChild(_content);
        };
        MachineStatus.prototype.setEventListener = function () {
            var _this = this;
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
                    var clickTarget = e.target;
                    if (String(clickTarget.id) === 'fs-background') {
                        document.getElementById('fs-background').style.display = 'none';
                        document.getElementById('fs-info-container').style.display = 'none';
                        document.getElementsByTagName('body')[0].style.overflowX = 'auto';
                        document.getElementsByTagName('body')[0].style.overflowY = 'auto';
                        if (document.getElementById('fs-state-circular')) {
                            document.getElementById('fs-state-circular').classList.remove('fs-circular-out');
                        }
                    }
                });
                document.getElementById('fs-select-days').addEventListener('change', function () {
                    var selectContainer = document.getElementById('fs-select-days');
                    _this.setCharts(parseInt(selectContainer.value));
                });
            }
        };
        MachineStatus.prototype.setTagChangeEventListener = function () {
            var e_1, _a;
            var chartList = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                chartList[_i] = arguments[_i];
            }
            if (document.getElementById('fs-info-tab')) {
                var liArr = document.getElementById('fs-info-tab').getElementsByTagName('li');
                var preNode_1 = document.getElementById('fs-info-tab-memory');
                var node_li_1 = liArr[0];
                var index = 0;
                var elemDict = {
                    0: 'fs-info-tab-memory',
                    1: 'fs-info-tab-cpu',
                    2: 'fs-info-tab-disk-usage',
                    3: 'fs-info-tab-loadavg'
                };
                var _loop_1 = function (item) {
                    var nowNode = document.getElementById(elemDict[index]);
                    item.children[0].addEventListener('click', function () {
                        item.classList.add('active');
                        node_li_1.classList.remove('active');
                        preNode_1.classList.remove('fs-show');
                        nowNode.classList.add('fs-show');
                        MachineStatus.resizeChart(chartList);
                        preNode_1 = nowNode;
                        node_li_1 = item;
                    });
                    index++;
                };
                try {
                    for (var liArr_1 = __values(liArr), liArr_1_1 = liArr_1.next(); !liArr_1_1.done; liArr_1_1 = liArr_1.next()) {
                        var item = liArr_1_1.value;
                        _loop_1(item);
                    }
                }
                catch (e_1_1) { e_1 = { error: e_1_1 }; }
                finally {
                    try {
                        if (liArr_1_1 && !liArr_1_1.done && (_a = liArr_1.return)) _a.call(liArr_1);
                    }
                    finally { if (e_1) throw e_1.error; }
                }
            }
        };
        MachineStatus.prototype.initFlaskStateLanguage = function () {
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
        };
        MachineStatus.prototype.setInitParams = function () {
            this.consoleCpuChart = echarts.init(document.getElementById('fs-info-cpu-chart'), null, { renderer: 'svg' });
            this.consoleMemoryChart = echarts.init(document.getElementById('fs-info-memory-chart'), null, { renderer: 'svg' });
            this.consoleLoadavgChart = echarts.init(document.getElementById('fs-info-loadavg-chart'), null, { renderer: 'svg' });
            this.consoleDiskUsageChart = echarts.init(document.getElementById('fs-info-diskusage-chart'), null, { renderer: 'svg' });
            this.cpuOption = MachineStatus.generateChatOption(this.mobile, this.language.cpu || 'CPU', '', this.language.today || 'Today');
            this.memoryOption = MachineStatus.generateChatOption(this.mobile, this.language.memory || 'Memory', '', this.language.today || 'Today');
            this.diskUsageOption = MachineStatus.generateChatOption(this.mobile, this.language.disk_usage || 'Disk Usage', '', this.language.today || 'Today');
            this.loadavgOption = MachineStatus.generateChatOption(this.mobile, 'Load Avg', 'loadavg', this.language.minutes || 'min');
        };
        MachineStatus.prototype.setCharts = function (days) {
            var _this = this;
            this.consoleCpuChart.showLoading();
            this.consoleMemoryChart.showLoading();
            this.consoleLoadavgChart.showLoading();
            this.consoleDiskUsageChart.showLoading();
            fetch("/v0/state/hoststatus", {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json;charset=UTF-8",
                },
                body: JSON.stringify({ "timeQuantum": days }),
            }).then(function (res) {
                if (res.ok) {
                    res.json().then(function (response) {
                        var e_2, _a;
                        if (response.code !== 200) {
                            return;
                        }
                        var fields = ["ts", "cpu", "memory", "load_avg", "disk_usage"];
                        var data = response.data;
                        data.items = data.items.map(function (item) {
                            var element = {};
                            fields.forEach(function (field, index) {
                                if (field === "ts") {
                                    element[field] = SECONDS_TO_MILLISECONDS * item[index];
                                }
                                else {
                                    element[field] = item[index];
                                }
                            });
                            return element;
                        });
                        var currentStatistic = data.currentStatistic;
                        if (Object.keys(currentStatistic).length) {
                            var hostInfoSpan_1 = document.getElementById('fs-host-status').getElementsByClassName('fs-badge-content');
                            hostInfoSpan_1[0].innerHTML = currentStatistic.memory + '%';
                            hostInfoSpan_1[1].innerHTML = currentStatistic.cpu + '%';
                            hostInfoSpan_1[2].innerHTML = currentStatistic.disk_usage + '%';
                            hostInfoSpan_1[3].innerHTML = currentStatistic.load_avg[0] + "，" + currentStatistic.load_avg[1] + "，" + currentStatistic.load_avg[2];
                            hostInfoSpan_1[4].innerHTML = MachineStatus.getFormatSeconds(currentStatistic.boot_seconds || 0, _this.language.days, _this.language.hours, _this.language.minutes, _this.language.seconds);
                            var machineIndex = ['memory', 'cpu', 'disk_usage', 'load_avg'];
                            machineIndex.forEach(function (item, index) {
                                var paramClass;
                                if (item === 'load_avg') {
                                    var loadavgAvg = (currentStatistic.load_avg[0] + currentStatistic.load_avg[1] + currentStatistic.load_avg[2]) / 3;
                                    paramClass = loadavgAvg >= LOADAVG_VALUE.WARNING ? loadavgAvg >= LOADAVG_VALUE.DANGER ? 'background-red' : 'background-orange' : 'background-green';
                                }
                                else {
                                    paramClass = currentStatistic[item] >= MACHINE_VALUE.WARNING ? currentStatistic.memory >= MACHINE_VALUE.DANGER ? 'background-red' : 'background-orange' : 'background-green';
                                }
                                var param = hostInfoSpan_1[index].classList;
                                param.remove('background-green', 'background-orange', 'background-red');
                                param.add(paramClass);
                            });
                            var hostInfoExtendSpan_1 = document.getElementById('fs-redis-status').getElementsByClassName('fs-badge-content');
                            var hostInfoKeysList = ['used_memory', 'used_memory_rss', 'mem_fragmentation_ratio', 'hits_ratio', 'delta_hits_ratio', 'uptime_in_seconds', 'connected_clients'];
                            var hideRedis = true;
                            try {
                                for (var hostInfoKeysList_1 = __values(hostInfoKeysList), hostInfoKeysList_1_1 = hostInfoKeysList_1.next(); !hostInfoKeysList_1_1.done; hostInfoKeysList_1_1 = hostInfoKeysList_1.next()) {
                                    var item = hostInfoKeysList_1_1.value;
                                    if (currentStatistic[item]) {
                                        hideRedis = false;
                                        break;
                                    }
                                }
                            }
                            catch (e_2_1) { e_2 = { error: e_2_1 }; }
                            finally {
                                try {
                                    if (hostInfoKeysList_1_1 && !hostInfoKeysList_1_1.done && (_a = hostInfoKeysList_1.return)) _a.call(hostInfoKeysList_1);
                                }
                                finally { if (e_2) throw e_2.error; }
                            }
                            if (hideRedis) {
                                document.getElementById('fs-redis-status-title').innerHTML = '';
                                document.getElementById('fs-redis-status-title').style.marginTop = '0';
                                document.getElementById('fs-redis-status').style.display = 'none';
                            }
                            else {
                                hostInfoKeysList.forEach(function (item, index) {
                                    switch (item) {
                                        case 'used_memory':
                                            hostInfoExtendSpan_1[index].innerHTML = Math.ceil(currentStatistic[item] / BIT_TO_MB) + ' M';
                                            break;
                                        case 'used_memory_rss':
                                            hostInfoExtendSpan_1[index].innerHTML = Math.ceil(currentStatistic[item] / BIT_TO_MB) + ' M';
                                            break;
                                        case 'mem_fragmentation_ratio':
                                            var ratio = currentStatistic[item];
                                            hostInfoExtendSpan_1[index].innerHTML = currentStatistic[item];
                                            if (ratio !== null && ratio !== undefined && ratio > 1) {
                                                var hostInfoExtendSpanClass = hostInfoExtendSpan_1[index].classList;
                                                hostInfoExtendSpanClass.remove('background-green');
                                                hostInfoExtendSpanClass.add('background-red');
                                            }
                                            break;
                                        case 'hits_ratio':
                                            hostInfoExtendSpan_1[index].innerHTML = currentStatistic[item] + '%';
                                            break;
                                        case 'delta_hits_ratio':
                                            hostInfoExtendSpan_1[index].innerHTML = currentStatistic[item] + '%';
                                            break;
                                        case 'uptime_in_seconds':
                                            hostInfoExtendSpan_1[index].innerHTML = MachineStatus.getFormatSeconds(currentStatistic[item], _this.language.days, _this.language.hours, _this.language.minutes, _this.language.seconds);
                                            break;
                                        case 'connected_clients':
                                            hostInfoExtendSpan_1[index].innerHTML = currentStatistic[item];
                                    }
                                });
                            }
                        }
                        data.items.reverse();
                        var dataMap = MachineStatus.getChartsData(data.items);
                        var tsList = dataMap.ts_list;
                        var cpuList = dataMap.cpu_list;
                        var memoryList = dataMap.memory_list;
                        var loadavgList = dataMap.load_avg_list[0];
                        var loadavg5MinList = dataMap.load_avg_list[1];
                        var loadavg15MinList = dataMap.load_avg_list[2];
                        var diskUsageList = dataMap.disk_usage_list;
                        _this.memoryOption.xAxis.data = tsList;
                        _this.cpuOption.xAxis.data = tsList;
                        _this.loadavgOption.xAxis.data = tsList;
                        _this.diskUsageOption.xAxis.data = tsList;
                        _this.memoryOption.series[0].data = memoryList;
                        _this.cpuOption.series[0].data = cpuList;
                        _this.diskUsageOption.series[0].data = diskUsageList;
                        _this.loadavgOption.series[0].data = loadavgList;
                        _this.loadavgOption.series[1].data = loadavg5MinList;
                        _this.loadavgOption.series[2].data = loadavg15MinList;
                        _this.consoleMemoryChart.setOption(_this.memoryOption);
                        _this.consoleCpuChart.setOption(_this.cpuOption);
                        _this.consoleLoadavgChart.setOption(_this.loadavgOption);
                        _this.consoleDiskUsageChart.setOption(_this.diskUsageOption);
                        MachineStatus.resizeChart([_this.consoleMemoryChart, _this.consoleCpuChart, _this.consoleLoadavgChart, _this.consoleDiskUsageChart]);
                    }).then(function () {
                        _this.consoleMemoryChart.hideLoading();
                        _this.consoleCpuChart.hideLoading();
                        _this.consoleLoadavgChart.hideLoading();
                        _this.consoleDiskUsageChart.hideLoading();
                    });
                }
            }).catch(function (err) {
                console.log(err);
            });
        };
        ;
        MachineStatus.prototype.resizeChartTimer = function (myChart) {
            clearTimeout(this.clearId);
            this.clearId = setTimeout(function () {
                MachineStatus.resizeChart(myChart);
            }, 200);
        };
        MachineStatus.isMobile = function () {
            var u = navigator.userAgent;
            var deviceBrowser = function () {
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
                };
            }();
            return deviceBrowser.iPhone || deviceBrowser.iPad || deviceBrowser.webApp || deviceBrowser.wechat
                || deviceBrowser.qq || deviceBrowser.ios || deviceBrowser.mobile || false;
        };
        ;
        MachineStatus.resizeChart = function (chartList) {
            chartList.forEach(function (chart) { return chart.resize(); });
        };
        MachineStatus.generateChatOption = function (isMobile, titleText, tableName, lineName) {
            if (tableName === void 0) { tableName = ''; }
            if (lineName === void 0) { lineName = ''; }
            var baseData = {
                color: tableName === 'loadavg' ? ['#ffa726', '#42a5f5', '#66bb6a'] : ['#42a5f5'],
                title: {
                    show: !isMobile,
                    text: titleText
                },
                tooltip: {
                    trigger: 'axis',
                    formatter: function (params) {
                        var value = echarts.format.formatTime('yyyy-MM-dd hh:mm:ss', new Date(parseInt(params[0].axisValue)), false) + '<br />';
                        for (var i = 0; i < params.length; i++) {
                            value += (params[i].marker + params[i].seriesName + ': ' + params[i].value +
                                (tableName === 'loadavg' ? '' : '%') + '<br />');
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
                        saveAsImage: {
                            title: ' ',
                        }
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
                baseData.legend.data.forEach(function (name) {
                    baseData.series.push({
                        name: name,
                        type: 'line',
                        symbol: 'none',
                        hoverAnimation: false
                    });
                });
            }
            return baseData;
        };
        MachineStatus.getChartsData = function (rawData) {
            var cpuList = [];
            var diskUsageList = [];
            var loadAvgList = [];
            var loadAvg5minList = [];
            var loadAvg15minList = [];
            var memoryList = [];
            var tsList = [];
            for (var i = 0; i < rawData.length; i++) {
                var item = rawData[i];
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
        ;
        MachineStatus.getFormatSeconds = function (value, days, hours, minutes, seconds) {
            if (days === void 0) { days = 'days'; }
            if (hours === void 0) { hours = 'hours'; }
            if (minutes === void 0) { minutes = 'min'; }
            if (seconds === void 0) { seconds = 'seconds'; }
            var secondTime = parseInt(value);
            var minuteTime = 0;
            var hourTime = 0;
            var dayTime = 0;
            var result = "";
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
            }
            else {
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
        ;
        return MachineStatus;
    }());
    function circularMove(moveEvent) {
        var triggerCircular = document.getElementById('fs-state-circular');
        triggerCircular.style.top = moveEvent.clientY - MOUSE_POSITION + 300 + 'px';
    }
    var FlaskStateInstance = (function () {
        var instance = null;
        return function (language) {
            return instance || (instance = new MachineStatus(language));
        };
    })();
    function Init(initMap) {
        var targetDom;
        var language = {};
        if (initMap !== null && typeof initMap === 'object') {
            targetDom = initMap.hasOwnProperty('dom') ? initMap.dom : null;
            language = initMap.hasOwnProperty('lang') ? initMap['lang'].hasOwnProperty('language') ? initMap['lang'] : {} : {};
        }
        if (targetDom instanceof HTMLElement) {
            if (targetDom.getAttribute('flaskState'))
                return;
            targetDom.setAttribute('flaskState', "true");
            targetDom.addEventListener('click', function () { return FlaskStateInstance(language).setFlaskStateData(); });
        }
        else {
            if (document.getElementById('fs-state-circular'))
                return;
            var str = "<div id='fs-state-circular' class='fs-circular' style='top:300px;border-radius:100px;opacity:0.3;border:2px solid purple;'></div>";
            var domBody = document.getElementsByTagName('body')[0];
            domBody.insertAdjacentHTML('beforeend', str);
            var triggerCircular_1 = document.getElementById('fs-state-circular');
            triggerCircular_1.onclick = function () {
                triggerCircular_1.classList.add('fs-circular-out');
                FlaskStateInstance(language).setFlaskStateData();
            };
            triggerCircular_1.onmousedown = function (downEvent) {
                MOUSE_POSITION = MOUSE_POSITION || downEvent.clientY;
                document.addEventListener("mousemove", circularMove);
            };
            document.onmouseup = function () {
                document.removeEventListener("mousemove", circularMove);
                var circularHeight = parseInt(triggerCircular_1.style.top);
                triggerCircular_1.classList.add("fs-circular-animation");
                triggerCircular_1.style.top = Math.min(Math.max(circularHeight, 50), window.screen.height - 200) + 'px';
                setTimeout(function () { return triggerCircular_1.classList.remove("fs-circular-animation"); }, 500);
            };
        }
    }
    function DOMParseChildren(children) {
        return children.map(function (child) {
            if (typeof child === 'string') {
                return document.createTextNode(child);
            }
            return child;
        });
    }
    function DOMcreateElement(element, properties) {
        var children = [];
        for (var _i = 2; _i < arguments.length; _i++) {
            children[_i - 2] = arguments[_i];
        }
        var isSVG = Object.prototype.hasOwnProperty.call(XML_ELEMENT, element);
        var el;
        if (isSVG) {
            el = document.createElementNS(XML_ELEMENT[element], element);
            for (var propName in properties) {
                el.setAttributeNS(XML_PROPS[propName], propName === "className" ? "class" : propName, properties[propName]);
            }
        }
        else {
            el = document.createElement(element);
            for (var propName in properties) {
                el[propName] = properties[propName];
            }
        }
        DOMParseChildren(children).forEach(function (child) {
            el.appendChild(child);
        });
        return el;
    }
    exports.init = Init;

})();