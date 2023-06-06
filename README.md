# MALARIS
This is the code for our PLOS ONE paper : An automated system for Plasmodium falciparum detection and parasitemia estimation: evaluation on thin blood smear images
{
  "appId": "4d4260be-eb3d-429c-9c81-acaf9b723d78",
  "fileType": "md",
  "fileName": "README.md",
  "content": "# Malaria Detection\n\nThis is a Python script for detecting malaria in blood smear images. The script uses OpenCV for image processing and a pre-trained TensorFlow model for classification.\n\n## Requirements\n\n- Python 3.7 or later\n- OpenCV\n- TensorFlow\n- Scipy\n- Scikit-image\n- Keras\n- Matplotlib\n- Numpy\n\n## Usage\n\n1. Load the pre-trained model using the `load_model` function.\n2. Use the `cropfield` function to crop the field of the image.\n3. Use the `exam` function to examine the image field and detect malaria.\n\n## License\n\nThis project is licensed under the terms of the MIT license."
}
