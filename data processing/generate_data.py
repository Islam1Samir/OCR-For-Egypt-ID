import arabic_reshaper
import csv
import random
from PIL import Image, ImageDraw, ImageFont
import pandas as pd


NUM_IMG = 10


df = pd.read_csv('files/Arabic_names.csv')
print(df.Name.head())

names = df.Name


image = Image.open('files/background.jpg')
w, h = image.size
print('image size', image.size)
paths = []
labels = []
for i in range(NUM_IMG):
    name = ''
    for _ in range(4):
        random_name = random.choice(names)
        name += random_name + ' '

    name_text = arabic_reshaper.reshape(name)
    from bidi.algorithm import get_display
    bidi_text = get_display(name_text)

    font = ImageFont.truetype('files/ARIAL.TTF', 30)

    im = image.copy()

    image_draw = ImageDraw.Draw(im)
    text_size = font.getsize(bidi_text)
    padding = 20
    image_draw.text((w - text_size[0] - padding ,70), bidi_text, fill=(0,0,0,255), font=font)

    im.save('../generated image/'+str(i)+".jpg")
    paths.append(str(i)+".jpg")
    labels.append(name_text)

df = pd.DataFrame({'paths':paths, 'labels':labels})
df.to_csv('files/data_labels.csv')