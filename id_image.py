import numpy as np
from skimage.transform import resize
import rawpy
from keras.models import Sequential
from keras.preprocessing import image
from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
from keras.layers.experimental.preprocessing import CenterCrop
from keras.layers.experimental.preprocessing import Rescaling

import matplotlib.pyplot as plt
from pathlib import Path

resnet = ResNet50(weights='imagenet')

def id_image(path):
    print(".. " + path)
    cropper = CenterCrop(height=2000, width=2000)
    if not Path(path).exists():
        return []
    if str(path).lower().endswith("nef") or str(path).lower().endswith("orf"): # 
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess()
    else:
        rgb = image.img_to_array(image.load_img(path))
        

    small = rgb

    small = resize(small,(224,224), preserve_range = True)
    small = np.expand_dims(small, axis = 0)

    small = preprocess_input(small)
    preds = resnet.predict(small)

    print('Predicted:', decode_predictions(preds, top=3)[0])
    
    return list(map(lambda a :  a[1] ,decode_predictions(preds, top=3)[0]))
