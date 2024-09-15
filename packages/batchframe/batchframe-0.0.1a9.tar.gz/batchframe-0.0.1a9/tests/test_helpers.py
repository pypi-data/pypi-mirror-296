from batchframe import helpers
from batchframe.models.configuration import Configuration

class ConfigChild(Configuration):
    pass

class ConfigGrandChild(ConfigChild):
    pass

def test_get_all_inheritors__gets_grandchildren():
    found_inheritors = helpers.get_all_inheritors(Configuration)

    assert len(found_inheritors) == 2
    assert ConfigChild in found_inheritors
    assert ConfigGrandChild in found_inheritors