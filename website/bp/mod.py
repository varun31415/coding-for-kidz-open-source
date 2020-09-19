from flask import *
from website import app, db, login_manager

mod = Blueprint('mod', __name__, subdomain="mod")


# TODO: Make mod site

@mod.route('/')
def mod_home():
    return render_template('../templates/mod/staff_article_list.html')
