# student_object_detection_challenge

This repo contains the code for the student object detection challenge with the Hochschule Kempten. The goal is that the students develop an object detector for sugarbeets. This folder provides a first starting point for the students, i.e. it contains a docker container, which can be adapted to their needs. Furthermore, it contains the evaluation script (evaluation.py) which is used to evaluate the results of the students and should not be modified. The proposed object detector should be implemented in the inference script (inference.py), which is called by the evaluation script.

## Requirements

This project does not require any dependencies on your ubuntu-computer except the installation of docker/nvidia-docker. The remaining dependencies for the student-object-detection-challenge should be added to the [dockerfile of this project](./docker/Dockerfile).

Information about the installation of docker of your system can be found [here](https://docs.docker.com/engine/install/)
    
## Installation and Setup

The provided docker-container can be built by a shell-script. For this, type in the terminal:
    
    $ ./docker/build_docker.sh
        
After the docker-container is built, you can start your docker-environment withthe following command in your terminal:
    
    $ ./run_docker.sh

If you require second terminal for your docker environment, open a second terminal tab and run the command again. 
        
## Evaluation

The developed object-detector is evaluated in different categories, e.g.
- inference time of your model (tested on a Nvidia GeForce RTX 3090)
- accuracy (using primary challenge metric of [COCO-evaluation metric](https://cocodataset.org/#detection-eval) for object detectors)
   
The evaluation is performed by the following script:

    $ python evaluation.py -d <path2imgset>

where <path2imgset> is the path to the image-list, you want to evaluate, i.e. 
    
    $ python evaluation.py -d imageSet/testset.txt 

> **Note**
> Please do not modify the evaluation script. The evaluation script calls the do_inference() function of inference.py, hence take care, that the full functionality for the inference is in this function.
        
>**Note**
> You can adjust the inference script and its do_inference() function as you like and implement your object-detector in this function.
> Just keep the interface of the do_inference() function, since it is called from our own evaluation script.

>**Note** 
> Remember, that your code should run in this (modified) docker-container!

