# Lenguaje de programación JOCOTE
## Creado por:
- ### Luis Fernando Benavides - 2023072689                          
- ### Kristhel Cordero - 2023135405                               
- ### Juan Diego Jiménez - 2019199111                            
- ### Alex Naranjo Masis - 2023063599                           
- ### José Pablo Vega - 2023367318                                    

## ¿Qué es JOCOTE?
Jocote es un lenguaje que fue diseñado como una metáfora viviente de la resiliencia, crecimiento y caos natural. Inspirado por la vida del jocote (el fruto), que a pesar de las adversidades del mundo actual, continúa creciendo y evolucionando.

Su implementación está hecha en python, y se compone de cuatro etapas que son el Explorador, el Analizador, el Verificador,
y el Generador de código.

Para el manejo de errores, se optó por una implementación del modo pánico, con el fin de evaluar si la mayor parte posible de el código es correcto en una sola compilación.

# Estructura del Proyecto
```bash
.
├── jocote.py                       # Punto de entrada del intérprete
├── explorador/
│   ├── examples/                   # Archivos de ejemplo escritos en JOCOTE
│   └── explorador.py               # Explorador léxico
├── analizador/
│   ├── examples/                   # Archivos de ejemplo escritos en JOCOTE
│   ├── asa.py                      # Clases y métodos para el árbol de sintáxis abstracta
│   ├── auxiliares_analizador.py    # Funciones de validacion para el analizador
│   └── analizador.py               # Analizador
├── verificador/
│   ├── examples/                   # Archivos de ejemplo escritos en JOCOTE
│   ├── tabla_simbolos.py           # Tabla para manejar la profundidad de las referencias
│   ├── visitador.py                # Clase que permite al verificador ir nodo por nodo
│   └── verificador.py              # Verificador
├── generador/
│   ├── examples/                   # Archivos de ejemplo escritos en JOCOTE
│   ├── visitador_python.py         # Clase que permite al generador recorrer el asa y generar el codigo .py
│   └── generador.py                # Generador
└── utils/
    ├── archivos.py                 # Funciones auxiliares para cargar archivos
    └── jocoterrores.py             # Clases de error del lenguaje JOCOTE
```

# Ejemplos
Para correr el transpilador, puede utilizar el programa de ejemplo que es una carrera de jocotes con el siguente comando:
```bash
python3 jocote.py --solo-jocotiar input/carreraCaracoles.tcj
```
Esto le generará un archivo en la carpeta output, que luego podrá correr como un archivo python común y corriente. Puede ver cómo funciona cada uno de los módulos de este proyecto en el README respectivo.