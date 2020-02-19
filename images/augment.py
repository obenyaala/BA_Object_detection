# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 17:16:29 2020

@author: Oussama Benyaala
"""
import os, cv2
import xml.etree.ElementTree as ET
import numpy as np

src = "original"
save_train = "augmented/training"
save_val = "augmented/validation"

exitloop = False
index = 0
for folders in os.listdir(src):
    if folders.startswith("cognex"):
        path = os.path.join(src, folders)
        for subfolders in os.listdir(path):
            path2 = os.path.join(path,subfolders)
            for files in os.listdir(path2):
                if files.endswith(".jpg"):
                    filename = files[0:len(files)-4]
                    img_path = os.path.join(path2, files)
                    #print("img:",img_path)
                    xml_path = os.path.join(path2, (filename+".xml"))
                    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
                    
                    if os.path.exists(xml_path):
                        xml_file = ET.parse(xml_path)
                        root = xml_file.getroot()
                        root[0].text = "training"
                        #print("root 0:",root[0].text)
                        
                        #################original image##################
                        img_name = "train_image_"+str(index)+".jpg"
                        img_save_path = os.path.join(save_train, img_name)
                        xml_name = "train_image_"+str(index)+".xml"
                        xml_save_path = os.path.join(save_train, xml_name)
                        root[1].text = img_name
                        root[2].text = img_save_path.replace("/", "\\")
                        
                        #print("save path: ",img_save_path)
                        #print("root 1:",root[1].text)
                        #print("root 2:",root[2].text)
                        cv2.imwrite(img_save_path, img)
                        xml_file.write(xml_save_path)
                        
                        #################darker image##################
                        #alpha = 0.3 # Simple contrast control [1.0-3.0]
                        #beta = 0    # Simple brightness control [0-100]
                        img_darker = cv2.convertScaleAbs(img, alpha=0.5, beta=-30)
                        img_name = "train_image_"+str(index)+"_a.jpg"
                        img_save_path = os.path.join(save_train, img_name)
                        xml_name = "train_image_"+str(index)+"_a.xml"
                        xml_save_path = os.path.join(save_train, xml_name)
                        root[1].text = img_name
                        root[2].text = img_save_path.replace("/", "\\")
                        
                        #print("save path: ",img_save_path)
                        #print("root 1:",root[1].text)
                        #print("root 2:",root[2].text)
                        cv2.imwrite(img_save_path, img_darker)
                        xml_file.write(xml_save_path)
                        
                        #################brighter image##################
                        img_brighter = cv2.convertScaleAbs(img, alpha=1.2, beta=40)
                        img_name = "train_image_"+str(index)+"_b.jpg"
                        img_save_path = os.path.join(save_train, img_name)
                        xml_name = "train_image_"+str(index)+"_b.xml"
                        xml_save_path = os.path.join(save_train, xml_name)
                        root[1].text = img_name
                        root[2].text = img_save_path.replace("/", "\\")
                        
                        #print("save path: ",img_save_path)
                        #print("root 1:",root[1].text)
                        #print("root 2:",root[2].text)
                        cv2.imwrite(img_save_path, img_brighter)
                        xml_file.write(xml_save_path)
                        
                        #################Gamma darker image##################
                        #img_gamma_darker = img.copy()
                        #invGamma = 1.0 / 0.4
                        table = np.array([((i / 255.0) ** 2.5) * 255 for i in np.arange(0, 256)]).astype("uint8")
                        img_gamma_darker =  cv2.LUT(img, table)
                        img_name = "train_image_"+str(index)+"_c.jpg"
                        img_save_path = os.path.join(save_train, img_name)
                        xml_name = "train_image_"+str(index)+"_c.xml"
                        xml_save_path = os.path.join(save_train, xml_name)
                        root[1].text = img_name
                        root[2].text = img_save_path.replace("/", "\\")
                        
                        #print("save path: ",img_save_path)
                        #print("root 1:",root[1].text)
                        #print("root 2:",root[2].text)
                        cv2.imwrite(img_save_path, img_gamma_darker)
                        xml_file.write(xml_save_path)
                        
                        #################Gamma brighter image##################
                        table = np.array([((i / 255.0) ** 0.5) * 255 for i in np.arange(0, 256)]).astype("uint8")
                        img_gamma_brighter =  cv2.LUT(img, table)
                        img_name = "train_image_"+str(index)+"_d.jpg"
                        img_save_path = os.path.join(save_train, img_name)
                        xml_name = "train_image_"+str(index)+"_d.xml"
                        xml_save_path = os.path.join(save_train, xml_name)
                        root[1].text = img_name
                        root[2].text = img_save_path.replace("/", "\\")
                        
                        #print("save path: ",img_save_path)
                        #print("root 1:",root[1].text)
                        #print("root 2:",root[2].text)
                        cv2.imwrite(img_save_path, img_gamma_brighter)
                        xml_file.write(xml_save_path)
                        
                        #################Morphological transformations on image##################
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
                        img_close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
                        img_name = "train_image_"+str(index)+"_e.jpg"
                        img_save_path = os.path.join(save_train, img_name)
                        xml_name = "train_image_"+str(index)+"_e.xml"
                        xml_save_path = os.path.join(save_train, xml_name)
                        root[1].text = img_name
                        root[2].text = img_save_path.replace("/", "\\")
                        
                        #print("save path: ",img_save_path)
                        #print("root 1:",root[1].text)
                        #print("root 2:",root[2].text)
                        cv2.imwrite(img_save_path, img_close)
                        xml_file.write(xml_save_path)
                        index += 1
                    else:
                        print("couldnt find the xml file for :", path2)
                        
                elif files == "validation":
                    path3 = os.path.join(path2,files)
                    for files2 in os.listdir(path3):
                        if files2.endswith(".jpg"):
                            filename = files2[0:len(files2)-4]
                            img_path = os.path.join(path3, files2)
                            #print("img val: ",img_path)
                            xml_path = os.path.join(path3, (filename+".xml"))
                            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
                            
                            if os.path.exists(xml_path):
                                xml_file = ET.parse(xml_path)
                                root = xml_file.getroot()
                                root[0].text = "validation"
                                #print("root 0:",root[0].text)
                                
                                #################original image##################
                                img_name = "validation_image_"+str(index)+".jpg"
                                img_save_path = os.path.join(save_val, img_name)
                                xml_name = "validation_image_"+str(index)+".xml"
                                xml_save_path = os.path.join(save_val, xml_name)
                                root[1].text = img_name
                                root[2].text = img_save_path.replace("/", "\\")
                                
                                #print("save path: ",img_save_path)
                                #print("root 1:",root[1].text)
                                #print("root 2:",root[2].text)
                                cv2.imwrite(img_save_path, img)
                                xml_file.write(xml_save_path)
                                
                                #################darker image##################
                                #alpha = 0.3 # Simple contrast control [1.0-3.0]
                                #beta = 0    # Simple brightness control [0-100]
                                img_darker = cv2.convertScaleAbs(img, alpha=0.5, beta=-30)
                                img_name = "validation_image_"+str(index)+"_a.jpg"
                                img_save_path = os.path.join(save_val, img_name)
                                xml_name = "validation_image_"+str(index)+"_a.xml"
                                xml_save_path = os.path.join(save_val, xml_name)
                                root[1].text = img_name
                                root[2].text = img_save_path.replace("/", "\\")
                                
                                #print("save path: ",img_save_path)
                                #print("root 1:",root[1].text)
                                #print("root 2:",root[2].text)
                                cv2.imwrite(img_save_path, img_darker)
                                xml_file.write(xml_save_path)
                                
                                #################brighter image##################
                                img_brighter = cv2.convertScaleAbs(img, alpha=1.2, beta=40)
                                img_name = "validation_image_"+str(index)+"_b.jpg"
                                img_save_path = os.path.join(save_val, img_name)
                                xml_name = "validation_image_"+str(index)+"_b.xml"
                                xml_save_path = os.path.join(save_val, xml_name)
                                root[1].text = img_name
                                root[2].text = img_save_path.replace("/", "\\")
                                
                                #print("save path: ",img_save_path)
                                #print("root 1:",root[1].text)
                                #print("root 2:",root[2].text)
                                cv2.imwrite(img_save_path, img_brighter)
                                xml_file.write(xml_save_path)
                                
                                #################Gamma darker image##################
                                #img_gamma_darker = img.copy()
                                #invGamma = 1.0 / 0.4
                                table = np.array([((i / 255.0) ** 2.5) * 255 for i in np.arange(0, 256)]).astype("uint8")
                                img_gamma_darker =  cv2.LUT(img, table)
                                img_name = "validation_image_"+str(index)+"_c.jpg"
                                img_save_path = os.path.join(save_val, img_name)
                                xml_name = "validation_image_"+str(index)+"_c.xml"
                                xml_save_path = os.path.join(save_val, xml_name)
                                root[1].text = img_name
                                root[2].text = img_save_path.replace("/", "\\")
                                
                                #print("save path: ",img_save_path)
                                #print("root 1:",root[1].text)
                                #print("root 2:",root[2].text)
                                cv2.imwrite(img_save_path, img_gamma_darker)
                                xml_file.write(xml_save_path)
                                
                                #################Gamma brighter image##################
                                table = np.array([((i / 255.0) ** 0.5) * 255 for i in np.arange(0, 256)]).astype("uint8")
                                img_gamma_brighter =  cv2.LUT(img, table)
                                img_name = "validation_image_"+str(index)+"_d.jpg"
                                img_save_path = os.path.join(save_val, img_name)
                                xml_name = "validation_image_"+str(index)+"_d.xml"
                                xml_save_path = os.path.join(save_val, xml_name)
                                root[1].text = img_name
                                root[2].text = img_save_path.replace("/", "\\")
                                
                                #print("save path: ",img_save_path)
                                #print("root 1:",root[1].text)
                                #print("root 2:",root[2].text)
                                cv2.imwrite(img_save_path, img_gamma_brighter)
                                xml_file.write(xml_save_path)
                                
                                #################Morphological transformations on image##################
                                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
                                img_close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
                                img_name = "validation_image_"+str(index)+"_e.jpg"
                                img_save_path = os.path.join(save_val, img_name)
                                xml_name = "validation_image_"+str(index)+"_e.xml"
                                xml_save_path = os.path.join(save_val, xml_name)
                                root[1].text = img_name
                                root[2].text = img_save_path.replace("/", "\\")
                                
                                #print("save path: ",img_save_path)
                                #print("root 1:",root[1].text)
                                #print("root 2:",root[2].text)
                                cv2.imwrite(img_save_path, img_close)
                                xml_file.write(xml_save_path)
                                index += 1
                            else:
                                print("couldnt find the xml file for :",xml_path)