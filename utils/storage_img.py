import os.path
import os

from django.conf import settings


class StorageImg:
    
    def __init__(self):
        self.limits = [
            'exts': ['jpeg', 'jpg', 'png'],
            'maxsize': 2*1024, # Kb
            'minsize':'0', # Kb
        ]
        self.path = os.path.join(settings.BASE_DIR, settings.STATIC_URL, "/storage_img")
        #if not os.path.exists(self.path):
        #    os.makedir(self.path)

    def get_default(size):
        """
        Возвращает путь на изображение по умолчанию
        :param: size - желаемый размер изображения: "{X}x{Y}" либо "origin"
        """
        size_path = os.path.join(self.path, size)
        if not os.path.exists(size_path):
            os.makedirs(size_path)
        iconed_img_path = os.path.join(size_path, 'default.png')
        origin_img_path = os.path.join('origin', 'default.png')
        
        if size != 'origin' and not os.path.exists(iconed_img_path):
            if os.path.exists(origin_img_path):
                self.transform_size(origin_img_path, size, iconed_img_path)
        
        return iconed_img_path
        
    def get_img_path(size, md5_hash, ext):
        img_dir = os.path.join(self.path, size, md5_hash[:3], md5_hash[3:6])
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        return os.path.join(img_dir, '{}.{}'.format(md5_hash[6:], ext))


class StorageFile(models.Model:
    