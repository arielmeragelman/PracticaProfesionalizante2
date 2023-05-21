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
    print("0000000000000000")
    print(filtros)
    print("0000000000000000")
    return (filtros,kernel,name,activation,units,full_data1,full_data2,full_data3)


parametros_modelo(r"analisis_imagenes_borrosas/Modelos/modelo_2023-05-20210236")

