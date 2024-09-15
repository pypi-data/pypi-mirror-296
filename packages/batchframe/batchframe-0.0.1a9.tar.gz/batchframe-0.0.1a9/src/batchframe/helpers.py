
def get_all_inheritors(clazz: type):
    subclasses: set[type] = set()
    parents: list[type] = [clazz]
    while parents:
        parent = parents.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                parents.append(child)
    return subclasses