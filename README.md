# desarrollo_web_marco_loyola
Muy buenas gente, acá encontrarán la tercera parte de mi página web. Me gustaría comentar algunos aspectos:
- Para el gráfico de actividades por día y por mes (dividido en mañana, mediodía y tarde) tomé la fecha de inicio como valor para decidir el día y mes en que se realizaba una actividad, esto quiere decir que si una actividad dura 3 días se va a tomar solamente el primer día para los gráficos.
- Corregí un error que había al crear una actividad con el tema "religión". Sucedía que al escoger ese tema y se guardaba la actividad ocurría un error, ya que en el archivo select.js el tema "religión" estaba escrito con una tilde en otra letra, generando una discrepancia con la base de datos.
- Corregí un error a la hora de enviar un formulario válido. Pasaba que si no completabas el campo del número de celular (osea quedaba vacío) y enviabas el formulario, la página se caía. Se debió corregir el validador del teléfono en el backend.
