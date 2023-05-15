import pytest
import sys       

root_path = "analisis_imagenes_borrosas/"

# inserting the mod.py directory at
# position 1 in sys.path
sys.path.insert(1, root_path)

from SRC.config import logeo
from SRC.training import escribir_modelo
from SRC.training import modelado
from SRC.training import entrenamiento


def test_logeo_1():
    b, a = logeo()
    b.error("TEST DE TESTING resultado")
    with open(root_path+'Log/resultados.log', 'r') as f:
        last_line = f.readlines()[-1]
    assert last_line[-26:] == "TEST DE TESTING resultado\n"


def test_logeo_2():
    b, a = logeo()
    a.error("TEST DE TESTING proceso")
    with open(root_path+'Log/proceso_entrenar.log', 'r') as f:
        last_line = f.readlines()[-1]
    assert last_line[-24:] == "TEST DE TESTING proceso\n"

def test_entreno_1():
    with pytest.raises(Exception) as e_info:
        escribir_modelo("archivonovalido", "testing")


def test_modelado_1():
    with pytest.raises(Exception) as e_info:
        modelado(IMAGE_SIZE=0, BATCH_SIZE=32, filters=32, kernel_size=3, activation='relu', units=2)

def test_modelado_2():
    with pytest.raises(Exception) as e_info:
        modelado(IMAGE_SIZE=10000, BATCH_SIZE=32, filters=32, kernel_size=3, activation='relu', units=2)

def test_modelado_3():
    with pytest.raises(Exception) as e_info:
        modelado(IMAGE_SIZE=600, BATCH_SIZE=0, filters=32, kernel_size=3, activation='relu', units=2)

def test_modelado_4():
    with pytest.raises(Exception) as e_info:
        modelado(IMAGE_SIZE=600, BATCH_SIZE=1000, filters=32, kernel_size=3, activation='relu', units=2)

def test_modelado_5():
    with pytest.raises(Exception) as e_info:
        modelado(IMAGE_SIZE=600, BATCH_SIZE=32, filters=0, kernel_size=3, activation='relu', units=2)

def test_modelado_6():
    with pytest.raises(Exception) as e_info:
        modelado(IMAGE_SIZE=600, BATCH_SIZE=32, filters=32, kernel_size=-1, activation='relu', units=2)

def test_modelado_7():
    with pytest.raises(Exception) as e_info:
        modelado(IMAGE_SIZE=600, BATCH_SIZE=32, filters=32, kernel_size=3, activation=22, units=2)

def test_modelado_7():
    with pytest.raises(Exception) as e_info:
        modelado(IMAGE_SIZE=600, BATCH_SIZE=32, filters=32, kernel_size=3, activation='relu', units=0)
