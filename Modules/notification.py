# Auto Almost Everything
# Youtube Channel https://www.youtube.com/c/AutoAlmostEverything
# Please read README.md carefully before use

# Solve captcha by using https://2captcha.com?from=11528745.

import winsound
from win10toast import ToastNotifier


def notify(app, content):
    try:
        toast = ToastNotifier()
        toast.show_toast(app, content, duration=5)
    except:
        pass


def sound():
    winsound.Beep(999, 500)
