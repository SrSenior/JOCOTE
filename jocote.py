"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                Lenguaje JOCOTE                                ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║ Autores:     Luis Fernando Benavides                                          ║
║              Kristhel Cordero                                                 ║
║              Juan Diego Jiménez                                               ║
║              Alex Naranjo Masis                                               ║
║              José Pablo Vega                                                  ║
║                                                                               ║
║ Descripción:                                                                  ║
║ Archivo principal para el transpilador del lenguaje jocote.                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

from utils import archivos as utils

from explorador.explorador import Explorador
from analizador.analizador import Analizador
from verificador.verificador import Verificador
from generador.generador import Generador
from utils.jocoterrores import *

import os
import sys
import argparse
from colorama import init



init()
parser = argparse.ArgumentParser(description='Interprete para el mejor lenguaje de programación de todo el universo JOCOTE')



# Opción --solo-explorar, si está presente, se ejecutará solo el análisis léxico.
parser.add_argument('--solo-explorar', dest='explorador', action='store_true', 
        help='ejecuta solo el explorador y retorna una lista de componentes léxicos ademas de que los imprime')



# Opción --solo-analizar, si está presente, se ejecutará solo el analizador.
parser.add_argument('--solo-analizar', dest='analizador', action='store_true',
        help='ejecuta solo el analizador y retorna un preorden del árbol sintáctico')



# Opción --solo-verificar, si está presente, se ejecutará solo el verificador.
parser.add_argument('--solo-verificar', dest='verificador', action='store_true',
        help='ejecuta solo el verificador y retorna el arbol decorado')



# Opción --solo-generar, si está presente, se ejecutará solo el generador.
parser.add_argument('--solo-generar', dest='generador', action='store_true',
        help='ejecuta solo el generador y retorna el codigo en python')



# Opción --solo-jocotiar, si está presente, se ejecutará todo.
parser.add_argument('--solo-jocotiar', dest='jocote', action='store_true',
        help='ejecuta todo el programa, generando un archivo .py con el código jocote')



parser.add_argument('archivo',
        help='Archivo de código fuente')



def jocote():
    """
        Función principal que ejecuta el codigo jocote.
    """
    args = parser.parse_args()
    try:

        if args.explorador is True: 

            texto = list(utils.cargar_archivo(args.archivo))

            explorador = Explorador(texto)
            explorador.explorar()

            explorador.imprimir_componentes()
        


        elif args.analizador is True:

            texto = list(utils.cargar_archivo(args.archivo))

            explorador = Explorador(texto)
            explorador.explorar()
            
            analizador = Analizador(explorador.componentes)
            analizador.analizar() 
            
            analizador.asa.imprimir_asa()



        elif args.verificador is True:

            texto = list(utils.cargar_archivo(args.archivo))

            explorador = Explorador(texto)
            explorador.explorar()
            
            analizador = Analizador(explorador.componentes)
            analizador.analizar() 

            verificador = Verificador(analizador.asa)
            verificador.verificar(impresiones=True)
            
            verificador.asa.imprimir_asa()



        elif args.generador is True:

            texto = list(utils.cargar_archivo(args.archivo))

            explorador = Explorador(texto)
            explorador.explorar()
            
            analizador = Analizador(explorador.componentes)
            analizador.analizar() 

            verificador = Verificador(analizador.asa)
            verificador.verificar()
            
            generador = Generador(verificador.asa)
            generador.generar()

            generador.imprimir_codigo()


        
        elif args.jocote is True:

            texto = list(utils.cargar_archivo(args.archivo))

            explorador = Explorador(texto)
            explorador.explorar()
            
            analizador = Analizador(explorador.componentes)
            analizador.analizar() 

            verificador = Verificador(analizador.asa)
            verificador.verificar()
            
            generador = Generador(verificador.asa)
            generador.generar()

            nombre_sin_extension = os.path.splitext(os.path.basename(args.archivo))[0]
            ruta_salida = os.path.join("output", nombre_sin_extension + ".py")

            utils.crear_archivo(ruta_salida, generador.codigo)
            print(f"\n--- Código generado en '{ruta_salida}' ---")



        else:
            parser.print_help()
            
    except ErrorSintácticoJocotil as e:
        print(f"\nError Sintáctico Jocotil: {e}", file=sys.stderr)
        sys.exit(1)
        
    except ErrorTokenInválidoJocotil as e:
        print(f"\nError Token Inválido Jocotil: {e}", file=sys.stderr)
        sys.exit(1)

    except ErrorQueJocotesWTF as e:
        print(f"\nError Que Jocotes???: {e}", file=sys.stderr)
        sys.exit(1)
    
    except ErrorCeroTolerancia as e:
        print(f"\nError Cero Tolerancia: {e}", file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        print(f"\nError inesperado: {str(e)}", file=sys.stderr)
        sys.exit(1)



if __name__ == '__main__':
    jocote()