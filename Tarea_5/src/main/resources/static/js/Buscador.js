const input      = document.getElementById('input-busqueda');
const resultados = document.getElementById('resultados');

// Guarda el último término buscado.
let patronActual = '';

// Se dispara cada vez que cambia el texto del input
input.addEventListener('input', function () {
  const q = input.value.trim();
  patronActual = q;

  // El enunciado pide buscar solo a partir de 3 caracteres
  if (q.length < 3) {
    resultados.innerHTML = '<p class="hint">Escribe al menos 3 caracteres...</p>';
    return;
  }

  buscar(q);
});

function buscar(q) {
  // encodeURIComponent escapa caracteres especiales en la URL
  fetch(`/api/buscar?q=${encodeURIComponent(q)}`)
    .then(r => r.json())
    .then(data => mostrarResultados(data))
    .catch(() => {
      resultados.innerHTML = '<p class="error">Error al buscar.</p>';
    });
}

function mostrarResultados(actividades) {
  resultados.innerHTML = '';

  // Mensaje si no hay resultados.
  if (actividades.length === 0) {
    resultados.innerHTML = '<p class="vacio">No se encontraron actividades.</p>';
    return;
  }

  // Crear una tarjeta por cada actividad.
  actividades.forEach(act => {
    const card = document.createElement('div');
    card.className = 'card-actividad';

    card.innerHTML = `
      <div class="card-top">
        <h3>${resaltar(act.nombre)}</h3>
        <span class="tipo">${escapeHtml(act.tipo)}</span>
      </div>
      <div class="card-meta">
        <span>👤 ${escapeHtml(act.nombreMiembro)}</span>
        <span>📅 ${escapeHtml(act.dia)}</span>
        <span>📍 ${resaltar(act.comuna)}</span>
      </div>
      <p class="card-desc">${resaltar(act.descripcion || '')}</p>
      <div class="card-bottom">
        <span class="nota">Nota: <strong id="nota-${act.id}">${escapeHtml(act.nota)}</strong></span>
        <button class="btn-evaluar" onclick="evaluar(${act.id})">Evaluar</button>
      </div>
    `;
    resultados.appendChild(card);
  });
}

function evaluar(actividadId) {
  // Pide la nota al usuario.
  const entrada = prompt('Ingresa una nota entre 1 y 7:');
  if (entrada === null) return;   // canceló

  const nota = parseInt(entrada, 10);

  // Validación lado cliente.
  if (isNaN(nota) || nota < 1 || nota > 7 || !Number.isInteger(Number(entrada))) {
    alert('La nota debe ser un número entero entre 1 y 7.');
    return;
  }

  fetch(`/api/actividades/${actividadId}/notas`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nota: nota })
  })
    .then(r => r.json())
    .then(resp => {
      if (resp.ok) {
        // Actualizar el promedio en pantalla sin recargar la página.
        document.getElementById(`nota-${actividadId}`).textContent = resp.promedio;
      } else {
        alert(resp.error || 'No se pudo agregar la nota.');
      }
    })
    .catch(() => alert('Error al enviar la nota.'));
}

// Escapa caracteres peligrosos para evitar XSS al insertar texto.
function escapeHtml(str) {
  const d = document.createElement('div');
  d.appendChild(document.createTextNode(str));
  return d.innerHTML;
}

// Resalta el patrón buscado dentro del texto, envolviéndolo en <mark>.
function resaltar(texto) {
  const seguro = escapeHtml(texto);
  if (!patronActual) return seguro;

  // Escapa el patrón para usarlo en una expresión regular.
  const patronEscapado = patronActual.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`(${patronEscapado})`, 'gi');  // g=global, i=insensible a mayúsculas
  return seguro.replace(regex, '<mark>$1</mark>');
}