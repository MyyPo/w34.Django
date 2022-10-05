from functools import reduce


def get_from_dict(dataDict, mapList):
    """Iterate nested dictionary"""
    return reduce(dict.get, mapList, dataDict)


def get_available_options(instance):
    index = 0
    available_options = []
    for i in instance.scene.options:
        if "TAG" in instance.scene.options[index]:
            if instance.tags.filter(slug=i["TAG"]):
                available_options.append(i)
        else:
            available_options.append(i)
        index += 1
    return available_options
