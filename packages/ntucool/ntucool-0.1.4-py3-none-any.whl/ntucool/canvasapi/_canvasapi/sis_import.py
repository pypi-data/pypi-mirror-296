from ..models.sis_imports import SisImport as SisImportModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .progress import Progress
from .canvas_object import CanvasObject
from .progress import Progress
from .util import combine_kwargs

class SisImport(SisImportModel):

    def __str__(self):
        return '{} ({})'.format(self.workflow_state, self.id)

    def abort(self, **kwargs) -> 'SisImport':
        """
        Abort this SIS import.

        Endpoint: PUT /api/v1/accounts/:account_id/sis_imports/:id/abort

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.abort
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'accounts/{}/sis_imports/{}/abort'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return SisImport(self._requester, response.json())

    async def abort_async(self, **kwargs) -> 'SisImport':
        """
        Abort this SIS import.

        Endpoint: PUT /api/v1/accounts/:account_id/sis_imports/:id/abort

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.abort
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'accounts/{}/sis_imports/{}/abort'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return SisImport(self._requester, response.json())

    def restore_states(self, **kwargs) -> 'Progress':
        """
        Restore workflow_states of SIS imported items.

        Endpoint: PUT /api/v1/accounts/:account_id/sis_imports/:id/restore_states

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.restore_states
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'accounts/{}/sis_imports/{}/restore_states'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self._requester, response.json())

    async def restore_states_async(self, **kwargs) -> 'Progress':
        """
        Restore workflow_states of SIS imported items.

        Endpoint: PUT /api/v1/accounts/:account_id/sis_imports/:id/restore_states

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.restore_states
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'accounts/{}/sis_imports/{}/restore_states'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self._requester, response.json())