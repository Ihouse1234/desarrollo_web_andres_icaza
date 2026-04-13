# desarrollo_web_andres_icaza

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
