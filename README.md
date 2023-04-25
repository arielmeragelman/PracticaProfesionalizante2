# PracticaProfesionalizante2
Grupo para ejercicios de practica profesionalizante 2

Proyecto:
Desarrollo de un sistema de deteccion de imágenes borrosas/fuera de foco .

Objetivo: desarrollar un sistema que permita detectar de forma automatica que imágenes son borrosas o fuera de foco, para esto contara con un threshold que se definira y una carpeta de archivos de imágenes para analizar

Metodo: se desarrollara un sistema de IA que pueda determinar el porcentaje de desenfoque que tiene una imagen y pueda clasificarla como borrosa o no. 

Para esto se realizarán investigaciones sobre trabajos relacionados, se evaluara su funcionalidad, ventaja y desventaja y se seleccionara un modelo a seguir.
Una vez definido el modelo se dejara registro en la wiki del notebook ejecutado con las pruebas y los resultados en la etapa de desarrollo para permitir futuros análisis. 
Se debera obtener y producir un set de datos/imagenes con sus labels correspondientes lo más amplio posible.
Una vez comprobado el modelo definitivo ,en el entorno de prueba , se migrara el notebook a una estructura de proyecto que permita su puesta en producción. Para esto se tomara en cuenta un diseño modular, con funciones atomicas , entorno de testing,  log de ejecucion, script de entrenamiento y script de prediccion. 



Dataset seleccionado para iniciar el proyecto:
https://www.kaggle.com/datasets/kwentar/blur-dataset


Contenido del Dataset

El dataset contiene 1050 imagenes divididas en grupos de 350 imagenes unicas (borrosas, movidas,correctas), las imagenes unicas estan repetidas para cada caso (movida,borrosa,correcta)

El dataset se utilizara para validar algoritmos de detección de imagenes borrosas.
El dataset no esta diseñado a partir de una transformación de "pixel-to-pixel", por lo que no es posible usar los analisis de PSNR ni SSIM

Estructura del dataset

El dataset contiene 3 carpetas sharp, defocused-blurred y motion-blurred
La estructura de nombres de los archivos es: id_device_type.extension donde:
ID - numero del 0 to 349;
device - que dispositivo saco la foto;
type - una letra entre : [S, F, M]. S  imagen correcta, F - imagen fuera de foco y M - imagen movida .
El dataset original puede descargarse sin ser escalado desde el google drive que provee el siguiente link
Fuente: https://www.kaggle.com/datasets/kwentar/blur-dataset
La version que utilizamos fue escalado previamente a nuestro uso a 2048px en el lado mas largo

