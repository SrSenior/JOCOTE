from colorama import Fore



linea_color = Fore.YELLOW
dato_color = Fore.MAGENTA



class ErrorSintácticoJocotil(Exception):
    """
        Excepción para errores sintácticos en JOCOTE
        (Cuando en el analizador llega un token que no se esperaba, se esperaba otro)
    """

    def __init__(self, texto_esperado, texto_actual, linea, columna):
        self.texto_esperado = texto_esperado
        self.texto_actual = texto_actual
        self.linea = linea + 1
        self.columna = columna
        


    def __str__(self):
        return (f"Error en {linea_color}línea {self.linea}{Fore.RESET}, {linea_color}columna {self.columna}{Fore.RESET}: "
                f"Se esperaba '{dato_color}{self.texto_esperado}{Fore.RESET}' pero se encontró '{dato_color}{self.texto_actual}{Fore.RESET}'")
    


class ErrorTokenInválidoJocotil(Exception):
    """
        Excepción para errores sintácticos inesperados en JOCOTE
        (Cuando en el analizador llega un token que nada que ver con las reglas de la gramática)
    """

    def __init__(self, texto_actual, linea, columna):
        self.texto_actual = texto_actual
        self.linea = linea + 1
        self.columna = columna
        


    def __str__(self):
        return (f"Error en {linea_color}línea {self.linea}{Fore.RESET}, {linea_color}columna {self.columna}{Fore.RESET}: "
                f"Token inválido: '{dato_color}{self.texto_actual}{Fore.RESET}'")
    


class ErrorQueJocotesWTF(Exception):
    """
        Excepción para algun error para el que me dio pereza crear una excepción específica
    """

    def __init__(self, mensaje, linea):      
        self.mensaje = mensaje
        self.linea = linea + 1
        

        
    def __str__(self):
        return (f"Error en {linea_color}línea {self.linea}{Fore.RESET}: {self.mensaje}")
    


class ErrorCeroTolerancia(Exception):
    """
        Excepción para cuando el código está contaminado con la palabra que todos los jocotes odian
    """

    def __init__(self, linea, columna):      
        self.linea = linea + 1
        self.columna = columna
        

        
    def __str__(self):
        return (f"Error en {linea_color}línea {self.linea}{Fore.RESET}, {linea_color}columna {self.columna}{Fore.RESET}: "
                f"Se encontró una {dato_color}contaminación{Fore.RESET} en el código, por favor, elimínala para continuar.")