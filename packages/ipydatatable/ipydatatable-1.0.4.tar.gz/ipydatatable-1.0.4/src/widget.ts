// Copyright (c) David Fernandez
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

import $ from "jquery";
import 'datatables.net'
import 'jszip'
import 'datatables.net-dt';
import 'datatables.net-select';
import 'datatables.net-colreorder';
import 'datatables.net-responsive';
import 'datatables.net-datetime';
import 'datatables.net-searchbuilder-dt';
import 'datatables.net-buttons';
import 'datatables.net-buttons-dt';
import 'datatables.net-buttons/js/buttons.colVis.js';
import 'datatables.net-buttons/js/buttons.html5.js';
import 'datatables.net-buttons/js/buttons.print.js';
import 'datatables.net-fixedheader';
// import 'datatables.net-plugins';
import 'datatables.net-scroller';
import 'fontawesome';
// import 'pdfmake'
import screenfull from 'screenfull';
import 'jszip';

// Import the CSS
import '../css/widget.css';

// Load datatables styles
import '!style-loader!css-loader!datatables.net-dt/css/dataTables.dataTables.css';
import '!style-loader!css-loader!datatables.net-searchbuilder-dt/css/searchBuilder.dataTables.css';
import '!style-loader!css-loader!datatables.net-buttons-dt/css/buttons.dataTables.css';
import '!style-loader!css-loader!datatables.net-datetime/dist/dataTables.dateTime.min.css';
import DataTable from 'datatables.net-dt';

export class InteractiveTableModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: InteractiveTableModel.model_name,
      _model_module: InteractiveTableModel.model_module,
      _model_module_version: InteractiveTableModel.model_module_version,
      _view_name: InteractiveTableModel.view_name,
      _view_module: InteractiveTableModel.view_module,
      _view_module_version: InteractiveTableModel.view_module_version,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'InteractiveTableModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'InteractiveTableView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class InteractiveTableView extends DOMWidgetView {
  column_order:any[] = [];
  style_context:any = null;
  selected_data:any[] = [];
  onclickRowSelection:boolean = false;
  groupClick:boolean = false;
  wrapper:any = null;
  tbl:any = null
  cols:any[] = [];
  dropdown:boolean = false;
  columns:any[] = [""];
  table:any = null;;
  selected:any[] = [];

  render () {
    console.log("in render!!")
    var self = this;
    // Keeps the order of the columns for filtering.
    // This is important for when we move the columns.
    self.column_order = [];
    // Loading CSS for library.
    self.create_style_jinteractive();
    // Get table data from Python
    var table_data = self.model.get('table');
    // Selected data variable.
    self.selected_data = []

    //self.model.on('change:selected_data', this.selected_data_changed, this);
    self.model.on('change:selected_index_row', this.selected_index_row_changed, this);
    self.model.on('change:selected_group', this.selected_group_changed, this);

    self.onclickRowSelection = false;
    self.groupClick = false;

    // Creating a wrapper element
    self.wrapper = document.createElement('div');
    self.wrapper.id = "wrapper_"+self.cid;
    self.wrapper.style.display = "none";
    self.wrapper.style.width = '100%';
    self.wrapper.style.setProperty('color', 'black', 'important');
    self.wrapper.style.backgroundColor="white";

    // Creating table element
    self.tbl = document.createElement('table');
    self.tbl.style.width = '100%';
    self.tbl.style.setProperty('color', 'black', 'important');
    self.tbl.style.wordWrap = "break-word";
    self.tbl.id = "example_"+self.cid;
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
    $.each(table_data,(i, value) => {
      self.dropdown = false;
      var tr = document.createElement('tr');
      // Go through each column of a row and add them to the element
      Object.keys(value).forEach(function(key) {
        var td = document.createElement('td');
        
        // Formatting the data
        if(typeof value[key] === 'string' || value[key] instanceof String){
          var temp_value:any = value[key];
        }
        else if (value[key] == null){
          var temp_value:any = "";
        }
        else{
          var temp_value:any = value[key].toString();
        }

        // Checking to see if data is overflowed on limit or is group.
        // Makes it so you will have a child row.
        if(key == "group"){
          self.dropdown = true;
        }else if(temp_value.length > self.model.get("text_limit")){
          self.dropdown = true;
          self.cols.push("over_length")
          td.appendChild(document.createTextNode(temp_value));
        }else{
          td.appendChild(document.createTextNode(temp_value));
        }

        // Storing the columns in the cols variable.
        if(!self.cols.includes(key) && key != "group"){
          self.cols.push(key)
        }
        if(key!="group"){
          tr.appendChild(td);
        }
      });
      // Adding the openning child column at beginning.
      if(self.dropdown){
        var td = document.createElement('td');
        // td.appendChild(document.createTextNode("+"));
        td.className = "dt-control";

        $(tr).prepend(td)
      }
      else{
        var td = document.createElement('td');
        $(tr).prepend(td)
      }

      tbdy.appendChild(tr);
    })
    // end Body

    // start heading
    var thead = document.createElement('thead');
    var tr = document.createElement('tr');
    var append_first = false;
    $.each(self.cols,(i, value) => {
      var td = document.createElement('th');
      if(value != "group" && value != "over_length"){
        self.columns.push(value)
        append_first = true;
        td.appendChild(document.createTextNode(value))
        tr.appendChild(td)
      }
      else{
        append_first = true;
        // td.orderable = false;
      }
    });

    if(append_first){
      var td = document.createElement('td');
      $(tr).prepend(td)
    }
    thead.appendChild(tr);

    self.tbl.appendChild(thead);
    self.tbl.appendChild(tbdy);
    self.wrapper.appendChild(self.tbl);
    self.el.appendChild(this.wrapper)
    // Finished creating table

    // Initializing everything
    $(document).ready(  () => {
      // Code for when fullScreen goes on.
      var calcDataTableHeight = function() {
        return ($(window).height() || 0) - 200;
      };
      
      $(window).on('resize', function(){
        if(screen.width === window.innerWidth){
          //$('#example_'+self.cid).dataTable().fnSettings().oScroll.sY = calcDataTableHeight();
          //$('.dataTables_scrollBody:has(#example_'+self.cid+')').height(calcDataTableHeight());  
          $('#example_'+self.cid+'_wrapper .dataTables_scrollBody').css("height",calcDataTableHeight()+"px").css("max-height",calcDataTableHeight()+"px");
          console.log("1");
        }
        else{
          //$('#example_'+self.cid).dataTable().fnSettings().oScroll.sY = '400px';
          //$('.dataTables_scrollBody:has(#example_'+self.cid+')').height('400px');  
          console.log($('#example_'+self.cid+'_wrapper .dataTables_scrollBody'))
          $('#example_'+self.cid+'_wrapper .dataTables_scrollBody').css("height",400+"px").css("max-height",400+"px");
          console.log("2");
        }
      });

      // Add event listener for opening and closing details
      $('#example_'+self.cid+' tbody').on('click', 'td.dt-control', (e) =>{
        var column_index = self.table.columns().header().toArray().map((x:any) => x.innerText)

        // Child on click
        function format ( d:any, index:any ) {
          // Get Child grouping select value
          let child_select = self.model.get("child_group_select");
          var tbl = document.createElement('table');
          tbl.style.paddingLeft = '50px';
          tbl.style.borderSpacing = '0';
          var btn_group:any = ""

          if(child_select){
            btn_group = document.createElement('div');
            btn_group.classList.add('btn-group');
            btn_group.classList.add('btn-group-toggle');
            btn_group.setAttribute("data-toggle","buttons");
          }
          $.each(d, (i, value) => {
            if(value.length > self.model.get("text_limit")){
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
          })
          var t_row = self.model.get('table')[index];

          if(t_row.hasOwnProperty('group')){
            $.each(t_row["group"], (i:any, value:any) => {
              if(!child_select){
                let tr = document.createElement('tr');
                let td_col = document.createElement('td');
                let td_value = document.createElement('td');
                
                td_col.appendChild(document.createTextNode(i));
                td_value.appendChild(document.createTextNode(value));
                tr.appendChild(td_col);
                tr.appendChild(td_value);
                tbl.appendChild(tr);
              }else{
                let label = document.createElement('label');
                label.style.marginRight = '10px'

                let input = document.createElement('input');
                input.setAttribute("type","checkbox");
                input.setAttribute("name","options");
                input.setAttribute("autocomplete","off")
                input.setAttribute("id",'group_'+self.cid+"_"+index);

                let selected_group = [...self.model.get("selected_group")];
                $.each(selected_group,function(i_group, item_group){
                  if(item_group == index+":"+i+":"+value){
                   input.checked=true;
                  }
                });
                
                
                input.onclick = function(){
                  let selected_group = [...self.model.get("selected_group")];
                  self.groupClick = true;
                  if(selected_group.indexOf(index+":"+i+":"+value)<0){
                    selected_group.push(index+":"+i+":"+value);
                    self.model.set('selected_group', selected_group);
                    self.touch();
                  }
                  else{
                    selected_group.splice(selected_group.indexOf(index+":"+i+":"+value),1);
                    self.model.set('selected_group', selected_group);
                    self.touch();
                  }
                }
                label.appendChild(input);
                label.appendChild(document.createTextNode(" "+value));
                btn_group.appendChild(label);
              }
            })
          }

          if(child_select){
            let div = document.createElement('div');
            div.appendChild(tbl);
            div.appendChild(btn_group)
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
      $('#example_'+self.cid+' tbody').on( 'click', 'tr', function () {
          console.log(self.table)
          var temp:any[] = []
          if(self.selected.includes(self.table.row( this ).index() )){
            self.selected.splice(self.selected.indexOf(self.table.row( this ).index() ),1)
          }else{
            self.selected.push(self.table.row( this ).index() );
          }
          $.each(self.selected,(i, value)=>{
            temp.push(table_data[value])
          })
          self.onclickRowSelection = true;
          self.touch();
          self.model.set('selected_data', temp);
          self.model.set('selected_index_row', [...self.selected]);
          self.touch();
      } );
      // End selected data

      // Adding column filtering spaces to table
      if(self.model.get("column_filter")){
        // First column in the child opening
        self.column_order.push(0);
        $('#example_'+self.cid+' thead tr').clone(true).appendTo( '#example_'+self.cid+' thead' );
        $('#example_'+self.cid+' thead tr:eq(1) th').each(  function (i) {
          var title = $(this).text();
          self.column_order.push(i+1);
          $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
          // Adding the search mechanism
          $( 'input', this ).on( 'keyup change clear',  function() {
              if ( self.table.column(self.column_order.indexOf(i+1)).search() !== (this as HTMLInputElement).value ) {
                self.table
                      .column(self.column_order.indexOf(i+1))
                      .search( (this as HTMLInputElement).value )
                      .draw();
              }
          } );
        } );
      }

      // Column index for sorting.
      var sort_col = self.columns.indexOf(self.model.get("sort_column")) > -1 ? self.columns.indexOf(self.model.get("sort_column")) : 1;
      // Initialize hiding columns
      var hide_cols:any[] = []
      $.each(self.columns, (i, item) => {
        if(item != ""){
          if(self.model.get("init_state") == "hide"){
            if(self.model.get("columns").includes(item) ){
              hide_cols.push(i)
            }
          }
          else{
            if(!self.model.get("columns").includes(item)){
              hide_cols.push(i)
            }
          }
        }
      });

      // Creating table object
      self.table = $('#example_'+self.cid).DataTable({
        dom: 'Blfrtip',
        buttons: [
          {
            text: 'Full Screen',
            action: ( e, dt, node, config ) => {
              if (screenfull.isEnabled) {
                screenfull.request($('#wrapper_'+self.cid)[0]);
              }
            }
          },
          {
            extend: 'selectAll',
            action:  (e:any, dt:any, node:any, config:any ) => {
              var temp:any[] = []
              self.selected = [];
              // dt.rows().every( function ( rowIdx:any, tableLoop:any, rowLoop:any ) {
              //   var data = this.data();
              //   self.selected.push( rowIdx );
              //   temp.push(data);
              // } );

              dt.rows((idx:any, data:any) => {
                self.selected.push( idx );
                temp.push(data);
              })
              self.model.set('selected_data', temp);
              self.model.set('selected_index_row', [...self.selected]);
              self.touch();
              // $.fn.dataTable.ext.buttons.selectAll.action!.call(this, e, dt, node, config);
            }
          },
          {
            extend: 'selectNone',
            action: ( e:any, dt:any, node:any, config:any ) => {
              let temp:any[] = []
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
          'searchBuilder','copy', 'csv', 'excel', 'print'
        ],
        orderCellsTop: true,
        //"autoWidth": false,
        order: [[ sort_col , "desc" ]],
        "lengthMenu": [[10, 25, 50, 100, 500, -1], [10, 25, 50, 100, 500, "All"]],
        fixedHeader: true,
        scrollY: "400px",
        // scrollResize: true,
        "scrollCollapse": true,
        scrollX: true,
        select:{
          style: 'multi'
        },
        colReorder: true,
        // responsive:true,
        columnDefs: [ 
          { width: "10px", targets: 0, orderable: false, className:"notToggleVis" },
          { targets: hide_cols, visible: false },
          {
              targets:"_all",
              "width": '70px',
              render: function ( data, type, row ) {
                return data.length > self.model.get("text_limit") ?
                  data.substr( 0, self.model.get("text_limit") ) +'…' :
                  data;
              }
          } 
        ]
      });
      $('#example_'+self.cid+' td').css('white-space','initial');
      $('#example_'+self.cid+' td').css('word-break','break-word');

      // Initalizing the selection of the data on the table.
      let selected_data:any[] = []
      $.each(self.model.get("selected_index_row"),(index, val) => {
        selected_data.push(self.model.get("table")[val])
        
        self.table.row( val ).select()
      })
      self.model.set('selected_data', selected_data);
      self.touch();
      // Ending selection data
      
      self.table.on( 'column-reorder', function ( e:any, settings:any, details:any ) {
        // var curr = details.mapping;

        var temp:any[] = []
        $.each(settings['aoColumns'],(index, val) => {
          temp.push(val['_ColReorder_iOrigCol']);
        });

        self.column_order = temp;
      } );

      self.wrapper.style.display = "block";
      // Only for JupyterLab to make table not be gigantic.
      if(true){
        self.wrapper.style.width = (document.getElementById("wrapper_"+self.cid)!.parentNode!.parentNode!.parentNode!.parentElement!.clientWidth-100)+"px";
        self.wrapper.style.setProperty('color', 'black', 'important');
      }        
      self.table.columns.adjust();
    } );
  }

  
  

  selected_group_changed(){
    let self = this;
    // let data = [...self.model.get('selected_group')];
    let table = new DataTable('#example_'+self.cid);
    if (!self.groupClick){
      table.rows().every(  function( rowIdx:any, tableLoop:any, rowLoop:any )  {
        let d = this.data();
        console.log("Data: ",d)
        
        if(d[0] == "-"){
          d[0] = "+"
          this.data(d);
        }
        
        this.invalidate();
    
        let child = table.row( rowIdx ).child;

        if ( child.isShown() ) {
            child.hide();
        }
        
      } );  

      table 
        .rows( '.selected' )
        .nodes()
        .to$() 
        .removeClass( 'selected' );  

      table.draw();
      self.touch();
    }
  }

  selected_index_row_changed (){
    let self = this;
    console.log(self.model.get('selected_index_row'));
    let table = $('#example_'+self.cid).DataTable();
    // Initalizing the selection of the data on the table.
    let selected_data:any[] = []
    if (!self.onclickRowSelection){
      console.log(table)
      table 
        .rows( '.selected' )
        .nodes()
        .to$() 
        .removeClass( 'selected' );

      $.each(self.model.get("selected_index_row"),(index:any, val:any ) => {
        selected_data.push(self.model.get("table")[val])
        
        let row:any = table.row( val )
        row.select()
      })
      self.model.set('selected_data', selected_data);
      self.touch();
    }else{
      self.onclickRowSelection = false;
    }
    self.groupClick = false;
    // Ending selection data
  }

  create_style_jinteractive (){
    if(true){
      var fa = 'Font Awesome\ 5 Free'
    }else{
      var fa = "fontawesome"
    }
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