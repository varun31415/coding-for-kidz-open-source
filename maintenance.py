import time
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=60)
def change_route_output_to_html():
    """
    """

    output = """Endpoint                       Methods    Rule
    -----------------------------  ---------  --------------------------------------------
    /error_400                     GET        /400-test
    /error_404                     GET        /404-test
    /error_500                     GET        /500-test
    _debug_toolbar.static          GET        /_debug_toolbar/static/<path:filename>
    _debug_toolbar.static          GET        /_debug_toolbar/static/<path:filename>
    about                          GET        /about
    access_lesson                  GET, POST  /card/<lesson_id>
    articles                       GET        /articles
    change_profile                 GET        /changeprofile
    create_all                     GET        /create-all
    create_all                     GET        /createall
    debugtoolbar.save_template     POST       /_debug_toolbar/views/template/<key>/save
    debugtoolbar.save_template     POST       /_debug_toolbar/views/template/<key>/save
    debugtoolbar.sql_select        GET, POST  /_debug_toolbar/views/sqlalchemy/sql_select
    debugtoolbar.sql_select        GET, POST  /_debug_toolbar/views/sqlalchemy/sql_select
    debugtoolbar.sql_select        GET, POST  /_debug_toolbar/views/sqlalchemy/sql_explain
    debugtoolbar.sql_select        GET, POST  /_debug_toolbar/views/sqlalchemy/sql_explain
    debugtoolbar.template_editor   GET        /_debug_toolbar/views/template/<key>
    debugtoolbar.template_editor   GET        /_debug_toolbar/views/template/<key>
    debugtoolbar.template_preview  POST       /_debug_toolbar/views/template/<key>
    debugtoolbar.template_preview  POST       /_debug_toolbar/views/template/<key>
    drop_all                       GET        /drop-all
    drop_all                       GET        /dropall
    index                          GET        /home
    index                          GET        /
    javascript                     GET        /code/javascript
    learn                          GET        /learn
    projects                       GET        /projects
    refresh                        GET        /refresh
    report_page_not_found_error    GET, POST  /page_not_found_error
    set_pic                        GET        /setpic
    set_profile                    POST       /setprofilepic
    set_profile_about              POST       /setprofileabout
    staff.staff                    GET        /
    staff.staff                    GET        /
    staff.staff                    GET        /
    staff.staff                    GET        /
    staff.staff_urls               GET        /urls
    staff.staff_urls               GET        /urls
    staff.staff_urls               GET        /urls
    staff.staff_urls               GET        /urls
    static                         GET        /static/<path:filename>
    test_code                      GET        /test-code
    test_code                      GET        /testcode
    view_user_profile              GET        /user/<username>"""
    ans = '<table style="width:100%">'
    lines = []
    line = "<tr><td>"
    second_line = False
    for item in output:
        if item == "\n":
            lines.append(line)
            second_line = False
            line = "<tr><td>"
        elif item == "/":
            if not second_line:
                line = line + "</td><td>/"
                second_line = True
            else:
                line = line + item

        else:
            line = line + item

    for item in lines:
        item += "</td></tr>"
        ans = ans + item + "\n"
    ans = ans + "</table>"
    return ans
