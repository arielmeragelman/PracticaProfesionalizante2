import pytest
import sys       
import os
import random
import shutil


root_path = "../analisis_imagenes_borrosas/"

# inserting the mod.py directory at
# position 1 in sys.path
sys.path.insert(1, root_path)

from SRC.config import logeo
from SRC.training import escribir_modelo
from SRC.training import modelado
from SRC.training import entrenamiento


def main():

    from SRC.config import logeo
    from SRC.training import escribir_modelo
    from SRC.training import modelado
    from SRC.training import entrenamiento
    import tensorflow as tf
  
    path=r""
    proceso, resultados = logeo()

    # Definicion de directorios de entrenamiento y testeos

    ENTRENAMIENTO = path + r"Entrenamiento/train"
    TESTING = path + r"Entrenamiento/test"
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
    # Montamos la carpeta del drive donde tenemos el dataset
    # En caso de que se modifique la ubicación del dataset debera modificarse este paso
  
    # Defino ubicación del dataset montado
    path_dataset = path+r"Dataset/"
    path_entrenamiento= path+r'Entrenamiento'
    listImage = []
    # Listamos todas las imagenes que estan "bien" en el folder de sharp
    for i in os.listdir(path_dataset):
          if i=="sharp" or i=="blur_dataset_scaled":
            continue
        for j in os.listdir(path_dataset+"/"+i):
            try:
                if j.split(".")[1]!="JPG" and j.split(".")[1]!="jpg" and j.split(".")[1]!="jpeg":
                pass
            except:
                pass
            # Creamos una lista con el nombre/path de las imagenes que estan "bien"        
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
            shutil.copyfile(i, path_entrenamiento+r"/train/blurImage/"+image_name)
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
        if i!="sharp":
            continue
        for j in os.listdir(path_dataset+"/"+i):
            try:
                if j.split(".")[1]!="JPG" and j.split(".")[1]!="jpg" and j.split(".")[1]!="jpeg":
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
            shutil.copyfile(i, path_entrenamiento+r"/train/sharpImage/"+image_name)
        except:
            pass
            
    # copiamos en la carpeta de testing de imagenes correctas
    for i in test_sharp:
        image_name = i.split("/")
        image_name = image_name[len(image_name)-1]
        try:
            shutil.copyfile(i, path_entrenamiento+r"/test/sharpImage/"+image_name)
        except:
            pass
            


    model, train_generator, val_generator = modelado(IMAGE_SIZE=600, BATCH_SIZE=32, filters=32, kernel_size=3, activation='relu', units=2)
    modelo=entrenamiento(model, train_generator, val_generator, epochs=2)
    escribir_modelo(model, path+r"Modelos/Test")
    return modelo

def test_integracioncompleta():
    modelo=main()
    assert(modelo.layers[1].get_config()['filters']==32) and \
    (modelo.layers[1].get_config()['kernel_size']==(3, 3)) and \
    (modelo.layers[1].get_config()['name']=='conv2d') and \
    (modelo.layers[1].get_config()['activation']=='relu') and \
    (modelo.layers[4].get_config()['units']==2)
  
