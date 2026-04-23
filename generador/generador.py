"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           Generador - Lenguaje JOCOTE                         ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║ Autores:     Luis Fernando Benavides                                          ║
║              Kristhel Cordero                                                 ║
║              Juan Diego Jiménez                                               ║
║              Alex Naranjo Masis                                               ║
║              José Pablo Vega                                                  ║
║                                                                               ║
║ Descripción:                                                                  ║
║ Este módulo realiza solo el generador de nuestro querido lenguaje JOCOTE.     ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

from analizador.asa import *
from generador.visitador_python import VisitadorPython



class Generador:
    """
        Clase principal encargada de generar el código fuente en Python a partir del Arbol Sintaxis Abstracto (ASA)
    """

    asa: ArbolSintaxisAbstracta
    vistador: VisitadorPython
    codigo: str = ""



    def __init__(self, asa):
        self.asa = asa
        self.visitador = VisitadorPython()


    
    def __cargar_ambiente_estándar(self):
        """
            Carga el ambiente estándar con las funciones y variables predefinidas.
        """
        
        return """# Ambiente estándar de JOCOTE en Python

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

"""



    def generar(self):
        """
            Método principal que inicia el proceso de generación del código fuente.
        """
        
        self.codigo = self.__cargar_ambiente_estándar()
        self.codigo += self.visitador.visitar(self.asa.raiz)

        return self.codigo
    


    def imprimir_codigo(self):
        print("\n--- Código generado ---")
        print(self.codigo)