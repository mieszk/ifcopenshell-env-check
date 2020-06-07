from itertools import chain

from OCC.Core import (
    gp,
    BRep,
    BRepMesh,
    Poly,
    TopAbs,
    TopLoc,
    Bnd,
    BRepBndLib,
    TopExp,
)

DEFLECTION = 1e-3


def write_shapes(obj_file, shape_map):
    index = 0

    for name, geometry in shape_map.items():
        if geometry is None:
            return

        # verify bounding box to prevent crashing due to empty shape
        bbox = Bnd.Bnd_Box()
        BRepBndLib.brepbndlib_Add(geometry, bbox)
        if bbox.IsVoid():
            print(f"Cannot serialize shape {name} due to invalid shape.")
            return

        mesh = BRepMesh.BRepMesh_IncrementalMesh(geometry, DEFLECTION).Shape()

        all_vertices = []
        all_triangles = []

        location = TopLoc.TopLoc_Location()
        tool = BRep.BRep_Tool()

        for face in iter_faces(mesh):
            face_vertices, face_triangles = triangulate_face(face, location, tool)
            all_vertices.extend(face_vertices)
            max_idx = max(chain.from_iterable(all_triangles)) if all_triangles else 0
            for polygon in face_triangles:
                all_triangles.append(tuple(p + max_idx for p in polygon))

        updated_triangles = [tuple(p + index for p in polygon) for polygon in all_triangles]
        index += max(chain.from_iterable(all_triangles))

        serialized_mesh = serialize_mesh(name, all_vertices, updated_triangles)
        obj_file.write(serialized_mesh)


def serialize_mesh(name, vertices, faces):
    mesh = f"g {name}\n"

    vertex_fmt = "v {:f} {:f} {:f}\n"
    for vertex in vertices:
        mesh += vertex_fmt.format(*vertex)

    face_fmt = "f {:d} {:d} {:d}\n"
    for face in faces:
        mesh += face_fmt.format(*face)

    return mesh


def triangulate_face(face, location, tool):
    tri = tool.Triangulation(face, location)
    if tri is None:
        return None

    nodes = tri.Nodes()
    triangles = tri.Triangles()
    surface_vertices = []
    surface_polygons = []

    for i in range(tri.NbNodes()):
        node: gp.gp_Pnt = nodes.Value(i + 1).Transformed(location.Transformation())
        surface_vertices.append((node.X(), node.Y(), node.Z()))

    for i in range(tri.NbTriangles()):
        triangle: Poly.Poly_Triangle = triangles.Value(i + 1)
        n1, n2, n3 = triangle.Get()
        if face.Orientation() == TopAbs.TopAbs_REVERSED:
            surface_polygons.append((n3, n2, n1))
        else:
            surface_polygons.append((n1, n2, n3))

    return surface_vertices, surface_polygons


def iter_faces(shape):
    exp = TopExp.TopExp_Explorer(shape, TopAbs.TopAbs_FACE)
    while exp.More():
        yield exp.Current()
        exp.Next()
