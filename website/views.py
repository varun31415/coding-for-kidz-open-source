from base64 import b64decode, b64encode
from flask import *
from sentry_sdk import last_event_id

from website import app, login_manager, cache
from website.models import *
from flask_login import current_user
# from flask_mail import Message
from mainstreamcode import *
from markupsafe import *
from markupsafe import escape

login_manager.login_view = 'home'


@app.before_request
def load_logged_in_user():
    """This handles app before request"""
    try:
        if current_user.is_authenticated:
            print(f"{current_user.username}: {request.url}, {request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]}")
        else:
            print(f"Anonymous User: {request.url}, {request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]}")
    except Exception as e:
        pass

    try:
        if current_user.is_authenticated:
            if current_user.id in [79, 84]:
                pre_content = open("ip.txt", 'r').read()
                f = open("ip.txt", '+')
                f.write(pre_content + "\n<User " + str(current_user.username) + ">: " + str(
                    request.environ['HTTP_X_FORWARDED_FOR']))
                f.close()
            else:
                pre_content = open("ip_good.txt", 'r').read()
                f = open("ip_good.txt", 'w+')
                f.write(pre_content + "\n<User " + str(current_user.username) + ">: " + str(
                    request.environ['HTTP_X_FORWARDED_FOR']))
                f.close()
        else:
            pre_content = open("ip_good.txt", 'r').read()
            f = open("ip_good.txt", 'w+')
            f.write(pre_content + "\n<User anonymous>: " + str(
                request.environ['HTTP_X_FORWARDED_FOR']))
            f.close()
    except BaseException:
        pass


@app.route('/home', endpoint='index')
@app.route('/', endpoint='index')
@cache.cached(timeout=50)
def index():
    return render_template('home.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/about', endpoint='about')
@cache.cached(timeout=50)
def about():
    return render_template('about.html')


# TODO: Fix data base and learn
@app.route('/learn', endpoint='learn')
def learn():
    lessons_to_render = Lesson.query.all()
    courses = []
    for item in lessons_to_render:
        courses.append(item.id)
    return render_template('learn.html', lessons=lessons_to_render)


@app.route('/articles', endpoint='articles')
def articles():
    return render_template('articles.html')


@app.route('/projects')
def projects():
    if current_user.is_authenticated:
        return render_template('projects.html')
    else:
        return redirect("/login/projects/")


@app.route('/page_not_found_error', methods=('GET', 'POST'))
def report_page_not_found_error():
    if request.method == 'POST':
        describe_the_error = request.form['describe-the-error']
        what_is_the_url = request.form['what-is-the-url']
        if not current_user.is_authenticated:
            db.session.add(describe_the_error, what_is_the_url, "unknown")
        else:
            db.session.add(describe_the_error, what_is_the_url, current_user.user_id)
        db.commit()
        return render_template('report_error/page_not_found_error.html')


@app.route("/user/<username>")
def view_user_profile(username):
    user = User.query.filter_by(user_id=current_user.username).first()
    return render_template("user_profile.html", username=user.username, user=user)


@app.route("/setpic")
def set_pic():
    if current_user.is_authenticated:
        return render_template("camera.html")
    else:
        return render_template("not_found.html")


@app.route("/setprofilepic", methods=["POST"])
def set_profile():
    try:
        about = request.form["about"]
        profile = User.query.filter_by(user_id=current_user.id).first()
        header, encoded = data["data_url"].split(",", 1)
        image = Images()
        image.content = b64decode(encoded)
        image.content_type = "image/png"
        db.session.add(image)
        db.session.commit()
        profile.image = "/image/" + str(image.id)
        db.session.commit()
        print(image.id)
        time.sleep(2)
        return jsonify({"saved": True})
    except:
        return jsonify({"saved": False}), 404


@app.route("/setprofileabout", methods=["POST"])
def set_profile_about():
    try:
        data = request.json
        about = data["about"]
        profile = User.query.filter_by(user_id=current_user.id).first()
        profile.about = about
        db.session.commit()
        return jsonify({"saved": True})
    except BaseException:
        return jsonify({"saved": False}), 404


@app.route("/changeprofile")
def change_profile():
    if current_user.is_authenticated:
        return render_template("change_profile.html", about=User.query.filter_by(user_id=current_user.id).first().about)
    else:
        return render_template("not_found.html")


@app.route('/refresh', endpoint='refresh')
def refresh():
    return redirect('/')


@app.route('/createall', endpoint="create_all")
@app.route('/create-all', endpoint="create_all")
def create_all():
    db.create_all()
    return redirect('/')


@app.route('/dropall', endpoint="drop_all")
@app.route('/drop-all')
def drop_all():
    if current_user.is_authenticated:
        # db.drop_all()
        return redirect('/')
    else:
        return render_template("not_found.html")


@app.route('/testcode', endpoint="test_code")
@app.route('/test-code')
def test_code():
    return render_template('test_code.html')


# test code stuff
# TODO: Fix the nothing is there error
@app.route('/code/javascript', endpoint="javascript")
def javascript():
    return render_template('code_langs/javascript.html')


# lessons
@app.route('/card/<lesson_id>', methods=['GET', 'POST'])
def access_lesson(lesson_id):
    """
    :type lesson_id: int
    """
    lesson_to_render = Lesson.query.filter_by(lesson_id=lesson_id).first()
    current_user.top_progress += "," + lesson_to_render.id
    lesson_title = lesson_to_render.title
    lesson_subtitle = lesson_to_render.subtitle
    lesson_img = lesson_to_render.img
    lesson_body = lesson_to_render.body
    questions = lesson_to_render.questions
    answers = lesson_to_render.answers
    return render_template("card_temp.html", title=lesson_title, subtitle=lesson_subtitle, img=lesson_img,
                           body=lesson_body, questions=questions, answers=answers)


# TODO: Add remember progress
# TODO: Add recommended courses heading along with all courses heading
@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

# for the minimalistic product, ALl we need are a system where people can view the sources available. We can do
# logging in and more complex features after we do the absolute minimum
