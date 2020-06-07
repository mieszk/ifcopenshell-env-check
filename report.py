#!/usr/bin/env python3
import csv
from pathlib import Path

from src.models_generator.product import Product

MODELS_DIRECTORY = "models"


def run():
    for model_dir in Path(MODELS_DIRECTORY).iterdir():
        report_model(model_dir)


def product_from_row(row):
    return Product(
        row[0],
        row[1],
        True if row[2] == "True" else False,
        float(row[3]),
        float(row[4]),
        float(row[5]),
    )


def report_model(model_directory):
    print(f"\n\nReporting {model_directory.stem}")
    all_envs = sorted(Path(model_directory).glob("*.csv"))
    reference_env = all_envs.pop(0)
    ref_products = load_products(reference_env)
    other_products = {env_csv.stem: load_products(env_csv) for env_csv in all_envs}
    for product in ref_products.values():
        for env_name, product_map in other_products.items():
            other_product = product_map[product.guid]
            compare(product, other_product, env_name)


def load_products(csv_file):
    products = {}
    with open(csv_file, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                product = product_from_row(row)
            except IndexError:
                print(f"Index error at row {row}")
                pass
            else:
                products[product.guid] = product
    return products


def compare(product, other, env_name):
    if product != other:
        print(f"Diff in {env_name}")
        print(f"Reference: {product}")
        print(f"Compared:  {other}\n")


if __name__ == "__main__":
    import os, sys
    run()
