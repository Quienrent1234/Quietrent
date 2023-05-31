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
  url: './admin-dashbord-commercial-ajax/',
  type: 'post',
  cache: false,
  contentType: false,
  processData: false
}).done(result => {
    
var options = {
    chart: {
      height: 375,
      type: 'line',
     
      toolbar: {
        show: false
      }
    },
    stroke: {
      width: 3,
      curve: 'smooth'
    },
    series: [{
      name: 'Likes',
      data: result.totalCustomersByMonth
    }],
    xaxis: {
      categories: ['Janv','Fevr', 'Mars', 'Avr', 'Mai', 'Juin', 'Juill', 'Aout', 'Sept', 'Oct','Nov','Dec'],
      axisBorder: {
        show: true,
        color: '#bec7e0',
      },      
    },
    colors:['#5766da'],
    markers: {
      size: 3,
      opacity: 0.9,
      colors: ["#fdb5c8"],
      strokeColors: '#fff',
      strokeWidth: 1,
      style: 'inverted', // full, hollow, inverted
      hover: {
        size: 5,
      }
    },
    yaxis: {
      title: {
        text: 'Engagement',
      },
    },
    grid: {
      row: {
        colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
        opacity: 0.2
      },
      strokeDashArray: 3.5,
    },
    responsive: [{
      breakpoint: 600,
      options: {
        chart: {
          toolbar: {
            show: false
          }
        },
        legend: {
          show: false
        },
      }
    }]
  }
  
  var chart = new ApexCharts(
    document.querySelector("#apex_line1"),
    options
  );
  chart.render();  

  var options = {
    chart: {
        height: 320,
        type: 'area',
        width: '100%',
        stacked: true,
        toolbar: {
          show: false,
          autoSelected: 'zoom'
        },
    },
    colors: ['#2a77f4','#a5c2f1'],
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: [1.5, 1.5],
        dashArray: [0, 4],
        lineCap: 'round',
    },
    grid: {
      padding: {
        left: 0,
        right: 0
      },
      strokeDashArray: 3,
    },
    markers: {
      size: 0,
      hover: {
        size: 0
      }
    },
    series: [{
        name: 'Demande cloturé',
        data: result.clotureDemande
    },
    {
      name: 'Demande en cours',
      data: result.encoursDemande
  }],
  
    xaxis: {
        type: 'month',
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        axisBorder: {
          show: true,
        },  
        axisTicks: {
          show: true,
        },                  
    },
    fill: {
      type: "gradient",
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.4,
        opacityTo: 0.3,
        stops: [0, 90, 100]
      }
    },
    
    tooltip: {
        x: {
            format: 'dd/MM/yy HH:mm'
        },
    },
    legend: {
      position: 'top',
      horizontalAlign: 'right'
    },
  }
  
  var chart = new ApexCharts(
    document.querySelector("#crm-dash"),
    options
  );
  
  chart.render();

var options5 = {
    series: [{
      name: 'New Visitors',
      data: result.uniqueCustomerReconnexionByMonth
    },],
  
    chart: {
    type: 'bar',
    width: 200,
    height: 35,
    sparkline: {
      enabled: true
    }
  },
  colors: ["#4d79f6", "#e0e7fd"],
  plotOptions: {
    bar: {
      columnWidth: '50%'
    }
  },
  labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
  xaxis: {
    crosshairs: {
      width: 2
    },
  },
  tooltip: {
    fixed: {
      enabled: false
    },
    x: {
      show: false
    },
    y: {
      title: {
        formatter: function (seriesName) {
          return ''
        }
      }
    },
    marker: {
      show: false
    }
  }
  };
  
  var chart5 = new ApexCharts(document.querySelector("#bar-1"), options5);
  chart5.render();


  var options7 = {
    series: [
      result.bounceRate
    ],
    chart: {
    type: 'radialBar',
    width: 50,
    height: 50,
    sparkline: {
      enabled: true
    }
  },
  dataLabels: {
    enabled: false
  },
  plotOptions: {
    radialBar: {
      hollow: {
        margin: 0,
        size: '50%'
      },
      track: {
        margin: 0
      },
      dataLabels: {
        show: false
      }
    }
  }
  };
  
  var chart7 = new ApexCharts(document.querySelector("#radialBar-1"), options7);
  chart7.render();
  
  var options1 = {
    series: [{
    data: result.newCustomersByMonth
  }],
    chart: {
    type: 'line',
    width: 200,
    height: 35,
    sparkline: {
      enabled: true
    }
  },
  stroke: {
    show: true,
    curve: 'smooth',
    width: [2],
    lineCap: 'round',
  },
  tooltip: {
    fixed: {
      enabled: false
    },
    x: {
      show: false
    },
    y: {
      title: {
        formatter: function (seriesName) {
          return ''
        }
      }
    },
    marker: {
      show: false
    }
  }
  };
  
  var chart1 = new ApexCharts(document.querySelector("#line-1"), options1);
chart1.render();

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
  series: result.etat,
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
  labels: [ "En cours", "Rejeté", "Validé", "Cloturé"],
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
    document.querySelector("#email_report"),
    options
  );
  
  chart.render();
  
})

})