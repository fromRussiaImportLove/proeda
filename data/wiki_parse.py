import requests
import os
import wikipedia
import csv
from pytils.translit import slugify
from PIL import Image

IMAGE_SIZE = 480, 480


def down_wiki_data():
    wikipedia.set_lang('ru')
    category = 'Категория:Блюда по алфавиту'
    dishes_name = wikipedia.search('Блюда_по_алфавиту', results=2)
    print('hello')
    for n, dish in enumerate(dishes_name, 1):
        wdish = wikipedia.page(dish)
        if category not in wdish.categories:
            continue
        for image in wdish.images:
            if 'logo' in image or 'jpg' not in image:
                continue
            r_image = image
            break

        if r_image:
            print(f'#Wiki [{n}/{len(dishes_name)}]')
            yield [wdish.title, wdish.summary.replace('\t', ' '), r_image]


def csv_make():
    filepath = 'dishes.csv'
    if not os.path.exists(filepath):
        file = open(filepath, 'w')
        file.close()
    #if not os.path.isdir('wiki'):
    os.makedirs('wiki/thumb', exist_ok=False)

    with open(filepath, 'a', newline='', ) as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t')
        for line in down_wiki_data():
            print(f'Handle dish: {line[0]}', end='\t')
            url = line[2]
            imagename = f'{slugify(line[0])}.jpg'
            imagepath = f'wiki/{imagename}'
            thumb_image_path = f'wiki/thumb/{slugify(line[0])}.jpg'
            line[2] = imagepath
            try:
                if not os.path.exists(imagepath):
                    # image_full = requests.get(url, stream=True).raw
                    with requests.get(url, stream=True) as r:
                        with open(imagepath, "wb") as f:
                            r.raw.decode_content = True
                            # shutil.copyfileobj(r.raw, f)
                            f.write(r.raw.read())
                    print(f'download image', end='\t')
                else:
                    print(f'image download already, skip process', end='\t')
                if not os.path.exists(thumb_image_path):
                    im = Image.open(imagepath)
                    im.thumbnail(IMAGE_SIZE)
                    im.save(thumb_image_path, 'JPEG', quality=90)
                    print(f'thumbed it', end='\t')
                else:
                    print(f'image thumbed already, skip process', end='\t')
                spamwriter.writerow(line)
                print(f'write to csv')
            except Exception as e:
                print(f'{e} on dish {line[0]}')


if __name__ == '__main__':
    csv_make()
