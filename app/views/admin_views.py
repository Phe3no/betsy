from flask import render_template


def init_app(app):
    @app.route("/admin/dashboard")
    def admin_dashboard():
        return render_template("admin/dashboard.html")
