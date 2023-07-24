# Diagrama de clases

## Torneo
### Relaciones
La clase ```Torneo``` esta compuesta por una sola arena de cualquier tipo, por lo que se expresa como una relacion de composicion con la clase abstracta ```Arena``` ya que no necesariamente esta compuesta por un tipo de Arena en particular o por una Arena de cada tipo, sino que por una sola.

Paralelamente la clase ```Torneo``` tambien esta compuesta por una o más instacias de alguno de los tipos de excavadores, pero como no necesariamente debe haber un excavador de cada tipo en el torneo la relacion de composicion es con la clase abstracta ```Excavador```.

Además la clase ```Torneo``` tiene la posibilidad de contener items de tipo tesoro y/o consumible, pero no es extrictamente necesario, por lo que tiene una relacion de agregacion con la clase abstracta ```Items```.

-------
## Arena (ABC)
### Relaciones
Los distintos tipos de arena tambien pueden o no contener items de tipo tesoro y/o consumble, por lo que  la clase abstracta  ```Arena``` tiene un relacion de agregacion con la clase  abstracta ```Item```

### Herencia
Las clases ```ArenaNormal```, ```ArenaMojada```, ```Arena Rocosa``` heredean de ```Arena``` ya que son tipos de arena.

La clase ```ArenaMagnetica``` hereda de ```Arena Mojada``` y ```Arena Rocosa```, ya que es un tipo de arena que comparte propiedades de ambas clases.

-------
## Excavador(ABC)
### Herencia
Las clases ```ExcavadorTareo``` y ```ExacavadorDocencio``` heredean de ```Excavador``` ya que son tipos de excavadores.

La clase ```ExcavadorHibrido``` hereda de ```ExcavadorTareo``` y ```ExacavadorDocencio``` ya que es un tipo de excavadores, que comparte propiedades de ambas clases.

-------
## Item(ABC)
### Herencia
Las clases ```Tesoro``` y ```Consumible``` heredean de ```Item``` ya que son tipos de items.







