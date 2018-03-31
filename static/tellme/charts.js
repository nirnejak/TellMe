$(document).ready(function() {
    // Javascript method's body can be found in assets/js/tellme.js
    new Chart(document.getElementById("dashboardChart-1"),{
            "type":"doughnut",
            "data":{
                "labels":["Canal","Pump","River","Other"],
                "datasets":[{
                    "label":"",
                    "data":[300,100,50,50],
                    "backgroundColor":[
                        "rgb(255, 99, 132)",
                        "rgb(54, 162, 235)",
                        "rgb(255, 205, 86)",
                        "rgb(10, 199, 0)"
                    ]
                }]
            },
            options: {
                 legend: {
                    display: true,
                    position : "bottom"
                 },
                 tooltips: {
                    enabled: true
                 }
            }
        }
    );
    new Chart(document.getElementById("dashboardChart-2"),{
            "type":"pie",
            "data":{
                "labels":["Canal","Pump","River","Other"],
                "datasets":[{
                    "label":"",
                    "data":[300,100,50,50],
                    "backgroundColor":[
                        "rgb(255, 99, 132)",
                        "rgb(54, 162, 235)",
                        "rgb(255, 205, 86)",
                        "rgb(10, 199, 0)"

                    ],
                }]
            },
            options: {
                 legend: {
                    display: true,
                    position : "bottom"
                 },
                 tooltips: {
                    enabled: true
                 }
            }
        }
    );
    new Chart(document.getElementById("dashboardChart-3"),{
            type: 'bar',
            data: {
                labels: ["Rice", "Wheat", "Sugarcane", "Sunflower", "Corn", "Others"],
                datasets: [{
                    label: '# of Votes',
                    data: [12, 19, 3, 7, 4, 9],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                }
            }
        }
    );
    new Chart(document.getElementById("dashboardChart-4"),{
            "type":"line",
            "data":{
                "labels": ["January", "February", "March", "April", "May", "June", "July"],
                datasets: [
                    {
                        label: "My First dataset",
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255,99,132,1)',
                        data: [0, 10, 5, 2, 20, 30, 45],
                    },
                    {
                        label: "My First dataset",
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        data: [0, 12, 14, 13, 9, 21, 15],
                    }
                ]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                },
                legend: {
                    display: false,
                    position : "bottom"
                 },
                 tooltips: {
                    enabled: true
                 }
            }
        }
    );

// Scatter Plot
    window.chartColors = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
    };


    var color = Chart.helpers.color;
    var scatterChartData = {
        datasets: [{
            borderColor: window.chartColors.red,
            backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
            label: 'V(node2)',
            data: [{
                x: 1,
                y: 1.711e-2,
            }, {
                x: 1.26,
                y: 2.708e-2,
            }, {
                x: 1.58,
                y: 4.285e-2,
            }, {
                x: 2.0,
                y: 6.772e-2,
            }, {
                x: 2.51,
                y: 1.068e-1,
            }, {
                x: 3.16,
                y: 1.681e-1,
            }, {
                x: 3.98,
                y: 2.635e-1,
            }, {
                x: 5.01,
                y: 4.106e-1,
            }, {
                x: 6.31,
                y: 6.339e-1,
            }, {
                x: 7.94,
                y: 9.659e-1,
            }, {
                x: 10.00,
                y: 1.445,
            }, {
                x: 12.6,
                y: 2.110,
            }, {
                x: 15.8,
                y: 2.992,
            }, {
                x: 20.0,
                y: 4.102,
            }, {
                x: 25.1,
                y: 5.429,
            }, {
                x: 31.6,
                y: 6.944,
            }, {
                x: 39.8,
                y: 8.607,
            }, {
                x: 50.1,
                y: 1.038e1,
            }, {
                x: 63.1,
                y: 1.223e1,
            }, {
                x: 79.4,
                y: 1.413e1,
            }, {
                x: 100.00,
                y: 1.607e1,
            }, {
                x: 126,
                y: 1.803e1,
            }, {
                x: 158,
                y: 2e1,
            }, {
                x: 200,
                y: 2.199e1,
            }, {
                x: 251,
                y: 2.398e1,
            }, {
                x: 316,
                y: 2.597e1,
            }, {
                x: 398,
                y: 2.797e1,
            }, {
                x: 501,
                y: 2.996e1,
            }, {
                x: 631,
                y: 3.196e1,
            }, {
                x: 794,
                y: 3.396e1,
            }, {
                x: 1000,
                y: 3.596e1,
            }]
        }]
    };

    var ctx = document.getElementById('dashboardChart-5').getContext('2d');
    window.myScatter = Chart.Scatter(ctx, {
        data: scatterChartData,
        options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                },
                legend: {
                    display: false,
                    position : "bottom"
                 },
                 tooltips: {
                    enabled: true
                 }
            }
    });
});