from flask import *
from flask_login import current_user

admin = Blueprint('admin', __name__, subdomain="admin")


# TODO: Make admin site

@admin.route('/')
def admin_home():
    if current_user.is_authenticated:
        return render_template('admin/admin_home.html')
    else:
        return render_template("not_found.html")
