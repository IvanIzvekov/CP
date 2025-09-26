from app.interfaces.interfaces import IScheduleRepository


class ScheduleService:
    def __init__(self, schedule_repo: IScheduleRepository):
        self.schedule_repo = schedule_repo
