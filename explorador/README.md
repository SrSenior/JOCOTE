# Explorador
Se implementa el explorador léxico de JOCOTE. El explorador se encarga de analizar el código fuente línea por línea para identificar los componentes léxicos para que puedan ser utilizados durante la etapa de análisis.  
El explorador nos permite identificar errores como el uso de símbolos inexistentes en el lenguaje. No realiza validación sintáctica ni semántica, solo reconoce tokens según las expresiones regulares definidas.

## Manejo de Errores
Para este proyecto se decidió usar un método de manejo de errores de modo pánico. Consiste en que al encontrar algún token inválido u otro error en la exploración de la gramática, se notifica el error junto con su línea y se continúan identificando el resto a partir del índice que sigue. Esto con el fin de evaluar si la mayor parte posible del código sigue con las reglas de la gramática en una sola compilación.

# Ejemplos
Este módulo se accede desde el archivo jocote.py mediante argumentos desde la línea de comandos.
Para visualizar cómo funciona el explorador, puedes correr:
```bash
jocote.py --solo-explorar archivo
```

Por ejemplo:
```bash
python jocote.py --solo-explorar explorador/examples/saludo.tcj
python jocote.py --solo-explorar explorador/examples/comparaciones.tcj
```