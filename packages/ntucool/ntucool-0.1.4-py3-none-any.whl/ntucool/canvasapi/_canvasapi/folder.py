from ..models.files import Folder as FolderModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .paginated_list import PaginatedList
    from .file import File
from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .upload import FileOrPathLike, Uploader
from .util import combine_kwargs, obj_or_id

class Folder(FolderModel):

    def __str__(self):
        return '{}'.format(self.full_name)

    def copy_file(self, source_file: 'int | File', **kwargs) -> 'Folder':
        """
        Copies a file into the current folder.

        Endpoint: POST /api/v1/folders/:dest_folder_id/copy_file

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.copy_file

        Parameters:
            source_file: int or :class:`canvasapi.file.File`
        """
        from .file import File
        file_id = obj_or_id(source_file, 'source_file', (File,))
        kwargs['source_file_id'] = file_id
        response: 'httpx.Response' = self._requester.request('POST', 'folders/{}/copy_file'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return File(self._requester, response.json())

    async def copy_file_async(self, source_file: 'int | File', **kwargs) -> 'Folder':
        """
        Copies a file into the current folder.

        Endpoint: POST /api/v1/folders/:dest_folder_id/copy_file

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.copy_file

        Parameters:
            source_file: int or :class:`canvasapi.file.File`
        """
        from .file import File
        file_id = obj_or_id(source_file, 'source_file', (File,))
        kwargs['source_file_id'] = file_id
        response: 'httpx.Response' = await self._requester.request_async('POST', 'folders/{}/copy_file'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return File(self._requester, response.json())

    def create_folder(self, name: 'str', **kwargs) -> 'Folder':
        """
        Creates a folder within this folder.

        Endpoint: POST /api/v1/folders/:folder_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.create

        Parameters:
            name: str
        """
        response: 'httpx.Response' = self._requester.request('POST', 'folders/{}/folders'.format(self.id), name=name, _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    async def create_folder_async(self, name: 'str', **kwargs) -> 'Folder':
        """
        Creates a folder within this folder.

        Endpoint: POST /api/v1/folders/:folder_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.create

        Parameters:
            name: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'folders/{}/folders'.format(self.id), name=name, _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    def delete(self, **kwargs) -> 'Folder':
        """
        Remove this folder. You can only delete empty folders unless you set the
        'force' flag.

        Endpoint: DELETE /api/v1/folders/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.api_destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'folders/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'Folder':
        """
        Remove this folder. You can only delete empty folders unless you set the
        'force' flag.

        Endpoint: DELETE /api/v1/folders/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.api_destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'folders/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    def get_files(self, **kwargs) -> 'PaginatedList[File]':
        """
        Returns the paginated list of files for the folder.

        Endpoint: GET /api/v1/folders/:id/files

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_index
        """
        from .file import File
        return PaginatedList(File, self._requester, 'GET', 'folders/{}/files'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_files_async(self, **kwargs) -> 'PaginatedList[File]':
        """
        Returns the paginated list of files for the folder.

        Endpoint: GET /api/v1/folders/:id/files

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_index
        """
        from .file import File
        return PaginatedList(File, self._requester, 'GET', 'folders/{}/files'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_folders(self, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of folders in the folder.

        Endpoint: GET /api/v1/folders/:id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.api_index
        """
        return PaginatedList(Folder, self._requester, 'GET', 'folders/{}/folders'.format(self.id))

    async def get_folders_async(self, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of folders in the folder.

        Endpoint: GET /api/v1/folders/:id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.api_index
        """
        return PaginatedList(Folder, self._requester, 'GET', 'folders/{}/folders'.format(self.id))

    def update(self, **kwargs) -> 'Folder':
        """
        Updates a folder.

        Endpoint: PUT /api/v1/folders/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'folders/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'name' in response.json():
            super(Folder, self).set_attributes(response.json())
        return Folder(self._requester, response.json())

    async def update_async(self, **kwargs) -> 'Folder':
        """
        Updates a folder.

        Endpoint: PUT /api/v1/folders/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'folders/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'name' in response.json():
            super(Folder, self).set_attributes(response.json())
        return Folder(self._requester, response.json())

    def upload(self, file: 'FileOrPathLike | str', **kwargs) -> 'tuple':
        """
        Upload a file to this folder.

        Endpoint: POST /api/v1/folders/:folder_id/files

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.create_file

        Parameters:
            file: file or str
        """
        my_path = 'folders/{}/files'.format(self.id)
        return Uploader(self._requester, my_path, file, **kwargs).start()

    async def upload_async(self, file: 'FileOrPathLike | str', **kwargs) -> 'tuple':
        """
        Upload a file to this folder.

        Endpoint: POST /api/v1/folders/:folder_id/files

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.create_file

        Parameters:
            file: file or str
        """
        my_path = 'folders/{}/files'.format(self.id)
        return Uploader(self._requester, my_path, file, **kwargs).start()