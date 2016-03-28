var data = {};
var sortable = [];
var csv_as_array = [];
var pie_data = [];

window.onload = function() {
  loadCSV();
};

function createRandomColor() {
  return '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6);
}

function addRecord(player, injury){
  if ( (data[injury] === undefined) || (data[injury] === null) ){
    data[injury] = [];                
  }
  data[injury].push(player);
}

function orderList(){
  for (var key in data){
    sortable.push([key, data[key]])
  }
  sortable.sort(function(a, b) {
    if (a[1].length === b[1].length){
      if(a[0] < b[0]) return -1;
      if(a[0] > b[0]) return 1;
    } else
      return b[1].length - a[1].length;
  });
}

function loadCSV() {
    $.ajax({
      url: "https://raw.githubusercontent.com/Xatpy/Scraping/master/injuriesLeagueBBVA/J31.csv",
      aync: false,
      success: function (csvd) {
          csv_as_array = $.csv2Array(csvd);
      }, 
      dataType: "text",
      complete: function () {
        for (var contCsv = 1; contCsv < csv_as_array.length; ++contCsv) {
          addRecord(csv_as_array[contCsv][0], csv_as_array[contCsv][1]);
        }

        orderList();   

        fillPieChart();

        fillTable();                 
      }
    });
};

function fillTable(){
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

  document.getElementById("tableInjuries").appendChild(table);
}

function fillPieChart(){
  for (var i = 0; i < sortable.length; ++i){
    pie_data[i] = {
        color : createRandomColor(),
        value : sortable[i][1].length,
        label : sortable[i][0]
      }
  };

  createPieChar();
}

function createPieChar(){
  // pie chart options
  var pieOptions = {
       segmentShowStroke : false,
       animateScale : true,
  }
  // get pie chart canvas
  var countries= document.getElementById("countries").getContext("2d");
  // draw pie chart
  var chart = new Chart(countries).Pie(pie_data, pieOptions);
}