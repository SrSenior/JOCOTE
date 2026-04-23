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

jocoteVerde: str = '\033[32m_@ï\033[0m'
jocotePinton: str = '\033[33m_@ï\033[0m'
jocoteMaduro: str = '\033[31m_@ï\033[0m'
def rodar(indice: int):
	if (	jocoteMalo()):
		indice = indice + 1
	return indice
def alguien_ganó(largo: int, indiceVerde: int, indicePinton: int, indiceMaduro: int):
	ganador: int = 0
	if (indiceVerde >= largo):
		ganador = 1
	elif (indicePinton >= largo):
		ganador = 1
	elif (indiceMaduro >= largo):
		ganador = 1
	else:
		ganador = 0
	return ganador
def quien_ganó(largo: int, indiceVerde: int, indicePinton: int, indiceMaduro: int):
	ganador: str = ' '
	if (indiceVerde >= largo):
		ganador = jocoteVerde
	elif (indicePinton >= largo):
		ganador = jocotePinton
	elif (indiceMaduro >= largo):
		ganador = jocoteMaduro
	else:
		ganador = 'Nadie'
	return ganador
def imprimir_carrera(largo: int, indiceVerde: int, indicePinton: int, indiceMaduro: int):
	mensaje: str = ''
	for i in range(largo):
		if (i == indiceVerde):
			mensaje = mensaje + jocoteVerde
		else:
			mensaje = mensaje + ' '
	mensaje = mensaje + '|\n'
	for i in range(largo):
		if (i == indicePinton):
			mensaje = mensaje + jocotePinton
		else:
			mensaje = mensaje + ' '
	mensaje = mensaje + '|\n'
	for i in range(largo):
		if (i == indiceMaduro):
			mensaje = mensaje + jocoteMaduro
		else:
			mensaje = mensaje + ' '
	mensaje = mensaje + '|\n'
	desestampar()
	estampar(mensaje)
	return mensaje
def carrera_de_jocotes(largo: int, velocidad: int):
	indiceVerde: int = 0
	indicePinton: int = 0
	indiceMaduro: int = 0
	while (	alguien_ganó(largo, indiceVerde, indicePinton, indiceMaduro) == 0):
		imprimir_carrera(largo, indiceVerde, indicePinton, indiceMaduro)
		suave(velocidad)
		indiceVerde = 		rodar(indiceVerde)
		indicePinton = 		rodar(indicePinton)
		indiceMaduro = 		rodar(indiceMaduro)
	return 'EL GANADOR ES ' + 	quien_ganó(largo, indiceVerde, indicePinton, indiceMaduro)
resultado: str = carrera_de_jocotes(15, 0.5)
estampar(resultado)