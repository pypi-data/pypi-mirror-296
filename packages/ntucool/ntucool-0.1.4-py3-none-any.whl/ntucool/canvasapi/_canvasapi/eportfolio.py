import httpx
import typing
if typing.TYPE_CHECKING:
    from .paginated_list import PaginatedList
from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .util import combine_kwargs

class EPortfolio(CanvasObject):

    def __str__(self):
        return '{}'.format(self.name)

    def delete(self, **kwargs) -> 'EPortfolio':
        """
        Delete an ePortfolio.

        Endpoint: DELETE /api/v1/eportfolios/:id

        Reference: https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.delete
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'eportfolios/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return EPortfolio(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'EPortfolio':
        """
        Delete an ePortfolio.

        Endpoint: DELETE /api/v1/eportfolios/:id

        Reference: https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.delete
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'eportfolios/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return EPortfolio(self._requester, response.json())

    def get_eportfolio_pages(self, **kwargs) -> 'PaginatedList[EPortfolioPage]':
        """
        Return a list of pages for an ePortfolio.

        Endpoint: GET /api/v1/eportfolios/:eportfolio_id/pages

        Reference: https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.pages
        """
        return PaginatedList(EPortfolioPage, self._requester, 'GET', 'eportfolios/{}/pages'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_eportfolio_pages_async(self, **kwargs) -> 'PaginatedList[EPortfolioPage]':
        """
        Return a list of pages for an ePortfolio.

        Endpoint: GET /api/v1/eportfolios/:eportfolio_id/pages

        Reference: https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.pages
        """
        return PaginatedList(EPortfolioPage, self._requester, 'GET', 'eportfolios/{}/pages'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def moderate_eportfolio(self, **kwargs) -> 'EPortfolio':
        """
        Update the spam_status of an eportfolio.
        Only available to admins who can `moderate_user_content`.

        Endpoint: PUT /api/v1/eportfolios/:eportfolio_id/moderate

        Reference: https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.moderate
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'eportfolios/{}/moderate'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return EPortfolio(self._requester, response.json())

    async def moderate_eportfolio_async(self, **kwargs) -> 'EPortfolio':
        """
        Update the spam_status of an eportfolio.
        Only available to admins who can `moderate_user_content`.

        Endpoint: PUT /api/v1/eportfolios/:eportfolio_id/moderate

        Reference: https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.moderate
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'eportfolios/{}/moderate'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return EPortfolio(self._requester, response.json())

    def restore(self, **kwargs) -> 'EPortfolio':
        """
        Restore an ePortfolio back to active that was previously deleted.
        Only available to admins who can moderate_user_content.

        Endpoint: PUT /api/v1/eportfolios/:eportfolio_id/restore

        Reference: https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.restore
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'eportfolios/{}/restore'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return EPortfolio(self._requester, response.json())

    async def restore_async(self, **kwargs) -> 'EPortfolio':
        """
        Restore an ePortfolio back to active that was previously deleted.
        Only available to admins who can moderate_user_content.

        Endpoint: PUT /api/v1/eportfolios/:eportfolio_id/restore

        Reference: https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.restore
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'eportfolios/{}/restore'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return EPortfolio(self._requester, response.json())

class EPortfolioPage(CanvasObject):

    def __str__(self):
        return '{}. {}'.format(self.position, self.name)