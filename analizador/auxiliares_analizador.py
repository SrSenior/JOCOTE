from utils.jocoterrores import *
from analizador.asa import *
from explorador.explorador import *

def esDeclaración(componente: ComponenteLexico):
    """
        Función para validar si el texto de un componente léxico es jocote, cele o fibra 
    """
    if (componente):
        return (componente.texto in ["jocote", "cele", "fibra"])
    return False



def esEstructura(componente: ComponenteLexico):
    """
        Función para validar si el texto de un componente léxico es qtmeten, madurar o cosechar
    """
    if (componente):
        return (componente.texto in ["qtmeten", "madurar", "cosechar"])
    return False



def esFuncion(componente: ComponenteLexico):
    """
        Función para validar si el texto de un componente léxico es jocotazo 
    """
    if (componente):
        return (componente.texto == "jocotazo")
    return False



def esAsignacion(componente: ComponenteLexico, siguienteComponente: ComponenteLexico | None):
    """
        Función para validar si el tipo de un componente es identificador y si el siguiente es un =
    """
    if (siguienteComponente):
        if (componente):
            if (componente.tipo == TipoComponente.IDENTIFICADOR):
                if (siguienteComponente.texto == "="):
                    return True
    return False



def esLlamadaFuncion(componente: ComponenteLexico, siguienteComponente: ComponenteLexico | None):
    """
        Función para validar si el tipo de un componente es identificador y si el siguiente es un (
    """
    if (siguienteComponente):
        if (componente):
            if (componente.tipo == TipoComponente.IDENTIFICADOR):
                if (siguienteComponente.texto == "("):
                    return True
    return False



def esIdentificador(componente: ComponenteLexico):
    """
        Función para validar si el tipo de un componente es identificador
    """
    if (componente):
        return (componente.tipo == TipoComponente.IDENTIFICADOR)
    return False



def esNumero(componente: ComponenteLexico):
    """
        Función para validar si el tipo de un componente es entero o flotante
    """
    if (componente):
        return (componente.tipo == TipoComponente.ENTERO or componente.tipo == TipoComponente.FLOTANTE)
    return False



def esString(componente: ComponenteLexico):
    """
        Función para validar si el tipo de un componente es string
    """
    if (componente):
        return (componente.tipo == TipoComponente.TEXTO)
    return False



def esTermino(componente: ComponenteLexico, siguienteComponente: ComponenteLexico | None):
    """
        Función para validar si el tipo de un componente es identificador, entero, flotante, string o si es una llamada a funcion
    """
    if (componente):
        if esString(componente):
            return True
        elif esNumero(componente):
            return True
        elif esLlamadaFuncion(componente, siguienteComponente):
            return True
        elif esIdentificador(componente):
            return True
    return False



def esOperador(componente: ComponenteLexico):
    """
        Función para validar si el texto de un componente léxico es uno de los siguientes: "apiar", "comer", "sembrar", "morder", "semilla", "<", "<=", ">", ">=", "==", "!=", "="
    """
    if (componente):
        return (componente.texto in ["apiar", "comer", "sembrar", "morder", "semilla", "<", "<=", ">", ">=", "==", "!="])
    return False