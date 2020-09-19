from werkzeug.security import *
from flask import *
from website import app, db, login_manager
from website.models import *
from flask_login import login_user, logout_user, login_required, current_user
from secrets import *


staff = Blueprint('staff', __name__, subdomain="staff")


# TODO: Make staff site
@staff.route('/')
def staff_home():
    return render_template('staff/staff_home.html')


@staff.route('/urls')
def staff_urls():
    if current_user.is_authenticated:
        return render_template('staff/staff_urls.html')
    else:
        return render_template('not_found.html')
