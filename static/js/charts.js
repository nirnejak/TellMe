$(document).ready(function() {
    // Javascript method's body can be found in assets/js/tellme.js
    new Chart(document.getElementById("chartjs-1"),{
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
                    display: false,
                    position : "bottom"
                 },
                 tooltips: {
                    enabled: true
                 }
            }
        }
    );
    new Chart(document.getElementById("chartjs-2"),{
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
                    ]
                }]
            },
            options: {
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
});