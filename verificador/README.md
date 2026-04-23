# Verificador
Se implementa el verificador de JOCOTE. El verificador se encarga de analizar ASA y decorarlo. Se implementa siguiendo una estrategia Descendente (Top-Down) siguiendo el patrón de diseño Visitante.

# Visitador
El visitador permite visitar a los nodos del árbol de sintáxis abstracta por medio de su referencia y su método visitar. Esto para recorrer el árbol de una manera más centralizada y ordenada. Va metiendose a cada uno y agregando las declaraciones a la tabla de simbolos cuando es necesario.

# Tabla de Símbolos
Es una estructura en la que se van almacenando los nombres de las variables, asi como sus declaraciones y la profundidad en el arbol en el que estan (para saber su scope).

# Funcionamiento
En escencia, transforma
```bash
--- Árbol de Sintáxis Abstracta ---
PROGRAMA
└── SENTENCIA
    └── DECLARACION - Contenido: fibra
        ├── IDENTIFICADOR - Contenido: saludo
        └── EXPRESION
            └── TERMINO
                └── STRING - Contenido: ωHola!ω
```
en
```bash
--- Árbol de Sintáxis Abstracta ---
PROGRAMA
└── SENTENCIA
    └── DECLARACION - Contenido: fibra
        ├── IDENTIFICADOR - Contenido: saludo - Atributos: {tipo: TiposTermino.STRING}
        └── EXPRESION - Atributos: {tipo: TiposTermino.STRING}
            └── TERMINO - Atributos: {tipo: TiposTermino.STRING}
                └── STRING - Contenido: ωHola!ω - Atributos: {tipo: TiposTermino.STRING}
```

## Manejo de Errores
El manejo de errores se implementa con la misma técnica del pánico que el resto de componentes del lenguaje, al encontrar una Excepción, la captura y la reporta sin ejecutar el código.

# Ejemplos
Este módulo se accede desde el archivo jocote.py mediante argumentos desde la línea de comandos.
Para visualizar cómo funciona el explorador, puedes correr:
```bash
jocote.py --solo-verificar archivo
```

Por ejemplo:
```bash
python jocote.py --solo-verificar verificador/examples/factorial.tcj
python jocote.py --solo-verificar verificador/examples/super_suma.tcj
```