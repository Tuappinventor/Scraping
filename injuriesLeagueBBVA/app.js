
var dataLeague = [ 
  {   
    url: "https://raw.githubusercontent.com/Xatpy/Scraping/master/injuriesLeagueBBVA/data/J31.csv", 
    chart:"chart_j31", table:"tableInjuries_j31"  , 
    dataCSV:{} , sortable : [] , pie_data : [] , num : 31 ,
  },
  { 
    url: "https://raw.githubusercontent.com/Xatpy/Scraping/master/injuriesLeagueBBVA/data/J32.csv", 
    chart:"chart_j32", table:"tableInjuries_j32"  , 
    dataCSV:{} , sortable : [] , pie_data : [] , num : 32 ,
  },
  { 
    url: "https://raw.githubusercontent.com/Xatpy/Scraping/master/injuriesLeagueBBVA/data/J33.csv", 
    chart:"chart_j33", table:"tableInjuries_j33"  , 
    dataCSV:{} , sortable : [] , pie_data : [] , num : 33 ,
  },
  { 
    url: "https://raw.githubusercontent.com/Xatpy/Scraping/master/injuriesLeagueBBVA/data/J34.csv", 
    chart:"chart_j34", table:"tableInjuries_j34"  , 
    dataCSV:{} , sortable : [] , pie_data : [] , num : 34 ,
  },
];

window.onload = function() {
  createDivs();

  for (var i = 0; i < dataLeague.length; ++i) {
    loadCSV(  dataLeague[i].url, dataLeague[i].chart, dataLeague[i].table, 
            dataLeague[i].dataCSV, dataLeague[i].sortable, dataLeague[i].pie_data );
  }
};

/* :== TEMPLATE ==:
    <div class="page-header" style="margin:10px" >
      <h2><a href="http://www.goal.com/es/news/27/liga-de-espa%C3%B1a/2015/12/30/4730098/sancionados-lesionados-y-apercibidos" target="_blank"><stroke>Jornada 31</stroke></a></h2>
    </div>
    <div class="row">
      <div class="col-md-6">
        <canvas id="chart_j31" max-width="650" height="400"></canvas>
      </div>
      <div class="col-md-6">
        <div id="tableInjuries_j31" style="overflow: scroll;height: 400px;"></div>
      </div>
    </div>
*/
function createDivs() {
  debugger
  var mainDiv = document.getElementById("mainContainer");

  for (var i = dataLeague.length - 1 ; i >= 0; --i) {
    debugger
    var divJornada = document.createElement("div");
    divJornada.appendChild(createHeaderDiv(i));
    divJornada.appendChild(createContentDiv(i));

    mainDiv.appendChild(divJornada);
  }
}

function createContentDiv(i) {
  debugger
  var divRow = document.createElement("div");
  divRow.className = "row";

  // Create char Canvas
  var divChar = document.createElement("div");
  divChar.className = "col-md-6";
  var canvas = document.createElement("canvas");
  canvas.id = dataLeague[i].chart;
  canvas.style.maxWidth = "600px";
  canvas.style.height = "400px";
  divChar.appendChild(canvas);

  var divColTable = document.createElement("div");
  divColTable.class = "col-md-6";
  var divTable = document.createElement("div");
  divTable.id = dataLeague[i].table;
  divTable.style.overflow = "scroll";
  divTable.style.height = "400px";

  divColTable.appendChild(divTable);

  divRow.appendChild(divChar);
  divRow.appendChild(divColTable);

  return divRow;
}

function createHeaderDiv(i) {
    var div = document.createElement("div");
    div.className = "page-header";
    div.style.margin = "10px";
    
    var a = document.createElement('a');
    var title = "Jornada " + dataLeague[i].num;
    var linkText = document.createTextNode(title);
    a.appendChild(linkText);
    a.title = title;
    a.href = "http://www.goal.com/es/news/27/liga-de-espa%C3%B1a/2015/12/30/4730098/sancionados-lesionados-y-apercibidos";

    var h2 = document.createElement('h2');

    h2.appendChild(a);
    div.appendChild(h2);
    return div;
}

function loadCSV(csv_url, chart, tableElement, dataCSV, sortable, pie_data) {
    $.ajax({
      url: csv_url,
      csv_as_array : [],
      aync: false,
      success: function (csvd) {
          csv_as_array = $.csv2Array(csvd);
      }, 
      dataType: "text",
      complete: function () {

        for (var contCsv = 1; contCsv < csv_as_array.length; ++contCsv) {
          addRecord(csv_as_array[contCsv][0], csv_as_array[contCsv][1], dataCSV);
        }

        orderList(dataCSV, sortable);   

        fillPieChart(chart, sortable, pie_data);

        fillTable(tableElement, sortable, pie_data);                 
      }
    });
};

function addRecord(player, injury, dataCSV){
  if ( (dataCSV[injury] === undefined) || (dataCSV[injury] === null) ){
    dataCSV[injury] = [];                
  }
  dataCSV[injury].push(player);
}

function orderList(dataCSV, sortable){
  for (var key in dataCSV){
    sortable.push([key, dataCSV[key]])
  }
  sortable.sort(function(a, b) {
    if (a[1].length === b[1].length){
      if(a[0] < b[0]) 
        return -1;
      if(a[0] > b[0]) 
        return 1;
    } else
      return b[1].length - a[1].length;
  });
}

function fillPieChart(chart, sortable, pie_data){
  for (var i = 0; i < sortable.length; ++i){
    pie_data[i] = {
        color : createRandomColor(),
        value : sortable[i][1].length,
        label : sortable[i][0]
      }
  };

  createPieChar(chart, pie_data);
}

function createPieChar(chart, pie_data){
  // pie chart options
  var pieOptions = {
       segmentShowStroke : false,
       animateScale : true,
  }
  // get pie chart canvas
  var countries= document.getElementById(chart).getContext("2d");
  // draw pie chart
  var chart = new Chart(countries).Pie(pie_data, pieOptions);
}

function createRandomColor() {
  return '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6);
}

function fillTable(tableElement, sortable, pie_data){
  var table = document.createElement('table');
  table.className = "table";
  var thead = document.createElement('thead');
  var tr = document.createElement('tr');   
  var td1 = document.createElement('th');
  var td2 = document.createElement('th');
  var td3 = document.createElement('th');
  var text1 = document.createTextNode("#");
  var text2 = document.createTextNode("Lesión");
  var text3 = document.createTextNode("Jugadores");
  td1.appendChild(text1);
  td2.appendChild(text2);
  td3.appendChild(text3);
  tr.appendChild(td1);
  tr.appendChild(td2);
  tr.appendChild(td3);
  thead.appendChild(tr);
      
  table.appendChild(thead);

  var tbody = document.createElement('tbody');   
  for (var i = 0; i < sortable.length; i++){
      var tr = document.createElement('tr');   

      var td1 = document.createElement('td');
      var td2 = document.createElement('td');
      var td3 = document.createElement('td');

      var text1 = document.createTextNode(sortable[i][1].length);
      var text2 = document.createTextNode(sortable[i][0]);
      var players = "";
      for (var j = 0; j < sortable[i][1].length; ++j){
        players += sortable[i][1][j] + "\r\n";
      }
      var text3 = document.createTextNode(players);

      td1.appendChild(text1);
      td1.style.background = pie_data[i].color; //pie_data is already filled,and it has the same index than sortable
      td2.appendChild(text2);
      td3.appendChild(text3);
      tr.appendChild(td1);
      tr.appendChild(td2);
      tr.appendChild(td3);
      
      tbody.appendChild(tr);
  }
  table.appendChild(tbody);

  document.getElementById(tableElement).appendChild(table);
}
