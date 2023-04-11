Este es el archivo Readme del ejercicio con CHATBOT

TAREA:
Implementar el chatbot en Google Colab.

Ejecutar el jupyter. Resolver y adaptar todo lo que se considere necesario.

Ejecutar Chattboter.py

Elaborar un informe de lo que funciona y no funciona y dejarlo en el Readme del repo.

----------------------INSTALACION LIBRERIAS-----------------------------

El primer paso que se realizo fue ejecutar el archivo chatterbot.py donde fallo en colab ya que estamos usando la libreria chatterbot sin que la misma fuera instalada ni figure entre los requirements para ejecutar el notebook
from chatterbot import ChatBot

Se puede buscar información de la libreria en la pagina: 
https://chatterbot.readthedocs.io/en/stable/

Siguiendo con los pasos del instructivo no se pudo hacer funcionar en colab la libreria de chattebot, por lo que encontramos el link
https://www.lawebdelprogramador.com/foros/Python/1772354-ChatterBot-con-Python-3.9.1-Error-en-la-instalacion.html

Que explica como instalar chatterbot mediante la instalación manual de determinadas librerias y con esto proceder a realizar la instalación de la libreria de chatterbot.
Siguiendo dichos pasos que pasamos a enumerar el entorno se ejecuto correctamente

"
mathparse>=0.1,<0.2
python-dateutil>=2.8,<2.9
sqlalchemy>=1.3,<1.4
pytz

Luego ejecute el comando: pip install chatterbot==1.0.4
"

En nuestro entorno esta recomendación se reprodujo asi:

!pip install mathparse
!pip install python-dateutil
!pip install "sqlalchemy==1.3.23"
!pip install pytz
!pip install chatterbot==1.0.4
----------------------------------------------

