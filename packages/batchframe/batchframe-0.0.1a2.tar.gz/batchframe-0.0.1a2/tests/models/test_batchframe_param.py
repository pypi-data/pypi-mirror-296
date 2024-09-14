from batchframe.models.batchframe_param import BatchframeParam, get_injectable_init_params, cast_param_to_type
from dataclasses import dataclass
import inspect
from datetime import datetime

@dataclass
class ParamTestClass():
    normal_str_param: str
    batchframe_str_param: BatchframeParam[str]
    batchframe_int_param_with_def_val: BatchframeParam[int] = 42


def test_get_injectable_init_params__should_detect_correct_number_of_params():
    result = get_injectable_init_params(ParamTestClass)
    assert len(result) == 2

def test_get_injectable_init_params__should_detect_default_values():
    result = get_injectable_init_params(ParamTestClass)
    param_name_def_val_dict = {entry[0]: entry[2] for entry in result}
    assert param_name_def_val_dict['batchframe_str_param'] is inspect._empty
    assert param_name_def_val_dict['batchframe_int_param_with_def_val'] == 42

def test_get_injectable_init_params__should_detect_injectable_types():
    result = get_injectable_init_params(ParamTestClass)
    param_name_type_dict = {entry[0]: entry[1] for entry in result}
    assert param_name_type_dict['batchframe_str_param'] is str
    assert param_name_type_dict['batchframe_int_param_with_def_val'] is int

def test_cast_param_to_type__should_handle_str():
    result = cast_param_to_type(str, 'input') == 'input'

def test_cast_param_to_type__should_handle_int():
    assert cast_param_to_type(int, '1') == 1

def test_cast_param_to_type__should_handle_float():
    assert cast_param_to_type(float, '1.5') == 1.5

def test_cast_param_to_type__should_handle_datetime():
    assert cast_param_to_type(datetime, '2024-03-02') == datetime(year=2024, month=3, day=2)
    assert cast_param_to_type(datetime, '2024-03-02T13:12:11') == datetime(year=2024, month=3, day=2, hour=13, minute=12, second=11)