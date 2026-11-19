# %%
import json
import shutil
from pathlib import Path

from cmlibs.zinc.context import Context
from cmlibs.zinc.field import Field
from scaffoldmaker.annotation.annotationgroup import findOrCreateAnnotationGroupForTerm

"""
Setup paths
"""
data_path = Path.cwd().parent / "data"
mesh_location = data_path / "_.exf"
mesh_location = mesh_location.as_posix()
output_filename = "_.exf"
annotations_file = data_path / "_.json"
"""
Import landmark annotation coordinates
"""
with open(annotations_file, "r") as f:
    annotations = json.load(f)
annotations = annotations["annotations"]
marker_list = {}
for point in annotations:
    marker_name = ""
    marker_coordinates = ""
    marker_list[marker_name] = marker_coordinates

"""
Create region and load mesh
"""
context = Context("offset_data")
region = context.getDefaultRegion()
fieldmodule = region.getFieldmodule()  # Initiaize field module
region.readFile(mesh_location)
coordinates_field_name = "coordinates"
coordinates_field = fieldmodule.findFieldByName(coordinates_field_name).castFiniteElement()
nodes = fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
node_identifier = nodes.getSize() + 1

"""
Add annotations as markers into mesh
"""
annotation_groups = []
for marker_name, marker_coordinates in marker_list.items():
    annotationGroup = findOrCreateAnnotationGroupForTerm(
        annotation_groups, region, (marker_name, ""), isMarker=True
    )
    annotationGroup.createMarkerNode(node_identifier, coordinates_field, marker_coordinates)
    node_identifier += 1

region.writeFile(output_filename)
shutil.copy(output_filename, data_path)
