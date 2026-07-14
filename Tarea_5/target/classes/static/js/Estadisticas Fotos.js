// Pide los conteos al servidor y dibuja el gráfico con Highcharts
fetch('/api/estadistica-fotos')
  .then(function (r) { return r.json(); })
  .then(function (data) {
    Highcharts.chart('chart-fotos', {
      chart: {
        type: 'pie',
        backgroundColor: 'transparent',
        style: { fontFamily: 'system-ui, sans-serif' }
      },
      title: { text: '' },
      credits: { enabled: false },
      plotOptions: {
        pie: {
          dataLabels: {
            enabled: true,
            format: '<b>{point.name}</b>: {point.y}',
            style: { color: '#e8eaf0' }
          }
        }
      },
      tooltip: {
        backgroundColor: '#1e2029',
        borderColor: '#2a2d3a',
        style: { color: '#e8eaf0' },
        pointFormat: '<b>{point.y}</b> foto(s)'
      },
      series: [{
        name: 'Fotos',
        data: [
          { name: 'Vigentes',   y: data.vigentes,   color: '#c8f060' },
          { name: 'Eliminadas', y: data.eliminadas, color: '#f06060' }
        ]
      }]
    });
  })
  .catch(function () {
    document.getElementById('chart-fotos').textContent =
      'Error al cargar los datos.';
  });