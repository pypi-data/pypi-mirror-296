import json
from inspect import Signature
from typing import Callable
from collections import Counter


class Value:
    def __init__(self, value=None, **kwargs):
        self.value = value
        self.kwargs = kwargs

    @property
    def response(self):
        # TODO: Build this out to do all of the necessary formatting and data cleaning
        if self.value:
            return self.value
        else:
            return self.kwargs


class Error:
    def __init__(self, message: str):
        self.message = str(message)

    @property
    def response(self):
        return {"error": self.message}


class Extend:
    def __init__(self, extend=True):
        self.extend = extend

    @property
    def response(self):
        return {"extend": self.extend}


def __build_params(func: Callable, event: dict, parameter_names: list[str]):
    params = {}
    for i, param in enumerate(Signature.from_callable(func).parameters):
        if param in parameter_names or f"{param}_" in parameter_names:
            params[param] = event.get(param)
        else:
            params[param] = event.get(parameter_names[i])
    return params


def response_bot(func):
    def wrapper(event, context=None):
        params = __build_params(
            func, event, parameter_names=["value", "input", "context", "parameters"]
        )
        result = func(**params)
        if isinstance(result, Value) or isinstance(result, Error):
            return {"value": result.response}
        else:
            return {"value": result}

    wrapper.local = func
    return wrapper


def result_bot(func):
    def wrapper(event, context=None):
        params = __build_params(
            func,
            event,
            parameter_names=["responses", "workers", "input", "context", "parameters"],
        )
        result = func(**params)
        if (
            isinstance(result, Value)
            or isinstance(result, Error)
            or isinstance(result, Extend)
        ):
            return {"value": result.response}
        else:
            return {"value": result}

    wrapper.local = func
    return wrapper


def text_agreement(values: list[str], count: int):
    counter = Counter([v.strip() for v in values])
    mc = counter.most_common(1)
    if mc[0][1] >= count:
        return mc[0][0]
    else:
        return None
