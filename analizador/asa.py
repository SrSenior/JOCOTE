from enum import Enum, auto
from colorama import Fore

import copy

class TipoNodo(Enum):
    """
        Enum para clasificar los distintos tipos de nodos en el árbol sintáctico.
        Cada tipo de nodo representa una construcción sintáctica en el lenguaje.
    """
    
    PROGRAMA = auto()
    SENTENCIA = auto()
    DECLARACION = auto()
    ASIGNACION = auto()
    EXPRESION = auto()
    TERMINO = auto()
    FUNCION = auto()
    LLAMADA_FUNCION = auto()
    IDENTIFICADOR = auto()
    RETORNO = auto()
    BUCLE = auto()
    ESTRUCTURA = auto()
    ESTRUCTURA_CONTROL = auto()
    PARAMETROS = auto()
    NUMERO = auto()
    STRING = auto()
    DIGIT = auto()
    LETTER = auto()
    PALABRA_RESERVADA = auto()
    PALABRA_CLAVE = auto()
    IDENTIFICADOR_ESPECIAL = auto()



class NodoArbol:
    """
        Nodo del árbol de sintáxis abstracta
        Cada nodo tiene tipo, contenido y atributos
    """

    tipo: TipoNodo
    contenido: str
    atributos: dict
    nodos: list
    linea: int
    


    def __init__(self, tipo, contenido = None, nodos = [], atributos = {}, linea = None):
        """
            Inicializar un NodoArbol
        """

        self.tipo      = tipo
        self.contenido = contenido
        self.nodos     = nodos
        self.atributos = copy.deepcopy(atributos)
        self.linea     = linea
        


    def __str__(self):
        """
            Retorna el nodo en formato string para impresión, incluyendo atributos.
        """

        tipo_color = Fore.CYAN
        contenido_color = Fore.YELLOW
        atributos_color = Fore.MAGENTA

        partes = [tipo_color + self.tipo.name + Fore.RESET]
        
        if self.contenido is not None:
            partes.append(f"{contenido_color}Contenido: {self.contenido}{Fore.RESET}")
        
        if self.atributos:
            atributos_str = ', '.join(f"{k}: {v}" for k, v in self.atributos.items())
            partes.append(f"{atributos_color}Atributos: {{{atributos_str}}}{Fore.RESET}")
        
        return ' - '.join(partes)



class ArbolSintaxisAbstracta:
    """
        Clase que representa el árbol de sintáxis abstracta.
        Contiene el nodo raíz y métodos para recorrer el árbol.
    """

    raiz: NodoArbol



    def __str__(self):
        """
            Retorna el árbol de sintáxis abstracta en formato string para impresión
        """

        if self.raiz is None:
            return "Árbol vacío"
        
        def generar_lineas(nodo, prefijo="", es_ultimo=True):
            lineas = []
            conectador = "└── " if es_ultimo else "├── "
            lineas.append(f"{prefijo}{conectador}{nodo}")
            
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            
            for i, hijo in enumerate(nodo.nodos):
                es_ultimo_hijo = i == len(nodo.nodos) - 1
                lineas.extend(generar_lineas(hijo, nuevo_prefijo, es_ultimo_hijo))
            
            return lineas
        
        lineas = [str(self.raiz)]
        for i, hijo in enumerate(self.raiz.nodos):
            es_ultimo = i == len(self.raiz.nodos) - 1
            lineas.extend(generar_lineas(hijo, "", es_ultimo))
        
        return "\n".join(lineas)
    


    def imprimir_asa(self):
        """
            Imprime el árbol de sintáxis abstracta.
        """

        print("\n--- Árbol de Sintáxis Abstracta ---")
        print(self)
    