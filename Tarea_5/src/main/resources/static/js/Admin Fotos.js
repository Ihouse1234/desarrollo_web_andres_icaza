document.addEventListener('DOMContentLoaded', function () {
  const botones = document.querySelectorAll('.btn-eliminar');

  botones.forEach(function (btn) {
    btn.addEventListener('click', function () {
      const fotoId = btn.getAttribute('data-id');
      eliminarFoto(fotoId, btn);
    });
  });
});

// Pide el motivo, lo valida y envía la eliminación al servidor.
function eliminarFoto(fotoId, btn) {
  // Solicitar el motivo al usuario
  const motivo = prompt('Indique el motivo de eliminación (5 a 200 caracteres):');

  // El usuario canceló el prompt
  if (motivo === null) {
    return;
  }

  const motivoLimpio = motivo.trim();

  // Validación en el cliente.
  if (motivoLimpio.length === 0) {
    alert('El motivo es obligatorio.');
    return;
  }
  if (motivoLimpio.length < 5 || motivoLimpio.length > 200) {
    alert('El motivo debe tener entre 5 y 200 caracteres.');
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Eliminando...';

  fetch('/api/fotos/' + fotoId + '/eliminar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ motivo: motivoLimpio })
  })
    .then(function (r) { return r.json(); })
    .then(function (resp) {
      if (resp.ok) {
        // Actualizar la interfaz sin recargar la página
        marcarComoEliminada(fotoId);
      } else {
        alert(resp.error || 'No se pudo eliminar la foto.');
        btn.disabled = false;
        btn.textContent = 'Marcar como eliminada';
      }
    })
    .catch(function () {
      alert('Error al comunicarse con el servidor.');
      btn.disabled = false;
      btn.textContent = 'Marcar como eliminada';
    });
}

function marcarComoEliminada(fotoId) {
  const card = document.getElementById('foto-' + fotoId);
  if (!card) return;

  card.classList.add('foto-eliminada');

  const acciones = card.querySelector('.foto-acciones');
  acciones.innerHTML = '';

  const badge = document.createElement('span');
  badge.className = 'badge-eliminada';
  badge.textContent = 'Eliminada';
  acciones.appendChild(badge);
}