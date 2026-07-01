# desarrollo_web_andres_icaza

Tarea 1
En terminos de diseño de la pagina solo use la base del ejercicio que nos mandaron las semanas anteriores.

Para empezar lo primero que nos permite identificar a una persona es el Rut, despues nombre y apellido asique por eso parto preguntando esos 3 primeros datos en el formulario.

Para la fecha use input type="date", esto hace mas facil elegir el dia en que se realizo la actividad, para las horas de inicio a fin lo logre con input type="time".

Para la subida de la foto o video use input type="file" accept="image/*,video/*", vi que podia elegir que aceptaba este input lo que me facilito la tarea.

Para el listado de miembros, hice que se pudiera filtrar por tipo de actividad y que se pudiera ordenar por nombre o apellido.

Para el grafico utilizo canvas id="grafico-miembros", busque como poner un grafico y esto aparecio de primero en mi busqueda.


Ahora en las validaciones, utilizando de base el ejercicio de las semanas anteriores, tomo los valores de todos los datos, utilizando trim() para los datos que son strings para evitar errores con espacios innecesarios.

Ademas me creé las funciones auxiliares mostrarError y ocultarError, que basicamente agregan la clase visible a la constante del error, para asi no tener 10 lineas con getdocument..., logrando un codigo mas ordenado.

Para el rut nesecitaba una base que acepta todos los ruts de manera xxxxxxxx-x, aceptando la k como ultimo digito, buscando por internet me encontre que si lo escribia asi /^[0-9]+-[0-9kK]$/, cubria todos los casos correctos, asique en la validacion si no hay rut o es diferente de nuestra base, tiramos error.

Para el nombre y apellido si son de menos de 3 letras los rechazo.

Para los tipos de estudiante/actividad si no responde tiro error.

Para las horas de inicio y fin, solo reviso si se respondia y ademas si la hora de fin es mayor a la de inicio, asumo que no va a empezar una actividad que dure mas de un dia y que si la hora de inicio es de x dia, la hora de fin estara en el mismo x dia.

Para el archivo que se sube, revisamos si es imagen o video con type.startswith.

Si se cumple todo, tiramos una alerta y reseteamos todos los valores de la pagina.


Tarea 2


El diseño lo busque en internet y me aparecio ese, no tengo realmente mucha explicacion que hace cada cosa ahi.

Resumen de cada HTML
base.html — Esqueleto base
Es la plantilla madre de la que heredan todos los demás con {% extends 'base.html' %}. Define la barra de navegación con los tres links (Registrar, Listado, Estadísticas), el sistema de flash messages, y los bloques vacíos {% block css %}, {% block content %} y {% block javascript %} que cada página rellena con su propio contenido.

registro.html — Formulario de registro
Tiene dos secciones: datos personales (nombre, email, teléfono, región, comuna) y actividades. El selector de comunas se filtra con JavaScript según la región elegida. Las actividades se agregan y eliminan dinámicamente con botones. Cada actividad tiene su propio campo de fotos con preview. Al hacer submit, el JS valida todo primero y si pasa, Flask valida nuevamente en el servidor. Si hay errores de servidor, muestra los mensajes de error.

miembros.html — Listado paginado
Muestra todos los miembros en una tabla con columnas de nombre, email, teléfono, comuna, región, cantidad de actividades y fecha de registro. Cada fila es clickeable y lleva al detalle del miembro. Abajo tiene paginación con botones de anterior/siguiente y números de página.

miembro_detalle.html — Perfil del miembro
Muestra el perfil completo de un miembro: un avatar con la inicial del nombre, sus datos de contacto y ubicación. Debajo hay una grilla de tarjetas, una por cada actividad, con su tipo (con color según categoría), día, hora, duración y descripción. Si la actividad tiene fotos se muestran en miniatura y al hacer click se abren.


Tarea 3

estadisticas.html - Estadisticas sobre los miembros y actividades
Página que muestra 3 gráficos generados en el lado del cliente con la librería Highcharts. Al cargar la página, se hacen llamadas asíncronas con fetch a tres endpoints del servidor (/api/miembros-por-dia, /api/actividades-por-tipo y /api/actividades-por-comuna), que devuelven los datos en formato JSON desde la base de datos. Con esos datos se construyen miembros registrados por día, total de actividades por tipo y el total de actividades por comuna. Cada gráfico muestra un mensaje de carga mientras llegan los datos y un mensaje de error si la petición falla. Al final incluye un enlace para volver a la portada.


Tarea 4

Arquitectura
El proyecto sigue la arquitectura en capas estándar de Spring Boot:
- Entity: clases JPA que mapean las tablas existentes (Actividad, Miembro, Comuna, Region, Nota).
- Repository: interfaces que extienden JpaRepository para el acceso a datos. Las queries complejas (buscador y cálculo de promedio) se definen con @Query en JPQL.
- Service: lógica de negocio, incluyendo la validación de notas (enteros 1-7) y el recálculo de promedios.
- Controller: endpoints REST que devuelven JSON (@RestController) y la vista del buscador (@Controller).
- DTO: objetos planos para enviar al frontend solo los datos necesarios, evitando las referencias circulares de las entidades al serializar a JSON.

Buscador
Se implementó con llamadas asíncronas (fetch) que se disparan automáticamente al escribir 3 o más caracteres. La búsqueda se realiza en el servidor con una query JPQL que recorre el nombre, la descripción y el nombre de la comuna mediante LIKE, de forma insensible a mayúsculas. Las coincidencias se resaltan en el cliente envolviendo el patrón en etiquetas <mark>.

Sistema de notas
Las notas se almacenan en la tabla nota (una fila por evaluación). Al evaluar, el cliente envía la nota de forma asíncrona; el servidor valida que sea un entero entre 1 y 7, la guarda, y recalcula el promedio con AVG(). El nuevo promedio se devuelve y actualiza en la interfaz sin recargar la página. Las actividades sin evaluaciones muestran "-".

Base de datos
Se reutiliza la base de datos tarea2, agregando únicamente la tabla nota mediante tabla-nota.sql. La configuración usa ddl-auto=none para que Hibernate no modifique las tablas existentes.

