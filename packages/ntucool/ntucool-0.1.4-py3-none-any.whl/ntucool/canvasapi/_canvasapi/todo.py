import httpx
import typing
from .canvas_object import CanvasObject

class Todo(CanvasObject):

    def __str__(self):
        return 'Todo Item ({})'.format(self.type)