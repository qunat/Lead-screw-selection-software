#!/usr/bin/env python

##Copyright 2016 Thomas Paviot (tpaviot@gmail.com)
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU Lesser General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Lesser General Public License for more details.
##
##You should have received a copy of the GNU Lesser General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

import random

from OCC.Display.WebGl import x3dom_renderer
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.gp import gp_Vec

from core_geometry_utils import translate_shp, rotate_shp_3_axis

my_ren = x3dom_renderer.X3DomRenderer()
trans_box = translate_shp(rotated_box, gp_Vec(tr_x, tr_y, tr_z))
my_ren.DisplayShape(trans_box, export_edges=True, color=rnd_color, transparency=random.random())
my_ren.render()
