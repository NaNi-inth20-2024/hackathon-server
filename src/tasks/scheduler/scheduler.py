from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.utils import timezone
from tasks.models import Task


def handle_tasks():
    now = timezone.now()

    tasks = Task.objects.filter(is_finished=False)
    for task in tasks:
        if now < task.deadline:
            continue

        task.is_finished = True
        task.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(handle_tasks, IntervalTrigger(seconds=1), name="Start and finish auctions", jobstore="default")
    scheduler.start()
    print("Scheduler started...")
