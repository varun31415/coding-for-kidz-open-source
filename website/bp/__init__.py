from website.bp.admin import admin
from website.bp.mod import mod
from website.bp.staff import staff
from website.bp.auth import auth
from website.bp.errors import *
from website import app
app.register_blueprint(admin)
app.register_blueprint(mod)
app.register_blueprint(staff)
app.register_blueprint(auth)
