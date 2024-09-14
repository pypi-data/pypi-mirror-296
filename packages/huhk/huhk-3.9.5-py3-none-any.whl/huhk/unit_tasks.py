import re
from threading import Thread
from apscheduler.schedulers.blocking import BlockingScheduler


def shared_task(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


class Scheduler:
    scheduler = None

    def __init__(self):
        if Scheduler.scheduler:
            try:
                Scheduler.scheduler.shutdown(False)
                Scheduler.scheduler = BlockingScheduler()
            except Exception as e:
                print(e)
            pass
        else:
            Scheduler.scheduler = BlockingScheduler()

    @staticmethod
    def get_cron(corn_str):
        cron_list = re.split(r'\s+', corn_str.strip().replace('?', '*').replace('？', '*'))
        cron_list = (cron_list + ["*"] * 7)[:7]
        second, minute, hour, day, month, day_of_week, year = cron_list
        return second, minute, hour, day, month, day_of_week, year

    def add_jobs(self, fun, schedules=None, cron=None):
        if cron:
            second, minute, hour, day, month, day_of_week, year = self.get_cron(cron)
            if schedules is not None:
                Scheduler.scheduler.add_job(fun, 'cron', year=year, day_of_week=day_of_week, month=month, day=day,
                                            hour=hour, minute=minute, second=second, args=(schedules,))
            else:
                Scheduler.scheduler.add_job(fun, 'cron', year=year, day_of_week=day_of_week, month=month, day=day,
                                            hour=hour, minute=minute, second=second)
            return True
        elif schedules:
            for schedule in schedules:
                if schedule.cron and schedule.cron.strip():
                    try:
                        second, minute, hour, day, month, day_of_week, year = self.get_cron(schedule.cron.strip())
                        Scheduler.scheduler.add_job(fun, 'cron', year=year, day_of_week=day_of_week, month=month,
                                                    day=day, hour=hour, minute=minute, second=second, args=(schedule,))
                    except Exception as e:
                        print("Error:" + str(e))
        return True

    @staticmethod
    def start():
        Scheduler.scheduler.start()