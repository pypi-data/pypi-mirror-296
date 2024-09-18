from ..models.notification_preferences import NotificationPreference as NotificationPreferenceModel
import httpx
import typing
from .canvas_object import CanvasObject

class NotificationPreference(NotificationPreferenceModel):

    def __str__(self):
        return '{} ({})'.format(self.notification, self.frequency)