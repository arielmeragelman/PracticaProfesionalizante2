def control_contraste(imagen,threshold):
  # Funcion para medir si el contraste de la imagen es suficiente
  import cv2
  from skimage.exposure import is_low_contrast

  img = cv2.imread(imagen)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
  if(is_low_contrast(gray,0.9)):
    return 0
  else:
    return 1


def dectectar_brillo(imagen,min_threshold,max_threshold):
  # Funcion para determinar si una imagen tiene la luminosidad correcta
  import cv2
  font = cv2.FONT_HERSHEY_SIMPLEX
  imagedark = cv2.imread(imagen)
  hsldark  = cv2.cvtColor(imagedark, cv2.COLOR_BGR2HLS)
  Lchanneld = hsldark[:,:,1]
  lvalueld =cv2.mean(Lchanneld)[0]
  if lvalueld < 100 :
    return -1
  elif lvalueld > 185 :
    return 1
  else:
    return 0