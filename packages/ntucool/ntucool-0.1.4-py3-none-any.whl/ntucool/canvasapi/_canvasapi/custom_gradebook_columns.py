import httpx
import typing
if typing.TYPE_CHECKING:
    from .paginated_list import PaginatedList
from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .util import combine_kwargs, is_multivalued

class CustomGradebookColumn(CanvasObject):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def delete(self, **kwargs) -> 'CustomGradebookColumn':
        """
        Permanently delete a custom column.

        Endpoint: DELETE /api/v1/courses/:course_id/custom_gradebook_columns/:id

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/custom_gradebook_columns/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return CustomGradebookColumn(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'CustomGradebookColumn':
        """
        Permanently delete a custom column.

        Endpoint: DELETE /api/v1/courses/:course_id/custom_gradebook_columns/:id

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/custom_gradebook_columns/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return CustomGradebookColumn(self._requester, response.json())

    def get_column_entries(self, **kwargs) -> 'PaginatedList[ColumnData]':
        """
        Returns a list of ColumnData objects.

        Endpoint: GET /api/v1/courses/:course_id/custom_gradebook_columns/:id/data

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.index
        """
        return PaginatedList(ColumnData, self._requester, 'GET', 'courses/{}/custom_gradebook_columns/{}/data'.format(self.course_id, self.id), {'course_id': self.course_id, 'gradebook_column_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_column_entries_async(self, **kwargs) -> 'PaginatedList[ColumnData]':
        """
        Returns a list of ColumnData objects.

        Endpoint: GET /api/v1/courses/:course_id/custom_gradebook_columns/:id/data

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.index
        """
        return PaginatedList(ColumnData, self._requester, 'GET', 'courses/{}/custom_gradebook_columns/{}/data'.format(self.course_id, self.id), {'course_id': self.course_id, 'gradebook_column_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def reorder_custom_columns(self, order: 'list[int]', **kwargs) -> 'bool':
        """
        Put the given columns in a specific order based on given parameter.

        Endpoint: POST /api/v1/courses/:course_id/custom_gradebook_columns/reorder

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.reorder

        Parameters:
            order: list of int
        """
        if is_multivalued(order):
            order = ','.join([str(topic_id) for topic_id in order])
        if not isinstance(order, str) or ',' not in order:
            raise ValueError('Param `order` must be a list, tuple, or string.')
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/custom_gradebook_columns/reorder'.format(self.course_id), _kwargs=combine_kwargs(**kwargs), order=order)
        return response.json().get('reorder')

    async def reorder_custom_columns_async(self, order: 'list[int]', **kwargs) -> 'bool':
        """
        Put the given columns in a specific order based on given parameter.

        Endpoint: POST /api/v1/courses/:course_id/custom_gradebook_columns/reorder

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.reorder

        Parameters:
            order: list of int
        """
        if is_multivalued(order):
            order = ','.join([str(topic_id) for topic_id in order])
        if not isinstance(order, str) or ',' not in order:
            raise ValueError('Param `order` must be a list, tuple, or string.')
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/custom_gradebook_columns/reorder'.format(self.course_id), _kwargs=combine_kwargs(**kwargs), order=order)
        return response.json().get('reorder')

    def update_custom_column(self, **kwargs) -> 'CustomGradebookColumn':
        """
        Update a CustomColumn object.

        Endpoint: PUT /api/v1/courses/:course_id/custom_gradebook_columns/:id

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/custom_gradebook_columns/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('title'):
            super(CustomGradebookColumn, self).set_attributes(response.json())
        return self

    async def update_custom_column_async(self, **kwargs) -> 'CustomGradebookColumn':
        """
        Update a CustomColumn object.

        Endpoint: PUT /api/v1/courses/:course_id/custom_gradebook_columns/:id

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/custom_gradebook_columns/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('title'):
            super(CustomGradebookColumn, self).set_attributes(response.json())
        return self

class ColumnData(CanvasObject):

    def __str__(self):
        return '{} ({})'.format(self.user_id, self.content)

    def update_column_data(self, column_data: 'str', **kwargs) -> 'ColumnData':
        """
        Sets the content of a custom column.

        Endpoint: PUT /api/v1/courses/:course_id/custom_gradebook_columns/:id/data/:user_id

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.update

        Parameters:
            column_data: str
        """
        kwargs['column_data'] = column_data
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/custom_gradebook_columns/{}/data/{}'.format(self.course_id, self.gradebook_column_id, self.user_id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('content'):
            super(ColumnData, self).set_attributes(response.json())
        return self

    async def update_column_data_async(self, column_data: 'str', **kwargs) -> 'ColumnData':
        """
        Sets the content of a custom column.

        Endpoint: PUT /api/v1/courses/:course_id/custom_gradebook_columns/:id/data/:user_id

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.update

        Parameters:
            column_data: str
        """
        kwargs['column_data'] = column_data
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/custom_gradebook_columns/{}/data/{}'.format(self.course_id, self.gradebook_column_id, self.user_id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('content'):
            super(ColumnData, self).set_attributes(response.json())
        return self