import json 
import glob 
import xml.dom.minidom as minidom
import os
import cv2
import glob
import xml
import random

face_color = (100, 200, 5)
limb_color = (0, 255, 0)
other_color = (200, 200, 50)
kp_color = (0, 0, 255)

segm_colors = [face_color] * 5 + [other_color] * 2 + [limb_color] * 4 + [other_color] * 4

def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))


def draw_keypoint(im, keypoints):
    '''
        order: 
        0-4 (face): left eye, right eye, nose, left earbase, right earbase
        5-16 (limbs):   L_F_elbow, R_F_elbow, L_B_elbow, R_B_elbow
                        L_F_knee, R_F_knee, L_B_knee, R_B_knee
                        L_F_paw, R_F_paw, L_B_paw, R_B_paw
        17-19 (others): throat, withers, tailbase
    '''
    segmts = [  (0,1), (0,2), (1,2), (0,3), (1,4),
                (2,17), (18,19),
                (5,9), (6,10), (7,11), (8,12),
                (9,13), (10,14), (11,15), (12,16)]


    for i in range(len(segmts)):
        segm = segmts[i]
        kp1 = keypoints[segm[0]]
        kp2 = keypoints[segm[1]]
        if kp1[2] == 0 or kp2[2] == 0:
            continue

        cv2.line(im, tuple(kp1[:2]), tuple(kp2[:2]), segm_colors[i], thickness=2)

    for kp in keypoints:
        if kp[2] == 0:
            continue
        cv2.circle(im, tuple(kp[:2]), radius=4, color=kp_color, thickness=-1)

    return im


def draw_bbox(im, xmin, ymin, xmax, ymax, color):
    cv2.rectangle(im, (xmin, ymin), (xmax, ymax), color, thickness=2)
    return im 


def visualize_json():
    output_dir = "visualization_animalpose"
    os.makedirs(output_dir, exist_ok=True)
    anno_dict = json.load(open("keypoints.json"))
    image_map = anno_dict["images"]
    annotations = anno_dict["annotations"]
    im_dict = dict()
    for anno in annotations:
        imagename = image_map[str(anno["image_id"])]
        bbox = anno["bbox"]
        keypoints = anno["keypoints"]
        image_path = os.path.join("images", imagename)
        if not imagename in im_dict:
            im = cv2.imread(image_path)
        else:
            im = im_dict[imagename]
        
        xmin, ymin, xmax, ymax = bbox 
        im = draw_bbox(im, xmin, ymin, xmax, ymax, random_color())
        im = draw_keypoint(im, keypoints)
        save_path = os.path.join(output_dir, imagename)
        cv2.imwrite(save_path, im)
        im_dict[imagename] = im


if __name__ == "__main__":
    visualize_json()
