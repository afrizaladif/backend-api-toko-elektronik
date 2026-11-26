
from flask import request, g
from models import activity_log


def simpan_activity_log(aktivitas, status_code):
    current_user = getattr(g, "current_user", None)

    if not current_user:
        return None

    id_user = current_user.get("id_user")

    if not id_user:
        return None

    return activity_log.create(
        id_user=id_user,
        aktivitas=aktivitas,
        endpoint=request.path,
        method=request.method,
        status_code=status_code,
        ip_address=request.remote_addr
    )
