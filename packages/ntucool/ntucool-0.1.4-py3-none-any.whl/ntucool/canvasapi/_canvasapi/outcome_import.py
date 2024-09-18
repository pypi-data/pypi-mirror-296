from ..models.outcome_imports import OutcomeImport as OutcomeImportModel
import httpx
import typing
from .canvas_object import CanvasObject

class OutcomeImport(OutcomeImportModel):

    def __str__(self):
        return '{} ({})'.format(self.workflow_state, self.id)