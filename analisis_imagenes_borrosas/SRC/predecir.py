def predecir(model, archivo):
    # Funcion para predecir si una imagen es borrosa segun un determinado modelo
    
    import tensorflow as tf
    import tensorflow_hub as hub
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    from tensorflow.keras.preprocessing import image
    from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
    #from SRC.config import logeo

    #proceso, resultados = logeo()

    # ETAPA DE PREDICCION
    # Basado en : https://towardsdatascience.com/how-to-predict-an-image-with-keras-ca97d9cd4817
    
    modelado = tf.keras.models.load_model(model,
                                          custom_objects={'KerasLayer': hub.KerasLayer})
    #path = "Predictor/files/"

    if modelado.layers[1].get_config():
        pass
    else:
        proceso.error(f'El modelo utilizado no es valido, es tipo: {type(modelado)}')
        raise Exception("La variable model no es un modelo valido")


    # Creamos el directorio donde se va a montar las imagenes
    # En esta seccion se debe programar la subida de la imagen (o las imagenes)
    #try:
    #    os.mkdir(path)
    #except:
    #    print("Directorios ya existen")

    # imagen a validar
    #img_path = path + archivo
    # Reescala de imagen
    try:
        img = image.load_img(archivo, target_size=(600, 600))
    except:
        raise Exception("Archivo no existe")

    # Convertimos la imagen en un array de datos
    img_array = image.img_to_array(img)
    # Expandimos las dimensiones ya que es un requerimiento de tensorflow
    img_batch = np.expand_dims(img_array, axis=0)
    img_preprocessed = preprocess_input(img_batch)
    # prediccion propíamente dicha
    prediccion = modelado.predict(img_preprocessed)

    #plt.imshow(img)
    #plt.show()
    print(f"EL VALOR PREDICHO ES: {prediccion}")

    if prediccion[0][0] > prediccion[0][1]:
        print("Label : blur")

    else:
        print("Label : sharp")

    return (prediccion)

