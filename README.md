# MALARIS

## Info
This is the code and data for our PLOS ONE paper : An automated system for Plasmodium falciparum detection and parasitemia estimation: evaluation on thin blood smear images
The script uses OpenCV for image processing and a pre-trained TensorFlow model for classification.
by [Aniss Acherar, Ph.D](http://aniss.acherar.free.fr/) et al.

![graphical abstract](https://github.com/anissacherar/MALARIS/assets/49938607/9c6aaf40-8e46-4d2d-aa69-29c53f198f4c)

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
flow cytometry.  

The datasets consist of parasitemia estimated by various techniques. There are two files: '14_patients.csv' includes 14 patients and their parasitemia estimated by the proposed system (attached Python code), as well as estimations made by manual techniques including standard measurement and that assisted by the Miller cell. The second file, '102_patients.csv', corresponds to estimated parasitemia and parasitemia estimates from three techniques including the system, the Miller cell, and flow cytometry for another 102 patients.



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

