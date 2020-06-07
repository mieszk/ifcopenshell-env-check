def make_bbox(shape):
    from OCC.Core import Bnd, BRepBndLib

    bbox = Bnd.Bnd_Box()
    BRepBndLib.brepbndlib_Add(shape, bbox)
    return bbox


def get_length(shape):
    """total length of edges"""
    from OCC.Core import GProp, BRepGProp

    gprops = GProp.GProp_GProps()
    BRepGProp.brepgprop_LinearProperties(shape, gprops)
    return gprops.Mass()


def get_area(shape):
    """total area of faces"""
    from OCC.Core import GProp, BRepGProp

    gprops = GProp.GProp_GProps()
    BRepGProp.brepgprop_SurfaceProperties(shape, gprops)
    return gprops.Mass()


def get_volume(shape):
    from OCC.Core import GProp, BRepGProp

    gprop = GProp.GProp_GProps()
    BRepGProp.brepgprop_VolumeProperties(shape, gprop)
    return gprop.Mass()


def is_valid_shape(shape):
    from OCC.Core import TopExp, TopAbs

    if shape is None:
        return False
    explorer = TopExp.TopExp_Explorer(shape, TopAbs.TopAbs_FACE)
    if not explorer.More():
        return False
    return True


def almost_equals(val1, val2, tol=1e-3):
    try:
        return abs(val1 / val2) - 1 < tol
    except ZeroDivisionError:
        return False


class Product:
    def __init__(
        self, guid, name, has_valid_shape=False, length=0.0, area=0.0, volume=0.0,
    ):
        self.guid = guid
        self.name = name

        self.has_valid_shape = has_valid_shape
        self.length = float(length)
        self.area = float(area)
        self.volume = float(volume)

    def load_shape(self, shape):
        self.has_valid_shape = is_valid_shape(shape)
        self.length = get_length(shape)
        self.area = get_area(shape)
        self.volume = get_volume(shape)

    def __eq__(self, other):
        return (
            self.guid == other.guid
            and self.name == other.name
            and self.has_valid_shape == other.has_valid_shape
            and almost_equals(self.length, other.length)
            and almost_equals(self.area, other.area)
            and almost_equals(self.volume, other.volume)
        )

    def __repr__(self):
        fmt = (
            "Product(guid={}, name={}, has_valid_shape={}, length={:.4f}, "
            "area={:.4f}, volume={:.4f})"
        )
        return fmt.format(
            self.guid, self.name, self.has_valid_shape, self.length, self.area, self.volume,
        )
