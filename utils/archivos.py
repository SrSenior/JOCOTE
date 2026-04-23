# Utilitarios para el manejo de archivos

def cargar_archivo(ruta_archivo):
    """
        Carga un archivo y lo retorna cómo un solo string pero línea por línea
        en caso de que el archivo sea muy grande.
        :param ruta_archivo: Ruta del archivo a cargar
        :return: Generador que retorna cada línea del archivo
        !FUNCION CUIDADOSAMENTE ROBADA DEL TODO PODEROSO AURELIO!
        !PROFE SI LEE ESTO, HOLA!
    """
    
    with open(ruta_archivo, encoding="utf-8") as archivo:
        for linea in archivo:
            yield linea.strip("\n")



def crear_archivo(ruta_archivo, contenido):
    """
        Crea un archivo en la ruta especificada con el contenido dado.
        :param ruta_archivo: Ruta del archivo a crear
        :param contenido: Contenido del archivo
    """
    
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)