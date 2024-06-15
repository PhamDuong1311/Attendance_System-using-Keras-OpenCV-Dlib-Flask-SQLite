from model import create_model
import numpy as np
from align import AlignDlib

nn4_small2_pretrained = create_model()
nn4_small2_pretrained.load_weights('models_weights_logo/nn4.small2.v1.h5')

alignment = AlignDlib('models_weights_logo/shape_predictor_68_face_landmarks.dat')
def align_image(img):
    return alignment.align(96, img, alignment.getLargestFaceBoundingBox(img),landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE) 
                           
def embedded(img):
    bounding_box = alignment.getLargestFaceBoundingBox(img)
    if bounding_box is None:
        return False
    img = align_image(img).astype(np.float32)
    img = (img / 255.).astype(np.float32)
    return nn4_small2_pretrained.predict(np.expand_dims(img, axis=0))[0]