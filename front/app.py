from flask import Flask
from flask import render_template, request , url_for
import requests


app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/modelos/<string:slug>/")
def mostrar_datos(slug):
    return "Mostrando datos del modelo {}".format(slug)



#########################

# Funciones adicionales
def listar_modelos():

    import os
    location='Modelos'


    absolute_path = os.path.dirname(__file__)
    relative_path = "../analisis_imagenes_borrosas/"+location
    full_path = os.path.join(absolute_path, relative_path)    

    modelos=[]
    
    for directorio in os.listdir(full_path):
        if directorio[-4]==".":
            pass

        else:
            modelos.append({'modelo':directorio})

    return modelos

#########################


@app.route("/")
def index():
    return render_template("index.html", num_posts=len(posts))
@app.route("/modelos/listar/")
def listado_modelos():
    lista=listar_modelos()
    return render_template("listar_modelos.html", lista=lista)

@app.route("/modelos/info/",methods=['GET', 'POST'])
def modeloinfo():
    import sys
    import pickle
    
    sys.path.append('../')
    from analisis_imagenes_borrosas.SRC.training import parametros_modelo
    import os
    modelo = request.form['comp_select']
    abs_path = os.path.dirname(__file__)
    rel_path = "../analisis_imagenes_borrosas/"
    ful_path = os.path.join(abs_path, rel_path)

    modelo = os.path.join(ful_path, "Modelos", modelo)

    print("se retornan datos del modelo")
    print(f"El modelo elegido es {modelo}")
    filtros, kernel, name, activation, units, full_data1, full_data2, full_data3 = parametros_modelo(modelo)
    # Cargar las variables desde el archivo
    with open(modelo+".pkl", 'rb') as archivo:
        back_modelo, loss, val_loss, acc, val_acc = pickle.load(archivo)       
    
    return render_template('parametros.html',filtros=filtros, kernel=kernel, name=name, activation=activation, units = units, full_data1 = full_data1, full_data2 = full_data2, full_data3 = full_data3, back_modelo=back_modelo, loss = loss, val_loss = val_loss, acc = acc, val_acc = val_acc)



@app.route("/modelos/entrenar/")
def entrenar_modelos():
    return render_template("entrenar_modelos.html")

@app.route("/modelos/datosentrenar/", methods=['GET', 'POST'])
def datosentrenar():
    import subprocess
    import os
    IMAGE_SIZE=request.form['IMAGE_SIZE']
    BATCH_SIZE=request.form['BATCH_SIZE']
    filters=request.form['filters']
    kernel_size=request.form['kernel_size']
    activation=request.form['activation']
    units=request.form['units']
    abs_path = os.path.dirname(__file__)
    rel_path = "../analisis_imagenes_borrosas/"
    ful_path = os.path.join(abs_path, rel_path)    
    print("se inicia datosentrenar")
    subprocess.call(['python', ful_path+'entrenar.py', str(IMAGE_SIZE), str(BATCH_SIZE), str(filters), str(kernel_size), str(activation), str(units)])
    
    return "<h1>Se entreno el modelo    </h1>"



@app.route("/predecir/")
def predecir_modelos():
    lista=listar_modelos()
    return render_template("predecir_modelos.html",lista=lista)

@app.route("/predecir/prediccion/", methods=['GET', 'POST'])
def datospredecir():
    import subprocess
    import os
    from pathlib import Path
    import sys
    sys.path.append('../')
    from analisis_imagenes_borrosas.SRC.predecir import predecir
    from analisis_imagenes_borrosas.SRC.config import logeo
    from analisis_imagenes_borrosas.SRC.manejo_imagen import control_contraste
    from analisis_imagenes_borrosas.SRC.manejo_imagen import dectectar_brillo

    proceso, resultados = logeo()

    modelo = request.form['pred_comp_select']
    abs_path2 = os.path.abspath(__file__)
    abs_path2 = Path(abs_path2)
    abs_path2 = abs_path2.parent.absolute()
    rel_path = "../analisis_imagenes_borrosas/"
    ful_path = os.path.join(abs_path2, rel_path)
    modelo = os.path.join(ful_path, "Modelos", modelo)

    if request.method == 'POST':
        imagen = request.files['uploaded-file']
        if imagen:
            if not os.path.exists(ful_path+'Predictor/'):
                os.mkdir(ful_path+'Predictor/')
                if not os.path.exists(ful_path+'Predictor/files'):
                    os.mkdir(ful_path+'Predictor/files')
                else:
                    print(f"el directorio {ful_path}+Predictor/files existe")
            else:
                print("Directorio existe")

            imagen.save(ful_path+'Predictor/files/' + imagen.filename)
            path_imagen = ful_path+'Predictor/files/'+imagen.filename

    print("se inicia datosentrenar")
    print(f"MODELO: {modelo}")
    
    contraste = control_contraste(path_imagen, 0.8)
    if contraste == 0:
        contraste_state = "Bajo Contraste"
    else:
        contraste_state = "Buen Contraste"
    brillo = dectectar_brillo(path_imagen, 55, 150)
    if brillo == 0:
        brillo_state = "Buena iluminación"
    elif brillo == -1:
        brillo_state = "Iluminación muy baja"
    else:
        brillo_state = "Iluminación muy alta"
    prediccion = predecir(modelo, path_imagen)
    
    if prediccion[0][0] > prediccion[0][1]:
        calidad = "Blur"
    else:
        calidad = "Sharp"

    
    return render_template('resultado_prediccion.html',archivo=imagen.filename,sharp=prediccion[0][0], blured=prediccion[0][1], resultado=calidad,brillo=brillo_state,contraste=contraste_state)


#########################


if __name__ == '__main__':
    app.run()