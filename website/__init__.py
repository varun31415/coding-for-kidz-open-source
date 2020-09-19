try:
    from flask import Flask
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager
    from flask_caching import Cache
    from flask_debugtoolbar import DebugToolbarExtension
    from flask_mail import Mail
    from flask_talisman import Talisman
    from sentry_sdk.integrations.flask import FlaskIntegration
    from logging import config
    from logging import handlers
    # from flask_seasurf import SeaSurf
    import sentry_sdk
    import flask_monitoringdashboard as dashboard
    import logging

    # from logging.handlers import SMTPHandler
    config.dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    sentry_sdk.init(release="coding-for-kidz@0.5.6")
    app = Flask('website')

    app.debug = True

    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Strict',
    )

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# secret key and database URI are removed for privacy purposes
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["CACHE_TYPE"] = "simple"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300
    # dashboard.config.init_from(file='config.cfg')
    db = SQLAlchemy(app)

    # mail
    mail = Mail(app)
    mail.init_app(app)

    # cache
    cache = Cache(config={'CACHE_TYPE': 'simple'})
    cache.init_app(app)

    # login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    # talisman
    csp = {
        'default-src': [
            '\'self\'',
            '*.coding-for-kidz.herokuapp.com',
        ],
        'img-src': '*'
    }
    talisman = Talisman(app, content_security_policy=csp, content_security_policy_nonce_in=['script-src'])

    # seasurf
    # csrf = SeaSurf(app)
    # limiter
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["4800 per day", "200 per hour"]
    )
    # toolbar
    toolbar = DebugToolbarExtension(app)
    toolbar.init_app(app)

    # dashboard
    dashboard.config.init_from(file='config.cfg')
    dashboard.bind(app)
    # blueprint import and registration
    from website.bp import *

    # logging
    mail_handler = handlers.SMTPHandler(
        mailhost='coding-for-kidz.herokuapp.com',
        fromaddr='errors@coding-for-kidz.herokuapp.com',
        toaddrs=['arihant2math@gmail.com'],
        subject='Application Error'
    )

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))

    if not app.debug:
        app.logger.addHandler(mail_handler)
    sentry_sdk.init(
        dsn="https://ea8e9e0ead8b4237bb50efa99f27ee5a@o440973.ingest.sentry.io/5410703",
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )

    # security
    if __name__ == '__main__':
        app.run(debug=True)

    import website.models
    import website.views
except:
    from flask import Flask

    app = Flask('website')


    @app.route('/home', endpoint='index')
    @app.route('/', endpoint='index')
    def index():
        return render_template('home.html')

    @app.route('/about', endpoint='about')
    def about():
        return render_template('about.html')
