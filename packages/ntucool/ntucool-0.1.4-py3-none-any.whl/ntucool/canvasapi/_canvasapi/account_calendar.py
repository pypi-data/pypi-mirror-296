from ..models.account_calendars import AccountCalendar as AccountCalendarModel
import httpx
import typing
from .canvas_object import CanvasObject

class AccountCalendar(AccountCalendarModel):

    def __str__(self):
        return '{} {} ({})'.format(self.name, self.visible, self.calendar_event_url)