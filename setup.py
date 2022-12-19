import base64
from flask import Flask, render_template, request,jsonify
import sqlite3
from PIL import Image
import io
import os

app = Flask(__name__)


@app.route('/')
def index():
    image_data = display_images()
    image = Image.open(io.BytesIO(image_data))
    data_url = image_to_data_url(image)
    return render_template('index.html')


@app.route('/display_images', methods=['POST'])
def display_images():
    counter = 1
    try:
        conn = sqlite3.connect('test1.db')
        cursor = conn.cursor()

        data = cursor.execute("""SELECT * FROM image_tes""")
        #rows = cursor.fetchall()
        images = []
        for x in data.fetchall():
            with open(images,"wb") as f:
                f.write(x[0])
                counter = counter + 1
                conn.commit()

        return jsonify({'images': images})

    except sqlite3.Error as error:
            print("Error while retriving a sqlite table", error)

    finally:
            if conn:
                conn.close()
                print("sqlite connection is closed")
    return  ('images=image_data')

def image_to_data_url(image):

    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    binary_data = buffer.getvalue()

    
    return 'data:image/png;base64,' + base64.b64encode(binary_data).decode()
    return render_template('images.html',images=display_images)


if __name__ == '__main__':
    app.run(debug= True, port=8000)
