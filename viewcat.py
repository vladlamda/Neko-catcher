
from flsdk import *
import os,sys
import json #謎の拡張子
import re
import sys

app=Flask(__name__)
app.secret_key='nekokawaii'

#getcat
image_ptrn=re.compile('.*[.](jpg|jpeg|png|bmp|gif)$')
image_dir=os.path.join('static','img')
images=[]
images=[images for image in os.listdir(image_dir)if re.match(image_ptrn,image)]
if not len(images):
    sys.exit('Error:404 Not found cats images')

logf=open('log.dat','w')

pos=0

@app.route('/')
def index():
    global pos
    #pos and neg files
    global positive
    global negative

    positive=open('info.dat','a')
    negative=open('bg.txt','a')
    #first cat pic
    imgsrc=os.path.join(image_dir,images[pos])
    imgnum=len(images)
    count=pos
    counter=''.join([str(pos+1).zfill(len(str(imgnum))),'of',str(imgnum)])
    return render_template('index.html',imgsrc=imgsrc, imgnum=imgnum,count=count,counter=counter)

@app.route('/_next')
def _next():
    global pos
    #skip the pic or not
    skip=request.args.get('skip')
    if skip==u'0':
        #囲まれた範囲の座標
        coords=request.args.get('coords')
        coords=json.loads(coords)
        #処理中の画像のpath
        image_path =os.path.join(image_dir,images[pos])
        #yes or # NOTE
        if len(coords)==0:
            negative.write(''.join([image_path,'\n']))
            logf.write(''.join([image_path,'\n']))
            logf.flush()
        else:
            s=''
            for coord in coords:
                s='  '.join([s,'  '.join([str(int(e))for e in coord])])

            positive.write('%s %d%s\n'%(image_path,len(coords),s))
            logf.write("%s %d%s\n"%(image_path,len(coords),s))
            logf.flush()
    #other cat pics is available?
    if pos+1>=len(images):
        imgsrc=""
        finished=True
        pos=pos+1
        logf.close()
        negative.close()
        positive.close()
    else:
        finished=False
        imgsrc=os.path.join(image_dir,images[pos+1])
        pos=pos+1
    return jsonify(imgsrc=imgsrc,finished=finished,count=pos)

if __name__=='__main__':
    app.debug=True
    app.run()
