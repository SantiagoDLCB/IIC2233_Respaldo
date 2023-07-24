# Tarea 0: DCCeldas 💣🐢🏰


## Consideraciones generales :octocat:

La tarea cumple con todo lo pedido en el enunciado, bajo las consideraciones definidas más adelante.

### Cosas implementadas y no implementadas :white_check_mark: :x:

- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores
#### Menú de Inicio (5 pts) (7%)
##### ✅ Seleccionar Archivo
##### ✅ Validar Archivos
#### Menú de Acciones (11 pts) (15%) 
##### ✅ Opciones
##### ✅ Mostrar tablero 
##### ✅ Validar bombas y tortugas
##### ✅ Revisar solución
##### ✅ Solucionar tablero
##### ✅ Salir
#### Funciones (34 pts) (45%)
##### ✅ Cargar tablero
##### ✅ Guardar tablero
##### ✅ Valor bombas
##### ✅ Alcance bomba
##### ✅ Verificar tortugas
##### ✅ Solucionar tablero
#### General: (19 pts) (25%)
##### ✅ Manejo de Archivos
##### ✅ Menús
##### ✅ tablero.py
##### ✅ Módulos
##### ✅ PEP-8
#### Bonus: 6 décimas
##### ✅ Funciones atómicas
##### ✅ Regla 5
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. 


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```path```, ```system()```
2. ```sys```: ```exit()```
3. ```collections```: ```deque()```
4. ```copy```: ```deepcopy()```


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```functions.py```: Hecha para definir las funciones pedidas en el enunciado y aquellas funciones adicionales creadas para facilitar el codigo

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Cualquier celda del tablero que entre a la variable solucionar_tablero es un str, esto debido a que los ejemplos entregados eso siempre se cumple
2. Los archivos a abrir seran siempre .txt, se encontraran en la carpeta Archivo y deberan ser escrita la extension en el menu de inicio tal y como es indicado.
3. Si se pide solucionar un tablero que ya esta solucionado cumpliendo las 5 reglas, el programa creara un archivo nuevo con un tablero identico y que agregara el sufijo _sol. De manera tal que si se le aplica esta accion a 5x5_sol.txt que ya esta solucionado, el programa creara un archivo identico con el nombre 5x5_sol_sol.txt. Esto porque no se especifica que no se ocupara esta accion para tableros ya resueltos.
4. La opcion 3 retorna que la solucion es valida inclusive si no se cumple la regla 5, esto porque el enunciado pide que solo se verifiquen el resto de reglas.
5. Las funciones estan implementadas para seguir el flujo generado en main.py 
6. Los archivo.txt a abrir cumplen con el formato descrito en el enunciado

