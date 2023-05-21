def logeo():
    # Funcion para generar los objetos de logging
    import logging
    import os
    # Defino el path donde se realizara el log
    
    absolute_path = os.path.dirname(__file__)
    relative_path = "../"
    full_path = os.path.join(absolute_path, relative_path) 
    
    path = full_path+"/Log/"
    proceso = logging.getLogger('proceso')
    resultados = logging.getLogger('resultado')
    proceso.setLevel(logging.DEBUG)
    resultados.setLevel(logging.DEBUG)

    # Definimos los handlers
    c_handler = logging.FileHandler(path+'proceso_entrenar.log')
    f_handler = logging.FileHandler(path+'resultados.log')

    # Definimos los formatters y los agregamos a los handlers
    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    resultados.addHandler(c_handler)
    proceso.addHandler(f_handler)
    return (proceso, resultados)


def limpiar(folder: str) -> None:
    # Funcion para eliminar archivos que no se deban usar
    import os
    import glob
    files = glob.glob(folder + "/*.jpg")
    for f in files:
        os.remove(f)
