$(document).ready(function(){
    $.ajax({
        url:'/line-query-chart',
        method:"GET",
        dataType:"JSON",
        success:function(data)
        {
            loadLineChart(data);
        },error:function(err){
           console.log("Erreur ");
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
});