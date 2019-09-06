from flask import request, current_app
from functools import update_wrapper

def check_ip():
    def decorator(f):
        def wrapped_function(*args, **kwargs):
            ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            if ip:
                if ip in current_app.config.get('ALLOWED_IPS'):
                     return f(*args, **kwargs)
            return {
                'message': 'Reject!'
            }, 404
        return update_wrapper(wrapped_function, f)
    return decorator
