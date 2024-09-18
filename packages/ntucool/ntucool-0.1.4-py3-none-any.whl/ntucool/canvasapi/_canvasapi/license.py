from ..models.files import License as LicenseModel
import httpx
import typing
from .canvas_object import CanvasObject

class License(LicenseModel):

    def __str__(self):
        return '{} {}'.format(self.name, self.id)