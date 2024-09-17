"use strict";
(self["webpackChunkipydatatable"] = self["webpackChunkipydatatable"] || []).push([["lib_widget_js"],{

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) David Fernandez
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


// Copyright (c) David Fernandez
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.InteractiveTableView = exports.InteractiveTableModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js"));
__webpack_require__(/*! datatables.net */ "./node_modules/datatables.net/js/dataTables.mjs");
__webpack_require__(/*! jszip */ "./node_modules/jszip/dist/jszip.min.js");
__webpack_require__(/*! datatables.net-dt */ "./node_modules/datatables.net-dt/js/dataTables.dataTables.mjs");
__webpack_require__(/*! datatables.net-select */ "./node_modules/datatables.net-select/js/dataTables.select.mjs");
__webpack_require__(/*! datatables.net-colreorder */ "./node_modules/datatables.net-colreorder/js/dataTables.colReorder.mjs");
__webpack_require__(/*! datatables.net-responsive */ "./node_modules/datatables.net-responsive/js/dataTables.responsive.mjs");
__webpack_require__(/*! datatables.net-datetime */ "./node_modules/datatables.net-datetime/dist/dataTables.dateTime.mjs");
__webpack_require__(/*! datatables.net-searchbuilder-dt */ "./node_modules/datatables.net-searchbuilder-dt/js/searchBuilder.dataTables.mjs");
__webpack_require__(/*! datatables.net-buttons */ "./node_modules/datatables.net-buttons/js/dataTables.buttons.mjs");
__webpack_require__(/*! datatables.net-buttons-dt */ "./node_modules/datatables.net-buttons-dt/js/buttons.dataTables.mjs");
__webpack_require__(/*! datatables.net-buttons/js/buttons.colVis.js */ "./node_modules/datatables.net-buttons/js/buttons.colVis.js");
__webpack_require__(/*! datatables.net-buttons/js/buttons.html5.js */ "./node_modules/datatables.net-buttons/js/buttons.html5.js");
__webpack_require__(/*! datatables.net-buttons/js/buttons.print.js */ "./node_modules/datatables.net-buttons/js/buttons.print.js");
__webpack_require__(/*! datatables.net-fixedheader */ "./node_modules/datatables.net-fixedheader/js/dataTables.fixedHeader.mjs");
// import 'datatables.net-plugins';
__webpack_require__(/*! datatables.net-scroller */ "./node_modules/datatables.net-scroller/js/dataTables.scroller.mjs");
__webpack_require__(/*! fontawesome */ "./node_modules/fontawesome/index.js");
// import 'pdfmake'
const screenfull_1 = __importDefault(__webpack_require__(/*! screenfull */ "./node_modules/screenfull/dist/screenfull.js"));
__webpack_require__(/*! jszip */ "./node_modules/jszip/dist/jszip.min.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
// Load datatables styles
__webpack_require__(/*! !style-loader!css-loader!datatables.net-dt/css/dataTables.dataTables.css */ "./node_modules/style-loader/dist/cjs.js!./node_modules/css-loader/dist/cjs.js!./node_modules/datatables.net-dt/css/dataTables.dataTables.css");
__webpack_require__(/*! !style-loader!css-loader!datatables.net-searchbuilder-dt/css/searchBuilder.dataTables.css */ "./node_modules/style-loader/dist/cjs.js!./node_modules/css-loader/dist/cjs.js!./node_modules/datatables.net-searchbuilder-dt/css/searchBuilder.dataTables.css");
__webpack_require__(/*! !style-loader!css-loader!datatables.net-buttons-dt/css/buttons.dataTables.css */ "./node_modules/style-loader/dist/cjs.js!./node_modules/css-loader/dist/cjs.js!./node_modules/datatables.net-buttons-dt/css/buttons.dataTables.css");
__webpack_require__(/*! !style-loader!css-loader!datatables.net-datetime/dist/dataTables.dateTime.min.css */ "./node_modules/style-loader/dist/cjs.js!./node_modules/css-loader/dist/cjs.js!./node_modules/datatables.net-datetime/dist/dataTables.dateTime.min.css");
const datatables_net_dt_1 = __importDefault(__webpack_require__(/*! datatables.net-dt */ "./node_modules/datatables.net-dt/js/dataTables.dataTables.mjs"));
class InteractiveTableModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: InteractiveTableModel.model_name, _model_module: InteractiveTableModel.model_module, _model_module_version: InteractiveTableModel.model_module_version, _view_name: InteractiveTableModel.view_name, _view_module: InteractiveTableModel.view_module, _view_module_version: InteractiveTableModel.view_module_version });
    }
}
exports.InteractiveTableModel = InteractiveTableModel;
InteractiveTableModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
InteractiveTableModel.model_name = 'InteractiveTableModel';
InteractiveTableModel.model_module = version_1.MODULE_NAME;
InteractiveTableModel.model_module_version = version_1.MODULE_VERSION;
InteractiveTableModel.view_name = 'InteractiveTableView'; // Set to null if no view
InteractiveTableModel.view_module = version_1.MODULE_NAME; // Set to null if no view
InteractiveTableModel.view_module_version = version_1.MODULE_VERSION;
class InteractiveTableView extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.column_order = [];
        this.style_context = null;
        this.selected_data = [];
        this.onclickRowSelection = false;
        this.groupClick = false;
        this.wrapper = null;
        this.tbl = null;
        this.cols = [];
        this.dropdown = false;
        this.columns = [""];
        this.table = null;
        this.selected = [];
    }
    ;
    render() {
        console.log("in render!!");
        var self = this;
        // Keeps the order of the columns for filtering.
        // This is important for when we move the columns.
        self.column_order = [];
        // Loading CSS for library.
        self.create_style_jinteractive();
        // Get table data from Python
        var table_data = self.model.get('table');
        // Selected data variable.
        self.selected_data = [];
        //self.model.on('change:selected_data', this.selected_data_changed, this);
        self.model.on('change:selected_index_row', this.selected_index_row_changed, this);
        self.model.on('change:selected_group', this.selected_group_changed, this);
        self.onclickRowSelection = false;
        self.groupClick = false;
        // Creating a wrapper element
        self.wrapper = document.createElement('div');
        self.wrapper.id = "wrapper_" + self.cid;
        self.wrapper.style.display = "none";
        self.wrapper.style.width = '100%';
        self.wrapper.style.setProperty('color', 'black', 'important');
        self.wrapper.style.backgroundColor = "white";
        // Creating table element
        self.tbl = document.createElement('table');
        self.tbl.style.width = '100%';
        self.tbl.style.setProperty('color', 'black', 'important');
        self.tbl.style.wordWrap = "break-word";
        self.tbl.id = "example_" + self.cid;
        self.tbl.className = "display";
        // All the columns of the data.
        self.cols = [];
        //  Basically means it will hace a child row.
        self.dropdown = false;
        // Columns in the data
        self.columns = [""];
        // Creating table
        // Adding body
        var tbdy = document.createElement('tbody');
        // Iterate through the table data.
        jquery_1.default.each(table_data, (i, value) => {
            self.dropdown = false;
            var tr = document.createElement('tr');
            // Go through each column of a row and add them to the element
            Object.keys(value).forEach(function (key) {
                var td = document.createElement('td');
                // Formatting the data
                if (typeof value[key] === 'string' || value[key] instanceof String) {
                    var temp_value = value[key];
                }
                else if (value[key] == null) {
                    var temp_value = "";
                }
                else {
                    var temp_value = value[key].toString();
                }
                // Checking to see if data is overflowed on limit or is group.
                // Makes it so you will have a child row.
                if (key == "group") {
                    self.dropdown = true;
                }
                else if (temp_value.length > self.model.get("text_limit")) {
                    self.dropdown = true;
                    self.cols.push("over_length");
                    td.appendChild(document.createTextNode(temp_value));
                }
                else {
                    td.appendChild(document.createTextNode(temp_value));
                }
                // Storing the columns in the cols variable.
                if (!self.cols.includes(key) && key != "group") {
                    self.cols.push(key);
                }
                if (key != "group") {
                    tr.appendChild(td);
                }
            });
            // Adding the openning child column at beginning.
            if (self.dropdown) {
                var td = document.createElement('td');
                // td.appendChild(document.createTextNode("+"));
                td.className = "dt-control";
                (0, jquery_1.default)(tr).prepend(td);
            }
            else {
                var td = document.createElement('td');
                (0, jquery_1.default)(tr).prepend(td);
            }
            tbdy.appendChild(tr);
        });
        // end Body
        // start heading
        var thead = document.createElement('thead');
        var tr = document.createElement('tr');
        var append_first = false;
        jquery_1.default.each(self.cols, (i, value) => {
            var td = document.createElement('th');
            if (value != "group" && value != "over_length") {
                self.columns.push(value);
                append_first = true;
                td.appendChild(document.createTextNode(value));
                tr.appendChild(td);
            }
            else {
                append_first = true;
                // td.orderable = false;
            }
        });
        if (append_first) {
            var td = document.createElement('td');
            (0, jquery_1.default)(tr).prepend(td);
        }
        thead.appendChild(tr);
        self.tbl.appendChild(thead);
        self.tbl.appendChild(tbdy);
        self.wrapper.appendChild(self.tbl);
        self.el.appendChild(this.wrapper);
        // Finished creating table
        // Initializing everything
        (0, jquery_1.default)(document).ready(() => {
            // Code for when fullScreen goes on.
            var calcDataTableHeight = function () {
                return ((0, jquery_1.default)(window).height() || 0) - 200;
            };
            (0, jquery_1.default)(window).on('resize', function () {
                if (screen.width === window.innerWidth) {
                    //$('#example_'+self.cid).dataTable().fnSettings().oScroll.sY = calcDataTableHeight();
                    //$('.dataTables_scrollBody:has(#example_'+self.cid+')').height(calcDataTableHeight());  
                    (0, jquery_1.default)('#example_' + self.cid + '_wrapper .dataTables_scrollBody').css("height", calcDataTableHeight() + "px").css("max-height", calcDataTableHeight() + "px");
                    console.log("1");
                }
                else {
                    //$('#example_'+self.cid).dataTable().fnSettings().oScroll.sY = '400px';
                    //$('.dataTables_scrollBody:has(#example_'+self.cid+')').height('400px');  
                    console.log((0, jquery_1.default)('#example_' + self.cid + '_wrapper .dataTables_scrollBody'));
                    (0, jquery_1.default)('#example_' + self.cid + '_wrapper .dataTables_scrollBody').css("height", 400 + "px").css("max-height", 400 + "px");
                    console.log("2");
                }
            });
            // Add event listener for opening and closing details
            (0, jquery_1.default)('#example_' + self.cid + ' tbody').on('click', 'td.dt-control', (e) => {
                var column_index = self.table.columns().header().toArray().map((x) => x.innerText);
                // Child on click
                function format(d, index) {
                    // Get Child grouping select value
                    let child_select = self.model.get("child_group_select");
                    var tbl = document.createElement('table');
                    tbl.style.paddingLeft = '50px';
                    tbl.style.borderSpacing = '0';
                    var btn_group = "";
                    if (child_select) {
                        btn_group = document.createElement('div');
                        btn_group.classList.add('btn-group');
                        btn_group.classList.add('btn-group-toggle');
                        btn_group.setAttribute("data-toggle", "buttons");
                    }
                    jquery_1.default.each(d, (i, value) => {
                        if (value.length > self.model.get("text_limit")) {
                            // If not child select put column and row as format, else 
                            // add buttons for selection.
                            let tr = document.createElement('tr');
                            let td_col = document.createElement('td');
                            let td_value = document.createElement('td');
                            td_col.appendChild(document.createTextNode(column_index[i]));
                            td_value.appendChild(document.createTextNode(value));
                            tr.appendChild(td_col);
                            tr.appendChild(td_value);
                            tbl.appendChild(tr);
                        }
                    });
                    var t_row = self.model.get('table')[index];
                    if (t_row.hasOwnProperty('group')) {
                        jquery_1.default.each(t_row["group"], (i, value) => {
                            if (!child_select) {
                                let tr = document.createElement('tr');
                                let td_col = document.createElement('td');
                                let td_value = document.createElement('td');
                                td_col.appendChild(document.createTextNode(i));
                                td_value.appendChild(document.createTextNode(value));
                                tr.appendChild(td_col);
                                tr.appendChild(td_value);
                                tbl.appendChild(tr);
                            }
                            else {
                                let label = document.createElement('label');
                                label.style.marginRight = '10px';
                                let input = document.createElement('input');
                                input.setAttribute("type", "checkbox");
                                input.setAttribute("name", "options");
                                input.setAttribute("autocomplete", "off");
                                input.setAttribute("id", 'group_' + self.cid + "_" + index);
                                let selected_group = [...self.model.get("selected_group")];
                                jquery_1.default.each(selected_group, function (i_group, item_group) {
                                    if (item_group == index + ":" + i + ":" + value) {
                                        input.checked = true;
                                    }
                                });
                                input.onclick = function () {
                                    let selected_group = [...self.model.get("selected_group")];
                                    self.groupClick = true;
                                    if (selected_group.indexOf(index + ":" + i + ":" + value) < 0) {
                                        selected_group.push(index + ":" + i + ":" + value);
                                        self.model.set('selected_group', selected_group);
                                        self.touch();
                                    }
                                    else {
                                        selected_group.splice(selected_group.indexOf(index + ":" + i + ":" + value), 1);
                                        self.model.set('selected_group', selected_group);
                                        self.touch();
                                    }
                                };
                                label.appendChild(input);
                                label.appendChild(document.createTextNode(" " + value));
                                btn_group.appendChild(label);
                            }
                        });
                    }
                    if (child_select) {
                        let div = document.createElement('div');
                        div.appendChild(tbl);
                        div.appendChild(btn_group);
                        return div;
                    }
                    return tbl;
                }
                // Getting the proper row.
                let tr = e.target.closest('tr');
                let row = this.table.row(tr);
                if (row.child.isShown()) {
                    // This row is already open - close it
                    row.child.hide();
                }
                else {
                    // Open this row
                    row.child(format(row.data(), row.index())).show();
                }
            });
            // End of open row.
            self.selected = [...self.model.get("selected_index_row")];
            // Selecting a row action
            (0, jquery_1.default)('#example_' + self.cid + ' tbody').on('click', 'tr', function () {
                console.log(self.table);
                var temp = [];
                if (self.selected.includes(self.table.row(this).index())) {
                    self.selected.splice(self.selected.indexOf(self.table.row(this).index()), 1);
                }
                else {
                    self.selected.push(self.table.row(this).index());
                }
                jquery_1.default.each(self.selected, (i, value) => {
                    temp.push(table_data[value]);
                });
                self.onclickRowSelection = true;
                self.touch();
                self.model.set('selected_data', temp);
                self.model.set('selected_index_row', [...self.selected]);
                self.touch();
            });
            // End selected data
            // Adding column filtering spaces to table
            if (self.model.get("column_filter")) {
                // First column in the child opening
                self.column_order.push(0);
                (0, jquery_1.default)('#example_' + self.cid + ' thead tr').clone(true).appendTo('#example_' + self.cid + ' thead');
                (0, jquery_1.default)('#example_' + self.cid + ' thead tr:eq(1) th').each(function (i) {
                    var title = (0, jquery_1.default)(this).text();
                    self.column_order.push(i + 1);
                    (0, jquery_1.default)(this).html('<input type="text" placeholder="Search ' + title + '" />');
                    // Adding the search mechanism
                    (0, jquery_1.default)('input', this).on('keyup change clear', function () {
                        if (self.table.column(self.column_order.indexOf(i + 1)).search() !== this.value) {
                            self.table
                                .column(self.column_order.indexOf(i + 1))
                                .search(this.value)
                                .draw();
                        }
                    });
                });
            }
            // Column index for sorting.
            var sort_col = self.columns.indexOf(self.model.get("sort_column")) > -1 ? self.columns.indexOf(self.model.get("sort_column")) : 1;
            // Initialize hiding columns
            var hide_cols = [];
            jquery_1.default.each(self.columns, (i, item) => {
                if (item != "") {
                    if (self.model.get("init_state") == "hide") {
                        if (self.model.get("columns").includes(item)) {
                            hide_cols.push(i);
                        }
                    }
                    else {
                        if (!self.model.get("columns").includes(item)) {
                            hide_cols.push(i);
                        }
                    }
                }
            });
            // Creating table object
            self.table = (0, jquery_1.default)('#example_' + self.cid).DataTable({
                dom: 'Blfrtip',
                buttons: [
                    {
                        text: 'Full Screen',
                        action: (e, dt, node, config) => {
                            if (screenfull_1.default.isEnabled) {
                                screenfull_1.default.request((0, jquery_1.default)('#wrapper_' + self.cid)[0]);
                            }
                        }
                    },
                    {
                        extend: 'selectAll',
                        action: (e, dt, node, config) => {
                            var temp = [];
                            self.selected = [];
                            // dt.rows().every( function ( rowIdx:any, tableLoop:any, rowLoop:any ) {
                            //   var data = this.data();
                            //   self.selected.push( rowIdx );
                            //   temp.push(data);
                            // } );
                            dt.rows((idx, data) => {
                                self.selected.push(idx);
                                temp.push(data);
                            });
                            self.model.set('selected_data', temp);
                            self.model.set('selected_index_row', [...self.selected]);
                            self.touch();
                            // $.fn.dataTable.ext.buttons.selectAll.action!.call(this, e, dt, node, config);
                        }
                    },
                    {
                        extend: 'selectNone',
                        action: (e, dt, node, config) => {
                            let temp = [];
                            self.selected = [];
                            self.model.set('selected_data', temp);
                            self.model.set('selected_index_row', []);
                            self.touch();
                            // $.fn.dataTable.ext.buttons.selectNone.action!.call(this, e, dt, node, config);
                        }
                    },
                    {
                        extend: 'colvis',
                        columns: ':not(.notToggleVis)',
                    },
                    'searchBuilder', 'copy', 'csv', 'excel', 'print'
                ],
                orderCellsTop: true,
                //"autoWidth": false,
                order: [[sort_col, "desc"]],
                "lengthMenu": [[10, 25, 50, 100, 500, -1], [10, 25, 50, 100, 500, "All"]],
                fixedHeader: true,
                scrollY: "400px",
                // scrollResize: true,
                "scrollCollapse": true,
                scrollX: true,
                select: {
                    style: 'multi'
                },
                colReorder: true,
                // responsive:true,
                columnDefs: [
                    { width: "10px", targets: 0, orderable: false, className: "notToggleVis" },
                    { targets: hide_cols, visible: false },
                    {
                        targets: "_all",
                        "width": '70px',
                        render: function (data, type, row) {
                            return data.length > self.model.get("text_limit") ?
                                data.substr(0, self.model.get("text_limit")) + '…' :
                                data;
                        }
                    }
                ]
            });
            (0, jquery_1.default)('#example_' + self.cid + ' td').css('white-space', 'initial');
            (0, jquery_1.default)('#example_' + self.cid + ' td').css('word-break', 'break-word');
            // Initalizing the selection of the data on the table.
            let selected_data = [];
            jquery_1.default.each(self.model.get("selected_index_row"), (index, val) => {
                selected_data.push(self.model.get("table")[val]);
                self.table.row(val).select();
            });
            self.model.set('selected_data', selected_data);
            self.touch();
            // Ending selection data
            self.table.on('column-reorder', function (e, settings, details) {
                // var curr = details.mapping;
                var temp = [];
                jquery_1.default.each(settings['aoColumns'], (index, val) => {
                    temp.push(val['_ColReorder_iOrigCol']);
                });
                self.column_order = temp;
            });
            self.wrapper.style.display = "block";
            // Only for JupyterLab to make table not be gigantic.
            if (true) {
                self.wrapper.style.width = (document.getElementById("wrapper_" + self.cid).parentNode.parentNode.parentNode.parentElement.clientWidth - 100) + "px";
                self.wrapper.style.setProperty('color', 'black', 'important');
            }
            self.table.columns.adjust();
        });
    }
    selected_group_changed() {
        let self = this;
        // let data = [...self.model.get('selected_group')];
        let table = new datatables_net_dt_1.default('#example_' + self.cid);
        if (!self.groupClick) {
            table.rows().every(function (rowIdx, tableLoop, rowLoop) {
                let d = this.data();
                console.log("Data: ", d);
                if (d[0] == "-") {
                    d[0] = "+";
                    this.data(d);
                }
                this.invalidate();
                let child = table.row(rowIdx).child;
                if (child.isShown()) {
                    child.hide();
                }
            });
            table
                .rows('.selected')
                .nodes()
                .to$()
                .removeClass('selected');
            table.draw();
            self.touch();
        }
    }
    selected_index_row_changed() {
        let self = this;
        console.log(self.model.get('selected_index_row'));
        let table = (0, jquery_1.default)('#example_' + self.cid).DataTable();
        // Initalizing the selection of the data on the table.
        let selected_data = [];
        if (!self.onclickRowSelection) {
            console.log(table);
            table
                .rows('.selected')
                .nodes()
                .to$()
                .removeClass('selected');
            jquery_1.default.each(self.model.get("selected_index_row"), (index, val) => {
                selected_data.push(self.model.get("table")[val]);
                let row = table.row(val);
                row.select();
            });
            self.model.set('selected_data', selected_data);
            self.touch();
        }
        else {
            self.onclickRowSelection = false;
        }
        self.groupClick = false;
        // Ending selection data
    }
    create_style_jinteractive() {
        if (true) {
            var fa = 'Font Awesome\ 5 Free';
        }
        else { var fa; }
        var style = `
    div.dataTables_scrollHead table.dataTable thead th.sorting_asc::after,
    div.dataTables_scrollHead table.dataTable thead th.sorting_desc::after {
      content:"" !important;
    }
    div.dataTables_scrollHead table.dataTable thead .sorting:after {
      content: "\\f0dc";
      float: left;
      font-family: '${fa}';
      padding-right:5px;
    }
    div.dataTables_scrollHead table.dataTable thead th.sorting_asc:after {
      font-family: '${fa}';
      float: left;
      content: "\\f0de" !important;
      padding-right:5px;
    }
    div.dataTables_scrollHead table.dataTable thead th.sorting_desc:after {
      font-family: '${fa}';
      float: left;
      content: "\\f0dd" !important;
      padding-right:5px;
    }
    div.dt-button-collection {
      max-height: 200px !important;
      overflow-y: auto !important;
    }
    `;
        this.style_context = document.createElement('style');
        this.style_context.innerHTML = style;
        this.el.appendChild(this.style_context);
    }
}
exports.InteractiveTableView = InteractiveTableView;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.custom-widget {
  background-color: lightseagreen;
  padding: 0px 2px;
}
`, "",{"version":3,"sources":["webpack://./css/widget.css"],"names":[],"mappings":"AAAA;EACE,+BAA+B;EAC/B,gBAAgB;AAClB","sourcesContent":[".custom-widget {\n  background-color: lightseagreen;\n  padding: 0px 2px;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = /*#__PURE__*/JSON.parse('{"name":"ipydatatable","version":"1.0.4","description":"Library to wrap interactive datatables js into a library that helps pandas dataframes","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://gitlab.com/teia_engineering/ipydatatable","bugs":{"url":"https://gitlab.com/teia_engineering/ipydatatable/issues"},"license":"BSD-3-Clause","author":{"name":"David Fernandez","email":"teia.eng.14@gmail.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://gitlab.com/teia_engineering/ipydatatable"},"scripts":{"build":"jlpm run build:lib && jlpm run build:nbextension && jlpm run build:labextension:dev","build:prod":"jlpm run build:lib && jlpm run build:nbextension && jlpm run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"jlpm run clean:lib && jlpm run clean:nbextension && jlpm run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipydatatable/labextension","clean:nbextension":"rimraf ipydatatable/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"jlpm run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6"},"devDependencies":{"@babel/core":"^7.23.7","@babel/preset-env":"^7.23.8","@jupyter-widgets/base-manager":"^1.0.7","@jupyterlab/builder":"^4.0.11","@lumino/application":"^2.3.0","@lumino/widgets":"^2.3.1","@types/jest":"^29.5.11","@types/jquery":"^3.5.30","@types/pdfmake":"^0.2.9","@types/webpack-env":"^1.18.4","@typescript-eslint/eslint-plugin":"^6.19.1","@typescript-eslint/parser":"^6.19.1","acorn":"^8.11.3","bootstrap":"^3.4.1","css-loader":"^6.9.1","datatables.net":"^2.1.6","datatables.net-buttons":"^3.1.2","datatables.net-buttons-dt":"^3.1.2","datatables.net-colreorder":"^2.0.4","datatables.net-datetime":"^1.5.3","datatables.net-dt":"^2.1.6","datatables.net-fixedheader":"^4.0.1","datatables.net-plugins":"^2.0.8","datatables.net-responsive":"^3.0.3","datatables.net-scroller":"^2.4.3","datatables.net-searchbuilder-dt":"^1.8.0","datatables.net-searchpanes":"^2.3.2","datatables.net-select":"^2.0.5","eslint":"^8.56.0","eslint-config-prettier":"^9.1.0","eslint-plugin-prettier":"^5.1.3","fontawesome":"^5.6.3","fs-extra":"^11.2.0","identity-obj-proxy":"^3.0.0","jest":"^29.7.0","jquery":"^3.6.0","jszip":"^3.6.0","lodash":"^4.17.4","mkdirp":"^3.0.1","npm-run-all":"^4.1.5","pdfmake":"^0.1.71","prettier":"^3.2.4","rimraf":"^5.0.5","sass-loader":"^12.1.0","screenfull":"^5.1.0","source-map-loader":"^5.0.0","style-loader":"^3.3.4","ts-jest":"^29.1.2","ts-loader":"^9.5.1","typescript":"~5.3.3","webpack":"^5.90.0","webpack-cli":"^5.1.4"},"devDependenciesComments":{"@jupyterlab/builder":"pinned to the latest JupyterLab 3.x release","@lumino/application":"pinned to the latest Lumino 1.x release","@lumino/widgets":"pinned to the latest Lumino 1.x release"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipydatatable/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.f3f34a18b72f45ab6122.js.map