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
  url: './admin-dashbord-ticket-ajax/',
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
      width: 2,
      colors: ['transparent']
  },
  colors: ["rgba(42, 118, 244, .18)", '#2a76f4'],
  series: [{
      name: 'New Tickets',
      data: result.newByMonth
  }, {
      name: 'Solved Tickets',
      data: result.closeByMonth
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
  yaxis: {
      title: {
          text: 'Tickets'
      }
  },
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

var chart = new ApexCharts(
  document.querySelector("#reports_tickets"),
  options
);

chart.render(); 


// saprkline chart


var dash_spark_1 = {
    
  chart: {
      type: 'area',
      height: 60,
      sparkline: {
          enabled: true
      },
  },
  stroke: {
      curve: 'smooth',
      width: 2,
    },
  fill: {
      opacity: 1,
      gradient: {
        shade: '#2c77f4',
        type: "horizontal",
        shadeIntensity: 0.5,
        inverseColors: true,
        opacityFrom: 0.1,
        opacityTo: 0.1,
        stops: [0, 80, 100],
        colorStops: []
    },
  },
  series: [{
    data: [4, 8, 5, 10, 4, 16, 5, 11, 6, 11, 30, 10, 13, 4, 6, 3, 6]
  }],
  yaxis: {
      min: 0
  },
  colors: ['#506ee4'],
}
new ApexCharts(document.querySelector("#dash_spark_1"), dash_spark_1).render();


var dash_spark_2 = {
    
  chart: {
      type: 'area',
      height: 60,
      sparkline: {
          enabled: true
      },
  },
  stroke: {
      curve: 'smooth',
      width: 2,
    },
  fill: {
      opacity: 1,
      gradient: {
        shade: '#fd3c97',
        type: "horizontal",
        shadeIntensity: 0.5,
        inverseColors: true,
        opacityFrom: 0.1,
        opacityTo: 0.1,
        stops: [0, 80, 100],
        colorStops: []
    },
  },
  series: [{
    data: [4, 8, 5, 10, 4, 25, 5, 11, 6, 11, 5, 10, 3, 14, 6, 8, 6]
  }],
  yaxis: {
      min: 0
  },
  colors: ['#fd3c97'],
}
new ApexCharts(document.querySelector("#dash_spark_2"), dash_spark_2).render();




// apex-bar-1

var options = {
  chart: {
      height: 275,
      type: 'bar',
      toolbar: {
          show: false
      },
      dropShadow: {
          enabled: true,
          top: 5,
          left: 5,
          bottom: 0,
          right: 0,
          blur: 5,
          color: '#45404a2e',
          opacity: 0.35
      },
  },
  plotOptions: {
    bar: {
      barHeight: '50%',
      distributed: false,
      horizontal: true,
      endingShape: 'rounded',
    }
  },
  dataLabels: {
    enabled: false,    
  },
  series: [{
      data: result.category,
  }],
colors: ['#506ee4'],
  yaxis: {
      axisBorder: {
          show: true,
          color: '#bec7e0',
        },  
        axisTicks: {
          show: true,
          color: '#bec7e0',
      }, 
  },
  xaxis: {
      categories: ['Information', 'technique', 'administration '],        
  },
  stroke: {
    show: true,
    width: 1,
    colors: ['#fff']
  },
  states: {
      hover: {
          filter: 'none'
      }
  },
  grid: {
      borderColor: '#f1f3fa',
      strokeDashArray: 4,
  }
}

var chart = new ApexCharts(
  document.querySelector("#requestType"),
  options
);


chart.render();

var options = {
  chart: {
      height: 240,
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
  series: [65, 20, 10, 5],
  legend: {
      show: false,
      position: 'bottom',
      horizontalAlign: 'center',
      verticalAlign: 'middle',
      floating: false,
      fontSize: '14px',
      offsetX: 0,
      offsetY: -13
  },
  labels: [ "Excellent", "Very Good", "Good", "Fair"],
  colors: ["#2a76f4", "#fdb5c8", "#67c8ff", "#c693ff"],
 
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

var options = {
  chart: {
      height: 305,
      type: 'pie',
      dropShadow: {
        enabled: true,
        top: 4,
        left: 0,
        bottom: 0,
        right: 0,
        blur: 2,
        color: '#45404a2e',
        opacity: 0.35
      },
  }, 
  stroke: {
    show: true,
    width: 2,
    colors: ['transparent']
  },
  series: result.etatNumber,
  labels: ["Clos", "En Cours", "Résolu"],
  colors: ["#0abb87", "#7367f0", "#ff9f43", "#fd3c97", "#41cbd8"],
  legend: {
      show: true,
      position: 'bottom',
      horizontalAlign: 'center',
      verticalAlign: 'middle',
      floating: false,
      fontSize: '14px',
      offsetX: 0,
      offsetY: 5
  },
  responsive: [{
      breakpoint: 600,
      options: {
          chart: {
              height: 240
          },
          legend: {
              show: false
          },
      }
  }]
}

var chartData = new ApexCharts(
  document.querySelector("#Tickets_Data"),
  options
);

chart.render();
chartData.render();

/* window.addEventListener('DOMContentLoaded', (event) => {
  chart.render();
  chartData.render();
}); */
})
})