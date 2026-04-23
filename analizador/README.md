# Analizador
Se implementa el analizador de JOCOTE. Se encarga de analizar la lista de componentes léxicos del explorador y validar que cumplan con todas las reglas de la gramática.

## Manejo de Errores
En esta etapa se usa un método de manejo de errores de modo pánico. Al analizar la lista de componentes léxicos del explorador e ir validándolos de acuerdo con las reglas de la gramática, al encontrar un token inesperado levantará un Error Sintáctico Jocotil que después será atrapado en donde se llama al analizador, y detendrá el proceso del analizador. Es una manera sencilla y efectiva de decirle al usuario cuál es el problema que hay en su código.

# Ejemplos
Este módulo se accede desde el archivo jocote.py mediante argumentos desde la línea de comandos.
Para visualizar cómo funciona el explorador, puedes correr:
```bash
jocote.py --solo-analizar archivo
```

Por ejemplo:
```bash
python jocote.py --solo-analizar analizador/examples/area_circulo.tcj
python jocote.py --solo-analizar analizador/examples/pares.tcj
```