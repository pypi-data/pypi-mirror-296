#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者:[郭磊]
手机:[5210720528]
email:[174000902@qq.com]
github:[https://github.com/guolei19850528/guolei_py3_images]
=================================================
"""
import os

from addict import Dict
from jsonschema.validators import Draft202012Validator
from jsonschema import validate
import imgkit


def from_string(
        output_path: str = "",
        string: str = "",
        imgkit_from_string_func_kwargs: dict = {}
):
    """
    call imgkit.from_string(output_path=output_path, string=string, **imgkit_from_string_func_kwargs)
    :param output_path:
    :param string:
    :param imgkit_from_string_func_kwargs:
    :return:
    """
    validate(instance=string, schema={"type": "string", "minLength": 1})
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(
            isinstance(imgkit_from_string_func_kwargs, dict)):
        imgkit_from_string_func_kwargs = {}
    imgkit_from_string_func_kwargs = Dict(imgkit_from_string_func_kwargs)
    imgkit.from_string(
        output_path=output_path,
        string=string,
        **imgkit_from_string_func_kwargs.to_dict(),
    )
    return output_path
