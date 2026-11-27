from flask import request, g
from models import activity_log


def register_activity_logger(app):

    @app.after_request
    def catat_semua_aktivitas_api(response):

        # Catat hanya request API
        if not request.path.startswith("/api/"):
            return response

        # Ambil ID user dari JWT jika tersedia
        current_user = getattr(g, "current_user", None)

        id_user = None

        if isinstance(current_user, dict):
            id_user = current_user.get("id_user")

        # Tentukan aktivitas berdasarkan status response
        status_code = response.status_code

        if 200 <= status_code < 300:
            aktivitas = "Request API berhasil"

        elif 300 <= status_code < 400:
            aktivitas = "Request API redirect"

        else:
            aktivitas = "Request API gagal"

        try:
            activity_log.create(
                id_user=id_user,
                aktivitas=aktivitas,
                endpoint=request.path[:255],
                method=request.method,
                status_code=status_code,
                ip_address=request.remote_addr
            )

        except Exception as error:
            # Jangan sampai kegagalan logging merusak response API
            app.logger.error(
                "Gagal menyimpan activity log: %s",
                error
            )

        return response