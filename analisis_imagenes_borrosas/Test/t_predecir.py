import pytest
import sys     

root_path = "../analisis_imagenes_borrosas/"

# inserting the mod.py directory at

# position 1 in sys.path
sys.path.insert(1, root_path)

from SRC.config import logeo
from SRC.training import escribir_modelo
from SRC.training import modelado
from SRC.training import entrenamiento
from SRC.predecir import predecir



def test_predecir_1():
    with pytest.raises(Exception) as e_info:
        predecir("Modelos/modelo_2023-04-27194035", "archivonoexiste")

def test_predecir_2():
    with pytest.raises(Exception) as e_info:
        predecir("Modelonoexiste", "0_IPHONE-SE_M.JPG")
