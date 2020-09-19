from website.models import *


def unpack_progress(progress):
    """
    :type progress: str
    """
    ans = []
    if progress == "":
        return []
    else:
        breaker = []
        for item in progress:
            breaker.append(item)
        lesson_id = ""
        for item in breaker:
            if not (str(item).isdigit()):
                if item == ",":
                    ans.append(int(lesson_id))
                    lesson_id = ""
                elif item != " ":
                    lesson_id += item


def find_next_lesson(current_lesson_id):
    """
    When given a lesson id this function can find the next lessons for a user
    :type current_lesson_id: int
    """
    the_lesson = Lesson.query.filter_by(lesson_id=current_lesson_id).first()
    next_lessons = the_lesson.goes_to
    return next_lessons


def clean_up(progress):
    """
    Cleans up progress so that progress only displays the users most advanced lessons learned rather that all of them
    :type progress: list
    """
    cleaned_up = []
    for item in progress:
        if find_next_lesson(item) in progress:
            progress.remove(item)
    return cleaned_up


def recommended(progress):
    """
    :type progress: list
    """
    display = []
    progress = clean_up(progress)
    for item in progress:
        for lesson in find_next_lesson(item):
            display.append(lesson)


forums = {"python": 11, "c": 21, "c++": 31, "java": 41, "ruby": 51, "go": 61, "c#": 51, "html": 12, "css": 22,
          "javascript": 32, "frontend": 32, "backend": 3, "php": 13, "asp": 23, "Programming": 1}


def can_go_to_forum(progress):
    allowed_to_go = []
    for key in forums:
        if str(forums.get(key)) in progress:
            allowed_to_go.append(key)
    return allowed_to_go
