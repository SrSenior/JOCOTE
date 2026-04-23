# Ambiente estándar de JOCOTE en Python

import sys
import os
import time
import random

def estampar(entrada: str):
    print(entrada)
    return entrada

def estampar_num(entrada: float):
    print(entrada)
    return entrada

def desestampar():
    os.system('cls' if os.name == 'nt' else 'clear')

def injerte(mensaje: str):
    return input(mensaje + ": ")

def suave(tiempo: float):
    time.sleep(tiempo)
    return tiempo

def jocoteMalo():
    return random.choice([True, False])

# Código generado por el generador de JOCOTE

def saludar(nombre: str):
	mensaje: str = 'Hola '
	mensaje = mensaje + nombre
	return mensaje
resultado: str = saludar('Jocoaquín')
estampar(resultado)