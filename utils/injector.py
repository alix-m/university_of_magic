from functools import wraps
import inspect


def inject(target_function, new_function):
    @wraps(target_function)
    def _inject(*args, **kwargs):
        return new_function(target_function, *args, **kwargs)

    return _inject


def inject_to(target_object, target_function_name):
    def _inject_to(new_function):
        target_function = getattr(target_object, target_function_name)
        setattr(target_object, target_function_name, inject(target_function, new_function))
        return new_function
    return _inject_to


def is_injectable(target_function, new_function):
    target_argspec = inspect.getargspec(target_function)
    new_argspec = inspect.getargspec(new_function)
    return len(target_argspec.args) == len(new_argspec.args) - 1


def turbo_inject(target_object, target_function_name, safe=False):
    if safe and not hasattr(target_object, target_function_name):

        def _self_wrap(wrap_function):
            return wrap_function

        return _self_wrap

    def _wrap_original_function(original_function, new_function):

        @wraps(original_function)
        def _wrapped_function(*args, **kwargs):
            if type(original_function) is property:
                return new_function(original_function.fget, *args, **kwargs)
            else:
                return new_function(original_function, *args, **kwargs)

        if inspect.ismethod(original_function):
            if hasattr(original_function, '__self__'):
                return _wrapped_function.__get__(original_function.__self__, original_function.__self__.__class__)
            return classmethod(_wrapped_function)
        elif type(original_function) is property:
            return property(_wrapped_function)
        else:
            return _wrapped_function
        return _wrapped_function

    def _injected(wrap_function):
        original_function = getattr(target_object, target_function_name)
        setattr(target_object, target_function_name, _wrap_original_function(original_function, wrap_function))
        return wrap_function

    return _injected