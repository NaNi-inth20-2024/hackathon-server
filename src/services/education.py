from datetime import datetime


def is_subject_valid(subject):
    date = datetime.now()
    sem = subject.semester
    year = subject.year
    if date.year == year:
        if sem == 1:
            return date.month >= 9 or date.month < 2
        else:
            return date.month >= 2 or date.month < 9

    return False
