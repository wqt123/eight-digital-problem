'''
    实现跨文件的全局变量
'''
_global_dict ={}

def set_value(name, value):
    global _global_dict
    _global_dict[name] = value

def get_value(name, defValue=None):
    global _global_dict
    try:
        return _global_dict[name]
    except KeyError:
        return defValue