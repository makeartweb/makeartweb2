import bpy

from io_curve_svg import import_svg #module blender
from mathutils import Matrix, Vector

import io
import subprocess
import re
import math
import getopt
import sys

def convert(hexcolor, cast=int):
    try:
        match = re.search('^#?([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})$', hexcolor)
        print (match, hexcolor)
        return [cast(c) for c in (match and tuple([int('0x%s' % f, 16) for f in match.groups()]) or (0, 0, 0))]
    except:
        return [cast(c) for c in (0, 0.0, 0.0)]



def svg_to_blender(file_svg, angle, color, file_jpg):
    color = convert(color, float)

    #seleciona os curvs e meshs para apaga-los
    if len([i for i in bpy.data.objects if i.type in ['CURVE', 'MESH']])>0:
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except:
            pass
        bpy.ops.object.select_by_type(type="CURVE")
        bpy.ops.object.delete(use_global=True)
        bpy.ops.object.select_by_type(type="MESH")
        bpy.ops.object.delete(use_global=True)
    
    #carrega o svg
    import_svg.load_svg(file_svg)
    bpy.ops.material.new()
    #define a cor do material
    bpy.data.materials[0].diffuse_color = tuple([c/255.0 for c in color ])
    
    #para todos os objetos do tipo curve faz um convert
    for o in bpy.data.objects:
        print (o.type, o.name)
        if o.type == 'CURVE':
            bpy.ops.object.select_name(name=o.name)
            bpy.ops.object.convert(target='MESH', keep_original=False)
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='TOGGLE')
            bpy.ops.mesh.extrude()
            
            bpy.ops.transform.translate(value=(0.0, 0.0, -0.3))
            o.active_material = bpy.data.materials[0]
            bpy.ops.object.editmode_toggle()
    
    #seleciona todos os meshs para fazer um join
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.join()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.ops.object.select_all(action='DESELECT')

    meshs = [i for i in bpy.data.objects if i.type  == 'MESH']
    for mesh in meshs:
        mesh.location = (0.0 , 0.0, 0.0)
    if meshs:
        dimensions = meshs[0].dimensions
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.transform.resize(value=(8.250/dimensions[0], 8.250/dimensions[0], 1.0))

    camera = [i for i in bpy.data.objects if i.type  == 'CAMERA']
    
    if camera:
        bpy.ops.object.select_name(name="Camera")
        _angle = math.radians(float(angle or 0.0)) #math.radians(float(angle or 0.0))
        camera[0].location = (0.0, 10* math.cos(_angle), 10* math.sin(_angle))
        camera[0].rotation_euler = (math.radians(-90.0+float(angle or 0.0)), 0.0, 0.0)

    obj_camera = [obj for obj in bpy.data.objects if obj.type =='CAMERA']
    scene_key = bpy.data.scenes.keys()
    
    #bpy.ops.wm.save_mainfile(filepath="/tmp/make3d.blend" )
    
    if obj_camera and scene_key:
        scene_key = scene_key[0]
        bpy.data.scenes[scene_key].camera = obj_camera[0]
        bpy.data.scenes[scene_key].render.image_settings.file_format = 'JPEG' 
        bpy.data.scenes[scene_key].render.filepath = file_jpg
        bpy.data.scenes[scene_key].render.resolution_x = 1024
        bpy.data.scenes[scene_key].render.resolution_y = 768
        bpy.ops.render.render( write_still=True )
    
def blender_svg_to_3d_render():
    
    index = sys.argv.index('--')
    options, ramainder = getopt.getopt(sys.argv[index+1:], '', ['svg=', 'jpg=', 'color=', 'angle='])
    for opt, arg in options:
        if opt in ('--svg'):
            path_svg = arg
        if opt in ('--jpg'):
            path_jpg = arg
        if opt in ('--color'):
            color = arg
        if opt in ('--angle'):
            angle = arg
    svg_to_blender(path_svg, angle, color, path_jpg)

blender_svg_to_3d_render()