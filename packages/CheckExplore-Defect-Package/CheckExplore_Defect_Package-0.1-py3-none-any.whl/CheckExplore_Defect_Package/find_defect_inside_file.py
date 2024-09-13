import detectron2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import detectron2
from detectron2.utils.logger import setup_logger
import numpy as np
import os, json, cv2, random,threading,shutil,uuid,glob,copy
from PIL import Image
import matplotlib.pyplot as plt
import colorsys
import numpy as np
from skimage.measure import find_contours as fc
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon as p
from matplotlib.patches import Polygon

#import modules
# from app.logs import *
# from app.error_INFO import error_dict

def in_out_damage(in_damage,out_damage):
    return_code = 200
    dict1 = {"Bead Damage":"Bead Damage","Sidewall Cut":"Cut Inside","Runflat":"Runflat","Tread Cut":"Cut Inside","CBU":"CBU"}
    if out_damage == "":
        for key, value in dict1.items():
            if value == in_damage:
                out_damage = key
                return_code = 200
    if in_damage == "":
        for key, value in dict1.items():
            if key == out_damage:
                in_damage = value
                return_code = 200
    return in_damage,out_damage,return_code

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
                # caption = "{} {:.3f}".format(label, score) if score else label
                caption = "{}".format(score*100)
                ax.text(x1, y1, caption, color='w', size=11, backgroundcolor="none")
                mask = pred_mask[i]
                p_m = np.zeros((mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
                p_m[1:-1, 1:-1] = mask
                con = fc(p_m, 0.5)
                for verts in con:
                    polCen = None
                    verts = np.fliplr(verts) - 1
                    pol_cor = p(verts)
                    poly_plot = Polygon(verts, edgecolor="red", facecolor='none',linewidth=5.0)
                    polCen = [pol_cor.centroid.x, pol_cor.centroid.y]
                    pol_list.append(polCen)
                    ax.add_patch(poly_plot)
    plt.savefig(claimid + "/image.jpg")

def configuration_model_inside():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_101_C4_3x.yaml"))
    cfg.DATALOADER.NUM_WORKERS = 4
    cfg.SOLVER.IMS_PER_BATCH = 4
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4
    cfg.MODEL.DEVICE = 'cuda'
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 # set a custom testing    
    cfg.MODEL.WEIGHTS="app/defect_model_inside.pth"
    predictor = DefaultPredictor(cfg)
    return predictor
wear_inside_predict = configuration_model_inside()

def damage_define_inside(claimid,img,path,model_config,class_names):
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
    print(labels)
    return labels

def find_defect_inside(claimid,claimwarranty_actual,AXIS_DICT):
    img_path = claimid + "/image.jpg"
    img=cv2.imread(img_path)
    class_names=["CBU","Bead Damage","Cut Inside","Runflat"]
    defect_type = ""
    return_defect = ""
    damage_list = damage_define_inside(claimid,img,img_path,wear_inside_predict,class_names)
    order = ["Bead Damage","Runflat","CBU","Cut Inside"]
    defect_type = high_priority_value(damage_list, order)
    print("Defect After filtering : ",defect_type)
    
    merge_defect_final = ""
    try:
        row_no,def_result,sideground = get_out_defect(str(claimwarranty_actual),"defect-outside")
        print("defect from outside image : ",def_result)
    except Exception as e:
        print("error in getting outside defect")
    
    # defining inside cuts on the basis of outside Image
    try:
        if defect_type=="" or def_result=="":
            defect_type_,def_result_,return_code = in_out_damage(defect_type,def_result)
        
        if def_result in ["Shoulder Cut","Sidewall Cut","Tread Cut"] and defect_type=="":
            defect_type = "Cut Inside"
            
        if defect_type=="":
            defect_type = defect_type_
        
        
        # if "Sidewall Cut" in def_result or "Shoulder Cut" in def_result or "Tread Cut" in def_result:
        #     # defect_type__=""
        #     if defect_type=="" or defect_type!="Cut Inside" or defect_type=="Sidewall Cut" or "Shoulder Cut" in def_result or "Tread Cut" in def_result:
        #         defect_type__ = "Cut Inside"
        #         return_code = 200
        #     defect_type =  defect_type__  
        # if "CBU" in def_result:
        #     if defect_type!="CBU":
        #         if ("Sidewall Cut" in defect_type) or ("Cut Inside" in defect_type):
        #             defect_type = "Cut Inside"
        #             return_code = 200
        #         else:
        #             defect_type = "CBU"
        #             return_code = 200

        # if def_result=="Tread Cut":
        #     if defect_type=="" or defect_type!="Cut Inside" or defect_type=="Sidewall Cut":
        #         defect_type = "Cut Inside"
        #         return_code = 200
        # elif ("Tread Cut" in def_result) and ("CBU" not in def_result):
        #     defect_type = "Cut Inside"
        #     return_code = 200

        # defining damages on the basis of inside Image
        if def_result=="" and defect_type=="":
            return_defect = ""
            return_code = 271
        elif def_result=="" or (def_result=="Shoulder Wear" and defect_type=="Cut Inside"):
            print("outside output >> ",def_result)
            if "Cut Inside" in defect_type:
                if sideground=="ground":
                    def_result_ = "Tread Cut"
                else:
                    def_result_ = "Sidewall Cut"
                def_result = def_result_
            def_AXIS_DICT = copy.deepcopy(AXIS_DICT)
            def_AXIS_DICT["Error_Code"]=200
            def_AXIS_DICT["Error_Message"]=error_dict["200"]
            defect_type_ = def_result_
            sr_one_dict_def={"Tyre_No": 1,
                "Tyre_Serial":"",
                "Photo_Name":"tyre.jpg",
                "Remark":"",
                "Gauge_Result":"",
                "QR_Result": "",
                "Defect_Result" :str(defect_type_),
                "Final_Defect_Result" : ""      
                }
            def_AXIS_DICT["Tyrewise_AI_Output"].append(sr_one_dict_def)
            def_AXIS_DICT["Type"] = "defect-outside"
            return_code=200
            Update_Defect(row_no,str(claimwarranty_actual),str(defect_type_),str(def_AXIS_DICT))
            # if "Cut Inside" in defect_type:
            #     print("inside output >> ",defect_type)
            #     # print("inside cut found")
            #     if sideground=="ground":
            #         defect_type_ = "Tread Cut"
            #     else:
            #         defect_type_ = "Sidewall Cut"
            #     sr_one_dict_def={"Tyre_No": 1,
            #         "Tyre_Serial":"",
            #         "Photo_Name":"tyre.jpg",
            #         "Remark":"",
            #         "Gauge_Result":"",
            #         "QR_Result": "",
            #         "Defect_Result" :str(defect_type_)
            #         }
            #     def_AXIS_DICT["Tyrewise_AI_Output"].append(sr_one_dict_def)
            #     def_AXIS_DICT["Type"] = "defect-outside"
            #     return_code=200
            #     print(def_AXIS_DICT)
            #     print(defect_type_)
            #     print(row_no)
            #     Update_Defect(row_no,str(claimwarranty_actual),str(defect_type_),str(def_AXIS_DICT))
    except Exception as e:
        print(e)
    
    # condtions to get final defect
    
    #1
    if defect_type=="Cut Inside" and def_result=="Shoulder Cut":
        merge_defect_final = "Shoulder Cut"
    #2
    if defect_type=="Runflat" and def_result=="Shoulder Cut":
        merge_defect_final = "Runflat"
    #3
    if defect_type=="Cut Inside" and def_result=="Sidewall Cut":
        merge_defect_final = "Sidewall Cut"
    #4
    if defect_type=="Runflat" and def_result=="Sidewall Cut":
        merge_defect_final = "Sidewall Cut"
    #5
    if defect_type=="CBU" and def_result=="":
        merge_defect_final = "CBU"
    #6
    if defect_type=="Runflat" and def_result=="CBU":
        merge_defect_final = "Runflat"
    #7
    if defect_type=="Cut Inside" and def_result=="CBU":
        merge_defect_final = "CBU"
    #8
    if defect_type=="Cut Inside" and def_result=="Bead Damage":
        merge_defect_final = "Bead Damage"
    #9
    if defect_type=="Runflat" and def_result=="Bead Damage":
        merge_defect_final = "Bead Damage"
    #10
    if defect_type=="Bead Damage" and def_result=="Bead Damage":
        merge_defect_final = "Bead Damage"
    #11
    if defect_type=="Cut Inside" and def_result=="Tread Cut":
        merge_defect_final = "Tread Cut"
    #12
    if defect_type=="Runflat" and def_result=="Tread Cut":
        merge_defect_final = "Tread Cut"
    #13
    if def_result=="Shoulder Wear":
        merge_defect_final = "Shoulder Wear"
    #14
    if defect_type=="Runflat" and def_result=="":
        merge_defect_final = "Runflat"
    #15
    if (defect_type=="" and def_result=="Shoulder Cut"):
        merge_defect_final = "Runflat"
    #16
    if defect_type=="CBU" and def_result=="Sidewall Cut":
        merge_defect_final = "Sidewall Cut"
    #17
    if defect_type=="Bead Damage" and def_result=="Sidewall Cut":
        merge_defect_final = "Bead Damage"
    #18
    if defect_type=="Cut Inside" and def_result=="Runflat":
        merge_defect_final = "Runflat"
    #19
    if defect_type=="Bead Damage" and def_result=="Runflat":
        merge_defect_final = "Bead Damage"
    #20
    if defect_type=="CBU" and def_result=="Shoulder Cut":
        merge_defect_final = "Shoulder Cut"

    if defect_type==def_result:
        merge_defect_final=defect_type
    
    if defect_type=="" or defect_type==None:
        return_defect = ""
        return_code = 271
    else:
        return_defect = defect_type
        return_code = 200
    
    return return_defect,return_code,merge_defect_final