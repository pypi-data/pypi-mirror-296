from ..models.enrollment_terms import EnrollmentTerm as EnrollmentTermModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class EnrollmentTerm(EnrollmentTermModel):

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def delete(self, **kwargs) -> 'EnrollmentTerm':
        """
        Delete this Enrollment Term.

        Endpoint: DELETE /api/v1/accounts/:account_id/terms/:id

        Reference: https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'accounts/{}/terms/{}'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return EnrollmentTerm(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'EnrollmentTerm':
        """
        Delete this Enrollment Term.

        Endpoint: DELETE /api/v1/accounts/:account_id/terms/:id

        Reference: https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'accounts/{}/terms/{}'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return EnrollmentTerm(self._requester, response.json())

    def edit(self, **kwargs) -> 'EnrollmentTerm':
        """
        Modify this Enrollment Term.

        Endpoint: PUT /api/v1/accounts/:account_id/terms/:id

        Reference: https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'accounts/{}/terms/{}'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return EnrollmentTerm(self._requester, response.json())

    async def edit_async(self, **kwargs) -> 'EnrollmentTerm':
        """
        Modify this Enrollment Term.

        Endpoint: PUT /api/v1/accounts/:account_id/terms/:id

        Reference: https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'accounts/{}/terms/{}'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return EnrollmentTerm(self._requester, response.json())