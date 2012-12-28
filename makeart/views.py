from pyramid.view import view_config, notfound_view_config
from .models import MyModel
import models
import re
import json
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound
from pyramid import traversal
from utils import create_image, create_svg, usemacro, convert
import cStringIO
import uuid
import urllib
import urllib2
import subprocess
import os

@view_config(context=MyModel, renderer='templates/index.pt')
def my_view(request):
    return {'project':'MakeArt'}



@view_config(context=MyModel, renderer='templates/a-grande-ideia.pt' , name="a-grande-ideia")
def grande_ideia(request):
    return {'project':'MakeArt'}

@view_config(context=models.ItemModelWood, name="remove-item")
def remove_item_wood(context, request):
    try:
        context.get_model().remove_item(context)
    except:
        _json = {'success': False}
    else:
        _json = {'success': True}
    
    return Response( json.dumps(_json), content_type="application/json")
    
@view_config(context=models.ItemModelWood, name="set-item")
def set_item_wood(context, request):
    try:
        data = json.loads(request.GET['data'])
        font = None
        if data.get('font') and data['font'] != context.font:
            font = traversal.find_resource(request.root, data['font'])
            if font:
                context.font = data['font']
                _width, _height = font.getsize(context.name, 100)
                context.ratio = float(_width)/_height
                context.height = context.width/context.ratio
            else:
                raise Exception, "Not Found Resource Font in %s" % data['font']
            
        if data.get('color') and data['color'] != context.color and re.match('^[0-9A-Fa-f]{6}$', data['color']):
            context.color = data['color']
        #print data.get('left') , data.get('top'), 'asasass', data.get('left') and data.get('top')
        
        if data.has_key('left') and data.has_key('top'):
            context.left = data['left']
            context.top = data['top']
            #print data['left'], data['top']
        
        if data.get('width') and data.get('height'):
            context.width = int(data['width'])
            context.height = int(data['height'])            
        
        if not font:
            font = traversal.find_resource(request.root, context.font)
    
    except:
        _json = {'success': False}
    else:
        print context.ratio, context.width, context.height
        print context.left, context.top
        _json = {'success': True,
                 'font_url': request.resource_url(font),
                 'item': dict([(f, getattr(context, f)) for f in ['name', 'color'] ]),
                 'ratio': context.ratio,
                 'width': context.width,
                 'height': context.height
                 }
        
    print _json['success']
    
    return Response( json.dumps(_json), content_type="application/json")

@view_config(context=models.ModelWood, renderer='templates/makewood/makewood.pt')
def makewood(context, request):
    return {'project':'MakeArtWeb', 'master': usemacro('makeart:templates/makewood/master.pt').macros['master'],
            'panel_input': usemacro('makeart:templates/makewood/input.pt').macros['panel_input'],
            'panel_font': usemacro('makeart:templates/makewood/font.pt').macros['panel_font'],
            'panel_add_item': usemacro('makeart:templates/makewood/add_item.pt').macros['panel_add_item'],
            'tabs_views': usemacro('makeart:templates/makewood/tabs_views.pt').macros['tabs_views'],
            'edit_item': usemacro('makeart:templates/makewood/edit_item.pt').macros['edit_item_view'],
            'sorted_items': usemacro('makeart:templates/makewood/item-model-wood.pt').macros['sorted_items'],
            'fonts': [f for f in request.root['fonts'].values()],
            }


@view_config(context=models.ModelWood , name="create-item")
def create_item_wood(context, request):
    try:
        new_item = models.add_content(context, models.ItemModelWood(), request.GET['text'])
    except:
        _json = {'success': False}
    else:
        _json = {'success': True, 'url_context': request.resource_url(new_item)}
        
    return Response( json.dumps(_json), content_type="application/json")


@view_config(context=models.ModelWood, name="edit-order-key")
def edit_order_key(context, request):
    try:
        sort = request.GET['sort']
        items = sort.split(';')
        order = 0 
        for item in items:
            context[item].order_key = order
            order+=1
        print 'okok', sort
    except:
        _json = {'success': False}
    else:
        _json = {'success': True}
    
    return Response( json.dumps(_json), content_type="application/json")

#@view_config(context=models.ItemModelWood, renderer='templates/makewood/item-model-wood.pt', name="get-item")
#def get_item_wood(request):
#    return {}

@view_config(context=models.ItemModelWood, renderer='templates/makewood/font.pt', name="get-page-edit")
def get_page_edit(context, request):
    fonts = request.root['fonts']
    return {'fonts': [fonts[f] for f in fonts]}


@view_config(context=MyModel, name="font")
def server_svg(request):
    return Response(open("../MakeArt/makeart/tmp/0a9f80c4-9bda-4f4b-87bf-1fd68de824ad.svg").read(), content_type="image/svg+xml")

@view_config(context=models.ModelWood, renderer='templates/makewood/item-model-wood.pt', name='menu-sorted-items')
def menu_sorted_items(context, request):
    return {}

@view_config(context=models.Font, name="draw-text")
def draw_text(context, request):
    text = request.GET['text']
    size = int(request.GET['size'] or 12)
    color = convert('#' + request.GET.get('color', '000000'))
    out = cStringIO.StringIO()
    #file_font = context.file.retrieve()
    context.create_image(text, out, size, color, 'png')
    out.seek(0)
    return Response(out.read(), content_type="image/png")

@view_config(context=models.Font, name="raster-text")
def raster(context, request):
    text = request.GET['text']
    filename = uuid.uuid4()
    color = convert('#' + request.GET.get('color', '000000'))
    pathname_bmp = './makeart/tmp/%s.bmp' % filename
    pathname_svg = './makeart/tmp/%s.svg' % filename
    out = cStringIO.StringIO()
    context.create_image(text, out, 100, color, 'png')
    #context.create_image(text, pathname_bmp, 100, (0, 0, 0), 'bmp')
    out.seek(0)
    return Response(out.read(), content_type="image/png")
    #context.create_svg(pathname_bmp, pathname_svg)
    #print pathname_svg
    #return Response(open(pathname_svg, 'rb').read(), content_type="image/svg+xml")

@view_config(context=models.Font, name="raster-text2")
def raster2(context, request):
    text = request.GET['text']
    filename = uuid.uuid4()
    color = convert('#' + request.GET.get('color', '000000'))
    pathname_bmp = './makeart/tmp/%s.bmp' % filename
    pathname_svg = './makeart/tmp/%s.svg' % filename
    #out = cStringIO.StringIO()
    #context.create_image(text, out, 100, color, 'png')
    context.create_image(text, pathname_bmp, 200, (0, 0, 0), 'bmp')
    #out.seek(0)
    #return Response(out.read(), content_type="image/png")
    context.create_svg(pathname_bmp, pathname_svg)
    print pathname_svg
    return Response(open(pathname_svg, 'rb').read(), content_type="image/svg+xml")

def svg_to_3drender(pathname_svg, pathname_jpg, color, angle):
    print pathname_svg, pathname_jpg, color, angle
    cmd = '/home/leandro/blender-2.61/blender --background ../cherrypy/teste.blend --python ../MakeArt/blender-console.py -- --svg={svg} --jpg={jpg} --color={color} --angle={angle}'
    pid = subprocess.Popen(cmd.format(**dict(svg=os.path.abspath(pathname_svg),
                                             jpg=os.path.abspath(pathname_jpg),
                                             color=color, angle='125')),
                            shell=True)
    pid.wait()

@view_config(context=models.Font, name="draw-3d")
def create_blender(context, request):
    text = request.GET['text']
    angle = request.GET['angle']
    size = int(request.GET['size'] or 12)
    color = request.GET.get('color', 'ffffff')#convert('#' + request.GET.get('color', '000000'))
    filename = uuid.uuid4()
    pathname_bmp = './makeart/tmp/%s.bmp' % filename
    pathname_svg = './makeart/tmp/%s.svg' % filename
    pathname_jpg = './makeart/tmp/%s.jpg' % filename
    
    context.create_image(text, pathname_bmp, 200, (0, 0 , 0), 'bmp')
    create_svg(pathname_bmp, pathname_svg)    
    
    svg_to_3drender(pathname_svg, pathname_jpg, color, angle)    
    
    #data = urllib.urlencode({'svg': open(pathname_svg).read(), 'angle': 125, 'color': request.GET.get('color', '000000') })
    #stream = urllib2.urlopen(urllib2.Request('http://localhost:3241/svg_to_blender', data))
    #
    if os.path.exists(pathname_jpg):
        stream = open(pathname_jpg)
        return Response(stream.read(), content_type="image/jpeg")
    else:
        return HTTPNotFound('There is no such resource')
    
    