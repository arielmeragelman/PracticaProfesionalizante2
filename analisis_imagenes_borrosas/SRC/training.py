def escribir_modelo(model, nombre):

    import tensorflow as tf
    import os
    from SRC.config import logeo
    proceso, resultados = logeo()
    # Funcion para escribir el modelo en archivo
    print("tflite_model creado")
    print("EL tipo de modelo es:")
    print(type(model))

    absolute_path = os.path.dirname(__file__)
    relative_path = "../"+nombre
    full_path = os.path.join(absolute_path, relative_path) 
    print(f"se escribira el modelo en {full_path}")

    if model.layers[1].get_config():
        tf.keras.models.save_model(model, full_path)
    else:
        proceso.error(f'El modelo utilizado no es valido, es tipo: {type(model)}')
        raise Exception("La variable model no es un modelo valido")


def modelado(IMAGE_SIZE=600, BATCH_SIZE=32, filters=32, kernel_size=3, activation='relu', units=2):
    # Funcion para generar el modelo
    import os

    if ((IMAGE_SIZE < 100 or IMAGE_SIZE > 2000) or (BATCH_SIZE < 20 or BATCH_SIZE > 40) or (kernel_size < 1 or kernel_size > 10) or (units < 1 or units > 10) or activation.isalpha()!=True  ):
        raise Exception("Parametros invalidos")
    import tensorflow as tf
    from SRC.config import logeo
    proceso, resultados = logeo()
    # Generate batches of tensor image data with real-time data augmentation. - funcion antigua se debe evaluar reemplazar

    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255, 
        validation_split=0.2)
    '''
    Intentar entrenar el modelo requiere de mucha memoria que no tenemos, por lo que es necesario dividir el proceso de entrenamiento en bloques (o batchs, en inglés) de menor tamaño de imágenes.
    Para ello, Keras cuenta con la clase ImageDataGenerator, que nos permite generar dichos bloques, además de realizar la técnica llamada data augmentation.
    Data augmentation
    La idea es que, cuando se dispone de un número de imágenes relativamente pequeño, podemos aumentar el número modificando las imágenes originales (haciendo zoom, escalado, flip horizontal, etc) 
    Fuente: https://www.enmilocalfunciona.io/tratamiento-de-imagenes-usando-imagedatagenerator-en-keras/
    '''

    
    # toma los datos de ingreso de imagenes para el entrenamiento y genera un objeto iterable con los datos de las imagenes y el label correspondiente
    
    absolute_path = os.path.dirname(__file__)
    relative_path = "../"
    full_path = os.path.join(absolute_path, relative_path) 
    path = full_path

    train_generator = datagen.flow_from_directory(
        path+r"Entrenamiento/train",
        target_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=BATCH_SIZE,
        subset='training')

    # toma los datos de ingreso de imagenes para el testing y genera un objeto iterable con los datos de las imagenes y el label correspondiente
    val_generator = datagen.flow_from_directory(
        path+r"Entrenamiento/test",
        target_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=BATCH_SIZE,
        subset='validation')

    image_batch, label_batch = next(val_generator)
    proceso.debug('Se genero batch de archivos')
    resultados.info(f"PARAMETROS USADOS: IMAGE SIZE: {IMAGE_SIZE} - BATCH_SIZE: {BATCH_SIZE} - filters: {filters} - kernel_size: {kernel_size}  - activation: {activation} - units: {units}")
    IMG_SHAPE = (IMAGE_SIZE, IMAGE_SIZE, 3)

    # Creamos el modelo de base usando el pre-trained MobileNet V2
    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                   include_top=False,
                                                   weights='imagenet')
    base_model.trainable = False
    proceso.debug("base_model creado - base_model.trainable=False")
    # Esta funcion devolvera un modelo de Keras para clasificacion de imagenes
    '''
    It is one of the models that is used to investigate varied types of neural networks where the model gets in one input as feedback and expects an output as desired. The Keras API and library is incorporated with a sequential model to judge the entire simple model not the complex kind of model. It passes on the data and flows in sequential order from top to bottom approach till the data reaches at end of the model.
    Keras sequential class is one of the important class as part of the entire Keras sequential model. This class helps in creating a cluster where a cluster is formed with layers of information or data that flows with top to bottom approach having a lot of layers incorporated with tf.Keras. a model where most of its features are trained with algorithms that provide a lot of sequence to the model.
    '''

    # Se define el modelo propiamente dicho
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.Conv2D(filters, kernel_size, activation=activation),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(units=2, activation='softmax')
        ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    proceso.debug("Modelo generado - optimizer adam")
    resultados.info('Se genero el modelo con los datos:')
    resultados.info(str(model.summary()))
    return (model, train_generator, val_generator)


def entrenamiento(model, train_generator, val_generator, epochs=5):
    # Funcion para entrenar el modelo y medir los resultados

    import tensorflow as tf
    from SRC.config import logeo
    import matplotlib.pyplot as plt
    proceso, resultados = logeo()
    proceso.debug('Inicia el entrenamiento del modelo')
    epochs_valor = epochs
    resultados.info(f"Entenamiento con epochs: {epochs_valor}")

    if model.layers[1].get_config():
        pass
    else:
        proceso.error(f'El modelo utilizado no es valido, es tipo: {type(model)}')
        raise Exception("La variable model no es un modelo valido")

    try:
        history = model.fit(train_generator,
                            steps_per_epoch=len(train_generator),
                            epochs=epochs_valor,
                            validation_data=val_generator,
                            validation_steps=len(val_generator))
        proceso.debug('Termina el entrenamiento del modelo')
    except Exception as a:
        proceso.error(f'El modelo no se pudo entrenar correctamente {a}')
        raise Exception(a)
    proceso.debug("Inicia proceso de medicion del modelo")
    acc = history.history['accuracy']
    resultados.info(f'Accuracy: {acc}')
    val_acc = history.history['val_accuracy']
    resultados.info(f'Val Accuracy: {val_acc}')
    '''
    Una función de pérdida, o Loss function, es una función que evalúa la desviación entre las predicciones realizadas por la red neuronal y los valores reales de las observaciones utilizadas durante el aprendizaje. Cuanto menor es el resultado de esta función, más eficiente es la red neuronal
    '''
    loss = history.history['loss']
    resultados.info(f'Loss: {loss}')
    val_loss = history.history['val_loss']
    resultados.info(f'Val Loss: {val_loss}')

    plt.figure(figsize=(8, 8))
    plt.subplot(2, 1, 1)
    plt.plot(acc, label='Training Accuracy')
    plt.plot(val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.ylabel('Accuracy')
    plt.ylim([min(plt.ylim()),1])
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 1, 2)
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.ylabel('Cross Entropy')
    plt.ylim([0, 1.0])
    plt.title('Training and Validation Loss')
    plt.xlabel('epoch')
    plt.show()
    return (model,loss,val_loss,acc,val_acc)


def parametros_modelo(model):
    import tensorflow as tf
    import tensorflow_hub as hub
    modelo = tf.keras.models.load_model(model,
                                          custom_objects={'KerasLayer': hub.KerasLayer})
										  
    filtros = modelo.layers[1].get_config()['filters']
    kernel = modelo.layers[1].get_config()['kernel_size']
    name = modelo.layers[1].get_config()['name']
    activation = modelo.layers[1].get_config()['activation']
    units = modelo.layers[4].get_config()['units']										  
    full_data1 = modelo.layers[1].get_config()
    full_data2 = kernel=modelo.layers[2].get_config()
    full_data3 = kernel=modelo.layers[3].get_config()

    return (filtros,kernel,name,activation,units,full_data1,full_data2,full_data3)


def escribir_metricas(back_modelo, loss, val_loss, acc, val_acc):
    # Funcion para guardar los datos de las metricas del modelo

    import pickle

    print("valores que se guardaran:")
    print(" ")
    print(f" modelo: {back_modelo}   ")
    print(f" loss: {loss}   ")
    print(f" val_loss: {val_loss}   ")
    print(f" acc: {acc}   ")
    print(f" acc: {val_acc}   ")



    with open("../Modelos/"+back_modelo+'.pkl', 'wb') as archivo:
        pickle.dump((back_modelo, loss, val_loss, acc, val_acc), archivo)
    return 1