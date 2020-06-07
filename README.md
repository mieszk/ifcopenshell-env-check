An utility for checking geometry output from ifcopenshell
 
## Requirements
- python >= 3.6
- docker (for generating models and CVSs)

## To test
- run `build_envs.py` to create containers with environments
- run `build_models.py` to generate OBJ models and CVSs with product data
- run `report.py` to check diffs between products in different environments
