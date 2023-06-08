import pytest
import sys     
import imghdr
import os

root_path = "../analisis_imagenes_borrosas/"

# inserting the mod.py directory at
# position 1 in sys.path
sys.path.insert(1, root_path)


def test_validararchivos():
    # Validamos que todos los archivos de entrenamiento sean imagenes
    for i in os.listdir("Dataset/sharp/"):
        assert (imghdr.what('/Dataset/sharp/'+i) == "jpeg")
