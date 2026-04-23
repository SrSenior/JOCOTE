"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      Explorador Léxico - Lenguaje JOCOTE                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║ Autores:     Luis Fernando Benavides                                          ║
║              Kristhel Cordero                                                 ║
║              Juan Diego Jiménez                                               ║
║              Alex Naranjo Masis                                               ║
║              José Pablo Vega                                                  ║
║                                                                               ║
║ Descripción:                                                                  ║
║ Este módulo realiza solo el explorador de nuestro querido lenguaje JOCOTE.    ║
║ Su propósito es identificar componentes del lenguaje según la gramática como: ║
║   - Palabras clave                                                            ║
║   - Identificadores                                                           ║
║   - Números                                                                   ║
║   - Cadenas de texto                                                          ║
║   - Comentarios                                                               ║
║                                                                               ║
║ Este explorador no realiza validaciones sintácticas de estructuras            ║
║ como declaraciones o asignaciones.                                            ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import re
from enum import Enum, auto
from colorama import Fore

from utils.jocoterrores import ErrorCeroTolerancia, ErrorQueJocotesWTF



class TipoComponente(Enum):
    """
        Enum para clasificar los distintos tipos de componentes léxicos que el explorador puede identificar
    """

    COMENTARIO    = auto()
    PALABRA_CLAVE = auto()
    TIPO_DATO     = auto()
    OPERADOR      = auto()
    COMPARADOR    = auto()
    ASIGNACION    = auto()
    TEXTO         = auto()
    IDENTIFICADOR = auto()
    ENTERO        = auto()
    FLOTANTE      = auto()
    PUNTUACION    = auto()
    ERROR         = auto()
    BLANCOS       = auto()



class ComponenteLexico:
    """
        Clase que representa un componente léxico con su tipo, texto y ubicación (línea y columna)
    """

    def __init__(self, tipo: TipoComponente, texto: str, linea: int, columna: int):
        self.tipo = tipo
        self.texto = texto
        self.linea = linea
        self.columna = columna



    def __str__(self):
        tipo_color = Fore.CYAN
        contenido_color = Fore.YELLOW
        return f"[Línea {str(self.linea + 1) + ",":<3}  Col {self.columna:<3}]  {tipo_color} {self.tipo.name:<20} {contenido_color} <{self.texto}> {Fore.RESET}"



class Explorador:
    """
        Clase principal que realiza el análisis léxico línea por línea del código fuente
    """

    # Lista de tuplas que contiene el tipo de componente y su expresión regular asociada
    descriptores_componentes = [
        (TipoComponente.COMENTARIO,    r'mae.+'),
        (TipoComponente.TEXTO,         r'(θ[^θ\n]*θ|ω[^ω\n]*ω)'),
        (TipoComponente.PALABRA_CLAVE, r'(jocotazo|qtmeten|qno|qmas|madurar|cosechar|brotar|en)\b'),
        (TipoComponente.TIPO_DATO,     r'(jocote|cele|fibra)\b'),
        (TipoComponente.COMPARADOR,    r'(<=|>=|<|>|==|!=)'),
        (TipoComponente.OPERADOR,      r'(apiar|comer|sembrar|morder|semilla)\b'),
        (TipoComponente.ASIGNACION,    r'='),
        (TipoComponente.FLOTANTE,      r'-?\d+\.\d+'),
        (TipoComponente.ENTERO,        r'-?\d+'),
        (TipoComponente.IDENTIFICADOR, r'[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ][a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ_]*'),
        (TipoComponente.PUNTUACION,    r'[\(\)\{\},;\.]'),
        (TipoComponente.BLANCOS,       r'\s+'),
    ]



    def __init__(self, contenido_archivo):
        """
            Inicializa el Explorador con el la lista de lineas del texto.

            Args:
                contenido_archivo (list): Lista de lineas del archivo .tcj
        """
        
        self.texto = contenido_archivo
        self.componentes = []
        self.errores = []



    def explorar(self):
        """
            Método principal que inicia el proceso de exploración léxica.
            Recorre cada línea del texto y llama al método _procesar_linea para analizarla.
        """

        for i, linea in enumerate(self.texto):
            self._procesar_linea(linea, i)

        if not self.componentes:
            raise ErrorQueJocotesWTF("Ocupamos un codigo para compilar jocotín!", 0)



    def _procesar_linea(self, linea: str, num_linea: int):
        """
            Procesa una línea de texto y busca coincidencias con los componentes léxicos definidos.
            Si encuentra un componente válido, lo agrega a la lista de componentes.
            Si no encuentra coincidencias, registra un error léxico.
        """

        pos = 0

        while pos < len(linea):
            match = None
        
            # Intenta hacer match con cada tipo de componente
            for tipo, regex in self.descriptores_componentes:
                pattern = re.compile(regex)
                match = pattern.match(linea, pos)
        
                if match:
                    valor = match.group()

                    # Cero tolerancia
                    if (valor.lower() == "windows"):
                        self.errores.append(ComponenteLexico(TipoComponente.ERROR, valor, num_linea, pos + 1))
                        pos = match.end()
                        raise ErrorCeroTolerancia(num_linea, pos)
                    
                    # Ignora espacios en blanco y comentarios, no los guarda
                    if tipo in [TipoComponente.BLANCOS, TipoComponente.COMENTARIO]:
                        
                        # Cero tolerancia
                        if ("windows" in valor.lower()):
                            self.errores.append(ComponenteLexico(TipoComponente.ERROR, valor, num_linea, pos + 1))
                            pos = match.end()
                            raise ErrorCeroTolerancia(num_linea, pos)

                        pos = match.end()
                        break
                    
                    # Agrega el componente válido a la lista
                    self.componentes.append(ComponenteLexico(tipo, valor, num_linea, pos + 1))
                    pos = match.end()
                    break
            
            # Si no hubo coincidencia con ningún componente, se registra como error
            if not match:
                self.errores.append(ComponenteLexico(TipoComponente.ERROR, linea[pos], num_linea, pos + 1))
                pos += 1



    def imprimir_componentes(self):
        """
            Imprimir los componentes léxicos encontrados y los errores léxicos.
        """

        print("\n--- Componentes Léxicos ---")
        for token in self.componentes:
            print(token)
        
        if self.errores:
            print("\n--- Errores Léxicos ---")
            for err in self.errores:
                print(err)