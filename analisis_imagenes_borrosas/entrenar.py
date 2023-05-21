# Importamos librerias
import shutil
import os
import sys
from pathlib import Path
import random
import numpy as np
from datetime import datetime
import tensorflow as tf
import tensorflow as tf
import matplotlib.pyplot as plt

from SRC.config import logeo
from SRC.config import limpiar
from SRC.training import escribir_modelo
from SRC.training import modelado
from SRC.training import entrenamiento
from SRC.training import escribir_metricas

def main(IMAGE_SIZE, BATCH_SIZE, filters, kernel_size, activation, units):
    # Funcion para ejecutar el proceso de cargado de imagenes para su entrenamiento  
    
    
    
    absolute_path = os.path.dirname(__file__)
    path=absolute_path+"/"
    
    proceso, resultados = logeo()

    # Definicion de directorios de entrenamiento y testeos
    ENTRENAMIENTO = path+r"Entrenamiento/train"
    TESTING = path+r"Entrenamiento/test"
    try:
        os.mkdir(ENTRENAMIENTO)
        os.mkdir(TESTING)
        os.mkdir(ENTRENAMIENTO+"/blurImage")
        os.mkdir(ENTRENAMIENTO+"/sharpImage")
        os.mkdir(TESTING+"/blurImage")
        os.mkdir(TESTING+"/sharpImage")
        proceso.info('Se crearon directorios - estructura de archivos no existia')
    except:
        print("Directorios ya existen")
    # En caso de que se modifique la ubicación del dataset debera modificarse este paso
    # Defino ubicación del dataset montado
    path_dataset = path+r"Dataset/"
    path_entrenamiento = path+r'Entrenamiento'
    listImage = []
    # Limpiamos los directorios de entrenamiento antes de comenzar las copias
    limpiar(ENTRENAMIENTO+"/blurImage")
    limpiar(ENTRENAMIENTO+"/sharpImage")
    limpiar(TESTING+"/blurImage")
    limpiar(TESTING+"/sharpImage")

    # Listamos todas las imagenes que estan "bien" en el folder de sharp
    for i in os.listdir(path_dataset):
        if i == "sharp" or i == "blur_dataset_scaled":
            continue
        for j in os.listdir(path_dataset+"/"+i):
            try:
                if j.split(".")[1] != "JPG" and j.split(".")[1] != "jpg" and j.split(".")[1] != "jpeg":
                    pass
            except:
                pass
            # Creamos una lista con el nombre/path de las imagenes"       
            listImage.append(path_dataset+"/"+i+"/"+j)
    # Reordenamos al azar dentro del array los nombres de archivos
    random.shuffle(listImage)
    # Separamos los nombres de archivos en 2 grupos (testeo y train)
    train_blur = listImage[0:500]
    resultados.debug(f'Se creo lista de archivos, train: {len(train_blur)}')
    test_blur = listImage[600:]
    resultados.debug(f'Se creo lista de archivos, test: {len(test_blur)}')
    # Listamos todas las imagenes que estan "mal" en el folder de blur
    for i in train_blur:
        image_name = i.split("/")
        image_name = image_name[len(image_name)-1]
        try:
            # copiamos las imagenes de entrenamiento borrosas
            shutil.copyfile(i, path_entrenamiento+r"/train/blurImage/" + image_name)
        except:
            pass
    # Copiamos los archivos que estan "mal" para testeo en otra carpeta
    for i in test_blur:
        image_name = i.split("/")
        image_name = image_name[len(image_name)-1]
        shutil.copyfile(i, path_entrenamiento+r"/test/blurImage/"+image_name)
    # Creamos una lista de imagenes "correctas"
    listImage = []
    for i in os.listdir(path_dataset):
        if i != "sharp":
            continue
        for j in os.listdir(path_dataset+"/"+i):
            try:
                if j.split(".")[1] != "JPG" and j.split(".")[1] != "jpg" and j.split(".")[1] != "jpeg":
                    pass
            except:
                pass
            listImage.append(path_dataset+"/"+i+"/"+j)
    # Reordenamos la lista de imagenes de forma que sea aleatorea su distribución
    random.shuffle(listImage)
    train_sharp = listImage[0:300]
    test_sharp = listImage[300:]
    # copiamos en la carpeta de entrenamiento de imagenes correctas
    for i in train_sharp:
        image_name = i.split("/")
        image_name = image_name[len(image_name)-1]
        try:
            shutil.copyfile(i, path_entrenamiento+r"/train/sharpImage/" + image_name)
        except:
            print(f"problema para copiar {image_name}")
            pass
    # copiamos en la carpeta de testing de imagenes correctas
    for i in test_sharp:
        image_name = i.split("/")
        image_name = image_name[len(image_name)-1]
        try:
            shutil.copyfile(i, path_entrenamiento+r"/test/sharpImage/"+image_name)
        except:
            print(f"problema para copiar {image_name}")
            pass

    model, train_generator, val_generator = modelado(IMAGE_SIZE, BATCH_SIZE, filters, kernel_size, activation, units)
    modelo, loss, val_loss, acc, val_acc = entrenamiento(model, train_generator, val_generator, epochs=2)
    escribir_modelo(model, path+r"Modelos/Main")
    # Guardamos un backup del modelo entrenado
    now = datetime.now()
    now = str(now).replace(" ", "").replace(":", "")[:16]

    proceso, resultados = logeo()

    try:
        back_modelo = "Modelos/modelo_"+now
        escribir_modelo(modelo, back_modelo)
        escribir_metricas(back_modelo, loss, val_loss, acc, val_acc)
        proceso.info(f'Se escribio el backup del modelo en: Modelos/modelo_{now}')
    except Exception as a:
        proceso.error(f'No se pudo crear el backup del modelo en: Modelos/modelo_{now}')
        proceso.error(f'No se pudo crear el backup del modelo Error: {a}')
    
    return modelo


# INICIA PROCESO DE EJECUCION DEL ENTRENAMIENTO

modelo = main(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))


