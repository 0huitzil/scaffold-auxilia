from cmlibs.zinc.field import (
    Field,
    FieldFindMeshLocation,
    FieldFiniteElement,
    FieldGroup,
    FieldStoredMeshLocation,
    FieldStoredString,
)
from cmlibs.zinc.node import Node
from scaffoldmaker.annotation.annotationgroup import (
    findOrCreateAnnotationGroupForTerm,
    getAnnotationMarkerNameField,
)


def create_marker_node_no_mesh(annotation_group, node_identifier,
                               materialCoordinatesField: FieldFiniteElement,
                               materialCoordinates: list, is_datapoint: True) -> Node:
    """
    Reconstruction of the similar function from scaffoldmaker.annotation.annotationgroup,
    used to add markers to a dataset which does not contain a mesh, such as a
    pointcloud (the original function only allows the insertion of markers on a region
    with an existing mesh.
    :param materialCoordinatesField: Material coordinates field to define
    location of marker point in.
    Must be a finite element type field for which isTypeCoordinates() is True
    with up to 3 components,
    and at least as many components as the highest mesh dimension.

    :param materialCoordinates: The coordinates to assign to the materialCoordinatesField.
        If supplied, the element:xi location is computed from it. 
        If not supplied its values are computed at the
        current element:xi location.
    :return markerNode: Zinc Node representing marker point, with either default location
        in first element or that supplied.
    """
    fieldmodule = annotation_group.getGroup().getFieldmodule()
    coordinatesCount = materialCoordinatesField.getNumberOfComponents()
    assert (len(materialCoordinates) >= coordinatesCount) and \
            materialCoordinatesField.castFiniteElement().isValid() and \
            materialCoordinatesField.isTypeCoordinate() \
    # Create template and corresponding fields
    markerName = getAnnotationMarkerNameField(fieldmodule)
    if is_datapoint:
        nodeset = fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
    else:
        nodeset = fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
    annotation_group._materialCoordinatesField = materialCoordinatesField
    annotation_group._markerMaterialCoordinatesField = materialCoordinatesField
    nodeTemplate = nodeset.createNodetemplate()
    nodeTemplate.defineField(materialCoordinatesField)
    nodeTemplate.defineField(markerName)
    # Create marker node
    markerNode = nodeset.createNode(node_identifier, nodeTemplate)
    annotation_group._markerIdentifier = node_identifier
    # Add marker node to group of marker nodes
    annotation_group.getNodesetGroup(nodeset).addNode(markerNode)
    # Add marker noche to cache and assign name and coordinates
    fieldcache = fieldmodule.createFieldcache()
    fieldcache.setNode(markerNode)
    markerName.assignString(fieldcache, annotation_group._name)
    annotation_group._markerMaterialCoordinatesField.assignReal(
        fieldcache, materialCoordinates
        )
    return markerNode