# Tarea 4: DCCachos :school_satchel:

## Consideraciones generales :octocat:

El codigo cumple con todos los criterios pedidos y los bonus. Tambien cuenta con una serie de consideraciones que se detallan más adelante como que el maximo de clientes conectados al mismo tiempo es 8 y que el servidor se desconecta cuando se acaba el juego.


### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Networking: 18 pts (16%)
##### ✅ Protocolo
###### Se usa implemento el protocolo TCP/IP
##### ✅ Correcto uso de sockets
###### Se logro instanciar y conectar correctamente los sockets. Los clientes y el servidor trabajan concurrentemente escuchandose mutuamente, se tuvo que hacer usos de locks a la hora de hacer pickle para evitar un error de underflow.
##### ✅ Conexión
###### La conexion es igual todo el tiempo y permite enviar todo tipo de mensajes. En este claso se implemento una clase mensaje que se envia y que puede o no contener otro tipo de clases como la clase Jugador o Status.
##### ✅ Manejo de Clientes
###### Se pueden conectar hasta 8 clientes en el servidor(mas adelante se aclara esto). Y no afecta el funcionamiento del programa
##### ✅ Desconexión Repentina
###### Si es que el servidor se desconecta se notifica a todos los clientes mediante un pop con el cual pueden cerrar su programa. Tambien si un cliente se desconecta se descarta su conexion y se actualiza la cola o se elimina de la partida dependiendo del caso.
#### Arquitectura Cliente - Servidor: 18 pts (16%)
##### ✅ Roles
###### Se sapara correctamente el servidor del cliente. El procesamiento de los datos y decisiones logicas las toma el servidor y es consistente con lo pedido en el enunciado. El cliente esta acargo de lo pedido por el enunciado
##### ✅ Consistencia
###### Se actualiza la informacion para todos los clientes y el servidor de una manera coordinada. Se utilizan locks cuando es necesario, en este caso para evitar multiples pickles al mismo tiempo
##### ✅ Logs
###### Se implementa el log del servidor con todos los elementos minimos requeridos y algunos adicionales para facilitar el seguimiento del juego.
#### Manejo de Bytes: 26 pts (22%)
##### ✅ Codificación
###### Se realizan todos los pasos correspondientes siguiente el enunciado.
##### ✅ Decodificación
###### Se realiza el proceso inverso a la codificacion siguiendo el enunciado
##### ✅ Encriptación
###### Se logra encriptar el mensaje usando un "N_PONDERADOR" siguiendo la segunda version del enunciado
##### ✅ Desencriptación
###### Se logra desencriptar el mensaje usando un "N_PONDERADOR" siguiendo la segunda version del enunciado
##### ✅ Integración
###### Se implementa correctamente el protocolo completo de envio de mensajes utilizando pickle.
#### Interfaz Gráfica: 22 pts (19%)
##### ✅ Ventana de Inicio
###### Se implemento la ventana con todos los elementos minimos, los usuarios se unen a una cola y en caso de haber cupos en la sala entran a esta ultima. Si es que no hay usuarios suficicentes se rrellena con bots. Si un cliente se intenta conectar con la partida ya comenzada este se le notifica de las situacion yse le pide intentar más tarde
##### ✅ Ventana de juego
###### La ventana cumple con todos los elementos graficos y botones minimos y se actualiza correctamente mediante el avance del juego. Se  visualiza a todos los jugadores ordenados de manera circular, se esconden los dados de los contrincante excepto cuando se duda y cuando se hace uso del bonus. Existen botones y formas para hacer todas las acciones correspindientes y se valida su validez para cada caso. Finalmente se notifica a los jugadores cuando pierden y ganan la partida.
#### Reglas de DCCachos: 22 pts (19%)
##### ✅ Inicio del juego
###### Se ordenan a los jugadores en un orden aleatorio, respetandose dicho orden en todo el juego, los lados se asignan de manera aleatoria.
##### ✅ Bots
###### Los bots siguen el procedimiento de turno definido en el enunciado usando probabilidades de realizar cada accion
##### ✅ Ronda
###### Se ejecutan correctamente todas las acciones de la ronda con sus regalas como anunciar, cambiar dados, dudar, usar poder y pasar.
##### ✅ Termino del juego
###### Se asigna correctamente el ganador del juego, ademaás se desconectan a los clientes y como no esta especificado se cierra el programa del servidor ya que no hay acciones restantes por el.
#### Archivos: 10 pts (9%)
##### ✅ Parámetros (JSON)
###### Todos los elementos minimos se encuentran en el parametros.json correspondiente dependiendo si es del servidor y el cliente, ademas se utiliza para manejar el resto de constantes como paths o textos. Se logra cargar y hacer uso de los parametros de manera correcta.
##### ✅ main.py
###### Tanto servidor como cliente se ejecutan desde un archivo main.py, este archivo main.py debe ser ejecutado indicando el puerto  como un argumento mediante consola
##### ✅ Cripto.py
###### Se implementa cripto.py de manera correcta, los testcase de prueba pasan sin errores, se utiliza este archivo para realizar la encriptacion ydesencriptacion de los mensajes entre servidor y cliente y viceversa.
#### Bonus: 4 décimas máximo
##### ✅ Cheatcodes
###### Se implementa el Cheatcode SEE como teclas que deben ser presionadas consecutivamente y muestra los dados de todos los jugadores al cliente que lo ejecute. Importante notar que debe presionar las teclas mientras no este seleccionado el QLineEdit para anunciar valores y usar poderes, ya que si no se registraran dentro de este.
##### ✅ Turno con tiempo
###### Se implementa cumpliendo todos los requisitos del bonus.

## Ejecución :computer:

### Servidor
El módulo principal de la tarea a ejecutar es  ```main.py```. No sera necesario crear directorios o archivos adicionales ademas de los directorios y librerias ya implementados.
   
### Cliente
El módulo principal del programa del servidor es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. La carpeta ```Sprites``` debe ser creada en el modulo ```frontend``` directorio principal del juego y debe contener a las carpetas ```background``` , ```dices``` , ```extra``` o cambiar los paths en la carpeta parametros. Cada una de estas carpetas debe contar con los element



## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```collections```: ```deque()```
2. ```copy```: ```deepcopy()```
3. ```json```: ```load()```
4. ```pickle```: ```loads(), dumps()```
5. ```PyQt5``` y sus librerias y modulos
6. ```os```: ```path, _exit()```
7. ```random```: ```choice(), randint(), random(), shuffle()```
8. ```socket```: ```socket, AF_INET, SOCK_STREAM```
9. ```sys```: ```argv, exit(), __excepthook__```
10. ```threading```: ```Event, Lock, Thread```
11. ```time```: ```sleep()```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

#### Servidor
1. ```main.py```: Es el modulo principal del servidor. Crea e instancia la clase ```Servidor```, maneja la logica de conexion desconexion, recepcion y envio de mensaje a clientes. Inicia y permite el desarrollo del juego a traves de importar e instanciar el modulo ```Juego```
2. ```juego.py```: Contiene a la clase ```Juego``` y es el encargado de manejar la logica de las rondas, turnos, eventos del juego, reglas, bots, etc...
3. ```parameteos.json``` Contiene los parametros o constantes del servidor.
   
4. Carpeta ```Scripts```
    1. ```clases.py```: Contiene a la clase ```Mensaje```, ```Jugador``` y ```Status```. Todas son utilizadas para almacenar información respectiva para posteriormente ser enviadas a los clientes o en su defecto para traducir la informacion enviada por estos. En particular  ```Mensaje``` es el objeto principal utilizado para comunicar y este objeto puede estar compuesto por instancias de las otras 2 clases. Ademas la clase ```Jugador``` es utilizada tambien para realizar logicas de vidas y de dados de cada jugador.
	2. ```codificacion.py```: Contiene a los metodos ```codificar``` y ```decodificar```, encargados de realizar los procesos respectivos de codificacion mencionados en el enunciado
    3. ```cripto.py```: Contiene a los metodos ```encriptar``` y ```desencriptar```, encargados de realizar los procesos respectivos de encriptaciones mencionados en el enunciado, contiene ademas unos test internos para probar dichos procesos.
    4. ```funciones.py```: Contiene a los metodos ```obtener_id_jugador``` e ```imprimir_logs```.
   
#### Cliente
1. ```main.py```: Es el modulo principal del cliente. Crea e instancia la clase ```Cliente```, encargada de importar e instanciar las clases ```Frontend``` y ```Backend```, ademas es la encargada de conectar las senales entre el frontend y el backend.
2. ```backend.py```: Contiene a la clase ```Backend``` encargada de la conexion, recepcion y envio de mensajes con el servidor, procesa los mensajes y manda senales al frontend para mantenerlo actualizado.
3. Carpeta ```Scripts```
    1. ```clases.py```: Contiene a la clase ```Mensaje```, ```Jugador``` y ```Status```. Todas son utilizadas para almacenar información respectiva para posteriormente ser enviadas al servidor o en su defecto para traducir la informacion enviada por este. En particular  ```Mensaje``` es el objeto principal utilizado para comunicar y este objeto puede estar compuesto por instancias de las otras 2 clases.
	2. ```codificacion.py```: Contiene a los metodos ```codificar``` y ```decodificar```, encargados de realizar los procesos respectivos de codificacion mencionados en el enunciado
    3. ```cripto.py```: Contiene a los metodos ```encriptar``` y ```desencriptar```, encargados de realizar los procesos respectivos de encriptaciones mencionados en el enunciado, contiene ademas unos test internos para probar dichos procesos.
4. Carpeta ```frontend```
   1. ```frontend.py```: Contiene a la clase ```Frontend```, ```Ventana Inicio```, ```VentanaJuego```, la primera clase crea instancias de las otras dos y maneja las acciones de cambio de ventanas y acciones iniciales. Las otras dos se encargan de actualizar la informacion de la interfaz grafica del cliente junto con sus elemntos graficos basicos y enviar senales al backend cuando algun cliente realize alguna accion, en sus ambitos respectivos. Para actualizar la informacion de los jugadores este modulo importa y crea instancias de ```IconoJugador```
   2. ```icono_jugador.py```: Contiene a la clase ```IconoJugador``` utilizada para mostrar los datos y elementos graficos de cada jugador en una partida segun el estado del juego actual.
   

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. El maximo de clientes que puede manejar el servidor es 8 ya que es la cantidad de IDs disponibles que tiene. Respaldo [Issue #437](https://github.com/IIC2233/Syllabus/issues/437)
2. Los bots tienen un id predefinido y se enumeran.Respaldo [Issue #438](https://github.com/IIC2233/Syllabus/issues/438)
3. Los jugadores se reordenan dependiendo de cuantos turnos quedan para que le toque a el. En este sentido para conservar que se juega de manera antihoraria, como siempre en este sentido le toca al de la derecha cuando se mira al centro, entonces una vez pasado ese turno todos avanzan un puesto a la izquierda, de manera tal que el que le tocaba porque estaba ubicado a la derecha a hora se ubique en el centro. En resumen para conservar un sentido de turno antihorario los jugadores rotan de asiento en manera horaria. Respaldo [Issue #440](https://github.com/IIC2233/Syllabus/issues/440)
4. Si se usa un poder se acabaa la ronda y continua el jugador que perdio la vida, en caso de no perder vida si no que aumentar o mantenerse constante por terremoto como no se especifica se acaba el turno y continua jugando el siguiente despues del que anuncia el poder. Respaldo [Issue #449](https://github.com/IIC2233/Syllabus/issues/449)
5. Si un jugador pierde se le desconecta del servidor
6. Si un jugador se desconecta es como si hubiera perdido y por lo tanto se acaba la ronda y parte el siguiente despues de el. Esto porque si no puede ocurrir que se intente dudar a alguien no presente en la ronda.
7.  Tiempo se congela cuando empieza una accion para que los lapsos de duracion de dichas acciones no afecten al resultado del jugador.
8.  Se desconecta el servidor al terminar el juego ya que no quedan más acciones pendientes por este. Para volver a jugar hay que cargarlo nuevamente