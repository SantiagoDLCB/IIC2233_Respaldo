# Tarea 2: DCCazafantasmas 👻🧱🔥


## Consideraciones generales :octocat:

El codigo cumple con todos los criterios pedidos y los bonus. Tambien cuenta con una serie de consideraciones que se detallan más adelante como por ejemplo que se hace uso de las abreviaciones de los distintos objetos para representarlos en el modo constructor y que se le asigno la abreviacion Q a el Follower Villain.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Ventanas: 27 pts (27%)
##### ✅ Ventana de Inicio
###### La ventana cumple con todos los criterios de la distribucion de puntajes. El modo constructor en el listado de opciones disponibles se puede visualizar como "*** MODO CONSTRUCTOR ***" y se puede cambiar dicho texto en parametros.py
##### ✅ Ventana de Juego
###### La Ventana cumple con todos los criterios de la distribucion de puntajes. El panel de construccion señala cuantos elementos queda de cada entidad pero aparecen los nombres de las entidades con su caracter que los abrevia y los representa en los archivos de mapa. En el caso del Follower Villain su caracter es una Q. Por otra parte el boton salir aparece cuando se pierde o gana un nivel en formato de pop-up.
#### Mecánicas de juego: 47 pts (47%)
##### ✅ Luigi
###### Luigi al colisionar con un fantasma o fuego en una misma casilla pierde una vida y reinicia el nivel. Tambien luigi choca con las paredes y puede arrastrar las rocas dependiendo de si tienen un objeto atras. Luigi se mueve segun las teclas apretadas una a la vez, osea no se mueve en diagonal y debe esperar el cambio de casilla para que la siguiente tecla apretada sea valida. En caso de mantener una tecla apretada luigi seguira avanzando en esa direccion hasta soltar y llegar a una casilla
##### ✅ Fantasmas
###### Los fantasmas se mueven de manera independiente entre ellos con una velocidad aleatoria definida en parametros.py. Se implementan correctamente tanto el fantasma vertical como horizontal. Además los fantasmas mueren al chocar con un fuego y se devuleven al sentido contrario al chocar con una pared o roca.
##### ✅ Modo Constructor
###### Se pueden colocar todos los tipos de bloques siempre y cuando no se superpongan, se respeta el maximo de elementos por entidad el cual puede ser cambiable en parametros.py. Ninguna sprite tiene movimiento al no haber iniciado el juego, solamente el follower villain cambia de sprite sin moverse en el panel para poder identificarlo. No se puede iniciar el modo jugar sin un luigi y una estrella y se deshabilita el modo constructor cuando se empieza a jugar. Se pude limpiar el modo constructor con su respectivo boton.

##### ✅ Fin de ronda
###### Se termina el juego correctamente. Cuando se gana o se pierde se notifica al usuario mostrando su nombre mediante un pop-up y se da la opcion de salir o volver a jugar. En caso de perder se notifica al usuario el motivo y en caso de ganar se muestra el puntaje.
#### Interacción con el usuario: 14 pts (14%)
##### ✅ Clicks
###### El modo constructor funciona con el click izquierdo y el drag and drop.
##### ✅ Animaciones
###### El movimiento de las entidades minimas es fluido y animado, respetando los sprites correspondientes. En el caso de Follower villain se hace uso de los sprites de los fantasmas horizontal y vertical.
#### Funcionalidades con el teclado: 8 pts (8%)
##### ✅ Pausa
###### Se puede pausar el juego con el boton Pausa y la letra P, dehabilitando el movimiento de Luigi y del resto de entidades
##### ✅ K + I + L
###### Al escribir las letras en orden se elimina a todos los fantasmas del mapa incluido el follower villain. Esto se reinicia al perder una vida
##### ✅ I + N + F
###### Al escribir las letras en orden se congelan las vidas de Luigi volviendose inmortal y se congela el tiempo por lo que no se puede perder.

#### Archivos: 4 pts (4%)
##### ✅ Sprites
###### Se trabajan correctamente los sprites y se dejan sus paths en parametros.py
##### ✅ Parametros.py
###### Contiene los parametros minimos pedidos y otros creados para el desarrollo del codigo. Se importa y utiliza correctamente el archivo
#### Bonus: 8 décimas máximo
##### ✅ Volver a Jugar
###### Se cumple con todos los requisitos de este bonus. Se presenta el boton volver a jugar en el mismo pop-up que informa si se perdio o se gano junto con el boton salir.
##### ✅ Follower Villain
###### Cumple con todos los requisitos de este bonus. En el juego se representa con la letra Q y con una mezclad e los sprites de los otros Fantasmas. Persigue a Luigi evadiendo a todos los obstaculos menos el fuego usando BFS.
##### ✅ Drag and Drop
###### Se cumple con todos los criterios de este bonus. Se utiliza la mecanica pedida para hacer drag and drop de los objetos y estos una vez posicionados no se pueden sacar sin limpiar el modo constructor. Ademas en caso de hacer drop de un objeto en un lugar no valido se notificara al usuario al respecto.

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. La carpeta ```mapas``` debe ser creada en el directorio principal del juego y debe contener los mapas en formato descrito en el enunciado.
2. La carpeta ```sounds``` debe ser creada en el directorio principal del juego y debe contener los sonidos que se reproducen al ganar y perder un nivel.
3. La carpeta ```sounds``` debe ser creada en el directorio principal del juego y debe contener a las carpetas ```Elementos``` , ```Fondos``` , ```Personajes```. Cada una de estas carpetas debe contar con los elementos graficos para reproducir el juego. 


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```copy```: ```deepcopy()```
2. ```random```: ```uniform()``` 
3. ```collection```: ```deque()``` 
4. ```os```: ```path / listdir()``` 
5. ```PyQt5``` y sus librerias y modulos

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

#### Directorio Principal
1. ```main.py```: Es el modulo principal del juego. Crea e instancia la clase ```Juego```, haciendo uso de instancias de la clase ```Logica``` del backend y las clases ```VentanInicio``` y ```VentanaJuego``` del frontend. La clase creada en este modulo conecta todas las señales del juego entre frontend y backend.
2. ```paremetros.py```: Contiene los aprametros minimos del programa y otros creados para el desarrollo correcto de la tarea.

#### Carpeta ```backend```
1. ```entidades.py```: Crea las clases ```Entidad```, ```Luigi```, ```Fantasma```,```FantasmaVertical```, ```FantasmaHorizontal``` y ```FollowerVillain```. Establece relaciones de herencias entre dichas clases, ademas de establecer sus atributos y metodos.
2. ```backend.py```: Contiene a la clase ```Logica```, que realiza la mayoria de las acciones del backend como el calculo posicional, cargar y eliminar objetos, reinicio de niveles, etc...Emite y recibe las señales necesarias para sincronizar el backend con el frontend. Hace uso de las clases del modulo ```entidades```
3. ```funciones.py```: Crea funciones utilizadas para el calculo posicional, de movimiento posibles y creación del mapa de juego.
   
#### Carpeta ```frontend```
1. ```frontend_entidades.py```: Crea las clases ```FrontendEntidad```, ```FrontendLuigi```, ```FrontendFantasma```,```FrontendFantasmaV```, ```FrontendFantasmaH``` y ```FrontendFollowerVillain```. Establece relaciones de herencias entre dichas clases,ademas de establecer sus atributos y metodos. Son el equivalentes a nivel de frontend de las clases creadas en  ```entidades.py``` y estan sincronizadas por un id.
2. ```bloques.py```: Crea las clases ```Bloque```, ```Borde```, ```Pared```,```Roca```, ```Fuego``` y ```Estrella```. Establece relaciones de herencias entre dichas clases,ademas de establecer sus atributos y metodos, las principales diferencias entre las clases son sus respectivos Pixmap.

3. ```mapa.py```: Contiene a la clase ```Mapa```, que instancia, elimina y en cierto nivel posiciona o mueve a los bloques y entidades dentro del mapa segun lo pedido por el backend

4. ```panel_lateral.py```: Contiene a la clase ```PanelLateral``` y ```OpcionesConstructos```, clases las cuales se hacen cargo de mostrar la informacion pertinente segun el modo de juego actual. Además crean los botones necesarios para el modo constructor y modo juego. Tambien permiten el Drag and Drop de los objetos.
   
5. ```frontend.py```:  Contiene a la clase ```VentanInicio``` y ```VentanaJuego```. Ambas clases se encargan de crear la interfaz grafica de las ventanas del juego y crean Pop-Ups en caso de algun error o mensaje de fin de juego. Mas especificamente la primera clase permite la eleccion del modo de juego inicial o de un mapa precargado y la seleccion de un nombre correcto, mientras que la segunda hace uso de las clases ```Mapa``` y ```PanelLateral``` definida en los modos anteriores para construir el modo de juego. Además las clases anteriores reciben las teclas apretadas o información puesta por el usuario y las manda al backend.


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Luigi no puede moverse en diagonal, como se dice en el enunciado al apretar una tecla este cambia de casilla entonces por lo tanto no se va mover cruzando casillas.
2. No se puede pedir a luigi que se mueva en otra direccion mientras ya se encuentra en movimiento. Respaldo[Issue #321](https://github.com/IIC2233/Syllabus/issues/321)
3. El tiempo de movimiento de los fantasma es cuanto tiempo se demoran en cambiar de una casilla a otra y que por lo tanto los fantasmas no esperan en casillas avanzan continuamente entre casillas demorandose dicha cantidad de tiempo en trasladarse entre estas. Respaldo [Issue #319](https://github.com/IIC2233/Syllabus/issues/319)
4. Como los fantasmas se mueven continuamente se evalua si luigi choca con fantasma cada vez que el fantasma se mueve y estan en una casilla. Eso significa que Luigi y los fantasmas se pueden atravesar si se encuentran cambiandose de casillas.
5. Al pausar el juego ya sea por el boton o por apretar la tecla p, las entidades terminan sus cambios de casilla actual y se congelean inmediatamente. Respaldo [Issue #333](https://github.com/IIC2233/Syllabus/issues/333)
6. No se implemento el sistema de clicks en el modo constructor ya que se implemento el bonus Drag and Drop. Respaldo [Issue #338](https://github.com/IIC2233/Syllabus/issues/338)
7. Para activar los CHEATCODES es necesario apretar las teclas en el orden que aparecen en el enunciado, osea para cheatcode1 K, I, L y para cheatcode2 I,N,F
8. El cheatcode KIL se reinicia cada vez que se reinicia el nivel
9. En el modo constructor las letras corresponden a la abreviacion de su bloque o entidad en el mapa. Por ejemplo L es luigi, P es pared, etc. El Follower Villain lo represente por la letra Q
10. Al reiniciar al perder una vida se reinicia el nivel con todas las entidades y bloques en su posicion original pero los fantasma adquieren una nueva velocidad dentro del rango especificado, ya que esta velocidad es aleatoria para cada fantasma
11. Los sprites del follower villain puede que presenten algun tipo de bug pero como no es requisito del bonus no se arreglo
12. El Follower Villain en el modo constructor se ve representado por un fantasma horizontal y un fantasma vertical cambiando constantemente.
13. En el caso de mantener apretado una tecla de movimiento, luigi se mantendra moviendo pero como en cada casilla vuelve a mostrarse de frente podria parecer que el movimiento no es continuo pero simplemente esta mostrandose de frente porque esta en una casilla.
14. En el modo constructor si no se pone al menos un Luigi y una Estrella el boton de Jugar no inicia el juego pero tampoco manda un mensaje avisando, esto debido a que no se pide en el enunciado que se haga.
15. El puntaje no se muestra en caso de perder, se asume que es 0. Respaldo [Issue #397](https://github.com/IIC2233/Syllabus/issues/397)
16. En caso de ganar con el cheatcode2 o INF activado el calculo de puntajes se realiza con el tiempo inicial de la partida y una 1 vida ocupada. Respaldo [Issue #401](https://github.com/IIC2233/Syllabus/issues/401)
17. En la ventana de juego el tiempo aparece en segundos, no se hace la division en minutos y segundos ya que el enunciado no lo pide.


-------
## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://www.pythonguis.com/faq/pyqt-drag-drop-widgets/: este permite el drag and drop de los objetos en el modo constructor y está implementado en el archivo ```frontend_entidades.py``` en la carpeta ```frontend``` en las líneas ```39 a 47```
2. https://stackoverflow.com/questions/47896461/get-shortest-path-to-a-cell-in-a-2d-array-in-python: este codigo permite obtener el camino más corto a recorrer por el follower villain de manera tal que evite los obstaculos, está implementado en el archivo ```entidades.py``` en la carpeta ```backend``` en las líneas ```166 a 182```.
   
https://www.pythonguis.com/faq/pyqt-drag-drop-widgets/
