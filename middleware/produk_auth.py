from functools import wraps
from middleware.jwt_auth import jwt_required


def product_read_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return jwt_required(f)(*args, **kwargs)

    return decorated