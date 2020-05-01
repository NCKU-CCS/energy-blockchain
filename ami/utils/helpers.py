from functools import update_wrapper
from flask import request, current_app

def check_ip():
    def decorator(func):
        def wrapped_function(*args, **kwargs):
            real_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            if real_ip:
                if real_ip in current_app.config.get('ALLOWED_IPS'):
                    return func(*args, **kwargs)
            return {
                'message': 'Reject!'
            }, 404
        return update_wrapper(wrapped_function, func)
    return decorator
