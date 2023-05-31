$(document).ready(function() {/**
 * Theme: Metrica - Responsive Bootstrap 5 Admin Dashboard
 * Author: Mannatthemes
 * Reports Js
 */
//colunm-1
function getCookie(c_name){ 
  if (document.cookie.length > 0) {
      c_start = document.cookie.indexOf(c_name + "=");
      if (c_start != -1) {
          c_start = c_start + c_name.length + 1;
          c_end = document.cookie.indexOf(";", c_start);
          if (c_end == -1)
              c_end = document.cookie.length;

          return unescape(document.cookie.substring(c_start,c_end));
      }
  }
  return "";
}
$.ajaxSetup({
  headers: {"X-CSRFToken": getCookie("csrftoken")}
});

$.ajax({
  url: './admin-dashbord-analytique-ajax/',
  type: 'post',
  cache: false,
  contentType: false,
  processData: false
}).done(result => {

 var options = {
  chart: {
      height: 325,
      type: 'bar',
      toolbar: {
          show: false
      },
  },
  plotOptions: {
      bar: {
          horizontal: false,
          endingShape: 'rounded',
          columnWidth: '25%',
      },
  },
  dataLabels: {
      enabled: false,
  },
  stroke: {
      show: true,
      width: 7,
      colors: ['transparent']
  },
  colors: ["rgba(42, 118, 244, .18)", '#2a76f4'],
  series: [{
      name: 'totalDone',
      data: result.totalDone
  }, {
      name: 'totalMax',
      data: result.totalMax
  },],
  xaxis: {
      categories: ['Janv','Fevr', 'Mars', 'Avr', 'Mai', 'Juin', 'Juill', 'Aout', 'Sept', 'Oct','Nov','Dec'],
      axisBorder: {
        show: true,
      },  
      axisTicks: {
        show: true,
      },    
  },
  legend: {
    offsetY: 6,
  },
  yaxis: [
    {
      labels: {
        formatter: function(val) {
          return val.toFixed(0);
        }
      }
    }
  ],
  fill: {
      opacity: 1,
  },
  // legend: {
  //     floating: true
  // },
  grid: {
      row: {
          colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
          opacity: 0.2
      },
      borderColor: '#f1f3fa',
      strokeDashArray: 3.5,
  },
  tooltip: {
      y: {
          formatter: function (val) {
              return "" + val + ""
          }
      }
  }
}
  var chartMain = new ApexCharts(document.querySelector("#ana_dash_1"), options);
  chartMain.render();




//Device-widget

 
var options = {
  chart: {
      height: 255,
      type: 'donut',
  }, 
  plotOptions: {
    pie: {
      donut: {
        size: '85%'
      }
    }
  },
  dataLabels: {
    enabled: false,
  },

  stroke: {
    show: true,
    width: 2,
    colors: ['transparent']
  },
 
  series: [result.totalOneShot, result.totalReccuring],
  legend: {
    show: true,
    position: 'bottom',
    horizontalAlign: 'center',
    verticalAlign: 'middle',
    floating: false,
    fontSize: '13px',
    offsetX: 0,
    offsetY: 0,
  },
  labels: [ "totalOneShot","totalReccuring" ],
  colors: ["#2a76f4","rgba(42, 118, 244, .5)"], //"rgba(42, 118, 244, .18)"
 
  responsive: [{
      breakpoint: 600,
      options: {
        plotOptions: {
            donut: {
              customScale: 0.2
            }
          },        
          chart: {
              height: 240
          },
          legend: {
              show: false
          },
      }
  }],
  tooltip: {
    y: {
        formatter: function (val) {
            return   val + " %"
        }
    }
  }
  
}

var chart = new ApexCharts(
  document.querySelector("#ana_device"),
  options
);

chart.render();
})
})
