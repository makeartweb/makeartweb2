from persistent.mapping import PersistentMapping
from persistent import Persistent
from pyramid  import traversal
from repoze.folder import Folder
from utils import add, get_next_id, add_content, create_svg, autocrop
from uuid import uuid1
import os
import shutil
import ImageFont, ImageDraw
import cStringIO
from PIL import Image
import uuid


class MyModel(PersistentMapping):
    __parent__ = __name__ = None

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = MyModel()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']


class Font(Persistent):
    name = ''
    def __init__(self, path_file=''):
        self.file = FileUpload()
        if os.path.exists(path_file):
            self.file.store(open(path_file, 'rb'))
    
    def getsize(self, text, size):
        font = ImageFont.truetype(self.file.get_path(), size)
        image = Image.new("RGB", font.getsize(" " + text + " "), (255, 255, 255))
        ImageDraw.Draw(image).text((0, 0), " " + text + " ", font=font, fill=(0, 0, 0))
        image = autocrop(image, (255, 255, 255, 0))
        return image.size
    
    def create_svg(self, pathname_bmp, pathname_svg):
        create_svg(pathname_bmp, pathname_svg)
        
    def create_image(self, text, filename, size=100, color=(0, 0, 0), format=None):
        font = ImageFont.truetype(self.file.get_path(), size)
        if format == 'bmp':
            image = Image.new("RGB", font.getsize(" " + text + " "), (255, 255, 255))
        else:
            image = Image.new("RGBA", font.getsize(" " + text + " "), (255, 255, 255, 0))
        ImageDraw.Draw(image).text((0, 0), " " + text + " ", font=font, fill=(color[0], color[1], color[2], 255))
        
        image = autocrop(image, (255, 255, 255, 0))
        
        if isinstance(filename, type(cStringIO.StringIO())):
            format=format or 'png'
            image.save(filename, format)
        else:
            image.save(filename, format)
            
class FileUpload(Persistent):
    hash = None
    def __init__(self):
        self.hash = str(uuid1())
        
    def store(self, fileobj):
        fileobjdest = open('./makeart/uploads/%s' % self.hash, 'wb')
        shutil.copyfileobj(fileobj, fileobjdest)
    
    def retrieve(self):
        return open('./makeart/uploads/%s' % self.hash, 'rb')

    def get_path(self):
        return './makeart/uploads/%s' % self.hash


class Folding(Folder):
    name = ''
    def __init__(self):
        super(Folding, self).__init__()

class ModelWood(Folding):
    def __init__(self):
        super(ModelWood, self).__init__()
    
    def get_sorted_items(self):
        return sorted([item for item in self.values()], key=lambda i: i.order_key)
    
    def remove_item(self, item):
        del self[item.__name__]

    #def __getitem__(self, key):
    #    print key
    #    if key=='makewood':
    #        raise KeyError
    #    super(ModelWood, self).__getitem__(key)
    

class ItemModelWood(Persistent):
    name = ''
    order_key = 0
    model_wood = None
    color = "ff0000"
    font = None
    scale = 1
    max_scale = 2
    min_scale = 1/2
    left = 0
    top = 0
    width = None
    height = None
    ratio = None
    hash = None
    
    def __init__(self):
        super(ItemModelWood, self).__init__()
    
    def get_hash(self):
        if not self.hash:
            self.hash = uuid1()
        return self.hash
        
    def get_model(self):
        if not self.model_wood:
            return self.__parent__
        return self.model_wood
    
    def calc_width_and_height(self):
        font = self.get_font()
        if font:
            self.width, self.height = font.getsize(self.name, 100)
            self.ratio = float(self.width)/self.height
        else:
            raise Exception, 'not found font for calc width and height text'
            
    def get_font(self):
        try:
            font = traversal.find_resource(traversal.find_root(self.get_model()), self.font)
        except:
            return None
        else:
            return font
    