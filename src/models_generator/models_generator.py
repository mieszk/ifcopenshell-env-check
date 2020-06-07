import csv
from pathlib import Path

import ifcopenshell.geom

from .product import Product
from .wavefront_writer import write_shapes


def create_models(files_dir, output_dir, env_name):
    """Checks all IFC files in specified directory."""
    print(f"Environment: {env_name}")
    for file in Path(files_dir).glob("*.ifc"):
        model_name = file.stem
        print(f"Creating models with env {env_name}: {model_name}")

        model_directory = Path(output_dir) / model_name
        model_directory.mkdir(exist_ok=True)

        csv_filename = env_name + ".csv"
        csv_path = model_directory / csv_filename

        obj_filename = env_name + ".obj"
        obj_path = model_directory / obj_filename

        ifc = ifcopenshell.open(str(file))

        if csv_path.exists() and obj_path.exists():
            print(f"Model {model_name} already created. Skipping.")
            return

        shape_map = create_shapes(ifc)

        products = create_products(ifc, shape_map)
        serialize_products(products, csv_path)
        write_model(obj_path, shape_map)


def create_shapes(ifc):
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)

    it = ifcopenshell.geom.iterator(settings, ifc)

    shape_map = {}
    valid_file = it.initialize()
    if valid_file:
        while 1:
            shape = it.get()
            shape_map[shape.data.guid] = shape.geometry
            if not it.next():
                break
    return shape_map


def create_products(ifc, shape_map):
    products = {}
    for prod in ifc.by_type("IfcProduct"):
        if not prod.is_a("IfcOpeningElement") and prod.Representation is not None:
            product = Product(prod.GlobalId, prod.Name)
            shape = shape_map.get(prod.GlobalId, None)
            if shape is not None:
                product.load_shape(shape)
            products[product.guid] = product
    return products


def serialize_products(products, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["guid", "name", "valid_shape", "length", "area", "volume"])
        for product in products.values():
            writer.writerow(
                [
                    product.guid,
                    product.name,
                    product.has_valid_shape,
                    product.length,
                    product.area,
                    product.volume,
                ]
            )


def write_model(obj_filename, shape_map):
    with open(obj_filename, "w") as outfile:
        write_shapes(outfile, shape_map)
