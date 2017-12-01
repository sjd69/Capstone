def get_obj(content, obj_type, name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, obj_type, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj
