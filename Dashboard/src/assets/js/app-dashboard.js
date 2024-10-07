    /**
     * Dashboard eCommerce
     */

    'use strict';

    (function () {
    let cardColor, labelColor, headingColor, borderColor, legendColor;

        cardColor = config.colors.cardColor;
        labelColor = config.colors.textMuted;
        legendColor = config.colors.bodyColor;
        headingColor = config.colors.headingColor;
        borderColor = config.colors.borderColor;


    // Donut Chart Colors
    const chartColors = {
        donut: {
        series1: '#22A95E',
        series2: '#24B364',
        series3: config.colors.success,
        series4: '#53D28C',
        series5: '#7EDDA9',
        series6: '#A9E9C5'
        }
    }

    const reportBarChartEl = document.querySelector('#reportBarChart'),
        reportBarChartConfig = {
        chart: {
            height: 230,
            type: 'bar',
            toolbar: {
            show: false
            }
        },
        plotOptions: {
            bar: {
            barHeight: '60%',
            columnWidth: '60%',
            startingShape: 'rounded',
            endingShape: 'rounded',
            borderRadius: 4,
            distributed: true
            }
        },
        grid: {
            show: false,
            padding: {
            top: -20,
            bottom: 0,
            left: -10,
            right: -10
            }
        },
        colors: [
            config.colors_label.primary,
            config.colors_label.warning,

        ],
        dataLabels: {
            enabled: false
        },
        series: [
            {
            data: [100, 80]
            }
        ],
        legend: {
            show: false
        },
        xaxis: {
            categories: ['متاح', 'قيد الأنتظار'],
            axisBorder: {
            show: false
            },
            axisTicks: {
            show: false
            },
            labels: {
            style: {
                colors: labelColor,
                fontSize: '13px'
            }
            }
        },
        yaxis: {
            labels: {
            show: false
            }
        },
        responsive: [
            {
            breakpoint: 1025,
            options: {
                chart: {
                height: 190
                }
            }
            },
            {
            breakpoint: 769,
            options: {
                chart: {
                height: 250
                }
            }
            }
        ]
        };
    if (typeof reportBarChartEl !== undefined && reportBarChartEl !== null) {
        const barChart = new ApexCharts(reportBarChartEl, reportBarChartConfig);
        barChart.render();
    }
    })();
