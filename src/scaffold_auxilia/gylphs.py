import json


def glyphs_to_annotation(filename):
    """
    Take a argon scene and convert the point glyphs into annotations for the acuviewer

    :param filename: Description
    """
    with open(filename + ".json", "r") as f:
        data = json.load(f)

    output_data = {"annotations": []}

    labels = data["label"]
    positions = data["positions"]["0"]

    for index, label in enumerate(labels):
        i = index * 3
        point_data = {  # Template
            "body": {"comment": "New", "evidence": []},
            "feature": {
                "geometry": {"coordinates": [], "type": "MultiPoint"},
                "id": "acupoints/CV 3",
                "properties": {"drawn": True, "label": "Drawn annotation"},
            },
            "group": "CV 3",
            "item": {"id": "acupoints/CV 3"},
            "region": "acupoints",
            "resource": "placeholder",
        }
        coordinates = [positions[i], positions[i + 1], positions[i + 2]]
        point_data["feature"]["geometry"]["coordinates"].append(coordinates)
        id = "acupoints/" + label
        point_data["feature"]["id"] = id
        point_data["item"]["id"] = id
        point_data["group"] = label
        output_data["annotations"].append(point_data)

    with open("annotation" + filename + ".json", "w") as f:
        f.write(json.dumps(output_data))
