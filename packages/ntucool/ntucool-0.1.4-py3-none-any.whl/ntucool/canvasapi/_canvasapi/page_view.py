from ..models.users import PageView as PageViewModel
import httpx
import typing
from .canvas_object import CanvasObject

class PageView(PageViewModel):

    def __str__(self):
        return '{} ({})'.format(self.context_type, self.id)