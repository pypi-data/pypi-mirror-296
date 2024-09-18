import importlib


def dynamic_func(module_name: str, function_name: str):
    """
    动态调用函数
    :param module_name:
    :param function_name:
    :return:
    """
    module = importlib.import_module(module_name)
    function = getattr(module, function_name)
    return function
