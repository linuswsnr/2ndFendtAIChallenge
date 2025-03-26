# 2nd Fendt AI Challenge – Sugar Beet Detection

This repository contains the solution developed for the 2nd Fendt AI Challenge, a student competition organized by AGCO/Fendt. The goal was to build an AI-based system for detecting sugar beet plants on images in an agricultural context.

## 🌱 Motivation

- Support sustainable agriculture through smart automation  
- Reduce the need for chemical herbicides via precise weed detection: chemicals can be applied only where necessary or weeds can be removed mechanically  
- Improve plant care through early and accurate identification  

## 🧠 What was the challenge?

Participants were provided with 300 labeled images. The task was to build an image classifier capable of distinguishing sugar beet plants from weeds or background. The solution needed to be:

- Lightweight and efficient  
- Reliable in several outdoor agricultural conditions  
- Interpretable and easy to integrate into existing systems  

## 🔍 Key aspects of the solution

- **YOLOv11**: The latest YOLO version (YOLOv11) was used for object detection
- **Data Preprocessing**: Around 25 diverse and potentially misleading test images were removed from the dataset to test the model 
- **Augmentation Testing**: Various augmentation methods were applied and compared, including Albumentations, YOLO's built-in augmentation, and a combination of both  
- **Image Resolution**: Training was conducted with relatively high-resolution images, which increased inference time (~1s) but improved detection accuracy  
- **Model Selection**: Final model was chosen based on performance metrics and visual validation of predictions
  
## 💡 What I learned

- Deepened my understanding of computer vision and convolutional neural networks (CNNs)  
- Gained experience in dataset handling and preprocessing techniques  
- Learned how to evaluate model performance in a meaningful way  
- Understood challenges specific to AI in agriculture (e.g., lighting conditions, plant variability, limited data)  

## 📁 Structure

- **YOLO\YoloSugarbeetDetector.ipynb**: build data struktur which is mandatory for yolo, train model, apply model
- **YOLO_kFoldCrossValidation\YoloSugarbeetDetectorWithCrossValidation.ipynb**: same as YoloSugarbeetDetector.ipynb but with k-fold cross validation
- **evaluation.py**: evaluate the model (provided by fendt)
- **inference.py**: apply the model (provided by fendt)

