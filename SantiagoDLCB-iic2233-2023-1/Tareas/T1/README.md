# Tarea 1: DCCavaCava 🏖⛏


## Consideraciones generales :octocat:

El codigo cumple con todo lo pedido en el enunciado, ademas cumple con el bonus.
Recordar que en general para salir del programa en los menus se escribe un `X` mayuscula y para volver atras una `Z` mayuscula. En ciertos casos el programa puede pedir un enter o input cualquiera para volver al menú en caso de estar en una opcion en particular o de poner un input no valido en un menú, esto ultimo se implemento para mantener la consola más limpia y facil de leer (Supuesto 7).



### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Programación Orientada a Objetos: 42 pts (35%)
##### ✅ Diagrama
###### Se ubica en archivo Diagrama_de_clases.pdf, contiene todas las clases modeladas, properties, relaciones de composicion, agregacion y herencia. 
##### ✅ Definición de clases, atributos, métodos y properties
###### El Torneo, las Arenas, los Excavadores y los Items estan bien modeladas con sus metodos y atributos siguiendo el enunciado, se hace uso de clases abstractas y  properties cuando corresponde.
##### ✅ Relaciones entre clases
###### Se hace uso de relacion de composicion, agregacion y herencia cuando corresponde. Revisar el diagrama para más detalle.
#### Preparación programa: 11 pts (9%)
##### ✅ Creación de partidas
###### Se pueden crear multiples partidas de DCCavaCava, instanciandose correctamente los excavadores, las arenas y los items con los valores de los archivos entregados, a excepcion de que los valores de los archivos no cumplan con los limites puestos en el enunciado, en dichos casos se corrigirian los valores (Supuesto 10).
#### Entidades: 22 pts (18%)
##### ✅ Excavador
###### Estos cavan, descansan, encuentran items, pierden energia y utilizan consumibles, respetando las formulas, probabilidades y limites de atributos puestos en el enunciado.
##### ✅ Arena
###### Tienen una dificultad que se calcula segun una formula que varia segun el tipo de arena, la ArenaMagnetica cambia su humedad y dureza a un valor aleatorio al inicio de simular un dia.
##### ✅ Torneo
###### Al simular un dia ocurren los eventos correspondientes segun las probabilidades establecidas.
#### Flujo del programa: 31 pts (26%)
##### ✅ Menú de Inicio
###### El menu permite iniciar una nueva partida, ir al menu de carga para abrir una partida guarda y salir de programa.
##### ✅ Menú Principal
###### El menu muestra y realiza todas las acciones pedidas
##### ✅ Simulación día Torneo
###### Muestra los metros cavados por cada excavador y en total en ese dia. Muestra los items encontrados por cada excavador junto al tipo de item. Ejecuta los eventos en caso de ocurrir y los muestra. En caso de cambiar de Arena muestra el cambio y el efecto en jugadores. Finalmente muestra los excavadores que actualmente estan descansando. 
##### ✅ Mostrar estado torneo
###### Se muestran todos lo minimo pedido en el enunciado.  
##### ✅ Menú Ítems
###### Muestra todos los items en la mochila, permite seleccionar uno, utilizarlo y posteriormente permite volver al menu en donde se habra eliminado ese item, aunque en caso de estar repetido solamente se habra eliminado esa unidad.
##### ✅ Guardar partida
###### Permite guardar el Torneo actual con un nombre ingresado por el usuario y se informa si se guardo exitosamente, no se guardan atributos como self.meta ya que esos deben proceder de parametros.py (Supuesto 8).
##### ✅ Robustez
###### Todos los menus permiten volver a su menu anterior y salir del programa. En ciertos casos en que se abran opciones como 'Mostrar Estado' se pedira un input cualquiera para volver al menu actual. Los menus son aprueba de todo input
#### Manejo de archivos: 14 pts (12%)
##### ✅ Archivos CSV 
###### La informacion de los archivos .csv se le con utf-8 correctamente y se ocupa para instanciar las clases de manera correcta
##### ✅ Archivos TXT
###### Se leen y escriben los archivos .txt para cargar y guardar partida de manera consistente, se ocupan como separadores de informacion los saltos de lineas, las comas y las dobles comas, de manera que no separen datos ingresados de manera inesperada. 
##### ✅ parametros.py
###### Contiene todos los parametros y constantes que dice el enunciado.
#### Bonus: 3 décimas máximo
##### ✅ Guardar Partida
###### Se guardan las partidas con los nombres ingresados por el usuario.
-------
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. En caso de no estar creada crear carpeta ```Partidas``` en el directorio principal de la tarea
2. Deben crearse los archivos csv especificiados en el enunciado: ```arenas.csv```, ```excavadores.csv```, ```consumibles.csv```, ```tesoros.csv```. Respetando el formato entregado de ejemplo





-------
## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```system()```, ```listdir()```,  ```path```
2. ```random```: ```random()```, ```randint()```, ```choice()```,```choices()```, ```sample()```
3. ```abc```: ```ABC```, ```abstractmethod```
   

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```parametros``` cumple con tener los parametros pedidos en el enunciado
2. ```clase_torneo```: Contiene a  la clase ```Torneo``` en la linea 10.
3. ```clase_arena```: Contiene a las clases ```Arena```, ```ArenaNormal```, ```ArenaMojada```, ```ArenaRocosa```, ```ArenaMagnetica``` en las lineas 7, 91, 104, 115, 127 respectivamente y a los metodos relacionados a la obtencion y creacion de instancias de estas clases.
4. ```clase_excavador```: Contiene a ```Excavador```, ```ExcavadorDocencio```, ```ExcavadorTareo```, ```ExcavadorHibrido``` en las lineas 12, 135, 152, 166 respectivamente y a los metodos relacionados a la obtencion y creacion de instancias de estas clases.
5. ```clase_item```: Contiene a ```Item```, ```Consumible```, ```Tesoro``` en las lineas 4, 11, 20 respectivamente y a los metodos relacionados a la obtencion y creacion de instancias de estas clases. 
6. ```funciones```: Hecha para definir funciones utilizadas en el flujo principal de los menús en el main.

-------
## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. ```CANTIDAD_EXCAVADORES_INICIALES``` de ```parametros.py``` es menor o igual a la cantidad de excavadores presentes en ```excavadores.csv``` y que a su vez es en este archivo existe al menos un excavador. Esto debido a que es la unica forma en que el torneo avance y que efectivamente se cave, ademas asi el parametros tiene sentido con los archivos entregados.
2. Existira al menos una arena de cada tipo en ```arenas.csv``` , ya que esa es la unica forma en que podran ocurrir todos los eventos posibles. 
3. Al consumir un ```Tesoro``` de calidad 2, el cual cambia el tipo de arena, se busca una arena random del tipo pedido dentro de ```arenas.csv```, osea no se le cambia el tipo a la arena existente actual, simplemente se busca una nueva. Respaldo [Issue #171](https://github.com/IIC2233/Syllabus/issues/171)
4. Derrumbe tambien afecta a arena normal. Respaldo [Issue #171](https://github.com/IIC2233/Syllabus/issues/171)
5. Cuando un ```Excavador``` empieza a descansar este cambia su atributo energia a ```100``` automaticamente a penas inicia dicho descanso y no cuando termina de descansar, a pesar de esto se respeta los dias de descanso. Respaldo [Issue #163](https://github.com/IIC2233/Syllabus/issues/163)
6. Un ```Tesoro``` o ```Consumible``` puede estar repetido y encontrarse multiples veces en un arena. Respaldo [Issue #167](https://github.com/IIC2233/Syllabus/issues/167)
7. Para las distintas opciones distintas a los menus se pide un input cualquiera para volver al menu que origino dicha opcion. Respaldo [Issue #200](https://github.com/IIC2233/Syllabus/issues/200)
8. Si se guarda una partida, se cierra el programa y posteriormente se carga nuevamenta la partida guardada, se asume que no se cambiaran los parametros de ```parametros.py``` ya que si se cambian la meta y los dias totales de la partida cambian. Respaldo [Issue #129](https://github.com/IIC2233/Syllabus/issues/129)
9. En un ```Torneo``` no existen dos excavadores en el equipo con el mismo nombre, en caso de consumir un ```Tesoro ``` de calidad 1 que agregue un tipo de excavador del cual ya no queden disponibles, se notificara que no fue posible y que se malgasto el item.
10. En caso de instanciar excavadores o arenas que originalmente no cumplan los criterios de sus distintos atributos especificados en el enunciado, se ajustaran dichos atributos con sus getter y setters al momento de instanciar para no generar contradicciones. Osea si por ejemplo se trata de instanciar un excavador de edad 68, esta se corrigira a 60.
11. Si ocurre un derrumbe en un ```Torneo``` en que su arena actual es ```ArenaNormal```, se busca una arena de tipo normal random entre las existentes en ```arenas.csv```, es posible que se realize el cambio a exactamente la misma arena en caso de que salga elegida aleatoriamente. Esto es valido ya que por ejemplo se nos entrega solo una arena normal en el documento no habria arena normal a la cual cambiar.
12. Como existe el evento Derrumbe y se puede poner  cualquier float positivo como parametro para `METROS_PERDIDOS_DERRUMBE`, entonces se puede dar el caso de que los metros cavados sean negativos ya que el derrumbe puede tapar lo actualmente cavado y agregar más arena.


-------
## Referencias de código externo :book:

No se ocupo codigo externo, todo el codigo es de mi autoría


