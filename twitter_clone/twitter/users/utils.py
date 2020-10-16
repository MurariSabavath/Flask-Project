import os
import secrets
from flask import current_app
from PIL import Image

def crop_image(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)

    im = Image.open(form_picture)

    width, height = im.size
    new_height, new_width = height, height

    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    new_im = im.crop((left, top, right, bottom))
    new_im.save(picture_path)

    return picture_fn
