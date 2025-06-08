document.addEventListener('DOMContentLoaded', function () {
    async function obtenerDatosParaGrafico() {
        try {
            const response = await fetch('http://127.0.0.1:5000/get-estadisticas-data');

            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }

            const datos = await response.json();

            renderizarGraficoLineas(datos.categories, datos.data);

        } catch (error) {
            console.error('Falló la obtención de datos para el gráfico:', error);
            document.getElementById('chart-lineas').innerHTML = '<h3>No se pudieron cargar los datos. Intenta de nuevo más tarde.</h3>';
        }
    }

    function renderizarGraficoLineas(fechas, cantidades) {
        Highcharts.chart('chart-lineas', {
            chart: {
                type: 'line',
                borderRadius: 10
            },
            title: {
                text: 'Cantidad de Actividades por Día'
            },
            xAxis: {
                // Eje X: Usamos las fechas que vienen de la API.
                categories: fechas,
                title: {
                    text: 'Fechas'
                }
            },
            yAxis: {
                title: {
                    text: 'Cantidad de Actividades'
                },
                allowDecimals: false // No tiene sentido tener actividades decimales.
            },
            series: [{
                name: 'Actividades',
                // Datos del Eje Y: Usamos las cantidades que vienen de la API.
                data: cantidades
            }]
        });
    }

    async function obtenerDatosParaGraficoTorta() {
        try {
            const response = await fetch('http://127.0.0.1:5000/get-estadisticas-data-torta');
            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }
            const datos = await response.json();
            renderizarGraficoTorta(datos.data);

        } catch (error) {
            console.error('Falló la obtención de datos para el gráfico de torta:', error);
            document.getElementById('chart-torta').innerHTML = '<h3>No se pudieron cargar los datos.</h3>';
        }
    }

    function renderizarGraficoTorta(datos) {
        Highcharts.chart('chart-torta', {
            chart: {
                type: 'pie',
                borderRadius: 10
            },
            title: {
                text: 'Total de Actividades por Tipo'
            },
            tooltip: {
                // Muestra "Tema: X actividades (Y.Y%)"
                pointFormat: '{series.name}: <b>{point.y} ({point.percentage:.1f}%)</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            series: [{
                name: 'Actividades',
                colorByPoint: true,
                data: datos
            }]
        });
    }

    async function obtenerDatosParaGraficoTriple() {
        try {
            const response = await fetch('http://127.0.0.1:5000/get-estadisticas-data-3');

            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }

            const datos = await response.json();

            renderizarGraficoBarrasTriple(datos.series);

        } catch (error) {
            console.error('Falló la obtención de datos para el gráfico:', error);
            document.getElementById('chart-barras').innerHTML = '<h3>No se pudieron cargar los datos. Intenta de nuevo más tarde.</h3>';
        }
    }

    function renderizarGraficoBarrasTriple(datos) {
        Highcharts.chart('chart-barras', {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Actividades por Mes'
            },
            xAxis: {
                categories: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
                title: {
                    text: 'Meses'
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Cantidad de Actividades'
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            plotOptions: {
                series: {
                    groupPadding: 0.05, // Espacio entre grupos de barras
                    pointPadding: 0.1,   // Espacio entre barras individuales
                    borderWidth: 0
                }
            },
            series: datos
        });
    }

    obtenerDatosParaGrafico();
    obtenerDatosParaGraficoTorta();
    obtenerDatosParaGraficoTriple()
});


