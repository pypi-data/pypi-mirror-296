from ..models.modules import Module as ModuleModel, ModuleItem as ModuleItemModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .paginated_list import PaginatedList
from .canvas_object import CanvasObject
from .exceptions import RequiredFieldMissing
from .paginated_list import PaginatedList
from .util import combine_kwargs, obj_or_id

class Module(ModuleModel):

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def create_module_item(self, module_item: 'dict', **kwargs) -> 'ModuleItem':
        """
        Create a module item.

        Endpoint: POST /api/v1/courses/:course_id/modules/:module_id/items

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.create

        Parameters:
            module_item: dict
        """
        unrequired_types = ['ExternalUrl', 'Page', 'SubHeader']
        if isinstance(module_item, dict) and 'type' in module_item:
            if module_item['type'] in unrequired_types or 'content_id' in module_item:
                kwargs['module_item'] = module_item
            else:
                raise RequiredFieldMissing("Dictionary with key 'content_id' is required.")
        else:
            raise RequiredFieldMissing("Dictionary with key 'type' is required.")
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/modules/{}/items'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_item_json: 'dict' = response.json()
        module_item_json.update({'course_id': self.course_id})
        return ModuleItem(self._requester, module_item_json)

    async def create_module_item_async(self, module_item: 'dict', **kwargs) -> 'ModuleItem':
        """
        Create a module item.

        Endpoint: POST /api/v1/courses/:course_id/modules/:module_id/items

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.create

        Parameters:
            module_item: dict
        """
        unrequired_types = ['ExternalUrl', 'Page', 'SubHeader']
        if isinstance(module_item, dict) and 'type' in module_item:
            if module_item['type'] in unrequired_types or 'content_id' in module_item:
                kwargs['module_item'] = module_item
            else:
                raise RequiredFieldMissing("Dictionary with key 'content_id' is required.")
        else:
            raise RequiredFieldMissing("Dictionary with key 'type' is required.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/modules/{}/items'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_item_json: 'dict' = response.json()
        module_item_json.update({'course_id': self.course_id})
        return ModuleItem(self._requester, module_item_json)

    def delete(self, **kwargs) -> 'Module':
        """
        Delete this module.

        Endpoint: DELETE /api/v1/courses/:course_id/modules/:id

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/modules/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_json: 'dict' = response.json()
        module_json.update({'course_id': self.course_id})
        return Module(self._requester, module_json)

    async def delete_async(self, **kwargs) -> 'Module':
        """
        Delete this module.

        Endpoint: DELETE /api/v1/courses/:course_id/modules/:id

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/modules/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_json: 'dict' = response.json()
        module_json.update({'course_id': self.course_id})
        return Module(self._requester, module_json)

    def edit(self, **kwargs) -> 'Module':
        """
        Update this module.

        Endpoint: PUT /api/v1/courses/:course_id/modules/:id

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/modules/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_json: 'dict' = response.json()
        module_json.update({'course_id': self.course_id})
        return Module(self._requester, module_json)

    async def edit_async(self, **kwargs) -> 'Module':
        """
        Update this module.

        Endpoint: PUT /api/v1/courses/:course_id/modules/:id

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/modules/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_json: 'dict' = response.json()
        module_json.update({'course_id': self.course_id})
        return Module(self._requester, module_json)

    def get_module_item(self, module_item: 'ModuleItem | dict', **kwargs) -> 'ModuleItem':
        """
        Retrieve a module item by ID.

        Endpoint: GET /api/v1/courses/:course_id/modules/:module_id/items/:id

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.show

        Parameters:
            module_item: :class:`canvasapi.module.ModuleItem` or dict
        """
        module_item_id = obj_or_id(module_item, 'module_item', (ModuleItem,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/modules/{}/items/{}'.format(self.course_id, self.id, module_item_id), _kwargs=combine_kwargs(**kwargs))
        module_item_json: 'dict' = response.json()
        module_item_json.update({'course_id': self.course_id})
        return ModuleItem(self._requester, module_item_json)

    async def get_module_item_async(self, module_item: 'ModuleItem | dict', **kwargs) -> 'ModuleItem':
        """
        Retrieve a module item by ID.

        Endpoint: GET /api/v1/courses/:course_id/modules/:module_id/items/:id

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.show

        Parameters:
            module_item: :class:`canvasapi.module.ModuleItem` or dict
        """
        module_item_id = obj_or_id(module_item, 'module_item', (ModuleItem,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/modules/{}/items/{}'.format(self.course_id, self.id, module_item_id), _kwargs=combine_kwargs(**kwargs))
        module_item_json: 'dict' = response.json()
        module_item_json.update({'course_id': self.course_id})
        return ModuleItem(self._requester, module_item_json)

    def get_module_items(self, **kwargs) -> 'PaginatedList[ModuleItem]':
        """
        List all of the items in this module.

        Endpoint: GET /api/v1/courses/:course_id/modules/:module_id/items

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.index
        """
        return PaginatedList(ModuleItem, self._requester, 'GET', 'courses/{}/modules/{}/items'.format(self.course_id, self.id), {'course_id': self.course_id}, _kwargs=combine_kwargs(**kwargs))

    async def get_module_items_async(self, **kwargs) -> 'PaginatedList[ModuleItem]':
        """
        List all of the items in this module.

        Endpoint: GET /api/v1/courses/:course_id/modules/:module_id/items

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.index
        """
        return PaginatedList(ModuleItem, self._requester, 'GET', 'courses/{}/modules/{}/items'.format(self.course_id, self.id), {'course_id': self.course_id}, _kwargs=combine_kwargs(**kwargs))

    def relock(self, **kwargs) -> 'Module':
        """
        Reset module progressions to their default locked state and recalculates
        them based on the current requirements.
        
        Adding progression requirements to an active course will not lock students
        out of modules they have already unlocked unless this action is called.

        Endpoint: PUT /api/v1/courses/:course_id/modules/:id/relock

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.relock
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/modules/{}/relock'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_json: 'dict' = response.json()
        module_json.update({'course_id': self.course_id})
        return Module(self._requester, module_json)

    async def relock_async(self, **kwargs) -> 'Module':
        """
        Reset module progressions to their default locked state and recalculates
        them based on the current requirements.
        
        Adding progression requirements to an active course will not lock students
        out of modules they have already unlocked unless this action is called.

        Endpoint: PUT /api/v1/courses/:course_id/modules/:id/relock

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.relock
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/modules/{}/relock'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_json: 'dict' = response.json()
        module_json.update({'course_id': self.course_id})
        return Module(self._requester, module_json)

class ModuleItem(ModuleItemModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def complete(self, **kwargs) -> 'ModuleItem':
        """
        Mark this module item as done.

        Endpoint: PUT /api/v1/courses/:course_id/modules/:module_id/items/:id/done

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.mark_as_done
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/modules/{}/items/{}/done'.format(self.course_id, self.module_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_item_json: 'dict' = response.json()
        module_item_json.update({'course_id': self.course_id})
        return ModuleItem(self._requester, module_item_json)

    async def complete_async(self, **kwargs) -> 'ModuleItem':
        """
        Mark this module item as done.

        Endpoint: PUT /api/v1/courses/:course_id/modules/:module_id/items/:id/done

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.mark_as_done
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/modules/{}/items/{}/done'.format(self.course_id, self.module_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_item_json: 'dict' = response.json()
        module_item_json.update({'course_id': self.course_id})
        return ModuleItem(self._requester, module_item_json)

    def delete(self, **kwargs) -> 'ModuleItem':
        """
        Delete this module item.

        Endpoint: DELETE /api/v1/courses/:course_id/modules/:module_id/items/:id

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/modules/{}/items/{}'.format(self.course_id, self.module_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_item_json: 'dict' = response.json()
        module_item_json.update({'course_id': self.course_id})
        return ModuleItem(self._requester, module_item_json)

    async def delete_async(self, **kwargs) -> 'ModuleItem':
        """
        Delete this module item.

        Endpoint: DELETE /api/v1/courses/:course_id/modules/:module_id/items/:id

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/modules/{}/items/{}'.format(self.course_id, self.module_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_item_json: 'dict' = response.json()
        module_item_json.update({'course_id': self.course_id})
        return ModuleItem(self._requester, module_item_json)

    def edit(self, **kwargs) -> 'ModuleItem':
        """
        Update this module item.

        Endpoint: PUT /api/v1/courses/:course_id/modules/:module_id/items/:id

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/modules/{}/items/{}'.format(self.course_id, self.module_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_item_json: 'dict' = response.json()
        module_item_json.update({'course_id': self.course_id})
        return ModuleItem(self._requester, module_item_json)

    async def edit_async(self, **kwargs) -> 'ModuleItem':
        """
        Update this module item.

        Endpoint: PUT /api/v1/courses/:course_id/modules/:module_id/items/:id

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/modules/{}/items/{}'.format(self.course_id, self.module_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_item_json: 'dict' = response.json()
        module_item_json.update({'course_id': self.course_id})
        return ModuleItem(self._requester, module_item_json)

    def uncomplete(self, **kwargs) -> 'ModuleItem':
        """
        Mark this module item as not done.

        Endpoint: DELETE /api/v1/courses/:course_id/modules/:module_id/items/:id/done

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.mark_as_done
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/modules/{}/items/{}/done'.format(self.course_id, self.module_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_item_json: 'dict' = response.json()
        module_item_json.update({'course_id': self.course_id})
        return ModuleItem(self._requester, module_item_json)

    async def uncomplete_async(self, **kwargs) -> 'ModuleItem':
        """
        Mark this module item as not done.

        Endpoint: DELETE /api/v1/courses/:course_id/modules/:module_id/items/:id/done

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.mark_as_done
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/modules/{}/items/{}/done'.format(self.course_id, self.module_id, self.id), _kwargs=combine_kwargs(**kwargs))
        module_item_json: 'dict' = response.json()
        module_item_json.update({'course_id': self.course_id})
        return ModuleItem(self._requester, module_item_json)