"""
 * evaluation.py
 *
 * This script evaluates all iamges of a given image set. The path of the images are stored
 * in a txt-file using the followoing format:
 *  <path2image.png> <path2xmlfile.json>
 * or 
 *  <path2image.png> 
 *
 * arguments:
 *      --dataset (short -d):      [REQUIRED] path to image_list.txt file
 *
 * examples:
 * $ python evaluation.py -d imageSet/testset.txt
 *
"""

import argparse
import numpy as np
import cv2 as cv2
import time
import os
import glob
import json

import coco_tools
from inference import do_inference

# classes containing matching between class_name and class_id
# classes.update({"class_name": class_id})
classes = {}
classes.update({"sugarbeet": 0})

# colors contains the color ob the bbox to be plotted
colors = {}
colors.update({"0": (255,0,0)})

categories = np.array([{'id': 0, 'name': 'sugarbeet'}])

# Function to convert a string to bool
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


# This main-function reads in the image from an image-list, applies the inference for each image
# and finally applies the evaluation on the image-set.
def main():
   
    # --------------------------------
    # readin arguments
    # --------------------------------

    # get arguments form argpaser

    parser = argparse.ArgumentParser()

    # required parameters
    parser.add_argument("-d", "--dataset", help="[REQUIRED] path to image_list.txt file", 
                        type=str, required=True)
                        
    # optional parameters     
    parser.add_argument("-p", "--plotImages", type=str2bool, nargs='?', const=True, default=False,
                        help="[OPTIONAL] path to folder, to which images should be dumped for visualization")    

    args = parser.parse_args()

    # read arguments from parser

    path2imglist = args.dataset
    
    plotImages = args.plotImages
    
    # -------------------------------
    # create some folders and clean them
    # -------------------------------
    
    # create folders, if not exist
    
    if not os.path.exists('evaluation'):
        os.makedirs('evaluation')
        
    if not os.path.exists('evaluation/gt'):
        os.makedirs('evaluation/gt')
        
    if not os.path.exists('evaluation/det'):
        os.makedirs('evaluation/det')
      
    if plotImages:  
        if not os.path.exists('results'):
            os.makedirs('results')
        
    # remove txt-files in dt and gt folder
    
    files = glob.glob('evaluation/gt/*')
    for f in files:
        os.remove(f)
        
    files = glob.glob('evaluation/det/*')
    for f in files:
        os.remove(f)
        
    if plotImages:  
        files = glob.glob('results/*')
        for f in files:
            os.remove(f)
    
    # -------------------------------
    # init evaluation stuff
    # -------------------------------
    
    image_ids = []
    gt_boxes = []
    gt_classes = []
    det_boxes = []
    det_classes = []
    det_scores = []


    # --------------------------------
    # open txt-file
    # --------------------------------

    try:
        imageListFile_txt = open(path2imglist, "r")
    except:
        print ("[ERROR] cannot load file '{}'".format(path2imglist)) 
        return
        
    # --------------------------------
    # open txt-file
    # --------------------------------
    
    total_inference_time = 0.0
    amount_images = 0

    for line in imageListFile_txt:

        # get current path of image
        path2img = line.split()[0]
        path2gt = line.split()[1]
        
        print(f"Process image '{path2img}'") 
        
        # --------------------------------------
        # inference of current image
        # --------------------------------------
        
        # check img path

        if not os.path.exists(path2img):
            print ("[ERROR] path '{}' does not exist!".format(path2img))
            return
        
        # read in image

        img = cv2.imread(path2img)
        
        # apply inference of image
        
        start = time.time()
        results = do_inference(img)
        inference_time = time.time() - start
        
        print (f"inference_time of image {amount_images}: {inference_time}")
        
        # increase total_inference_time for later evaluation
        
        total_inference_time += inference_time
        amount_images += 1
        
        # avoid error, if result-vector is empty
        
        if (len(results) == 0):
            results.append([0.0, 0.0, 0.0, 0.0, 0, 0.0])
        
        # ------------------------------------------
        # convert detections in evaluation-format
        # ------------------------------------------
        
        # get img-name:
        
        img_prefix = path2img.split('/')[-1].split('.')[0]
        image_ids.append(img_prefix)
        detection_file = os.path.join("evaluation", "det", img_prefix+'.txt')
        
        with open(detection_file, 'w') as f:
        
            det_bbox = []
            det_class_id = []
            det_score = []
        
            for result in results:
                x_min, y_min, x_max, y_max, class_id, score = result
                f.write(f"{class_id} {score} {x_min} {y_min} {x_max} {y_max}\n")
                
                # plot bbox in image, if desired
                
                if plotImages:
                    cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color=colors[str(class_id)], thickness=5)
                
                # for evaluation
                
                det_bbox.append([x_min, y_min, x_max, y_max])
                det_class_id.append(class_id) 
                det_score.append(score)
                    
            det_boxes.append(np.array(det_bbox))
            det_scores.append(np.array(det_score))
            det_classes.append(np.array(det_class_id))
                
            f.close()
            
        # save image
        
        if plotImages:
            img_name = path2img.split("/")[-1]
            cv2.imwrite(os.path.join("results",img_name), img)
            
            
        # ------------------------------------------
        # convert grount-truth in evaluation-format
        # ------------------------------------------
        
        # check annotation path

        if not os.path.exists(path2gt):
            print ("[ERROR] path '{}' does not exist!".format(path2gt))
            return
            
        # load json annotation file
        
        with open(path2gt, 'r') as f:
            annotation_dict = json.load(f)
            
        # generate gt-file
        
        groundtruth_file = os.path.join("evaluation", "gt", img_prefix+'.txt')
        
        with open(groundtruth_file, 'w') as f_gt:
                  
            # iterate through annotation_dictionary  
            
            gt_bbox_img = []
            gt_classed_img = []  
                
            for objects in annotation_dict['objects']:   
                          
                # check, if current label is member of Classes
                
                label = objects['label']
                label_id = classes[label]
                
                # get bbox and plot it to image
            
                bbox = objects['bbox']
                if (len(bbox) == 2):     
                    x_min = int(bbox[0][0])
                    y_min = int(bbox[0][1])
                    x_max = int(bbox[1][0])
                    y_max = int(bbox[1][1])
                else:
                    print ("[ERROR] bbox can only have two points!")
        
                f_gt.write(f"{label_id} {x_min} {y_min} {x_max} {y_max}\n")
                
                # for evaluation
                
                gt_classed_img.append(label_id) 
                gt_bbox_img.append([x_min, y_min, x_max, y_max])

            gt_boxes.append(np.array(gt_bbox_img))
            gt_classes.append(np.array(gt_classed_img))
                
            f_gt.close()
    
    # close file
    
    imageListFile_txt.close()        
            
    # ------------------------------------------
    # apply evaluation
    # ------------------------------------------
        
    # convert into coco-format
    
    dict_gt = coco_tools.ExportGroundtruthToCOCO(image_ids, gt_boxes, gt_classes, categories)
    dict_det = coco_tools.ExportDetectionsToCOCO(image_ids, det_boxes, det_scores, det_classes, categories)
 
    # evaulation according to coco
    
    groundtruth = coco_tools.COCOWrapper(dict_gt)
    detections = groundtruth.LoadAnnotations(dict_det)
    evaluator = coco_tools.COCOEvalWrapper(groundtruth, detections, agnostic_mode=False)
    metrics, empty = evaluator.ComputeMetrics()
    
    # --------------------------------
    # sum up results
    # --------------------------------
    
    average_inference_time = total_inference_time / amount_images
    
    print (f"###################################################################")
    print (f"average inference_time per image: {average_inference_time} s")
    print (f"Precision/mAP:        {metrics['Precision/mAP']}")
    print (f"Precision/mAP@.50IOU: {metrics['Precision/mAP@.50IOU']}")
    print (f"Precision/mAP@.75IOU: {metrics['Precision/mAP@.75IOU']}")
    print (f"###################################################################")
    
    return
    


if __name__ == "__main__":
    main()

