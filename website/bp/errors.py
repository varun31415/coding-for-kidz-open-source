from website import app
from flask import render_template
from sentry_sdk import last_event_id


@app.errorhandler(400)
def error_400(e):
    return "oops the error is on your end\n extra info: 400 error"


@app.route('/401-test', endpoint="/error_401")
@app.errorhandler(401)
def error_401(e):
    return "This page is top secret, maybe if you do ten push-ups I will let you in." + e


@app.route('/404-test', endpoint="/error_404")
@app.errorhandler(404)
def error_404(e):
    return render_template('not_found.html', error=e), 404


@app.route('/500-test', endpoint="/error_500")
@app.errorhandler(500)
def error_500(e):
    return render_template('error.html', sentry_event_id=last_event_id(), error=e), 500
