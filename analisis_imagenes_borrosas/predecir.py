from SRC.config import logeo
from SRC.predecir import predecir
import os
from pathlib import Path
import random
import shutil
import logging
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt


modelo = "Modelos/Main"
archivo = "0_IPHONE-SE_M.JPG"
predecir(modelo, archivo)
