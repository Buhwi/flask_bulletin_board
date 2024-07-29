from flask import redirect, url_for
from flask_login import current_user

def id_one_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return redirect(url_for('routes.index'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
