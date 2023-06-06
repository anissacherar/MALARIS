# MALARIS

## Info
This is the code for our PLOS ONE paper : An automated system for Plasmodium falciparum detection and parasitemia estimation: evaluation on thin blood smear images
The script uses OpenCV for image processing and a pre-trained TensorFlow model for classification.
by [Aniss Acherar, Ph.D](http://aniss.acherar.free.fr/) et al.

## Abstract

Malaria is a deadly disease that is transmitted through mosquito bites. Biologists use a
microscope to examine thin blood smears at high magnification (1000x) to identify
parasites in red blood cells (RBCs). Estimating parasitemia is essential in determining
the severity of the infection and guiding treatment. However, this process is timeconsuming, labor-intensive, and subject to variation, which can directly affect patient
outcomes.  
This study focuses on comparing three methods for estimating parasitemia in patients
infected with Plasmodium falciparum. We first analyzed the impact of the number of
field images on parasitemia estimates using our framework, MALARIS, which includes
a top classifier convolutional neural network (CNN). Additionally, we studied the
variation between different readers using two manual techniques to demonstrate the
need for a reliable and reproducible automated system. Finally, we included blood
smears from an additional 102 patients to compare the performance and correlation of
our system with manual microscopy and semi-automatic techniques using commercial
flow cytometry. Our results showed strong correlations b

## Requirements
* Python 3.7 or later  
* OpenCV  
* TensorFlow  
* Scipy   
* Scikit-image  
* Keras  
* Matplotlib  
* Numpy  

## Tasks
* Load the pre-trained model using the `load_model` function. 
* Use the `cropfield` function to crop the field of the image. 
* Use the `exam` function to examine the image field and detect malaria and estimate parasitemia.


## License : This project is licensed under the terms of the GNU General Public License (GPL)."

