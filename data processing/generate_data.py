import arabic_reshaper
import csv
import random
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import glob

NUM_IMG = 200


df = pd.read_csv('files/Arabic_names.csv')
print(df.Name.head())
names = df.Name


image = Image.open('files/background.jpg')
w, h = image.size
print('image size', image.size)
paths = []
labels = []
filter_nmaes = []
for n in names:
    if  'ء' in n:
        continue
    filter_nmaes.append(n)
for i in range(NUM_IMG):
    name = ''
    for _ in range(4):
        random_name = random.choice(filter_nmaes)
        name += random_name + ' '

    name = name[:-1]
    # name = "خ ح جءءءأإابتثجحخدذرزسشصضطظعغفقكلمنهويؤء"
    # default_reshaper = ArabicReshaper()
    name_text = arabic_reshaper.reshape(name)
    # print(name_text)
    from bidi.algorithm import get_display
    bidi_text = get_display(name_text)
    fonts_paths = glob.glob('files/*.ttf') + glob.glob('files/*.TTF')

    font_path = random.choice(fonts_paths)
    # font_path = 'files/Tajawal-Bold.ttf'
    # print(fonts_paths[7])
    font_size = 23
    font = ImageFont.truetype(font_path, font_size)
    im = image.copy()

    image_draw = ImageDraw.Draw(im)
    text_size = font.getsize(bidi_text)
    while text_size[0] > 260:
        font_size -=1
        font = ImageFont.truetype(font_path, font_size)
        text_size = font.getsize(bidi_text)

    padding = 20
    # print(i)
    # print(text_size)
    if font_path.split('\\')[-1] == 'Hacen Egypt.ttf' or font_path.split('\\')[-1].split('-')[0] == 'Cairo':
        image_draw.text((w - text_size[0] - padding, 115), bidi_text, fill=(0, 0, 0, 255), font=font)
        # print('jjj', text_size)
    elif font_path.split('\\')[-1] == 'Tajawal-Bold.ttf':
        image_draw.text((w - text_size[0] - padding, 130), bidi_text, fill=(0, 0, 0, 255), font=font)
        # print('kk', text_size)
    else:
        image_draw.text((w - text_size[0] - padding, 125), bidi_text, fill=(0, 0, 0, 255), font=font)
        # print('kk', text_size)

    im.save('../generated image/'+str(i)+".jpg")
    paths.append(str(i)+".jpg")
    labels.append(name)
df = pd.DataFrame({'paths':paths, 'labels':labels})
df.to_csv('files/data_labels.csv')