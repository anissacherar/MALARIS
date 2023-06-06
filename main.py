import cv2
import numpy as np
import tensorflow as tf
from scipy import ndimage
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from skimage.morphology import area_opening, area_closing
from keras.preprocessing import image as imp
import matplotlib.pyplot as plt
import time


"""Load a pre-trained model"""
def load_model(model):
    model = tf.keras.models.load_model(model)
    return model


"""Function to subtract the background of an image"""
def background_subtract_area(image, area_threshold=7000, light_bg=True):
    #  default area_threshold is similar to the area of a disk with radius 50, which is ImageJ's default
    if light_bg:
        return area_closing(image, area_threshold) - image
    else:
        return image - area_opening(image, area_threshold)
    
    
"""Function to predict if an image is positive or negative"""
def posouneg(img,model):       
    img_r = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    img_r = imp.img_to_array(img_r)
    img_r = np.expand_dims(img_r, axis=0)
    img_r /= 255.

    res=np.argmax(model.predict(img_r),axis=1)
    if res==0:
        prediction = 'N'
    elif res==1:
        prediction='P'

    return prediction


"""Function to crop the field of an image"""
def cropfield(image):
    e = 40  # adapt
    plt.imshow(image)
    plt.show()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    rayon = cv2.pointPolygonTest(c, (cX, cY), True)
    ima = image.copy()
    cv2.circle(ima, (cX, cY), int(rayon - e), (255, 0, 0), 1) 
    mask = np.zeros_like(image)
    mask = cv2.circle(mask, (cX, cY), int(rayon - e), (255, 255, 255), -1)
    # apply mask to image
    result = cv2.bitwise_and(ima, mask)
    ret, thresh = cv2.threshold(cv2.cvtColor(result, cv2.COLOR_BGR2GRAY), 100, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    field = result[y:y + h, x:x + w]

    if field.shape[0] >= 4000 or field.shape[1] >= 4000:
        field= field.resize((int(field.shape[1] * 0.4), int(field.shape[0] * 0.4)), field.ANTIALIAS)
        print("New shape :", field.shape)
    else:
        print("Uploaded Image")
        print("Width, Height, Channels :", field.shape)

    return field


"""Function to examine an image field"""
def exam(field,model):
    field_seg = field.copy()  
    start_time = time.time()
    gray = cv2.cvtColor(field, cv2.COLOR_BGR2GRAY)
    gray = background_subtract_area(gray)
    gray = cv2.equalizeHist(gray)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations=3)  
    thresh = cv2.dilate(erosion, kernel, iterations=2)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        cv2.drawContours(thresh, [cnt], 0, 255, -1)
    ################################# watershed ########################################################################
    D = ndimage.distance_transform_edt(thresh)
    localMax = peak_local_max(D, indices=False, min_distance=10, labels=thresh)
    markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
    labels = watershed(-D, markers, mask=thresh)

    truecells = []  # une liste ou on va stocker les vrais GR
    pos = []
    idx = 1
    for label in np.unique(labels):
        if label == 0:
            continue
        # otherwise, allocate memory for the label region and draw
        # it on the mask
        mask = np.zeros(gray.shape, dtype="uint8")
        mask[labels == label] = 255

        # detect contours in the mask and grab the largest one
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        c = max(cnts, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(c)
        if 30 <= w <= 100 and 30 <= h <= 100:  # 20 si c'est du x100 ou oculaire x 12 30 si c'est du X50 champ large
            cell = field[y-5:y + h+5, x-5:x + w+5]
            count = cell[cell==0]            
            if cell.shape[0]>0 and cell.shape[1]>0 and len(count)<600: #20% of image 
                truecells.append(cell)
                res = posouneg(cell,model)
                if res == 'P':
                    cv2.rectangle(field_seg, (x-5, y-5), (x + w+5, y + h+5), (255, 0, 0), 2)
                    pos.append(cell)

                elif res == 'N':
                    cv2.rectangle(field_seg, (x-5, y-5), (x + w+5, y + h+5), (0, 255, 0), 2)
        idx += 1
        
    neg=len(truecells)-len(pos)
    p = '%03.03f%%' % ((len(pos) / len(truecells) * 100))
    print("Infected RBCs : ", len(pos))
    print("Uninfected Blood Components : ", neg)
    print("Estimated parasitaemia :")
    print(p)
    print("###########################################################################")
    print("Analysis of " + str(len(truecells)) + " cells in  --- %s secondes ---" % ((time.time() - start_time)))
    print("###########################################################################")
    return field_seg, pos, p, neg


model="model.h5"
path = 'path_to_image'
model = load_model(model)

def main():
    image = Image.open(path)
    image = np.asarray(image)
    field = cropfield(image)
    field_f, pos, p, neg = exam(field, model=model)
    
main()
