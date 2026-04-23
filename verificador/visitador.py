from enum import Enum
from analizador.asa import NodoArbol, TipoNodo
from utils.jocoterrores import ErrorQueJocotesWTF
from verificador.tabla_simbolos import TablaSimbolos



class Visitador():
    """
        Esta clase permite visitar a los nodos del árbol de sintáxis abstracta por medio de su
        referencia y su método visitar. Esto para recorrer el árbol de una manera más centralizada y ordenada.
    """

    tabla_simbolos: TablaSimbolos
    impresiones: bool = False  # Controla si se imprimen los mensajes de la tabla de símbolos



    def __init__(self, tabla_simbolos):
        self.tabla_simbolos = tabla_simbolos



    def visitar(self, nodo: NodoArbol):
        """
            Método para visitar un nodo del árbol de sintáxis abstracta
            y realizar las verificaciones necesarias.
        """

        if self.impresiones:
            print(f"Visitando nodo: {nodo}")

        if nodo.tipo == TipoNodo.PROGRAMA:
            self._visitar_programa(nodo)

        elif nodo.tipo == TipoNodo.SENTENCIA:
            self._visitar_sentencia(nodo)

        elif nodo.tipo == TipoNodo.DECLARACION:
            self._visitar_declaracion(nodo)

        elif nodo.tipo == TipoNodo.ASIGNACION:
            self._visitar_asignacion(nodo)

        elif nodo.tipo == TipoNodo.PALABRA_RESERVADA:
            self._visitar_palabra_reservada(nodo)

        elif nodo.tipo == TipoNodo.PALABRA_CLAVE:
            self._visitar_palabra_clave(nodo)

        elif nodo.tipo == TipoNodo.FUNCION:
            self._visitar_funcion(nodo)

        elif nodo.tipo == TipoNodo.LLAMADA_FUNCION:
            self._visitar_llamada_funcion(nodo)

        elif nodo.tipo == TipoNodo.PARAMETROS:
            self._visitar_parametros(nodo)

        elif nodo.tipo == TipoNodo.ESTRUCTURA:
            self._visitar_estructura(nodo)

        elif nodo.tipo == TipoNodo.ESTRUCTURA_CONTROL:
            self._visitar_estructura_control(nodo)

        elif nodo.tipo == TipoNodo.BUCLE:
            self._visitar_bucle(nodo)

        elif nodo.tipo == TipoNodo.NUMERO:
            self._visitar_numero(nodo)

        elif nodo.tipo == TipoNodo.STRING:
            self._visitar_string(nodo)

        elif nodo.tipo == TipoNodo.IDENTIFICADOR:
            self._visitar_identificador(nodo)
            
        else:
            raise ErrorQueJocotesWTF(f"No se ha implementado la visita para el tipo de nodo: {nodo.tipo}", nodo.linea)



    def _visitar_programa(self, nodo: NodoArbol):
        """
            Método para visitar el nodo raíz del árbol de sintáxis abstracta.

            Programa ::= Sentencia+;
        """

        for hijo in nodo.nodos:
            self.visitar(hijo)



    def _visitar_sentencia(self, nodo: NodoArbol):
        """
            Sentencia ::= Declaracion | Asignacion | Estructura | Comentario | Funcion | Llamada_funcion;
        """

        for hijo in nodo.nodos:
            self.visitar(hijo)



    def _visitar_declaracion(self, nodo: NodoArbol):
        """
            Declaración ::= ("jocote" | "cele" | "fibra") Identificador "=" Expresion ;
        """
        
        # nodo.contenido es el nombre del tipo de la variable que se declara
        
        # El primer hijo es el identificador de la variable
        if self.tabla_simbolos.existe_en_esta_profundidad(nodo.nodos[0].contenido):
            raise ErrorQueJocotesWTF(f"El identificador '{nodo.nodos[0].contenido}' ya ha sido declarado en la profundidad '{self.tabla_simbolos.profundidad}'.", nodo.linea)

        # Ponerle al identificador el tipo de la variable
        if (nodo.contenido == "jocote"):
            nodo.nodos[0].atributos['tipo'] = TiposTermino.NUMERO

        elif (nodo.contenido == "cele"):
            nodo.nodos[0].atributos['tipo'] = TiposTermino.NUMERO

        elif (nodo.contenido == "fibra"):
            nodo.nodos[0].atributos['tipo'] = TiposTermino.STRING

        # Registrar al identificador en la tabla
        self.tabla_simbolos.nuevo_registro(nodo.nodos[0])

        # Visitar al segundo hijo que es la expresion, expresion la cual debe ser del tipo de la variable declarada
        self._visitar_expresion(nodo.nodos[1], nodo.nodos[0].atributos['tipo'])



    def _visitar_asignacion(self, nodo: NodoArbol):
        """
            Asignacion ::= Identificador "=" (Expresion | Numero | String) ;
        """

        # El primer hijo es el identificador de la variable
        if not self.tabla_simbolos.existe(nodo.nodos[0].contenido):
            raise ErrorQueJocotesWTF(f"El identificador '{nodo.nodos[0].contenido}' no ha sido declarado.", nodo.linea)

        identificador = self.tabla_simbolos.buscar(nodo.nodos[0].contenido).referencia_nodo

        # Debe ser un identificador, no una funcion
        if identificador.tipo != TipoNodo.IDENTIFICADOR:
            raise ErrorQueJocotesWTF(f"El nodo '{nodo.nodos[0].contenido}' no es un identificador válido para una asignación.", nodo.linea)

        # Adornar el tipo del identificador
        nodo.nodos[0].atributos['tipo'] = identificador.atributos['tipo']

        # Como el identificador ya fue declarado, y en la visita de la declaracion se le pone el tipo al identificador, ya sabemos el tipo.

        # El segundo hijo es una expresion
        self._visitar_expresion(nodo.nodos[1], nodo.nodos[0].atributos['tipo'])



    def _visitar_expresion(self, nodo: NodoArbol, tipo_esperado: str): 
        """
            Expresion ::= Termino ( ("apiar" | "comer" | "sembrar" | "morder" | "semilla" | "<" | "<=" | ">" | ">=" | "==" | "!=" ) Termino )* ;
        """

        nodo.atributos['tipo'] = tipo_esperado

        # Puede o no haber palabra reservada y el segundo termino, pero siempre debe haber un termino. Y debe ser del mismo tipo que el tipo esperado
        for hijo in nodo.nodos:
            if hijo.tipo == TipoNodo.TERMINO:
                self._visitar_termino(hijo, tipo_esperado)
            
            elif hijo.tipo == TipoNodo.PALABRA_RESERVADA:
                self._visitar_palabra_reservada(hijo)



    def _visitar_termino(self, nodo: NodoArbol, tipo_esperado: str):
        """
            Termino ::= Numero | Identificador | String | Llamada_funcion ;
        """

        nodo.atributos['tipo'] = tipo_esperado

        # Si el primer hijo es el identificador
        if nodo.nodos[0].tipo == TipoNodo.IDENTIFICADOR:
            
            # Debe existir en la tabla de símbolos
            if not self.tabla_simbolos.existe(nodo.nodos[0].contenido):
                raise ErrorQueJocotesWTF(f"El identificador '{nodo.nodos[0].contenido}' no ha sido declarado.", nodo.linea)
            
            self._visitar_identificador(nodo.nodos[0])
            
            registro_encontrado = self.tabla_simbolos.buscar(nodo.nodos[0].contenido)
            if registro_encontrado.referencia_nodo.atributos['tipo'] != tipo_esperado:
                raise ErrorQueJocotesWTF(f"El identificador '{nodo.nodos[0].contenido}' no es del tipo esperado '{tipo_esperado}', sino del tipo '{registro_encontrado.referencia_nodo.atributos['tipo']}'.", nodo.linea)

        elif nodo.nodos[0].tipo == TipoNodo.LLAMADA_FUNCION:

            # Debe existir en la tabla de símbolos
            if not self.tabla_simbolos.existe(nodo.nodos[0].contenido):
                raise ErrorQueJocotesWTF(f"La funcion '{nodo.nodos[0].contenido}' no ha sido declarada.", nodo.linea)
            
            self._visitar_llamada_funcion(nodo.nodos[0])

            registro_encontrado = self.tabla_simbolos.buscar(nodo.nodos[0].contenido)
            if registro_encontrado.referencia_nodo.atributos['tipo'] != tipo_esperado and registro_encontrado.referencia_nodo.atributos['tipo'] != TiposTermino.INDEFINIDO:
                raise ErrorQueJocotesWTF(f"El identificador '{nodo.nodos[0].contenido}' no es del tipo esperado '{tipo_esperado}', sino del tipo '{registro_encontrado.referencia_nodo.atributos['tipo']}'.", nodo.linea)

        # Si es un numero o string, debe ser del tipo esperado
        else:
            if nodo.nodos[0].tipo == TipoNodo.NUMERO:
                nodo.nodos[0].atributos['tipo'] = TiposTermino.NUMERO

            elif nodo.nodos[0].tipo == TipoNodo.STRING:
                nodo.nodos[0].atributos['tipo'] = TiposTermino.STRING

            if nodo.nodos[0].atributos['tipo'] != tipo_esperado:
                raise ErrorQueJocotesWTF(f"El nodo '{nodo.nodos[0].contenido}' no es del tipo esperado '{tipo_esperado}', sino del tipo '{nodo.nodos[0].atributos['tipo']}'.", nodo.linea)



    def _visitar_palabra_reservada(self, nodo: NodoArbol):
        """
            "apiar" | "comer" | "sembrar" | "morder" | "semilla" ;
        """

        for hijo in nodo.nodos:
            self.visitar(hijo)
    


    def _visitar_palabra_clave(self, nodo: NodoArbol):
        """
            "qtmeten" | "qmas" | "qno" | "cele" | "jocote" | "fibra";
        """

        self.tabla_simbolos.abrir_bloque()

        if nodo.contenido in ("qtmeten", "qmas"):

            # Si es una estructura de control, debe tener una expresión
            self._visitar_expresion_booleana(nodo.nodos[0], TiposTermino.BOOLEANO)

            # El primer hijo es la expresión
            for hijo in nodo.nodos[1:]: 
                self.visitar(hijo)

        else:
            for hijo in nodo.nodos: 
                self.visitar(hijo)
        
        self.tabla_simbolos.cerrar_bloque()



    def _visitar_expresion_booleana(self, nodo: NodoArbol, tipo_esperado: str): 
        """
            Expresion ::= Termino ( ( "<" | "<=" | ">" | ">=" | "==" | "!=" ) Termino )* ;
        """

        nodo.atributos['tipo'] = tipo_esperado

        # Puede o no haber palabra reservada y el segundo termino, pero siempre debe haber un termino. Y debe ser del mismo tipo que el tipo esperado
        for hijo in nodo.nodos:
            if hijo.tipo == TipoNodo.TERMINO:
                self._visitar_termino(hijo, TiposTermino.NUMERO)
            
            elif hijo.tipo == TipoNodo.PALABRA_RESERVADA:
                self._visitar_palabra_reservada(hijo)



    def _visitar_funcion(self, nodo: NodoArbol):
        """
            Funcion ::= "jocotazo" Identificador "(" Parametros? ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ Retorno "}" ;
        """
        
        # El primer nodo.contenido es el identificador de la función
        if self.tabla_simbolos.existe_en_esta_profundidad(nodo.contenido):
            raise ErrorQueJocotesWTF(f"El identificador '{nodo.contenido}' ya ha sido declarado en la profundidad '{self.tabla_simbolos.profundidad}'.", nodo.linea)

        # Ponerle temporalmente el tipo de la función como indefinido, ya que no se sabe hasta que se llegue al retorno
        nodo.atributos['tipo'] = TiposTermino.INDEFINIDO

        # Guardar la función en la tabla de símbolos
        self.tabla_simbolos.nuevo_registro(nodo)

        # Abrir un nuevo bloque en la tabla de símbolos para todo lo que haya en la función
        self.tabla_simbolos.abrir_bloque()

        # Visitar los hijos del nodo función, exepto el último que es el retorno
        for hijo in nodo.nodos[:-1]:
            self.visitar(hijo)

        # El último hijo es el retorno, que debe asignar el tipo de la función al identificador de la función
        self._visitar_retorno(nodo.nodos[-1], nodo)

        # Cerrar el bloque de la función en la tabla de símbolos para que los identificadores locales no se filtren fuera de la función
        self.tabla_simbolos.cerrar_bloque()



    def _visitar_llamada_funcion(self, nodo: NodoArbol):
        """
            Llamada_funcion ::= Identificador "(" (Termino)? | (Termino ("," Termino)+ ")" ;
        """

        # Si es un identificador, debe existir en la tabla de símbolos
        if not self.tabla_simbolos.existe(nodo.contenido):
            raise ErrorQueJocotesWTF(f"El identificador '{nodo.contenido}' no ha sido declarado.", nodo.linea)

        # Debe ser una función, no una variable
        registro_funcion_llamada = self.tabla_simbolos.buscar(nodo.contenido)
        if registro_funcion_llamada.referencia_nodo.tipo != TipoNodo.FUNCION:
            raise ErrorQueJocotesWTF(f"El identificador '{nodo.contenido}' no es del tipo esperado '{TipoNodo.FUNCION}', sino del tipo '{registro_funcion_llamada.referencia_nodo.tipo}'.", nodo.linea)

        # Ponerle a la llamada función el tipo de la función
        if 'tipo' in registro_funcion_llamada.referencia_nodo.atributos:
            nodo.atributos['tipo'] = registro_funcion_llamada.referencia_nodo.atributos['tipo']
        else:
            nodo.atributos['tipo'] = TiposTermino.INDEFINIDO

        # Puede tener varios terminos o ninguno

        if len(registro_funcion_llamada.referencia_nodo.nodos) > 0:
            if (registro_funcion_llamada.referencia_nodo.nodos[0].tipo == TipoNodo.PARAMETROS):

                parametros_formales = registro_funcion_llamada.referencia_nodo.nodos[0].nodos

                if (len(nodo.nodos) < len(parametros_formales)/2):
                    raise ErrorQueJocotesWTF(f"Se le mandaron muy pocos parámetros a la función '{nodo.contenido}'.", nodo.linea)
                
                if (len(nodo.nodos) > len(parametros_formales)/2):
                    raise ErrorQueJocotesWTF(f"Se le mandaron muchos parámetros a la función '{nodo.contenido}'.", nodo.linea)

                count = 1                                                                               # El segundo elemento en los parametros es el identificador, el primero es la palabra clave
                for hijo in nodo.nodos:
                    identificador = parametros_formales[count]
                    count += 2                                                          

                    self._visitar_termino(hijo, identificador.atributos['tipo'])
                
            else:
                if (len(nodo.nodos) > 0):
                    raise ErrorQueJocotesWTF(f"Se le mandaron muchos parámetros a la función '{nodo.contenido}'.", nodo.linea)



    def _visitar_parametros(self, nodo: NodoArbol):
        """
            Parametros ::= ("jocote" | "cele" | "fibra") Identificador ( "," ("jocote" | "cele" | "fibra") Identificador ) * ;
        """

        for tipo, identificador in zip(nodo.nodos[::2], nodo.nodos[1::2]):
            
            if self.tabla_simbolos.existe_en_esta_profundidad(identificador.contenido):
                raise ErrorQueJocotesWTF(f"El identificador '{identificador.contenido}' ya ha sido declarado en la profundidad '{self.tabla_simbolos.profundidad}'.", nodo.linea)

            if (tipo.contenido == "jocote"):
                identificador.atributos['tipo'] = TiposTermino.NUMERO

            elif (tipo.contenido == "cele"):
                identificador.atributos['tipo'] = TiposTermino.NUMERO

            elif (tipo.contenido == "fibra"):
                identificador.atributos['tipo'] = TiposTermino.STRING

            self.tabla_simbolos.nuevo_registro(identificador)
 


    def _visitar_estructura(self, nodo: NodoArbol):
        """
            Estructura ::= Estructura_control | Bucle ;
        """

        for hijo in nodo.nodos:
            self.visitar(hijo)



    def _visitar_estructura_control(self, nodo: NodoArbol):
        """
            Estructura_control ::=  "qtmeten" "(" Expresion ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}" 
                                    ("qmas" "(" Expresion ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}")*
                                    ("qno" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}")? ;
        """

        for hijo in nodo.nodos:
            self.visitar(hijo)



    def _visitar_bucle(self, nodo: NodoArbol):
        """
            Bucle ::=   ("madurar" "(" Expresion ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}")
                        | ("cosechar" Identificador "en" "(" Identificador ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}") ;
        """
        self.tabla_simbolos.abrir_bloque()

        if nodo.contenido == "madurar":
            
            # Si es un while, debe tener una expresión
            self._visitar_expresion_booleana(nodo.nodos[0], TiposTermino.BOOLEANO)

            # El primer hijo es la expresión
            for hijo in nodo.nodos[1:]: 
                self.visitar(hijo)

        else:
            
            # El primer hijo es que se va a ir actualizando, hay que declararlo
            if self.tabla_simbolos.existe_en_esta_profundidad(nodo.nodos[0].contenido):
                raise ErrorQueJocotesWTF(f"El identificador '{nodo.nodos[0].contenido}' ya ha sido declarado en la profundidad '{self.tabla_simbolos.profundidad}'.", nodo.linea)

            nodo.nodos[0].atributos['tipo'] = TiposTermino.NUMERO

            # Registrar al identificador en la tabla
            self.tabla_simbolos.nuevo_registro(nodo.nodos[0])

            # El segundo hijo es el identificador del numero al que se va a llegar
            self._visitar_identificador(nodo.nodos[1])
            if (nodo.nodos[1].atributos['tipo'] != TiposTermino.NUMERO):
                raise ErrorQueJocotesWTF(f"El identificador '{nodo.nodos[1].contenido}' no es del tipo esperado '{TiposTermino.NUMERO}', sino del tipo '{nodo.nodos[1].atributos['tipo']}'.", nodo.linea)

            for hijo in nodo.nodos[2:]:
                self.visitar(hijo)

        self.tabla_simbolos.cerrar_bloque()
    


    def _visitar_identificador(self, nodo: NodoArbol):
        """
            Identificador ::= letras mayusculas o munúsculas, con tilde y guiones bajos
        """

        # Si es un identificador, debe existir en la tabla de símbolos
        if not self.tabla_simbolos.existe(nodo.contenido):
            raise ErrorQueJocotesWTF(f"El identificador '{nodo.contenido}' no ha sido declarado.", nodo.linea)

        # Debe ser un identificador, no una funcion
        registro = self.tabla_simbolos.buscar(nodo.contenido)
        if registro.referencia_nodo.tipo != TipoNodo.IDENTIFICADOR:
            raise ErrorQueJocotesWTF(f"El identificador '{nodo.contenido}' no es del tipo esperado '{TipoNodo.IDENTIFICADOR}', sino del tipo '{registro.referencia_nodo.tipo}'.", nodo.linea)

        # Ponerle el tipo al identificador
        registro_encontrado = self.tabla_simbolos.buscar(nodo.contenido)
        nodo.atributos['tipo'] = registro_encontrado.referencia_nodo.atributos['tipo']



    def _visitar_retorno(self, nodo: NodoArbol, nodo_funcion: NodoArbol):
        """
            Retorno ::= "brotar" Expresion ;
        """

        # El primer hijo es una expresión, la funcion debe ser del atributo tipo de la función
        tipo_esperado = self._obtener_tipo_termino(nodo.nodos[0].nodos[0])
        self._visitar_expresion(nodo.nodos[0], tipo_esperado)

        nodo_funcion.atributos['tipo'] = nodo.nodos[0].atributos['tipo']



    def _obtener_tipo_termino(self, nodo: NodoArbol):
        """
            Obtiene un término.
            Retorna el tipo del término según su contenido.
        """

        if nodo.nodos[0].tipo == TipoNodo.IDENTIFICADOR or nodo.nodos[0].tipo == TipoNodo.LLAMADA_FUNCION:

            # Debe existir en la tabla de símbolos
            if not self.tabla_simbolos.existe(nodo.nodos[0].contenido):
                raise ErrorQueJocotesWTF(f"El identificador '{nodo.nodos[0].contenido}' no ha sido declarado.", nodo.linea)

            registro_encontrado = self.tabla_simbolos.buscar(nodo.nodos[0].contenido)
            return registro_encontrado.referencia_nodo.atributos['tipo']

        elif nodo.nodos[0].tipo == TipoNodo.NUMERO:
            return TiposTermino.NUMERO
        
        elif nodo.nodos[0].tipo == TipoNodo.STRING:
            return TiposTermino.STRING
        
        else:
            raise ErrorQueJocotesWTF(f"El nodo '{nodo.contenido}' no es un término válido para obtener su tipo.", nodo.linea)
                


class TiposTermino(Enum):
    """
        Enum que representa los tipos de término en el lenguaje JOCOTE.
    """
    STRING = "string"
    NUMERO = "numero"
    BOOLEANO = "booleano"
    INDEFINIDO = "indefinido" # Solo se usa cuando se hace recursividad, porque no hay un tipo definido hasta que llame el retorno