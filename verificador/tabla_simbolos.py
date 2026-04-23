from typing import List
from analizador.asa import NodoArbol
from utils.jocoterrores import ErrorQueJocotesWTF



class Registro:
    """
        Clase que representa un registro en la tabla de símbolos.
        Contiene información sobre el nodo, su tipo y atributos.
    """

    def __init__(self, nodo: NodoArbol, profundidad: int):
        self.identificador: str = nodo.contenido
        self.profundidad: int = profundidad
        self.referencia_nodo: NodoArbol = nodo



class TablaSimbolos:
    """ 
       Es una tabla en la que se almacenan los identificadores y sus respectivos nodos, asi como la profundidad en el codigo.
       Permite verificar la existencia de identificadores y gestionar el ámbito de los mismos.
    """

    impresiones: bool = False  # Controla si se imprimen los mensajes de la tabla de símbolos



    def __init__(self):
        self.profundidad: int = 0
        self.registros: List[Registro] = []



    def nuevo_registro(self, nodo: NodoArbol):
        """ 
            Crea un nuevo registro en la tabla de símbolos.
        """

        registro = Registro(nodo, self.profundidad)
        self.registros.append(registro)

        if self.impresiones:
            print("\n" + "Nuevo Registro, " + "Profundidad " + str(self.profundidad) + "\n" + str(self) + "\n")



    def abrir_bloque(self):
        """ 
            Aumenta la profundidad de la tabla de símbolos.
        """

        self.profundidad += 1

        if self.impresiones:
            print("\n" + "Aumenta Bloque, " + "Profundidad " + str(self.profundidad) + "\n" + str(self) + "\n")



    def cerrar_bloque(self):
        """ 
            Disminuye la profundidad de la tabla de símbolos.
        """

        # Elimina todos los registros de la profundidad actual, se usa una copia de la lista
        for registro in self.registros[:]:
            if registro.profundidad == self.profundidad:
                self.registros.remove(registro)

        self.profundidad -= 1

        if self.impresiones:
            print("\n" + "Disminuye Bloque, " + "Profundidad " + str(self.profundidad) + "\n" + str(self) + "\n")



    def existe_en_esta_profundidad(self, identificador: str):
        """ 
            Verifica si un identificador existe en la tabla de símbolos.
            Retorna True si existe, de lo contrario, retorna False.
        """

        for registro in self.registros:
            if registro.identificador == identificador and registro.profundidad == self.profundidad:
                return True

        return False
    


    def existe(self, identificador: str) -> bool:
        """ 
            Verifica si un identificador existe en la tabla de símbolos.
            Retorna True si existe, de lo contrario, retorna False.
        """

        for registro in self.registros:
            if registro.identificador == identificador and registro.profundidad <= self.profundidad:
                return True

        return False



    def buscar(self, identificador: str) -> Registro:
        """ 
            Busca un identificador en la tabla de símbolos.
            Retorna el registro si se encuentra, de lo contrario, retorna None.
        """

        # Buscar desde el final para encontrar el registro más reciente
        for registro in reversed(self.registros):

            if registro.identificador == identificador and registro.profundidad <= self.profundidad:
                return registro

        raise ErrorQueJocotesWTF(f"Identificador '{identificador}' no encontrado en la tabla de símbolos.")
    


    def __str__(self):
        """ 
            Retorna la tabla de símbolos en formato string con indentación
            proporcional a la profundidad y tabulaciones consistentes.
        """
        
        if not self.registros:
            return "Tabla de símbolos vacía"

        registros_str = []
        for registro in self.registros:
            indentacion = "\t" + "\t" * registro.profundidad
            linea = f"{indentacion}{registro.identificador} \t(Profundidad: {registro.profundidad})"
            registros_str.append(linea)

        return "\n".join(registros_str)
