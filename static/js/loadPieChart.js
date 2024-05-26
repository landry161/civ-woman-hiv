$(document).ready(function(){
    //Pie Chart
    $.ajax({
        url:"/pie-chart",
        method:"GET",
        dataType:"JSON",
        success:function(result){
            console.log(result);
            loadPieChart(result);
        },
        error:function(error){
            console.log(error);
        }
    });

    //Line Chart
    $.ajax({
        url:'/line-query-chart',
        method:"GET",
        dataType:"JSON",
        success:function(data)
        {
            console.log(typeof data);
            console.log(data);
            console.log("Voici ici oh");
            loadLineChart(data);
            console.log("Fin");
        },error:function(err){
           console.log("Erreur ici ");
                console.log-(err);
        }
    });

    function loadLineChart(data){
        console.log(data);
        console.log("Fin déclaration");
        Highcharts.chart('containerLineChart', {
title: {
    text: 'Repartition par année et par pays',
    align: 'left'
},
subtitle: {
    text: 'Source: <a href="https://data.gouv.ci/datasets/couverture-des-femmes-enceintes-sous-traitement-anti-retroviraux" target="_blank">OPEN Data Côte d\Ivoire</a>.',
    align: 'left'
},
yAxis: {
    title: {
        text: 'Number of Employees'
    }
},

xAxis: {
    accessibility: {
        rangeDescription: 'Range: 2000 to 2020'
    }
},

legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle'
},

plotOptions: {
    series: {
        label: {
            connectorAllowed: false
        },
        pointStart: 2000
    }
},
series: data,
responsive: {
    rules: [{
        condition: {
            maxWidth: 500
        },
        chartOptions: {
            legend: {
                layout: 'horizontal',
                align: 'center',
                verticalAlign: 'bottom'
            }
        }
    }]
}
});
}
    

   function loadPieChart(pieChart)
    {
        (function (H) {
            H.seriesTypes.pie.prototype.animate = function (init) {
            const series = this,
                chart = series.chart,
                points = series.points,
                {
                    animation
                } = series.options,
                {
                    startAngleRad
                } = series;

            function fanAnimate(point, startAngleRad) {
                const graphic = point.graphic,
                    args = point.shapeArgs;

                if (graphic && args) {

                    graphic
                    // Set inital animation values
                    .attr({
                        start: startAngleRad,
                        end: startAngleRad,
                        opacity: 1
                    })
                    // Animate to the final position
                    .animate({
                        start: args.start,
                        end: args.end
                    }, {
                        duration: animation.duration / points.length
                    }, function () {
                        // On complete, start animating the next point
                        if (points[point.index + 1]) {
                            fanAnimate(points[point.index + 1], args.end);
                        }
                        // On the last point, fade in the data labels, then
                        // apply the inner size
                        if (point.index === series.points.length - 1) {
                            series.dataLabelsGroup.animate({
                                opacity: 1
                            },
                            void 0,
                            function (){
                                points.forEach(point => {
                                    point.opacity = 1;
                                });
                                series.update({
                                    enableMouseTracking: true
                                },false);
                                chart.update({
                                    plotOptions: {
                                        pie: {
                                            innerSize: '40%',
                                            borderRadius: 8
                                        }
                                    }
                                });
                            });
                        }
                    });
            }
        }

        if (init) {
            // Hide points on init
            points.forEach(point => {
                point.opacity = 0;
            });
        } else {
            fanAnimate(points[0], startAngleRad);
        }
    };
}(Highcharts));

Highcharts.chart('containerPieChart', {
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Proportion des femmes ayant bénéficié des ARV',
        align: 'left'
    },
    subtitle: {
        text: 'De 2000 à 2020',
        align: 'left'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.2f}%</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            borderWidth: 2,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>Année {point.name}</b><br>{point.y} Femmes',
                distance: 20
            }
        }
    },
    series: [{
        // Disable mouse tracking on load, enable after custom animation
        enableMouseTracking: false,
        animation: {
            duration: 2000
        },
        colorByPoint: true,
        name:"Pourcentage",
        data:pieChart
        }]
    });
}
});