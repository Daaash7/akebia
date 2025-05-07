import hashlib
import os.path
import shutil
from pathlib import Path
import random

from fastapi import UploadFile, HTTPException
from fastapi.templating import Jinja2Templates

def get_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def save_manufacturer_image(manufacturer_name:str, file:UploadFile):
    return _save_image("static/img/manufacturers_images/", manufacturer_name, file)

def save_product_image(product_name:str, file:UploadFile):
    return _save_image("static/img/products_images/", product_name, file)

def generate_article_number():
    return int(''.join(random.choices('0123456789', k=11)))


def _save_image(path, name, file:UploadFile):
    if not os.path.exists(path):
        os.mkdir(path)

    filename = f'{name}{Path(file.filename).suffix}'
    try:
        with open(f"{path}{filename}", 'wb+') as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    return filename

templates = Jinja2Templates(directory="templates")
