import ImageFont, ImageDraw, ImageChops
from PIL import Image
import subprocess
import cStringIO
from pyramid.renderers import get_renderer
import htmlentitydefs
import re


def usemacro(t):
    return get_renderer(t).implementation()

def autocrop(im, bgcolor):
    if im.mode != "RGB":
        im = im.convert("RGB")
    bg = Image.new("RGB", im.size, bgcolor)
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return None # no contents


def create_image(text, filename, format=None):
    font = ImageFont.truetype("./makeart/fonts/ADDLN.TTF", 100)
    image = Image.new("L", font.getsize(" " + text + " "), 'white')
    ImageDraw.Draw(image).text((0, 0), text, font=font)
    
    if isinstance(filename, type(cStringIO.StringIO())):
        format=format or 'png'
        image.save(filename, format)
        #out.seek(0)
    else:
        image.save(filename, format)

def convert(hexcolor, cast=int):
    try:
        match = re.search('^#([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})$', hexcolor)
        return [cast(c) for c in (match and tuple([int('0x%s' % f, 16) for f in match.groups()]) or (0, 0, 0))]
    except:
        return [cast(c) for c in (0, 0.0, 0.0)]
        
    
def create_svg(filename_img, filename_svg):
    subprocess.call(['potrace', filename_img, '--backend', 'svg', '-o', filename_svg])
    
def add(parent, name, item):
    parent[name] = item
    item.__name__ = name
    item.__parent__ = parent
    item.name = name
    return item

def get_next_id(prefix, context):
    i=0
    while (prefix % i) in context:
        i+=1
    return prefix % i

def add_content(parent, content, name):
    content.__name__ = slugfy(name, '-')
    content.name = name
    content.__parent__  = parent
    parent[content.__name__] = content
    return content


def slugfy(text, separator):
    ret = ""
    for c in text.lower():
        try:
            ret += htmlentitydefs.codepoint2name[ord(c)]
        except:
            ret += c
    ret = re.sub("([a-zA-Z])(uml|acute|grave|circ|tilde|cedil)", r"\1", ret)
    ret = re.sub("\W", " ", ret)
    ret = re.sub(" +", separator, ret)
    return ret.strip()

    