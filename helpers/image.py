import os
from PIL import Image
from flask import send_file

def upload_image(image_file, news_id):
    path = os.getcwd()
    save_path = os.path.join(path, 'static/images', news_id + '.jpg')
    # Convert image to JPG format
    image = Image.open(image_file)
    image = image.convert('RGB')
    # Save the image
    image.save(save_path)
    return f"/static/images/{news_id}.jpg"


def get_image(news_id):
    path = os.getcwd()
    image_path = os.path.join(path, 'static/images', news_id + '.jpg')
    # Check if the image file exists
    if not os.path.isfile(image_path):
        image_path = os.path.join(path, 'static/images', 'none.jpg')
    # Return the image file using send_file
    return send_file(image_path, mimetype='image/jpeg')
