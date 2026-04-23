"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      Analizador Léxico - Lenguaje JOCOTE                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║ Autores:     Luis Fernando Benavides                                          ║
║              Kristhel Cordero                                                 ║
║              Juan Diego Jiménez                                               ║
║              Alex Naranjo Masis                                               ║
║              José Pablo Vega                                                  ║
║                                                                               ║
║ Descripción:                                                                  ║
║ Este módulo realiza solo el analizador de nuestro querido lenguaje JOCOTE.    ║
║ Su propósito es crear el árbol de sintáxis abstracta                          ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

from analizador.asa import ArbolSintaxisAbstracta, NodoArbol, TipoNodo
from explorador.explorador import ComponenteLexico, TipoComponente
from utils.jocoterrores import *
from analizador.auxiliares_analizador import *



class Analizador:
    """
        Clase principal encargada de realizar el análisis sintáctico por descenso recursivo.
        
        Atributos:
            componentes_léxicos (list): Lista de tokens producidos por el analizador léxico.
            cantidad_componentes (int): Número total de tokens en la lista.
            posición_componente_actual (int): Índice del token que se está procesando.
            componente_actual (ComponenteLexico): Token en el que se está trabajando actualmente.
            asa (ArbolSintaxisAbstracta): Árbol de sintaxis abstracta construido durante el análisis.
    """
    
    componentes_léxicos : list
    cantidad_componentes : int
    posición_componente_actual : int
    componente_actual : ComponenteLexico
    asa : ArbolSintaxisAbstracta



    def __init__(self, lista_componentes):
        """
            Inicializa el Analizador con la lista de tokens.

            Args:
                lista_componentes (list): Tokens obtenidos tras el análisis léxico.
        """
        
        self.componentes_léxicos = lista_componentes
        self.cantidad_componentes = len(lista_componentes)

        self.posición_componente_actual = 0
        self.componente_actual = lista_componentes[0]

        self.asa = ArbolSintaxisAbstracta()
    


    def __ver_siguiente_componente(self):
        """
            Retorna el componente que sigue, sin descartarlo.
        """

        if self.posición_componente_actual + 1 < self.cantidad_componentes:
            return self.componentes_léxicos[self.posición_componente_actual + 1]
        
        else:
            return None



    def verificar(self, texto_esperado ):
        """
            Verifica si el texto del componente léxico actual corresponde con el esperado como argumento
        """      

        if self.componente_actual.texto != texto_esperado:
            raise ErrorSintácticoJocotil(texto_esperado, self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        self.siguiente()



    def siguiente(self):
        """
            Avanza al siguiente componente si no está al final.
        """

        self.posición_componente_actual += 1

        if self.posición_componente_actual < self.cantidad_componentes:
            self.componente_actual = self.componentes_léxicos[self.posición_componente_actual]

        else:
            self.componente_actual = None



    def analizar(self):
        """
            Método principal que inicia el análisis siguiendo el esquema de análisis por descenso recursivo
        """

        self.asa.raiz = self.analizar_programa()
    


    def analizar_programa(self):
        """
            Programa ::= Sentencia+;
        """

        linea_programa = self.componente_actual.linea if self.componente_actual else None

        nodos_nuevos=[]
        
        # Mientras queden tokens, analizamos sentencias
        while self.componente_actual is not None:
            nodos_nuevos += [self.analizar_sentencia()]
        
        return NodoArbol(TipoNodo.PROGRAMA, nodos=nodos_nuevos, linea=linea_programa)



    def analizar_sentencia(self):
        """
            Sentencia ::= Declaracion | Asignacion | Estructura | Comentario | Funcion | Llamada_funcion;
            
        Determina el tipo de sentencia según el token actual o
        la pareja actual-siguiente y delega al método correspondiente.
        
        Returns:
            NodoArbol: Nodo de tipo SENTENCIA que contiene el subnodo específico.
        
        Raises:
            ErrorTokenInválidoJocotil: Si el token no corresponde a ninguna sentencia válida.
        """

        linea_sentencia = self.componente_actual.linea if self.componente_actual else None

        nodos_nuevos = []

        # Chequeamos cada posibilidad en orden de prioridad
        if esDeclaración(self.componente_actual):
            nodos_nuevos += [self.analizar_declaracion()]

        elif esEstructura(self.componente_actual):
            nodos_nuevos += [self.analizar_estructura()]

        elif esFuncion(self.componente_actual): 
            nodos_nuevos += [self.analizar_funcion()]

        elif esLlamadaFuncion(self.componente_actual, self.__ver_siguiente_componente()):
            nodos_nuevos += [self.analizar_llamada_funcion()]

        elif esAsignacion(self.componente_actual, self.__ver_siguiente_componente()):
            nodos_nuevos += [self.analizar_asignacion()]

        else:
            raise ErrorTokenInválidoJocotil(self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        return NodoArbol(TipoNodo.SENTENCIA, nodos=nodos_nuevos, linea=linea_sentencia)
        


    def analizar_declaracion(self):
        """
            Declaración ::= ("jocote" | "cele" | "fibra") Identificador "=" Expresion ;

        - Primero verifica y captura el tipo de dato (jocote, cele o fibra).
        - Luego analiza el identificador.
        - Después consume el “=” y analiza la expresión que inicializa la variable.
        - Finalmente, crea y devuelve un nodo de tipo DECLARACION con el nombre del tipo
        y los subnodos correspondientes.
        """

        linea_declaracion = self.componente_actual.linea if self.componente_actual else None

        nodos_nuevos = []

        tipoDato = self.componente_actual
        if esDeclaración(self.componente_actual):
            self.siguiente()
        else:
            raise ErrorSintácticoJocotil("jocote | cele | fibra", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)
        
        if esIdentificador(self.componente_actual):
            nodos_nuevos += [self.analizar_identificador()]
        else:
            raise ErrorSintácticoJocotil("identificador", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        self.verificar('=')

        nodos_nuevos += [self.analizar_expresion()]

        return NodoArbol(TipoNodo.DECLARACION, nodos=nodos_nuevos, contenido=tipoDato.texto, linea=linea_declaracion)



    def analizar_asignacion(self):
        """
            Asignacion ::= Identificador "=" (Expresion | Numero | String) ;
            
        - Primero analiza el identificador de la variable.
        - Luego consume el “=” y analiza la expresión o literal asignado.
        - Devuelve un nodo de tipo ASIGNACION con los subnodos correspondientes.
        """

        linea_asignacion = self.componente_actual.linea if self.componente_actual else None

        nodos_nuevos = []
        
        # Analizar identificador destino de la asignación
        if esIdentificador(self.componente_actual):
            nodos_nuevos += [self.analizar_identificador()]
        else:
            raise ErrorSintácticoJocotil("identificador", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        self.verificar("=")
        
        # Analizar la expresión que se asigna (número, cadena u otra expresión)
        nodos_nuevos += [self.analizar_expresion()]
        
        return NodoArbol(TipoNodo.ASIGNACION, nodos=nodos_nuevos, linea=linea_asignacion)



    def analizar_expresion(self): 
        """
            Expresion ::= Termino ( ("apiar" | "comer" | "sembrar" | "morder" | "semilla" | "<" | "<=" | ">" | ">=" | "==" | "!=" ) Termino )* ;
        - Empieza analizando un término.
        - Si tras el término va un operador válido, lo captura y analiza el siguiente término.
        - Devuelve un nodo EXPRESION con los subnodos en orden.
        """

        linea_expresion = self.componente_actual.linea if self.componente_actual else None
        
        nodos_expresion = []
        # Primer término obligatorio
        if esTermino(self.componente_actual, self.__ver_siguiente_componente()):
            nodos_expresion += [self.analizar_termino()]
        else:
            raise ErrorSintácticoJocotil("termino", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)
        
        # Si hay un operador, lo consumimos y procesamos un segundo término
        if esOperador(self.componente_actual):
            linea_operador = self.componente_actual.linea if self.componente_actual else None
            nodos_expresion += [NodoArbol(TipoNodo.PALABRA_RESERVADA, contenido=self.componente_actual.texto, linea=linea_operador)]     
            self.siguiente()
        else:
            return NodoArbol(TipoNodo.EXPRESION, nodos=nodos_expresion, linea=linea_expresion)
        
        # Analizar el término tras el operador
        if esTermino(self.componente_actual, self.__ver_siguiente_componente()):
            nodos_expresion += [self.analizar_termino()]
        else:
            raise ErrorSintácticoJocotil("termino", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)
        
        # Devolver la estructura completa de la expresión
        return NodoArbol(TipoNodo.EXPRESION, nodos=nodos_expresion, linea=linea_expresion)



    def analizar_termino(self):
        """
            Analiza un término, que puede ser:
            - Un número
            - Una cadena (String)
            - Una llamada a función
            - Un identificador

            Termino ::= Numero | Identificador | String | Llamada_funcion ;

            Identifica qué tipo de término es y delega al método apropiado.
        """

        linea_termino = self.componente_actual.linea if self.componente_actual else None
        
        nodos_nuevos = []

        if esNumero(self.componente_actual):
            nodos_nuevos += [self.analizar_numero()]

        elif esString(self.componente_actual):
            nodos_nuevos += [self.analizar_string()]

        elif esLlamadaFuncion(self.componente_actual, self.__ver_siguiente_componente()):
            nodos_nuevos += [self.analizar_llamada_funcion()]

        elif esIdentificador(self.componente_actual):
            nodos_nuevos += [self.analizar_identificador()]

        else: 
            raise ErrorSintácticoJocotil("termino", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        return NodoArbol(TipoNodo.TERMINO, nodos=nodos_nuevos, linea=linea_termino)



    def analizar_funcion(self):
        """
            Funcion ::= "jocotazo" Identificador "(" Parametros? ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ Retorno "}" ;
        Flujo:
        1. Consume la palabra clave 'jocotazo'.
        2. Captura el nombre de la función (identificador).
        3. Procesa los paréntesis y, si hay, los parámetros.
        4. Recorre el bloque de sentencias hasta encontrar la palabra clave de retorno.
        5. Analiza la instrucción de retorno.
        6. Cierra la llave y retorna un nodo FUNCION con su nombre y cuerpo.
        """

        linea_funcion = self.componente_actual.linea if self.componente_actual else None

        nodos_nuevos = []

        self.siguiente() # por jocotazo

        nombreFuncion = ""
        # Leer el nombre de la función
        if esIdentificador(self.componente_actual):    
            nombreFuncion = self.componente_actual.texto
            self.siguiente()
        else:
            raise ErrorSintácticoJocotil("identificador", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)
        
        self.verificar('(')

        if (self.componente_actual.texto != ')'):
            nodos_nuevos += [self.analizar_parametros()]

        self.verificar(')')
        
        self.verificar('{')

        # Analizar todas las sentencias hasta 'brotar' (retorno)
        while self.componente_actual:
            if (self.componente_actual.texto == 'brotar'):
                break
            
            if esDeclaración(self.componente_actual):
                nodos_nuevos += [self.analizar_declaracion()]

            elif esEstructura(self.componente_actual):
                nodos_nuevos += [self.analizar_estructura()]

            elif esLlamadaFuncion(self.componente_actual, self.__ver_siguiente_componente()):
                nodos_nuevos += [self.analizar_llamada_funcion()]

            elif esAsignacion(self.componente_actual, self.__ver_siguiente_componente()):
                nodos_nuevos += [self.analizar_asignacion()]

            else:
                raise ErrorSintácticoJocotil("brotar", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)
        
        # Analizar la instrucción de retorno
        nodos_nuevos += [self.analizar_retorno()]

        self.verificar('}')

        return NodoArbol(TipoNodo.FUNCION, nodos=nodos_nuevos, contenido=nombreFuncion, linea=linea_funcion)



    def analizar_llamada_funcion(self):
        """
            Llamada_funcion ::= Identificador "(" (Termino)? | (Termino ("," Termino)+ ")" ;
        Flujo:
        1. Captura el nombre (identificador).
        2. Consigue el paréntesis de apertura.
        3. Si hay argumentos, analiza uno o varios términos separados por comas.
        4. Cierra el paréntesis y retorna un nodo LLAMADA_FUNCION.
        """

        linea_llamada_funcion = self.componente_actual.linea if self.componente_actual else None

        nodos_nuevos = []

        nombreFuncion = ""
        if esIdentificador(self.componente_actual):    
            nombreFuncion = self.componente_actual.texto
            self.siguiente()
        else:
            raise ErrorSintácticoJocotil("identificador", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)
        
        self.verificar('(')
        # Si no es paréntesis de cierre, procesar argumentos
        if (self.componente_actual.texto != ')'):
    
            if esTermino(self.componente_actual, self.__ver_siguiente_componente()):
                nodos_nuevos += [self.analizar_termino()]
            else:
                raise ErrorSintácticoJocotil("termino", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)
            
            # Más argumentos separados por comas
            while self.componente_actual:
                if self.componente_actual.texto != ',':
                    break

                self.verificar(',')

                if esTermino(self.componente_actual, self.__ver_siguiente_componente()):
                    nodos_nuevos += [self.analizar_termino()]
                else:
                    raise ErrorSintácticoJocotil("termino", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        self.verificar(')')

        return NodoArbol(TipoNodo.LLAMADA_FUNCION, nodos=nodos_nuevos, contenido=nombreFuncion, linea=linea_llamada_funcion)
    


    def analizar_parametros(self):
        """
            Parametros ::= ("jocote" | "cele" | "fibra") Identificador ( "," ("jocote" | "cele" | "fibra") Identificador ) * ;
        Flujo:
        1. Para cada par tipo/nombre, crea un subnodo.
        2. Si hay comas, repite el proceso.
        3. Retorna un nodo PARAMETROS con todos los pares.
        """

        linea_parametros = self.componente_actual.linea if self.componente_actual else None

        nodos_nuevos=[]

        #Componente actual: "jocote" | "cele" | "fibra"
        if esDeclaración(self.componente_actual):
            nodos_nuevos += [NodoArbol(TipoNodo.PALABRA_CLAVE, contenido=self.componente_actual.texto, linea=self.componente_actual.linea)]
            self.siguiente()
        else:
            raise ErrorSintácticoJocotil("declaración", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        #Componente actual: Identificador
        if esIdentificador(self.componente_actual):
            nodos_nuevos+= [self.analizar_identificador()]
        else:
            raise ErrorSintácticoJocotil("identificador", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        # Parámetros adicionales separados por comas
        while self.componente_actual:
            if self.componente_actual.texto != ',':
                break

            # Componente actual: ","
            self.verificar(',')

            #Componente actual: "jocote" | "cele" | "fibra"
            if esDeclaración(self.componente_actual):
                nodos_nuevos += [NodoArbol(TipoNodo.PALABRA_CLAVE, contenido=self.componente_actual.texto, linea=self.componente_actual.linea)]
                self.siguiente()
            else:
                raise ErrorSintácticoJocotil("declaración", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)
            
            if esIdentificador(self.componente_actual):
                nodos_nuevos += [self.analizar_identificador()]
            else:
                raise ErrorSintácticoJocotil("identificador", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        return NodoArbol(TipoNodo.PARAMETROS, nodos=nodos_nuevos, linea=linea_parametros)
    


    def analizar_estructura(self):
        """
            Estructura ::= Estructura_control | Bucle ;
        - Si ve 'qtmeten', delega a analizar_estructura_control (if/elif/else).
        - Si ve 'madurar' o 'cosechar', llama a analizar_bucle.
        - En caso contrario, lanza un error.
        """

        linea_estructura = self.componente_actual.linea if self.componente_actual else None

        nodos_nuevos = []

        if self.componente_actual.texto == "qtmeten":
            nodos_nuevos += [self.analizar_estructura_control()]

        elif self.componente_actual.texto == "madurar" or self.componente_actual.texto == "cosechar":
            nodos_nuevos += [self.analizar_bucle()]

        else:      
            raise ErrorSintácticoJocotil("qtmeten | madurar | cosechar", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        return NodoArbol(TipoNodo.ESTRUCTURA, nodos=nodos_nuevos, linea=linea_estructura)



    def analizar_estructura_control(self):
        """
            Estructura_control ::=  "qtmeten" "(" Expresion ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}" 
                                    ("qmas" "(" Expresion ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}")*
                                    ("qno" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}")? ;
        """

        linea_estructura_control = self.componente_actual.linea if self.componente_actual else None

        nodos_nuevos = [] # Lista donde iremos acumulando los nodos hijos de la estructura de control

        # --- Manejo de la rama "qtmeten" (equivalente a un if) ---
        if (self.componente_actual.texto == "qtmeten"):
            linea_qtmeten = self.componente_actual.linea if self.componente_actual else None
            nodos_qtmeten = []

            self.siguiente() # qtemeten
            self.verificar('(')

            nodos_qtmeten += [self.analizar_expresion()]

            self.verificar(')') 

            self.verificar('{')

            # Procesamos todas las sentencias dentro de las llaves
            while self.componente_actual:
                if (self.componente_actual.texto == '}'):
                    break

                if esDeclaración(self.componente_actual):
                    nodos_qtmeten += [self.analizar_declaracion()]

                elif esEstructura(self.componente_actual):
                    nodos_qtmeten += [self.analizar_estructura()]

                elif esLlamadaFuncion(self.componente_actual, self.__ver_siguiente_componente()):
                    nodos_qtmeten += [self.analizar_llamada_funcion()]

                elif esAsignacion(self.componente_actual, self.__ver_siguiente_componente()):
                    nodos_qtmeten += [self.analizar_asignacion()]

                else:
                    raise ErrorSintácticoJocotil("}", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)
            
            self.verificar('}')
            nodos_nuevos += [NodoArbol(TipoNodo.PALABRA_CLAVE, contenido="qtmeten", nodos=nodos_qtmeten, linea=linea_qtmeten)]
        
        # --- Manejo de las ramas "qmas" (equivalentes a else-if), pueden repetirse ---
        while (self.componente_actual.texto == "qmas"):
            linea_qmas = self.componente_actual.linea if self.componente_actual else None
            nodos_qmas = []

            self.siguiente() # qmas
            self.verificar('(')

            nodos_qmas += [self.analizar_expresion()]

            self.verificar(')')

            self.verificar('{')

            # Igual que antes, procesamos declaraciones, estructuras, llamadas o asignaciones
            while self.componente_actual:
                if (self.componente_actual.texto == '}'):
                    break

                if esDeclaración(self.componente_actual):
                    nodos_qmas += [self.analizar_declaracion()]

                elif esEstructura(self.componente_actual):
                    nodos_qmas += [self.analizar_estructura()]

                elif esLlamadaFuncion(self.componente_actual, self.__ver_siguiente_componente()):
                    nodos_qmas += [self.analizar_llamada_funcion()]
                    
                elif esAsignacion(self.componente_actual, self.__ver_siguiente_componente()):
                    nodos_qmas += [self.analizar_asignacion()]

                else:
                    raise ErrorSintácticoJocotil("}", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)
            
            self.verificar('}')
            nodos_nuevos += [NodoArbol(TipoNodo.PALABRA_CLAVE, contenido="qmas", nodos=nodos_qmas, linea=linea_qmas)]

        # --- Manejo opcional de la rama "qno" (equivalente a else) ---
        if (self.componente_actual.texto == "qno"):
            linea_qno = self.componente_actual.linea if self.componente_actual else None
            nodos_qno = []

            self.siguiente() # qno

            self.verificar('{')

            while self.componente_actual:
                if (self.componente_actual.texto == '}'):
                    break

                if esDeclaración(self.componente_actual):
                    nodos_qno += [self.analizar_declaracion()]

                elif esEstructura(self.componente_actual):
                    nodos_qno += [self.analizar_estructura()]

                elif esLlamadaFuncion(self.componente_actual, self.__ver_siguiente_componente()):
                    nodos_qno += [self.analizar_llamada_funcion()]

                elif esAsignacion(self.componente_actual, self.__ver_siguiente_componente()):
                    nodos_qno += [self.analizar_asignacion()]

                else:
                    raise ErrorSintácticoJocotil("}", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)
            
            self.verificar('}')
            nodos_nuevos += [NodoArbol(TipoNodo.PALABRA_CLAVE, contenido="qno", nodos=nodos_qno, linea=linea_qno)]

        # Finalmente, envolvemos todas las partes en un nodo de estructura de control
        return NodoArbol(TipoNodo.ESTRUCTURA_CONTROL, nodos=nodos_nuevos, linea=linea_estructura_control)



    def analizar_bucle(self):
        """
            Analiza un bucle en el lenguaje Jocotil, que puede ser de dos tipos:
    
            1. madurar(Expresion) { … }
            2. cosechar Identificador en(Identificador) { … }

            Bucle ::=   ("madurar" "(" Expresion ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}")
                        | ("cosechar" Identificador "en" "(" Identificador ")" "{" (Declaracion | Asignacion | Estructura | Comentario | Llamada_funcion)+ "}") ;
            
            Flujo:
                - Si es 'madurar': consume la condición (expresión) entre paréntesis.
                - Si es 'cosechar': lee la variable de iteración, consume 'en' y el identificador del contenedor.
                - En ambos casos, abre el bloque con '{' y procesa todas las sentencias internas.
                - Cierra el bloque con '}' y retorna un nodo BUCLE indicando el tipo.
        """

        linea_bucle = self.componente_actual.linea if self.componente_actual else None

        nodos_nuevos = []

        nombre = ""
        # Diferenciar tipo de bucle
        if self.componente_actual.texto == "madurar":
            nombre = "madurar"
            self.siguiente() 

            self.verificar("(")

            nodos_nuevos += [self.analizar_expresion()]

            self.verificar(')') 

            self.verificar('{') 
            
        elif self.componente_actual.texto == "cosechar":
            nombre = "cosechar"
            self.siguiente()

            if esIdentificador(self.componente_actual):
                nodos_nuevos += [self.analizar_identificador()]
            else:
                raise ErrorSintácticoJocotil("identificador", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

            self.verificar('en')

            self.verificar('(') 

            # Leer identificador del iterable
            if esIdentificador(self.componente_actual):
                nodos_nuevos += [self.analizar_identificador()]
            else:
                raise ErrorSintácticoJocotil("identificador", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

            self.verificar(')')

            self.verificar('{')

        else:
            raise ErrorSintácticoJocotil("madurar | cosechar", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        # Procesar el cuerpo del bucle
        while self.componente_actual:
            if (self.componente_actual.texto == '}'):
                break

            if esDeclaración(self.componente_actual):
                nodos_nuevos += [self.analizar_declaracion()]

            elif esEstructura(self.componente_actual):
                nodos_nuevos += [self.analizar_estructura()]

            elif esLlamadaFuncion(self.componente_actual, self.__ver_siguiente_componente()):
                nodos_nuevos += [self.analizar_llamada_funcion()]

            elif esAsignacion(self.componente_actual, self.__ver_siguiente_componente()):
                nodos_nuevos += [self.analizar_asignacion()]

            else:
                raise ErrorSintácticoJocotil("}", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        self.verificar('}')
        # Devolver nodo BUCLE con nombre ('madurar' o 'cosechar') y contenido
        return NodoArbol(TipoNodo.BUCLE, nodos=nodos_nuevos, contenido=nombre, linea=linea_bucle)



    def analizar_retorno(self):
        """
            Analiza la instrucción de retorno en una función.

            Retorno ::= "brotar" Expresion ;
            
            Flujo:
            - Verifica y consume la palabra clave 'brotar'.
            - Analiza la expresión cuyo valor se retorna.
            - Retorna un nodo RETORNO con el subnodo de la expresión.
        """

        linea_retorno = self.componente_actual.linea if self.componente_actual else None

        nodos_nuevos = []

        self.verificar('brotar')

        nodos_nuevos += [self.analizar_expresion()] # Analizar valor de retorno

        return NodoArbol(TipoNodo.RETORNO, nodos=nodos_nuevos, linea=linea_retorno)
    


    def analizar_numero(self):
        """
            Numero ::= ("-"? Digit+ "." Digit+ | "-"? Digit+) ; 
            Flujo:
                - Comprueba que el token actual sea ENTERO o FLOTANTE.
                - Lo consume y devuelve un nodo NUMERO con su texto.
        """

        linea_numero = self.componente_actual.linea if self.componente_actual else None

        if self.componente_actual.tipo != TipoComponente.ENTERO and self.componente_actual.tipo != TipoComponente.FLOTANTE:
            raise ErrorSintácticoJocotil("numero", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        componente = self.componente_actual
        self.siguiente()

        return NodoArbol(TipoNodo.NUMERO, contenido=componente.texto, linea=linea_numero)



    def analizar_string(self):
        """
            String ::= "θ" cualquier_caracter+ "θ"| "ω" cualquier_caracter+ "ω" ; 
            Flujo:
                - Comprueba que el token actual sea de tipo TEXTO.
                - Lo consume y devuelve un nodo STRING con el contenido.
        """

        linea_string = self.componente_actual.linea if self.componente_actual else None

        if self.componente_actual.tipo != TipoComponente.TEXTO:
            raise ErrorSintácticoJocotil("string", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        componente = self.componente_actual
        self.siguiente()

        return NodoArbol(TipoNodo.STRING, contenido=componente.texto, linea=linea_string)
    


    def analizar_identificador(self):
        """
            Analiza un identificador de variable o función.

            - Verifica que el token actual sea IDENTIFICADOR.
            - Lo consume y devuelve un nodo IDENTIFICADOR con su nombre.
        """

        linea_identificador = self.componente_actual.linea if self.componente_actual else None

        if (self.componente_actual.tipo != TipoComponente.IDENTIFICADOR):
            raise ErrorSintácticoJocotil("identificador", self.componente_actual.texto, self.componente_actual.linea, self.componente_actual.columna)

        componente = self.componente_actual
        self.siguiente()
        
        return NodoArbol(TipoNodo.IDENTIFICADOR, contenido=componente.texto, linea=linea_identificador)