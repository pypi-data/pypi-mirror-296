#
# This is an auto-generated file.  DO NOT EDIT!
#


from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from typing import Union, List, Tuple

from .id_2 import id as id_cls
from .condition_1 import condition as condition_cls
from .observable_3 import observable as observable_cls
from .goal import goal as goal_cls
from .value_24 import value as value_cls
from .lower_bound import lower_bound as lower_bound_cls
from .upper_bound import upper_bound as upper_bound_cls
from .tolerance_8 import tolerance as tolerance_cls
from .as_percentage import as_percentage as as_percentage_cls

class objectives_child(Group):
    fluent_name = ...
    child_names = ...
    id: id_cls = ...
    condition: condition_cls = ...
    observable: observable_cls = ...
    goal: goal_cls = ...
    value: value_cls = ...
    lower_bound: lower_bound_cls = ...
    upper_bound: upper_bound_cls = ...
    tolerance: tolerance_cls = ...
    as_percentage: as_percentage_cls = ...
