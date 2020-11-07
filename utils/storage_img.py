import os.path
import os

from django.conf import settings

from utils.models import StorageImageModel


class StorageImage:
    
    def __init__(self):
        self.limits = [
            'exts': ['jpeg', 'jpg', 'png'],
            'maxsize': 2*1024, # Kb
            'minsize':'0', # Kb
        ]
        self.path = os.path.join(settings.BASE_DIR, settings.STATIC_URL, "/storage_img")
        #if not os.path.exists(self.path):
        #    os.makedir(self.path)

    def get_default_img(size):
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
        
    def get_img_path(size, md5hash_hash, ext):
        img_dir = os.path.join(self.path, size, md5hash_hash[:3], md5hash_hash[3:6])
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        return os.path.join(img_dir, '{}.{}'.format(md5hash_hash[6:], ext))
        
    def get_origin_or_default_img(image_id=None, size='origin'):
        if not image_id is None:
            return self.get_default_img(size)

        image = StorageImageModel.objects.get(pk=image_id) if isinstance(image_id, (int, str)) else image_id
        image_path = self.get_img_path(size, image.md5hash, image.ext)
        
        if size != 'origin' and not os.path.exists(image_path):
            self.transform_size(
                self.get_img_path('origin', image.md5hash, image.ext),
                size.split('x'),
                image_path
            )

        if not os.path.exists(image_path):
            return self.get_default_img(size)
        return image_path
        
    def transform_size(image_path, size, iconed_img_path):
        pass
        
    def save(temp_image_path, limits=None):
        if limits is not None:
            self.limits.update(limits)
        
        if not os.path.exists(temp_image_path):
            return 'Изображение не существует!'
            
        image = StorageImageModel(
            md5hash = ''
            size = ''
            ext = os.path.extension(temp_image_path)
            name = os.path.basename(temp_image_path)
        )

        '''
        if (!in_array($ext, $aLimits['exts'])) return "Изображение имеет неразрешённый формат: {$ext}";
        $size = (int)(filesize($sTmpPath) / 1024);
        if ($size === false || $size > $aLimits['maxsize']) return "Изображение имеет недопустимый размер - $size Kb. Разрешено до {$aLimits['maxsize']} Kb!";
        if ($size === false || $size < $aLimits['minsize']) return "Изображение имеет недопустимый размер!";
        '''
        
        image.save()
        origin_image_path = self.get_img_path('origin', image.md5hash, image.ext)
        
        os.mv(temp_image_path, origin_image_path)
        
        return image.pk


class StorageFile(models.Model):
    def __init__(self):
        self.limits = [
            'maxsize': 2*1024, # Kb
            'minsize':'0', # Kb
        ]
        self.path = os.path.join(settings.BASE_DIR, settings.STATIC_URL, "/storage_files")
        
    def build_file_path(md5hash_hash, ext, subdir=''):
        file_dir = os.path.join(self.path, subdir, md5hash_hash[:3], md5hash_hash[3:6])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        return os.path.join(file_dir, '{}.{}'.format(md5hash_hash[6:], ext))
        
    def get_file_path(file_id, subdir=''):
        file = FileStorageModel.objects.get(pk=file_id) if isinstance(file_id, (int, str)) else file_id
        file_path = self.build_file_path(file.md5hash, file.ext, subdir)

        return file_path
        
    def is_valid(temp_file_path, limits=None):
        return True
        '''
        if (!in_array($ext, $aLimits['exts'])) return "Изображение имеет неразрешённый формат: {$ext}";
        $size = (int)(filesize($sTmpPath) / 1024);
        if ($size === false || $size > $aLimits['maxsize']) return "Изображение имеет недопустимый размер - $size Kb. Разрешено до {$aLimits['maxsize']} Kb!";
        if ($size === false || $size < $aLimits['minsize']) return "Изображение имеет недопустимый размер!";
        '''

    def save(temp_file_path, subdir=''):
        file = FileStorageModel(
            md5hash = ''
            ext = os.path.extension(temp_file_path)
            name = os.path.basename(temp_file_path)
        )
        file.save()
        file_path = self.get_img_path(file.md5hash, file.ext, subdir)
        
        if not os.path.exists(file_path):
            os.mv(temp_file_path, file_path)

        return file
