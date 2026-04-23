# Generador
Se implementa el generador de código de JOCOTE. El generador se encarga de agarrar el asa decorado y generar el código en python.

# Funcionamiento
En escencia, transforma
```bash
mae esta es una función que recibe un texto y retorna otro

jocotazo saludar(fibra nombre) {
    fibra mensaje = ωHola ω
    mensaje = mensaje apiar nombre
    brotar mensaje
}

fibra resultado = saludar(ωJocoaquínω) 
mae Jocoaquín = Jocote más Joaquín
estampar(resultado)

ඞ mae en JOCOTE no se permiten esas cosas
```
en
```python
# Ambiente estándar de JOCOTE en Python

...

def estampar(entrada: str):
    print(entrada)
    return entrada

...

# Código generado por el generador de JOCOTE

def saludar(nombre: str):
	mensaje: str = 'Hola '
	mensaje = mensaje + nombre
	return mensaje
resultado: str = saludar('Jocoaquín')
estampar(resultado)
```

# Ejemplos
Este módulo se accede desde el archivo jocote.py mediante argumentos desde la línea de comandos.
Para visualizar cómo funciona el explorador, puedes correr:
```bash
jocote.py --solo-generar archivo
```

Por ejemplo:
```bash
python jocote.py --solo-generar generador/examples/simon_dice.tcj
python jocote.py --solo-generar generador/examples/mayor.tcj
```