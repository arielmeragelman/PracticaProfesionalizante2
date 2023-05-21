from flask import Flask
from flask import render_template, request
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
       
    #return f"<h1>Se muestran los datos del modelo {filtros}   </h1>"
    return render_template('parametros.html',filtros=filtros, kernel=kernel, name=name, activation=activation, units = units, full_data1 = full_data1, full_data2 = full_data2, full_data3 = full_data3)



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

@app.route("/admin/post/")
@app.route("/admin/post/<int:post_id>/")
def post_form(post_id=None):
    return render_template("admin/post_form.html", post_id=post_id)

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    return render_template("signup_form.html")

def show_signup_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        next = request.args.get('next', None)
        if next:
            return redirect(next)
            print(f"Nombre: {name}")
        return redirect(url_for('index'))
    return render_template("signup_form.html")



#########################


if __name__ == '__main__':
    app.run()