###############################################################################
#                                                                             #
# This file is part of IfcOpenShell.                                          #
#                                                                             #
# IfcOpenShell is free software: you can redistribute it and/or modify        #
# it under the terms of the Lesser GNU General Public License as published by #
# the Free Software Foundation, either version 3.0 of the License, or         #
# (at your option) any later version.                                         #
#                                                                             #
# IfcOpenShell is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
# Lesser GNU General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the Lesser GNU General Public License    #
# along with this program. If not, see <http://www.gnu.org/licenses/>.        #
#                                                                             #
###############################################################################
# type: ignore

from collections import namedtuple

from OCC.Core import TopoDS, gp, BRepTools

shape_tuple = namedtuple('shape_tuple', ('data', 'geometry', 'styles'))

handle, main_loop, add_menu, add_function_to_menu = None, None, None, None

DEFAULT_STYLES = {
    "DEFAULT": (.7, .7, .7),
    "IfcWall": (.8, .8, .8),
    "IfcSite": (.75, .8, .65),
    "IfcSlab": (.4, .4, .4),
    "IfcWallStandardCase": (.9, .9, .9),
    "IfcWall": (.9, .9, .9),
    "IfcWindow": (.75, .8, .75, .3),
    "IfcDoor": (.55, .3, .15),
    "IfcBeam": (.75, .7, .7),
    "IfcRailing": (.65, .6, .6),
    "IfcMember": (.65, .6, .6),
    "IfcPlate": (.8, .8, .8)
}


def yield_subshapes(shape):
    it = TopoDS.TopoDS_Iterator(shape)
    while it.More():
        yield it.Value()
        it.Next()


def set_shape_transparency(ais, t):
    handle.Context.SetTransparency(ais, t)


def get_bounding_box_center(bbox):
    bbmin = [0.] * 3
    bbmax = [0.] * 3
    bbmin[0], bbmin[1], bbmin[2], bbmax[0], bbmax[1], bbmax[2] = bbox.Get()
    return gp.gp_Pnt(*map(lambda xy: (xy[0] + xy[1]) / 2., zip(bbmin, bbmax)))


def serialize_shape(shape):
    shapes = BRepTools.BRepTools_ShapeSet()
    shapes.Add(shape)
    return shapes.WriteToString()


def create_shape_from_serialization(brep_object):
    brep_data, occ_shape, styles = None, None, ()

    is_product_shape = True
    try:
        brep_data = brep_object.geometry.brep_data
        styles = brep_object.geometry.surface_styles
    except BaseException:
        try:
            brep_data = brep_object.brep_data
            styles = brep_object.surface_styles
            is_product_shape = False
        except BaseException:
            pass

    styles = tuple(styles[i:i + 4] for i in range(0, len(styles), 4))

    if not brep_data:
        return shape_tuple(brep_object, None, styles)

    try:
        ss = BRepTools.BRepTools_ShapeSet()
        ss.ReadFromString(brep_data)
        occ_shape = ss.Shape(ss.NbShapes())
    except BaseException:
        pass

    if is_product_shape:
        return shape_tuple(brep_object, occ_shape, styles)
    else:
        return occ_shape
