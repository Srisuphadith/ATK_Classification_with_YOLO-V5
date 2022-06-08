"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import os
from PIL import Image
import mysql.connector
import torch, json
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def predict():
    
    if request.method == "POST":
        if "image" not in request.files:
            return redirect(request.url)
        file = request.files["image"]
        if not file:
            return
        username = request.form['student_id']
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model(img, size=640)
        
        # for debugging
        data = results.pandas().xyxy[0].to_json(orient="records")
        mydata = json.loads(data)

        temp = []
        result = ""

        for i in mydata:
            temp.append(i['name'])
        print(temp)
        for i in temp:
            if i == 'Negative':
                result = i
            if i == 'Positive':
                result = i
        mydata = result
        path_img = ((str(file).split())[1]).strip("'")
        path_img = (path_img.split("."))[0]
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="",
          database="ATK_management"
        )
        mycursor = mydb.cursor()
        #/Users/srisuphadith/AI2022/yolov5-flask/static/img_atk/
        sql = "INSERT INTO image_src (student_id,image) VALUES (%s, %s)"
        val = (f"{username}",f"/Users/srisuphadith/AI2022/yolov5-flask/static/img_atk/{path_img}.jpg")
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        sql = "UPDATE student_list SET Result = (%s) WHERE student_id = (%s);"
        val = (f"{result}",f"{username}")
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        
        #return data

        results.render()  # updates results.imgs with boxes and labels
        
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            img_base64.save(f"/Users/srisuphadith/AI2022/yolov5-flask/static/img_atk/{path_img}.jpg", format="JPEG")
        #return redirect("static/image0.jpg")
        return render_template("display.html", label=mydata, imagesource='static/img_atk/'+path_img+'.jpg')

    return render_template("index2.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

   #  model = torch.hub.load(
#         "ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True, autoshape=True
#     )  # force_reload = recache latest code
    model = torch.hub.load('./yolov5', 'custom', path='best59posneg.pt', source='local')
    model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat


