from analizador.asa import NodoArbol, TipoNodo
from utils.jocoterrores import ErrorQueJocotesWTF



class VisitadorPython:
    """
        Esta clase permite visitar a los nodos del árbol de sintáxis abstracta por medio de su
        referencia, para ir generando las instrucciones en Python.
    """

    identacion: int = 0

    def visitar(self, nodo: NodoArbol):
        """
            Método para visitar un nodo del árbol de sintáxis abstracta y generar el código Python correspondiente.
            Se llama a sí mismo recursivamente para visitar todos los nodos hijos del nodo actual.
        """

        # print(f"Visitando nodo: {nodo}")    #! DEBUG

        if nodo.tipo == TipoNodo.PROGRAMA:
            return self._visitar_programa(nodo)

        elif nodo.tipo == TipoNodo.SENTENCIA:
            return self._visitar_sentencia(nodo)
        
        elif nodo.tipo == TipoNodo.DECLARACION:
            return self._visitar_declaracion(nodo)
        
        elif nodo.tipo == TipoNodo.ASIGNACION:
            return self._visitar_asignacion(nodo)

        elif nodo.tipo == TipoNodo.EXPRESION:
            return self._visitar_expresion(nodo)

        elif nodo.tipo == TipoNodo.TERMINO:
            return self._visitar_termino(nodo)

        elif nodo.tipo == TipoNodo.FUNCION:
            return self._visitar_funcion(nodo)

        elif nodo.tipo == TipoNodo.LLAMADA_FUNCION:
            return self._visitar_llamada_funcion(nodo)

        elif nodo.tipo == TipoNodo.PARAMETROS:
            return self._visitar_parametros(nodo)

        elif nodo.tipo == TipoNodo.IDENTIFICADOR:
            return self._visitar_identificador(nodo)

        elif nodo.tipo == TipoNodo.ESTRUCTURA:
            return self._visitar_estructura(nodo)

        elif nodo.tipo == TipoNodo.ESTRUCTURA_CONTROL:
            return self._visitar_estructura_control(nodo)

        elif nodo.tipo == TipoNodo.BUCLE:
            return self._visitar_bucle(nodo)

        elif nodo.tipo == TipoNodo.RETORNO:
            return self._visitar_retorno(nodo)

        elif nodo.tipo == TipoNodo.PALABRA_CLAVE:
            return self._visitar_palabra_clave(nodo)

        elif nodo.tipo == TipoNodo.PALABRA_RESERVADA:
            return self._visitar_palabra_reservada(nodo)
        
        elif nodo.tipo == TipoNodo.STRING:
            return self._visitar_string(nodo)
        
        elif nodo.tipo == TipoNodo.NUMERO:
            return self._visitar_numero(nodo)
            
        else:
            raise ErrorQueJocotesWTF(f"No se ha implementado la visita para el tipo de nodo: {nodo.tipo}", nodo.linea)
        


    def _visitar_programa(self, nodo: NodoArbol):
        """
            Método para visitar el nodo raíz del árbol de sintáxis abstracta.

            Programa ::= Sentencia+;
        """

        instrucciones = []

        for hijo in nodo.nodos:
            instrucciones.append(self.visitar(hijo))

        # Esto retornará el generador, todas las instrucciones de los hijos de la raíz separados por enters
        return '\n'.join(instrucciones)



    def _visitar_sentencia(self, nodo: NodoArbol):
        """
            Sentencia ::= Declaracion | Asignacion | Estructura | Comentario | Funcion | Llamada_funcion;
        """

        instrucciones = []

        for hijo in nodo.nodos:
            instrucciones.append(self.visitar(hijo))

        return '\n'.join(instrucciones)



    def _visitar_declaracion(self, nodo: NodoArbol):
        """
            Declaración ::= ("jocote" | "cele" | "fibra") Identificador "=" Expresion ;
        """

        instrucciones = []

        for hijo in nodo.nodos:
            instrucciones.append(self.visitar(hijo))

        plantilla = "{}: {} = {}"

        # nodo.contenido: tipo
        # instrucciones[0]: identificador
        # instrucciones[1]: valor

        return self.__retornar_identacion() + plantilla.format(instrucciones[0], self.__retornar_tipo(nodo.contenido), instrucciones[1])
        


    def _visitar_asignacion(self, nodo: NodoArbol):
        """
            Asignacion ::= Identificador "=" (Expresion | Numero | String) ;
        """

        instrucciones = []

        for hijo in nodo.nodos:
            instrucciones.append(self.visitar(hijo))

        plantilla = "{} = {}"

        # instrucciones[0]: identificador
        # instrucciones[1]: expresion

        return self.__retornar_identacion() + plantilla.format(instrucciones[0], instrucciones[1])



    def _visitar_expresion(self, nodo: NodoArbol): 
        """
            Expresion ::= Termino ( ("apiar" | "comer" | "sembrar" | "morder" | "semilla" | "<" | "<=" | ">" | ">=" | "==" | "!=" ) Termino )* ;
        """

        instrucciones = []

        for hijo in nodo.nodos:
                instrucciones.append(self.visitar(hijo))

        if len(instrucciones) == 1:
    
            plantilla = "{}"

            # instrucciones[0]: termino

            return plantilla.format(instrucciones[0])

        else:

            plantilla = "{} {} {}"

            # instrucciones[0]: termino
            # instrucciones[1]: operador
            # instrucciones[2]: termino

            return plantilla.format(instrucciones[0], instrucciones[1], instrucciones[2])



    def _visitar_termino(self, nodo: NodoArbol):
        """
            Termino ::= Numero | Identificador | String | Llamada_funcion ;
        """
        
        instrucciones = []

        for hijo in nodo.nodos:
                instrucciones.append(self.visitar(hijo))

        # intrucciones[0]: identificador, numero, string o llamada a función
        
        return instrucciones[0]



    def _visitar_palabra_reservada(self, nodo: NodoArbol):
        """
            "apiar" | "comer" | "sembrar" | "morder" | "semilla" ;
        """

        return self.__retornar_operador(nodo.contenido)
    


    def _visitar_palabra_clave(self, nodo: NodoArbol):
        """
            "qtmeten" | "qmas" | "qno" | "cele" | "jocote" | "fibra";
        """

        instrucciones = []

        if nodo.contenido in ("qtmeten"):

            plantilla = "if ({}):"

            # instrucciones[0]: expresión

            instrucciones.append(plantilla.format(self.visitar(nodo.nodos[0])))

            # Se analizan el resto de los hijos
            self.identacion += 1

            for hijo in nodo.nodos[1:]:
                instrucciones.append(self.visitar(hijo))

            self.identacion -= 1

        elif nodo.contenido in ("qmas"):

            plantilla = "elif ({}):"

            # instrucciones[0]: expresión

            instrucciones.append(plantilla.format(self.visitar(nodo.nodos[0])))

            # Se analizan el resto de los hijos
            self.identacion += 1

            for hijo in nodo.nodos[1:]:
                instrucciones.append(self.visitar(hijo))

            self.identacion -= 1

        else:
            
            plantilla = "else:"

            instrucciones.append(plantilla)

            # Se analizan todos los hijos
            self.identacion += 1

            for hijo in nodo.nodos:
                instrucciones.append(self.visitar(hijo))

            self.identacion -= 1
        
        return self.__retornar_identacion() + '\n'.join(instrucciones)



    def _visitar_funcion(self, nodo: NodoArbol):
        """
            Funcion ::= "jocotazo" Identificador "(" Parametros? ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ Retorno "}" ;
        """

        instrucciones = []

        plantilla_funcion = "def {}({}):"
        parametros = ""

        # Si tiene parámetros, se debe declarar la función con los parámetros
        if nodo.nodos[0].tipo == TipoNodo.PARAMETROS:
            parametros = self._visitar_parametros(nodo.nodos[0])

        # nodo.contenido: nombre de la función
        # plantilla_parametros: parámetros de la función

        instrucciones.append(plantilla_funcion.format(nodo.contenido, parametros))

        self.identacion += 1

        for hijo in nodo.nodos:
            if hijo.tipo == TipoNodo.PARAMETROS:
                continue  # Ya se procesó los parámetros al inicio
            instrucciones.append(self.visitar(hijo))

        self.identacion -= 1

        return '\n'.join(instrucciones)



    def _visitar_llamada_funcion(self, nodo: NodoArbol):
        """
            Llamada_funcion ::= Identificador "(" (Termino)? | (Termino ("," Termino)+ ")" ;
        """

        plantilla = "{}({})"

        return self.__retornar_identacion() + plantilla.format(nodo.contenido, ', '.join(self.visitar(hijo) for hijo in nodo.nodos))



    def _visitar_parametros(self, nodo: NodoArbol):
        """
            Parametros ::= ("jocote" | "cele" | "fibra") Identificador ( "," ("jocote" | "cele" | "fibra") Identificador ) * ;
        """

        parametros = []

        for i in range(0, len(nodo.nodos), 2):
            tipo_nodo = nodo.nodos[i]
            id_nodo = nodo.nodos[i + 1]

            tipo = tipo_nodo.contenido
            identificador = id_nodo.contenido

            parametros.append(f"{identificador}: {self.__retornar_tipo(tipo)}")

        return ", ".join(parametros)
        


    def _visitar_estructura(self, nodo: NodoArbol):
        """
            Estructura ::= Estructura_control | Bucle ;
        """

        instrucciones = []

        for hijo in nodo.nodos:
            instrucciones.append(self.visitar(hijo))

        return '\n'.join(instrucciones)



    def _visitar_estructura_control(self, nodo: NodoArbol):
        """
            Estructura_control ::=  "qtmeten" "(" Expresion ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}" 
                                    ("qmas" "(" Expresion ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}")*
                                    ("qno" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}")? ;
        """

        instrucciones = []

        for hijo in nodo.nodos:
            instrucciones.append(self.visitar(hijo))

        return '\n'.join(instrucciones)



    def _visitar_bucle(self, nodo: NodoArbol):
        """
            Bucle ::=   ("madurar" "(" Expresion ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}")
                        | ("cosechar" Identificador "en" "(" Identificador ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}") ;
        """

        instrucciones = []

        if nodo.contenido in ("madurar"):

            plantilla = "while ({}):"

            # nodo.nodos[0]: expresión

            instrucciones.append(plantilla.format(self.visitar(nodo.nodos[0])))

            # Se analizan el resto de los hijos
            self.identacion += 1

            for hijo in nodo.nodos[1:]:
                instrucciones.append(self.visitar(hijo))

            self.identacion -= 1

        elif nodo.contenido in ("cosechar"):

            plantilla = "for {} in range({}):"

            # nodo.nodos[0]: identificador de la nueva variable
            # nodo.nodos[1]: numero hasta el que se va a cosechar

            instrucciones.append(plantilla.format(self.visitar(nodo.nodos[0]), self.visitar(nodo.nodos[1])))

            # Se analizan el resto de los hijos
            self.identacion += 1

            for hijo in nodo.nodos[2:]:
                instrucciones.append(self.visitar(hijo))

            self.identacion -= 1
        

        return self.__retornar_identacion() + '\n'.join(instrucciones)



    def _visitar_identificador(self, nodo: NodoArbol):
        """
            Identificador ::= letras mayusculas o munúsculas, con tilde y guiones bajos
        """

        # retornar el identificador, facilito
        return nodo.contenido



    def _visitar_retorno(self, nodo: NodoArbol):
        """
            Retorno ::= "brotar" Expresion ;
        """

        return f"{self.__retornar_identacion()}return {self.visitar(nodo.nodos[0])}"



    def _visitar_numero(self, nodo: NodoArbol):
        """
            entero o flotante
        """

        # retornar el numero, facilito
        return nodo.contenido



    def _visitar_string(self, nodo: NodoArbol):
        """
            ωcadenaω
        """

        # Se quita el inicio y el final de la cadena (ω) y se le pone comillas simples para que sea un string válido en Python.
        return f"'{nodo.contenido[1:-1]}'"



    def __retornar_identacion(self):
        """
            Retorna la cantidad de tabulaciones según el nivel de indentación actual.
        """

        return "\t" * self.identacion
    


    def __retornar_tipo(self, tipo_JOCOTE):
        """
            Retorna el tipo de dato en Python según el tipo JOCOTE.
        """

        tipos = {
            "jocote": "int",
            "cele": "float",
            "fibra": "str"
        }

        if tipo_JOCOTE not in tipos:
            raise ErrorQueJocotesWTF(f"Tipo JOCOTE no reconocido: {tipo_JOCOTE}", -1)

        return tipos.get(tipo_JOCOTE)
    


    def __retornar_operador(self, operador_JOCOTE):
        """
            Retorna el operador en Python según el operador JOCOTE.
        """

        operadores = {
            "apiar": "+",
            "comer": "-",
            "sembrar": "*",
            "morder": "/",
            "semilla": "%",
            "<": "<",
            "<=": "<=",
            ">": ">",
            ">=": ">=",
            "==": "==",
            "!=": "!="
        }

        if operador_JOCOTE not in operadores:
            raise ErrorQueJocotesWTF(f"Operador JOCOTE no reconocido: {operador_JOCOTE}", -1)

        return operadores.get(operador_JOCOTE)
