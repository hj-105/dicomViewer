# 모듈 임포트
from flask import Flask, flash, redirect, render_template, request, url_for, send_from_directory, sessions, send_file
from werkzeug.utils import secure_filename
from collections import OrderedDict
import matplotlib.image as mplimg
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image
import pydicom as dc
import numpy as np
import cv2 as cv
import shutil
import json
import sys
import os


application = Flask(__name__)
global a

#링크들
@application.route("/", methods=['GET', 'POST'])
def hello():
    return render_template('upload.html')

# @application.route("/fig", methods = ['GET', 'POST'])
# def fig():
#         return render_template('fig.html')

@application.route("/DCshow", methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        f = request.files['file']
        f.save("./" + secure_filename(f.filename))

        src = os.path.join("./" + f.filename)
        dst = os.path.join("./static/" + f.filename)
        shutil.copyfile(src,dst)
        
        ds = dc.dcmread(dst)
        pix = ds.pixel_array

        # name, ext = os.path.splitext(dst)
        a = f.filename.split('.')
        
        #meta data dump
        meta = OrderedDict()
        meta_attributes = ['StudyDate','StudyTime','PatientName','PatientID',
                        'PatientBirthDate','PatientSex','StudyID']

        for i in meta_attributes:
            if i in ds:
                meta[i] = ds[i].to_json()
            else:
                pass
            
        #meta data save as json 
        with open("./metaData.json", 'w',encoding='utf-8') as outfile:
            json.dump(meta, outfile, indent=4)

        #meta data's key,val
        k, v = [],[]
        for key, val in meta.items():
            k.append(key)
            v.append(val)
            print(key)
            print(val)
            
        # pixel = ds['PixelData'].to_json()
        #pixel data save as json
        with open("./pixelData.json", 'w',encoding='utf-8') as outfile:
            json.dump(ds['PixelData'].to_json(), outfile, indent=4)
        
        #for i in range(pix.shape[0]):
            #cv.imwrite(".image/%s_%d.png"%(f.filename,i),pix[i,:,:])
            #plt.imsave("./static/image/%s_%d.png"%(a[0],i),pix[i,:,:], cmap = cm.gray)
        slice = None
        if slice:
            slice = request.form['slice']

        return render_template('image.html',image_file='test.png',a=a[0],fn=f.filename,pix=pix,k=k,v=v,sliceNum=pix.shape[0],h=round(int(pix.shape[0])/2),h_=str(round(int(pix.shape[0])/2)),slice=slice)
    else:
        return render_template('upload.html')


    
@application.route("/saveJson", methods = ['GET', 'POST'])
def saveJson():
    files = "./metaData.json"
    return send_file(files, attachment_filename = files, as_attachment=True)

@application.route("/saveJson_p", methods = ['GET', 'POST'])
def saveJson_p():
    files = "./pixelData.json"
    return send_file(files, attachment_filename = files, as_attachment=True)    
    
# @application.route("/image")
# def img():
#     return render_template('image.html')


if __name__ == "__main__":
    application.debug = True
    application.run(threaded=True)



#import time
#import flask
#import pyscreenshot as ImageGrab
    
'''
@application.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save("./uploads/" + secure_filename(f.filename))

        src = os.path.join("./uploads/" + f.filename)
        dst = os.path.join("./static/input/" + f.filename)
        shutil.copyfile(src,dst)

        finding,melanoma,nv,bkl = model(f.filename, model_dir)
        # finding = "Prediction) NV: 95.80%"
        # melanoma,nv,bkl = 3.1762884,95.79547,1.0282432

        return render_template('result.html', image_file = f.filename, finding=finding,mel=melanoma,nv=nv,bkl=bkl)
    else:
        return render_template('applyPhoto.html')
'''   
'''
@application.route("/us")
def us():
    return render_template("us.html")

@application.route("/skin")
def skin():
    return render_template("skin.html")

@application.route("/agree")
def agree():
    return render_template("agree.html")

@application.route("/applyPhoto")
def applyPhoto():
    return render_template("applyPhoto.html")

@application.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save("./uploads/" + secure_filename(f.filename))

        src = os.path.join("./uploads/" + f.filename)
        dst = os.path.join("./static/input/" + f.filename)
        shutil.copyfile(src,dst)

        finding,melanoma,nv,bkl = model(f.filename, model_dir)
        # finding = "Prediction) NV: 95.80%"
        # melanoma,nv,bkl = 3.1762884,95.79547,1.0282432

        return render_template('result.html', image_file = f.filename, finding=finding,mel=melanoma,nv=nv,bkl=bkl)
    else:
        return render_template('applyPhoto.html')
'''
'''
@application.route("/download")
def download():
    global time
    now = time.localtime()
    time = "%04d-%02d-%02d-%02dh-%02dm-%02ds" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    img=ImageGrab.grab()
    saveas="{}{}".format(time,'.png')
    img.save(saveas)
    return flask.send_file(saveas, as_attachment=True)
'''
