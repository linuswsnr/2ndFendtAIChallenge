import cv2 as cv2
from ultralytics import YOLO

model = YOLO("best.pt")

# do_inference
#   this function applies an object detector on a given image
# arguments
# @PARAM img    [INPUT]:  input image of the object detector
# @PARAM result [OUTPUT]: python list, which list element contains information of one object in the form [x_min, y_min, x_max, y_max, class_id, score]
def do_inference(img):

    # Run prediction on the loaded image
    results = model.predict(img)

    # Extract and format the predictions
    formatted_results = []

    for box in results[0].boxes:  # Access the first image's results
        x_min, y_min, x_max, y_max = box.xyxy[0].tolist()  # Bounding box coordinates
        class_id = int(box.cls)  # Class ID
        score = float(box.conf)  # Confidence score
        formatted_results.append([x_min, y_min, x_max, y_max, class_id, score])
    
    return formatted_results
