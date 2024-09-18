from ..models.progress import Progress as ProgressModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class Progress(ProgressModel):

    def __str__(self):
        return '{} - {} ({})'.format(self.tag, self.workflow_state, self.id)

    def query(self, **kwargs) -> 'Progress':
        """
        Return completion and status information about an asynchronous job.

        Endpoint: GET /api/v1/progress/:id

        Reference: https://canvas.instructure.com/doc/api/progress.html#method.progress.show
        """
        response: 'httpx.Response' = self._requester.request('GET', 'progress/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        super(Progress, self).set_attributes(response_json)
        return Progress(self._requester, response_json)

    async def query_async(self, **kwargs) -> 'Progress':
        """
        Return completion and status information about an asynchronous job.

        Endpoint: GET /api/v1/progress/:id

        Reference: https://canvas.instructure.com/doc/api/progress.html#method.progress.show
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'progress/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        super(Progress, self).set_attributes(response_json)
        return Progress(self._requester, response_json)