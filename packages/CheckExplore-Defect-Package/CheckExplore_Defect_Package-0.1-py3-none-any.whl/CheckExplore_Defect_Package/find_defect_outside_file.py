import detectron2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import detectron2
from detectron2.utils.logger import setup_logger
import numpy as np
import os, json, cv2, random,threading,shutil,uuid,glob
from PIL import Image
import matplotlib.pyplot as plt
import colorsys
from skimage.measure import find_contours as fc
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon as p
from matplotlib.patches import Polygon

from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow
from tensorflow.keras.models import load_model
from imutils import build_montages
from imutils import paths
import argparse

sideground_model_resnet = load_model("app/side_ground_resnet_model")
tire_detect_resnet = load_model("app/tyre_detect_resnet_model")

def tiredetect(img_pt):
    classs = ["not_tyre","tyre"]
    orig = cv2.imread(img_pt)
    # pre-process our image by converting it from BGR to RGB channel
    # ordering (since our Keras mdoel was trained on RGB ordering),
    # resize it to 64x64 pixels, and then scale the pixel intensities
    # to the range [0, 1]
    image = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (256, 256))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    # make predictions on the input image
    pred = tire_detect_resnet.predict(image)
    pred = pred.argmax(axis=1)[0]
    pred_class = classs[pred]
    return pred_class

def sideground_resnet(img_pt):
    classs = ["ground","side"]
    orig = img_pt
    # pre-process our image by converting it from BGR to RGB channel
    # ordering (since our Keras mdoel was trained on RGB ordering),
    # resize it to 64x64 pixels, and then scale the pixel intensities
    # to the range [0, 1]
    image = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (256, 256))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    # make predictions on the input image
    pred = sideground_model_resnet.predict(image)
    pred = pred.argmax(axis=1)[0]
    pred_class = classs[pred]
    return pred_class

def high_priority_value(input_list, priority_list):
    for value in priority_list:
        if value in input_list:
            return value
    return ""

def random_colors(N, bright=True):
        brightness = 1.0 if bright else 0.7
        hsv = [(i / N, 1, brightness) for i in range(N)]
        colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
        random.shuffle(colors)
        return colors

def draw_mask_image(claimid,img,pred_class,pred_score,pred_box,pred_mask,img_path,label_):
    imm = Image.open(img_path)
    fig = plt.figure(frameon=False)
    w, h = imm.size
    print(h, w)
    fig.set_size_inches(w / 100, h / 100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(imm, aspect='auto')
    length_of_pred_class = len(pred_class)
    print(length_of_pred_class)
    colors = random_colors(length_of_pred_class)
    pol_list=[]
    if length_of_pred_class != 0:
        for i in range(length_of_pred_class):
                color = colors[i]
                score = pred_score[i]
                x1, y1, x2, y2 = pred_box[i]
                label = label_
                caption = "{} {:.3f}".format(label, score) if score else label
                ax.text(x1, y1, caption, color='w', size=11, backgroundcolor="none")
                mask = pred_mask[i]
                p_m = np.zeros((mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
                p_m[1:-1, 1:-1] = mask
                con = fc(p_m, 0.5)
                for verts in con:
                    polCen = None
                    verts = np.fliplr(verts) - 1
                    pol_cor = p(verts)
                    poly_plot = Polygon(verts, edgecolor=color, facecolor='none')
                    polCen = [pol_cor.centroid.x, pol_cor.centroid.y]
                    pol_list.append(polCen)
                    ax.add_patch(poly_plot)
    plt.savefig(claimid + "/image.jpg")
    
def sideground_configuration_model():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_C4_3x.yaml"))
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4
    cfg.MODEL.DEVICE = 'cuda'
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8# set a custom testing    
    cfg.MODEL.WEIGHTS = 'app/sideground.pth'
    predictor = DefaultPredictor(cfg)
    return predictor
sideground_predict = sideground_configuration_model() 

def sideground_configuration_model_new():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_C4_3x.yaml"))
    cfg.DATALOADER.NUM_WORKERS = 4
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3
    cfg.MODEL.DEVICE = 'cuda'
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8# set a custom testing    
    cfg.MODEL.WEIGHTS = 'app/sideground_new.pth'
    predictor = DefaultPredictor(cfg)
    return predictor
sideground_predict_new = sideground_configuration_model_new()

def sideground_detection(img_path):
    try:
        # clss=["damage","damage","ground","side"]
        clss=["sideground","ground","side"]
        # output = sideground_predict(img_path)
        output = sideground_predict_new(img_path)
        pred_class = output["instances"].pred_classes.cpu().numpy()
        if len(pred_class)>0:
            for i in range(len(pred_class)):
                pred_cls=clss[pred_class[i]]
    except Exception as e:
        pred_cls = ""
    return pred_cls

def configuration_model_ground():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_101_C4_3x.yaml"))
    cfg.DATALOADER.NUM_WORKERS = 16
    cfg.SOLVER.IMS_PER_BATCH = 4
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
    cfg.MODEL.DEVICE = 'cuda'
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 # set a custom testing    
    cfg.MODEL.WEIGHTS="app/defect_model_ground.pth"
    predictor = DefaultPredictor(cfg)
    return predictor
wear_ground_predict = configuration_model_ground()

def configuration_model_side():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_101_C4_3x.yaml"))
    cfg.DATALOADER.NUM_WORKERS = 4
    cfg.SOLVER.IMS_PER_BATCH = 4
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 5
    cfg.MODEL.DEVICE = 'cuda'
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 # set a custom testing    
    cfg.MODEL.WEIGHTS="app/defect_model_side.pth"
    predictor = DefaultPredictor(cfg)
    return predictor
wear_side_predict = configuration_model_side()

def damage_define(claimid,img,path,model_config,class_names):
    img_path = path
    outputs1=model_config(img)
    pred_class = outputs1["instances"].pred_classes.cpu().numpy()
    pred_score = outputs1["instances"].scores.cpu().numpy()
    pred_box = outputs1["instances"].pred_boxes.tensor.cpu().numpy()
    pred_mask_dent = outputs1["instances"].pred_masks.cpu().numpy()
    labels = []
    label_wear = ""
    if len(pred_class)>0:
        for i in range(len(pred_class)):          
            label_wear = class_names[pred_class[i]]
            labels.append(label_wear)

        draw_mask_image(claimid,img,pred_class,pred_score,pred_box,pred_mask_dent,img_path,label_wear)

    # labels = list(set(labels))
    print(labels)
    return labels


def find_defect_outside(claimid):
    img_path = claimid + "/image.jpg"
    img=cv2.imread(img_path)
    tyre_cls = ""
    # tyre_cls = sideground_detection(img)
    tyre_cls = sideground_resnet(img)
    print("Side/Ground >>> ",tyre_cls)
    class_names_ground=["Shoulder Wear","Tread Cut"]
    class_names_side=["CBU","Bead Damage","Shoulder Cut","Runflat","Sidewall Cut"]
    defect_cls = ""
    reutrn_defect = ""
    if tyre_cls!="" or tyre_cls==None:
        if tyre_cls=="ground":
            damage_list = damage_define(claimid,img,img_path,wear_ground_predict,class_names_ground)
            order = ["Shoulder Wear","Tread Cut"]
            defect_cls = high_priority_value(damage_list, order)
            print("Defect After filtering : ",defect_cls)
        elif tyre_cls=="side":
            damage_list = damage_define(claimid,img,img_path,wear_side_predict,class_names_side)
            order = ["Bead Damage","Shoulder Cut","Sidewall Cut","Runflat","CBU"]
            defect_cls = high_priority_value(damage_list, order)
            print("Defect After filtering : ",defect_cls)
        if defect_cls=="" or defect_cls==None:
            reutrn_defect = ""
            reutrn_code = 271
        else:
            reutrn_defect = defect_cls
            reutrn_code = 200
    else:
        reutrn_defect = ""
        reutrn_code = 271
        
    if reutrn_defect=="":
        reutrn_code = 271
    
    return reutrn_defect,reutrn_code,tyre_cls