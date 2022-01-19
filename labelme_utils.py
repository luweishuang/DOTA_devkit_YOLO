# -*- coding: utf-8 -*-
import sys
import codecs
import shapely.geometry as shgeo
import os
import json

"""
    some basic functions which are useful for process DOTA data
"""
classnames_powertower = ["broken","laughcrack","damage","corroison","rust","endjump","bondlinebroken","straightpipebend"]


def custombasename(fullname):
    return os.path.basename(os.path.splitext(fullname)[0])


def GetFileFromThisRootDir(dir,ext = None):
  allfiles = []
  needExtFilter = (ext != None)
  for root,dirs,files in os.walk(dir):
    for filespath in files:
      filepath = os.path.join(root, filespath)
      extension = os.path.splitext(filepath)[1][1:]
      if needExtFilter and extension in ext:
        allfiles.append(filepath)
      elif not needExtFilter:
        allfiles.append(filepath)
  return allfiles


def parse_labelme_poly(cur_jsonf):
    src_data = json.load(open(cur_jsonf))
    # Convert the data
    objects = []
    for cur_ins in src_data['shapes']:
        object_struct = {}
        object_struct['name'] = cur_ins['label']
        object_struct['difficult'] = '0'
        object_struct['poly'] = []
        cur_pts = cur_ins['points']
        for port in cur_pts:
            object_struct['poly'].append((float(port[0]), float(port[1])))
        gtpoly = shgeo.Polygon(object_struct['poly'])
        object_struct['area'] = gtpoly.area
        objects.append(object_struct)
    return objects


def parse_longsideformat(filename):  # filename=??.txt
    """
        parse the longsideformat ground truth in the format:
        objects[i] : [classid, x_c, y_c, longside, shortside, theta]
    """
    objects = []
    f = []
    if (sys.version_info >= (3, 5)):
        fd = open(filename, 'r')
        f = fd
    elif (sys.version_info >= 2.7):
        fd = codecs.open(filename, 'r')
        f = fd
    # count = 0
    while True:
        line = f.readline()
        if line:
            splitlines = line.strip().split(' ')
            object_struct = {}
            ### clear the wrong name after check all the data
            #if (len(splitlines) >= 9) and (splitlines[8] in classname):
            if (len(splitlines) < 6) or (len(splitlines) > 6):
                print('labels长度不为6,出现错误,与预定形式不符')
                continue
            object_struct = [int(splitlines[0]), float(splitlines[1]),
                             float(splitlines[2]), float(splitlines[3]),
                             float(splitlines[4]), float(splitlines[5])
                            ]
            objects.append(object_struct)
        else:
            break
    return objects





