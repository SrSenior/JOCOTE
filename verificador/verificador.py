"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                          Verificador - Lenguaje JOCOTE                        ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║ Autores:     Luis Fernando Benavides                                          ║
║              Kristhel Cordero                                                 ║
║              Juan Diego Jiménez                                               ║
║              Alex Naranjo Masis                                               ║
║              José Pablo Vega                                                  ║
║                                                                               ║
║ Descripción:                                                                  ║
║ Este módulo realiza solo el verificador de nuestro querido lenguaje JOCOTE.   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

from analizador.asa import *
from explorador.explorador import TipoComponente
from verificador.tabla_simbolos import TablaSimbolos
from verificador.visitador import TiposTermino, Visitador



class Verificador:
    """
        Clase principal encargada de realizar el análisis de identificación y la inferencia de tipo
    """

    asa: ArbolSintaxisAbstracta
    vistador: Visitador
    tabla_simbolos: TablaSimbolos



    def __init__(self, asa):
        self.asa = asa

        self.tabla_simbolos = TablaSimbolos()
        self.__cargar_ambiente_estándar()

        self.visitador = Visitador(self.tabla_simbolos)



    def __cargar_ambiente_estándar(self):
        """
            Carga el ambiente estándar con las funciones y variables predefinidas.
        """
        
        componentes = [ 
            ('estampar', TipoNodo.FUNCION, TiposTermino.STRING, [
                                                                    NodoArbol(TipoNodo.PARAMETROS, nodos=[
                                                                                                            NodoArbol(TipoComponente.PALABRA_CLAVE, contenido="fibra"), 
                                                                                                            NodoArbol(TipoComponente.IDENTIFICADOR, contenido="entrada", atributos={'tipo': TiposTermino.STRING})
                                                                                                        ])
                                                                ]),                      # Un print de strings de toda la vida
            ('estampar_num', TipoNodo.FUNCION, TiposTermino.NUMERO, [
                                                                    NodoArbol(TipoNodo.PARAMETROS, nodos=[
                                                                                                            NodoArbol(TipoComponente.PALABRA_CLAVE, contenido="cele"), 
                                                                                                            NodoArbol(TipoComponente.IDENTIFICADOR, contenido="entrada", atributos={'tipo': TiposTermino.NUMERO})
                                                                                                        ])
                                                                ]),                      # Un print de numeros toda la vida
            ('desestampar', TipoNodo.FUNCION, TiposTermino.STRING, []),                  # Que sea el os.system('cls / clear')
            ('injerte', TipoNodo.FUNCION, TiposTermino.STRING, [
                                                                    NodoArbol(TipoNodo.PARAMETROS, nodos=[
                                                                                                            NodoArbol(TipoComponente.PALABRA_CLAVE, contenido="fibra"), 
                                                                                                            NodoArbol(TipoComponente.IDENTIFICADOR, contenido="mensaje", atributos={'tipo': TiposTermino.STRING})
                                                                                                        ])
                                                                ]),                      # Que sea el input() de toda la vida
            ('suave', TipoNodo.FUNCION, TiposTermino.NUMERO, [
                                                                    NodoArbol(TipoNodo.PARAMETROS, nodos=[
                                                                                                            NodoArbol(TipoComponente.PALABRA_CLAVE, contenido="cele"), 
                                                                                                            NodoArbol(TipoComponente.IDENTIFICADOR, contenido="tiempo", atributos={'tipo': TiposTermino.NUMERO})
                                                                                                        ])
                                                                ]),    
            # ('jocoteMalo', TipoNodo.IDENTIFICADOR_ESPECIAL, TiposTermino.NUMERO, [])   # La variable que puede ser true o false aleatoriamente, y cada vez que se llama cambia
            ('jocoteMalo', TipoNodo.FUNCION, TiposTermino.NUMERO, [])                    # Estaba muy dificil hacerlo una variable, así que lo hice una función
        ]

        for nombre, tipo, tipo_retorno, nodos in componentes:
            
            if (tipo == TipoNodo.FUNCION):
                nodo = NodoArbol(tipo, contenido=nombre, atributos={'tipo': tipo_retorno}, nodos=nodos)
                self.tabla_simbolos.nuevo_registro(nodo)
            else:
                nodo = NodoArbol(tipo, contenido=nombre, atributos={'tipo': tipo_retorno})
                self.tabla_simbolos.nuevo_registro(nodo)



    def verificar(self, impresiones: bool = False):
        """
            Método principal que inicia la verificación del ASA.
        """

        self.tabla_simbolos.impresiones = impresiones
        self.visitador.impresiones = impresiones

        self.visitador.visitar(self.asa.raiz)


