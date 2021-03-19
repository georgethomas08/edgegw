document.addEventListener('DOMContentLoaded', function() {
  $(document).ready(function(){
     tChartLoad();
     hChartLoad();
     pChartLoad();
  });

 setInterval(tChartLoad(),5000);

    document.getElementById("tbutton").onclick = function() {tChartLoad()};
    document.getElementById("hbutton").onclick = function() {hChartLoad()};
    document.getElementById("pbutton").onclick = function() {pChartLoad()};

    function arrayMin(arr) {
    var len = arr.length, min = Infinity;
    while (len--) {
      if (arr[len] < min) {
        min = arr[len];
      }
    }
    return min;
    };

    function arrayMax(arr) {
    var len = arr.length, max = -Infinity;
    while (len--) {
      if (arr[len] > max) {
        max = arr[len];
      }
    }
    return max;
    };

    function arrayAvg(arr) {
    var len = arr.length, avg = 0;
    while (len--) {
      avg += arr[len];
    }
    return (parseFloat((avg / arr.length)).toFixed(2));
    };

    function tChartLoad() {
      var getData = $.get('/tdata');
      getData.done(function(temprecs){
        //console.log(temprecs);
        var tempArr = temprecs.temprecs.map(element => element.temp);
        console.log(tempArr);
        //var tAvg = tempArr.reduce(function(sum, a) { return sum + a },0)/(tempArr.length||1);
        document.getElementById('tTable').rows[1].cells[0].innerHTML = arrayMin(tempArr);
        document.getElementById('tTable').rows[1].cells[1].innerHTML = arrayMax(tempArr);
        document.getElementById('tTable').rows[1].cells[2].innerHTML = arrayAvg(tempArr);
        var tsArr = temprecs.temprecs.map(element => element.ts.$date);
        //console.log(tsArr);
        var cnvTsArr = tsArr.map(function(element){
        var temp = new Date(parseInt(element))
        element = temp.toISOString().substring(11,19)
        return element;
        });
        console.log(cnvTsArr);

        var ctx = document.getElementById('tChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: cnvTsArr,
                datasets: [{
                    label: 'Temperature',
                    data: tempArr,
                    borderWidth: 2,
                    borderColor: 'brown',
                    backgroundColor: 'rgba(0, 0, 255, 0.1)',
                    fillOpacity: 0.3
                }]
            },
            options: {
                responsive: false,
                title:{
                  display: true,
                  text: "Temparature time series(Last 1 hr)"
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
      });
    };

    function hChartLoad(){
      var getData = $.get('/hdata');
      getData.done(function(humrecs){
        //console.log(humrecs);

        var humArr = humrecs.humrecs.map(element => element.humidity);
        console.log(humArr);
        //var hAvg = humArr.reduce(function(sum, a) { return sum + a },0)/(humArr.length||1);
        document.getElementById('hTable').rows[1].cells[0].innerHTML = arrayMin(humArr);
        document.getElementById('hTable').rows[1].cells[1].innerHTML = arrayMax(humArr);
        document.getElementById('hTable').rows[1].cells[2].innerHTML = arrayAvg(humArr);
        var tsArr = humrecs.humrecs.map(element => element.ts.$date);
        //console.log(tsArr);

        var cnvTsArr = tsArr.map(function(element){
          var temp = new Date(parseInt(element))
          element = temp.toISOString().substring(11,19)
          return element;
        });
        console.log(cnvTsArr);

        var ctx = document.getElementById('hChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: cnvTsArr,
                datasets: [{
                    label: 'Humidity',
                    data: humArr,
                    borderWidth: 2,
                    borderColor: 'blue',
                    backgroundColor: 'rgba(0,255, 0, 0.1)',
                    fillOpacity: 0.3
                }]
            },
            options: {
                responsive: false,
                title:{
                  display: true,
                  text: "Humidity time series(Last 1 hr)"
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
      });
    };

    function pChartLoad(){
      var getData = $.get('/pdata');
      getData.done(function(presrecs){
        //console.log(presrecs);

        var presArr = presrecs.presrecs.map(element => element.pressure);
        console.log(presArr);
        //var pAvg = presArr.reduce(function(sum, a) { return sum + a },0)/(presArr.length||1);
        document.getElementById('pTable').rows[1].cells[0].innerHTML = arrayMin(presArr);
        document.getElementById('pTable').rows[1].cells[1].innerHTML = arrayMax(presArr);
        document.getElementById('pTable').rows[1].cells[2].innerHTML = arrayAvg(presArr);
        var tsArr = presrecs.presrecs.map(element => element.ts.$date);
        //console.log(tsArr);

        var cnvTsArr = tsArr.map(function(element){
        var temp = new Date(parseInt(element))
        element = temp.toISOString().substring(11,19)
        return element;
        });
        console.log(cnvTsArr);

        var ctx = document.getElementById('pChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: cnvTsArr,
                datasets: [{
                    label: 'Pressure',
                    data: presArr,
                    borderWidth: 2,
                    borderColor: 'green',
                    backgroundColor: 'rgba(255, 0, 0, 0.1)',
                    fillOpacity: 0.3
                }]
            },
            options: {
                responsive: false,
                title:{
                  display: true,
                  text: "Pressure time series(Last 1 hr)"
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
      });
    };
});
