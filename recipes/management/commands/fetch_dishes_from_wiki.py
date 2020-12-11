import csv
import os

import requests
import wikipedia
from PIL import Image
from django.conf import settings
from django.core.management.base import BaseCommand
from pytils.translit import slugify

IMAGE_SIZE = 480, 480


class Command(BaseCommand):
    help = 'Generate recipes: names, description and photo from ru.wikipedia'

    def down_wiki_data(self):
        wikipedia.set_lang('ru')
        category = 'Категория:Блюда по алфавиту'
        dishes_name = wikipedia.search('Блюда_по_алфавиту', results=200)
        self.stdout.write('hello')
        for n, dish in enumerate(dishes_name, 1):
            r_image = False
            wdish = wikipedia.page(dish)
            if category not in wdish.categories:
                continue
            for image in wdish.images:
                if 'logo' in image or 'jpg' not in image:
                    continue
                r_image = image
                break

            if r_image:
                self.stdout.write(f'#Wiki [{n}/{len(dishes_name)}]')
                yield [wdish.title, wdish.summary.replace('\t', ' '), r_image]

    def handle(self, *args, **options):

        filepath = os.path.join(settings.BASE_DIR, "data/dishes.csv")
        media_path = settings.MEDIA_ROOT
        original_image_dir = os.path.join(settings.BASE_DIR, 'data/wiki')
        os.makedirs(original_image_dir, exist_ok=True)
        thumb_dir = os.path.join(media_path, 'wiki')
        os.makedirs(thumb_dir, exist_ok=True)

        if not os.path.exists(filepath):
            file = open(filepath, 'w')
            file.close()

        with open(filepath, 'a', newline='', ) as csvfile:
            spamwriter = csv.writer(csvfile, delimiter='\t')
            for line in self.down_wiki_data():
                self.stdout.write(f'Handle dish: {line[0]}', ending='\t')
                url = line[2]
                imagename = f'{slugify(line[0])}.jpg'
                imagepath = os.path.join(original_image_dir, imagename)
                thumb_image_path = os.path.join(
                    thumb_dir, f'{slugify(line[0])}_.jpg')
                line[2] = thumb_image_path
                try:
                    if not os.path.exists(imagepath):
                        with requests.get(url, stream=True) as r:
                            with open(imagepath, "wb") as f:
                                r.raw.decode_content = True
                                f.write(r.raw.read())
                        self.stdout.write('download image', ending='\t')
                    else:
                        self.stdout.write('image download already, skip it',
                                          ending='\t')
                    if not os.path.exists(thumb_image_path):
                        im = Image.open(imagepath)
                        im.thumbnail(IMAGE_SIZE)
                        im.save(thumb_image_path, 'JPEG', quality=90)
                        self.stdout.write('thumbed it', ending='\t')
                    else:
                        self.stdout.write('image thumbed already, skip it',
                                          ending='\t')
                    spamwriter.writerow(line)
                    self.stdout.write('write to csv')
                except Exception as e:
                    self.stdout.write(f'{e} on dish {line[0]}')
            self.stdout.write('job is done')
