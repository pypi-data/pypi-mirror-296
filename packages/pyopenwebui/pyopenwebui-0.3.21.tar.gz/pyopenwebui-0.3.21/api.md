# Shared Types

```python
from pyopenwebui.types import DocumentResponse, FileModel, PromptModel, UserResponse
```

# Configs

Types:

```python
from pyopenwebui.types import ConfigExportResponse, ConfigImportResponse
```

Methods:

- <code title="get /configs/export">client.configs.<a href="./src/pyopenwebui/resources/configs/configs.py">export</a>() -> <a href="./src/pyopenwebui/types/config_export_response.py">object</a></code>
- <code title="post /configs/import">client.configs.<a href="./src/pyopenwebui/resources/configs/configs.py">import\_</a>(\*\*<a href="src/pyopenwebui/types/config_import_params.py">params</a>) -> <a href="./src/pyopenwebui/types/config_import_response.py">object</a></code>

## Default

### Models

Types:

```python
from pyopenwebui.types.configs.default import ModelCreateResponse
```

Methods:

- <code title="post /configs/default/models">client.configs.default.models.<a href="./src/pyopenwebui/resources/configs/default/models.py">create</a>(\*\*<a href="src/pyopenwebui/types/configs/default/model_create_params.py">params</a>) -> str</code>

### Suggestions

Types:

```python
from pyopenwebui.types.configs.default import PromptSuggestion, SuggestionCreateResponse
```

Methods:

- <code title="post /configs/default/suggestions">client.configs.default.suggestions.<a href="./src/pyopenwebui/resources/configs/default/suggestions.py">create</a>(\*\*<a href="src/pyopenwebui/types/configs/default/suggestion_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/configs/default/suggestion_create_response.py">SuggestionCreateResponse</a></code>

## Banners

Types:

```python
from pyopenwebui.types.configs import BannerModel, BannerCreateResponse, BannerListResponse
```

Methods:

- <code title="post /configs/banners">client.configs.banners.<a href="./src/pyopenwebui/resources/configs/banners.py">create</a>(\*\*<a href="src/pyopenwebui/types/configs/banner_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/configs/banner_create_response.py">BannerCreateResponse</a></code>
- <code title="get /configs/banners">client.configs.banners.<a href="./src/pyopenwebui/resources/configs/banners.py">list</a>() -> <a href="./src/pyopenwebui/types/configs/banner_list_response.py">BannerListResponse</a></code>

# Auths

Types:

```python
from pyopenwebui.types import (
    APIKey,
    SigninResponse,
    AuthListResponse,
    AuthUpdatePasswordResponse,
    AuthUpdateProfileResponse,
)
```

Methods:

- <code title="get /auths/">client.auths.<a href="./src/pyopenwebui/resources/auths/auths.py">list</a>() -> <a href="./src/pyopenwebui/types/auth_list_response.py">AuthListResponse</a></code>
- <code title="post /auths/add">client.auths.<a href="./src/pyopenwebui/resources/auths/auths.py">add</a>(\*\*<a href="src/pyopenwebui/types/auth_add_params.py">params</a>) -> <a href="./src/pyopenwebui/types/signin_response.py">SigninResponse</a></code>
- <code title="post /auths/signin">client.auths.<a href="./src/pyopenwebui/resources/auths/auths.py">signin</a>(\*\*<a href="src/pyopenwebui/types/auth_signin_params.py">params</a>) -> <a href="./src/pyopenwebui/types/signin_response.py">SigninResponse</a></code>
- <code title="post /auths/signup">client.auths.<a href="./src/pyopenwebui/resources/auths/auths.py">signup</a>(\*\*<a href="src/pyopenwebui/types/auth_signup_params.py">params</a>) -> <a href="./src/pyopenwebui/types/signin_response.py">SigninResponse</a></code>
- <code title="post /auths/update/password">client.auths.<a href="./src/pyopenwebui/resources/auths/auths.py">update_password</a>(\*\*<a href="src/pyopenwebui/types/auth_update_password_params.py">params</a>) -> <a href="./src/pyopenwebui/types/auth_update_password_response.py">AuthUpdatePasswordResponse</a></code>
- <code title="post /auths/update/profile">client.auths.<a href="./src/pyopenwebui/resources/auths/auths.py">update_profile</a>(\*\*<a href="src/pyopenwebui/types/auth_update_profile_params.py">params</a>) -> <a href="./src/pyopenwebui/types/auth_update_profile_response.py">AuthUpdateProfileResponse</a></code>

## Admin

Types:

```python
from pyopenwebui.types.auths import (
    AdminRetrieveConfigResponse,
    AdminRetrieveDetailsResponse,
    AdminUpdateConfigResponse,
)
```

Methods:

- <code title="get /auths/admin/config">client.auths.admin.<a href="./src/pyopenwebui/resources/auths/admin.py">retrieve_config</a>() -> <a href="./src/pyopenwebui/types/auths/admin_retrieve_config_response.py">object</a></code>
- <code title="get /auths/admin/details">client.auths.admin.<a href="./src/pyopenwebui/resources/auths/admin.py">retrieve_details</a>() -> <a href="./src/pyopenwebui/types/auths/admin_retrieve_details_response.py">object</a></code>
- <code title="post /auths/admin/config">client.auths.admin.<a href="./src/pyopenwebui/resources/auths/admin.py">update_config</a>(\*\*<a href="src/pyopenwebui/types/auths/admin_update_config_params.py">params</a>) -> <a href="./src/pyopenwebui/types/auths/admin_update_config_response.py">object</a></code>

## APIKey

Types:

```python
from pyopenwebui.types.auths import APIKeyDeleteResponse
```

Methods:

- <code title="post /auths/api_key">client.auths.api_key.<a href="./src/pyopenwebui/resources/auths/api_key.py">create</a>() -> <a href="./src/pyopenwebui/types/api_key.py">APIKey</a></code>
- <code title="get /auths/api_key">client.auths.api_key.<a href="./src/pyopenwebui/resources/auths/api_key.py">retrieve</a>() -> <a href="./src/pyopenwebui/types/api_key.py">APIKey</a></code>
- <code title="delete /auths/api_key">client.auths.api_key.<a href="./src/pyopenwebui/resources/auths/api_key.py">delete</a>() -> <a href="./src/pyopenwebui/types/auths/api_key_delete_response.py">APIKeyDeleteResponse</a></code>

# Users

Types:

```python
from pyopenwebui.types import UserModel, UserListResponse, UserDeleteResponse
```

Methods:

- <code title="get /users/{user_id}">client.users.<a href="./src/pyopenwebui/resources/users/users.py">retrieve</a>(user_id) -> <a href="./src/pyopenwebui/types/shared/user_response.py">UserResponse</a></code>
- <code title="get /users/">client.users.<a href="./src/pyopenwebui/resources/users/users.py">list</a>(\*\*<a href="src/pyopenwebui/types/user_list_params.py">params</a>) -> <a href="./src/pyopenwebui/types/user_list_response.py">UserListResponse</a></code>
- <code title="delete /users/{user_id}">client.users.<a href="./src/pyopenwebui/resources/users/users.py">delete</a>(user_id) -> <a href="./src/pyopenwebui/types/user_delete_response.py">UserDeleteResponse</a></code>

## Permissions

Types:

```python
from pyopenwebui.types.users import PermissionRetrieveUserResponse
```

Methods:

- <code title="get /users/permissions/user">client.users.permissions.<a href="./src/pyopenwebui/resources/users/permissions/permissions.py">retrieve_user</a>() -> <a href="./src/pyopenwebui/types/users/permission_retrieve_user_response.py">object</a></code>

### User

Types:

```python
from pyopenwebui.types.users.permissions import UserCreateResponse
```

Methods:

- <code title="post /users/permissions/user">client.users.permissions.user.<a href="./src/pyopenwebui/resources/users/permissions/user.py">create</a>(\*\*<a href="src/pyopenwebui/types/users/permissions/user_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/users/permissions/user_create_response.py">object</a></code>

## Update

### Role

Methods:

- <code title="post /users/update/role">client.users.update.role.<a href="./src/pyopenwebui/resources/users/update/role.py">create</a>(\*\*<a href="src/pyopenwebui/types/users/update/role_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/user_model.py">Optional</a></code>

## User

Types:

```python
from pyopenwebui.types.users import UserSettings
```

### Settings

Methods:

- <code title="get /users/user/settings">client.users.user.settings.<a href="./src/pyopenwebui/resources/users/user/settings.py">retrieve</a>() -> <a href="./src/pyopenwebui/types/users/user_settings.py">Optional</a></code>
- <code title="post /users/user/settings/update">client.users.user.settings.<a href="./src/pyopenwebui/resources/users/user/settings.py">update</a>(\*\*<a href="src/pyopenwebui/types/users/user/setting_update_params.py">params</a>) -> <a href="./src/pyopenwebui/types/users/user_settings.py">UserSettings</a></code>

### Info

Types:

```python
from pyopenwebui.types.users.user import InfoRetrieveResponse, InfoUpdateResponse
```

Methods:

- <code title="get /users/user/info">client.users.user.info.<a href="./src/pyopenwebui/resources/users/user/info.py">retrieve</a>() -> <a href="./src/pyopenwebui/types/users/user/info_retrieve_response.py">object</a></code>
- <code title="post /users/user/info/update">client.users.user.info.<a href="./src/pyopenwebui/resources/users/user/info.py">update</a>(\*\*<a href="src/pyopenwebui/types/users/user/info_update_params.py">params</a>) -> <a href="./src/pyopenwebui/types/users/user/info_update_response.py">object</a></code>

# Chats

Types:

```python
from pyopenwebui.types import (
    ChatResponse,
    ChatTitleIDResponse,
    ChatListResponse,
    ChatDeleteResponse,
    ChatArchiveAllResponse,
    ChatListAllResponse,
    ChatListUserResponse,
    ChatUnshareResponse,
)
```

Methods:

- <code title="post /chats/{id}">client.chats.<a href="./src/pyopenwebui/resources/chats/chats.py">create</a>(id, \*\*<a href="src/pyopenwebui/types/chat_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/chat_response.py">Optional</a></code>
- <code title="get /chats/{id}">client.chats.<a href="./src/pyopenwebui/resources/chats/chats.py">retrieve</a>(id) -> <a href="./src/pyopenwebui/types/chat_response.py">Optional</a></code>
- <code title="get /chats/">client.chats.<a href="./src/pyopenwebui/resources/chats/chats.py">list</a>(\*\*<a href="src/pyopenwebui/types/chat_list_params.py">params</a>) -> <a href="./src/pyopenwebui/types/chat_list_response.py">ChatListResponse</a></code>
- <code title="delete /chats/{id}">client.chats.<a href="./src/pyopenwebui/resources/chats/chats.py">delete</a>(id) -> <a href="./src/pyopenwebui/types/chat_delete_response.py">ChatDeleteResponse</a></code>
- <code title="get /chats/{id}/archive">client.chats.<a href="./src/pyopenwebui/resources/chats/chats.py">archive</a>(id) -> <a href="./src/pyopenwebui/types/chat_response.py">Optional</a></code>
- <code title="post /chats/archive/all">client.chats.<a href="./src/pyopenwebui/resources/chats/chats.py">archive_all</a>() -> <a href="./src/pyopenwebui/types/chat_archive_all_response.py">ChatArchiveAllResponse</a></code>
- <code title="get /chats/{id}/clone">client.chats.<a href="./src/pyopenwebui/resources/chats/chats.py">clone</a>(id) -> <a href="./src/pyopenwebui/types/chat_response.py">Optional</a></code>
- <code title="get /chats/all">client.chats.<a href="./src/pyopenwebui/resources/chats/chats.py">list_all</a>() -> <a href="./src/pyopenwebui/types/chat_list_all_response.py">ChatListAllResponse</a></code>
- <code title="get /chats/list/user/{user_id}">client.chats.<a href="./src/pyopenwebui/resources/chats/chats.py">list_user</a>(user_id, \*\*<a href="src/pyopenwebui/types/chat_list_user_params.py">params</a>) -> <a href="./src/pyopenwebui/types/chat_list_user_response.py">ChatListUserResponse</a></code>
- <code title="get /chats/share/{share_id}">client.chats.<a href="./src/pyopenwebui/resources/chats/chats.py">retrieve_share</a>(share_id) -> <a href="./src/pyopenwebui/types/chat_response.py">Optional</a></code>
- <code title="post /chats/{id}/share">client.chats.<a href="./src/pyopenwebui/resources/chats/chats.py">share</a>(id) -> <a href="./src/pyopenwebui/types/chat_response.py">Optional</a></code>
- <code title="delete /chats/{id}/share">client.chats.<a href="./src/pyopenwebui/resources/chats/chats.py">unshare</a>(id) -> <a href="./src/pyopenwebui/types/chat_unshare_response.py">Optional</a></code>

## All

### Archived

Types:

```python
from pyopenwebui.types.chats.all import ArchivedListResponse
```

Methods:

- <code title="get /chats/all/archived">client.chats.all.archived.<a href="./src/pyopenwebui/resources/chats/all/archived.py">list</a>() -> <a href="./src/pyopenwebui/types/chats/all/archived_list_response.py">ArchivedListResponse</a></code>

### DB

Types:

```python
from pyopenwebui.types.chats.all import DBListResponse
```

Methods:

- <code title="get /chats/all/db">client.chats.all.db.<a href="./src/pyopenwebui/resources/chats/all/db.py">list</a>() -> <a href="./src/pyopenwebui/types/chats/all/db_list_response.py">DBListResponse</a></code>

## Archived

Types:

```python
from pyopenwebui.types.chats import ArchivedListResponse
```

Methods:

- <code title="get /chats/archived">client.chats.archived.<a href="./src/pyopenwebui/resources/chats/archived.py">list</a>(\*\*<a href="src/pyopenwebui/types/chats/archived_list_params.py">params</a>) -> <a href="./src/pyopenwebui/types/chats/archived_list_response.py">ArchivedListResponse</a></code>

## Tags

Types:

```python
from pyopenwebui.types.chats import (
    ChatIDTagModel,
    TagModel,
    TagListResponse,
    TagDeleteResponse,
    TagDeleteAllResponse,
)
```

Methods:

- <code title="post /chats/{id}/tags">client.chats.tags.<a href="./src/pyopenwebui/resources/chats/tags.py">create</a>(id, \*\*<a href="src/pyopenwebui/types/chats/tag_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/chats/chat_id_tag_model.py">Optional</a></code>
- <code title="get /chats/{id}/tags">client.chats.tags.<a href="./src/pyopenwebui/resources/chats/tags.py">list</a>(id) -> <a href="./src/pyopenwebui/types/chats/tag_list_response.py">TagListResponse</a></code>
- <code title="delete /chats/{id}/tags">client.chats.tags.<a href="./src/pyopenwebui/resources/chats/tags.py">delete</a>(id, \*\*<a href="src/pyopenwebui/types/chats/tag_delete_params.py">params</a>) -> <a href="./src/pyopenwebui/types/chats/tag_delete_response.py">Optional</a></code>
- <code title="delete /chats/{id}/tags/all">client.chats.tags.<a href="./src/pyopenwebui/resources/chats/tags.py">delete_all</a>(id) -> <a href="./src/pyopenwebui/types/chats/tag_delete_all_response.py">Optional</a></code>

# Documents

Types:

```python
from pyopenwebui.types import DocumentListResponse
```

Methods:

- <code title="post /documents/create">client.documents.<a href="./src/pyopenwebui/resources/documents/documents.py">create</a>(\*\*<a href="src/pyopenwebui/types/document_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/shared/document_response.py">Optional</a></code>
- <code title="get /documents/">client.documents.<a href="./src/pyopenwebui/resources/documents/documents.py">list</a>() -> <a href="./src/pyopenwebui/types/document_list_response.py">DocumentListResponse</a></code>

## Doc

Types:

```python
from pyopenwebui.types.documents import DocDeleteResponse
```

Methods:

- <code title="get /documents/doc">client.documents.doc.<a href="./src/pyopenwebui/resources/documents/doc/doc.py">retrieve</a>(\*\*<a href="src/pyopenwebui/types/documents/doc_retrieve_params.py">params</a>) -> <a href="./src/pyopenwebui/types/shared/document_response.py">Optional</a></code>
- <code title="post /documents/doc/update">client.documents.doc.<a href="./src/pyopenwebui/resources/documents/doc/doc.py">update</a>(\*\*<a href="src/pyopenwebui/types/documents/doc_update_params.py">params</a>) -> <a href="./src/pyopenwebui/types/shared/document_response.py">Optional</a></code>
- <code title="delete /documents/doc/delete">client.documents.doc.<a href="./src/pyopenwebui/resources/documents/doc/doc.py">delete</a>(\*\*<a href="src/pyopenwebui/types/documents/doc_delete_params.py">params</a>) -> <a href="./src/pyopenwebui/types/documents/doc_delete_response.py">DocDeleteResponse</a></code>

### Tags

Methods:

- <code title="post /documents/doc/tags">client.documents.doc.tags.<a href="./src/pyopenwebui/resources/documents/doc/tags.py">create</a>(\*\*<a href="src/pyopenwebui/types/documents/doc/tag_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/shared/document_response.py">Optional</a></code>

# Models

Types:

```python
from pyopenwebui.types import ModelModel, ModelDeleteResponse
```

Methods:

- <code title="post /models/update">client.models.<a href="./src/pyopenwebui/resources/models.py">update</a>(\*\*<a href="src/pyopenwebui/types/model_update_params.py">params</a>) -> <a href="./src/pyopenwebui/types/model_model.py">Optional</a></code>
- <code title="get /models/">client.models.<a href="./src/pyopenwebui/resources/models.py">list</a>(\*\*<a href="src/pyopenwebui/types/model_list_params.py">params</a>) -> <a href="./src/pyopenwebui/types/model_model.py">Optional</a></code>
- <code title="delete /models/delete">client.models.<a href="./src/pyopenwebui/resources/models.py">delete</a>(\*\*<a href="src/pyopenwebui/types/model_delete_params.py">params</a>) -> <a href="./src/pyopenwebui/types/model_delete_response.py">ModelDeleteResponse</a></code>
- <code title="post /models/add">client.models.<a href="./src/pyopenwebui/resources/models.py">add</a>(\*\*<a href="src/pyopenwebui/types/model_add_params.py">params</a>) -> <a href="./src/pyopenwebui/types/model_model.py">Optional</a></code>

# Prompts

Types:

```python
from pyopenwebui.types import PromptListResponse
```

Methods:

- <code title="post /prompts/create">client.prompts.<a href="./src/pyopenwebui/resources/prompts/prompts.py">create</a>(\*\*<a href="src/pyopenwebui/types/prompt_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/shared/prompt_model.py">Optional</a></code>
- <code title="get /prompts/">client.prompts.<a href="./src/pyopenwebui/resources/prompts/prompts.py">list</a>() -> <a href="./src/pyopenwebui/types/prompt_list_response.py">PromptListResponse</a></code>

## Commands

Types:

```python
from pyopenwebui.types.prompts import CommandDeleteResponse
```

Methods:

- <code title="get /prompts/command/{command}">client.prompts.commands.<a href="./src/pyopenwebui/resources/prompts/commands.py">retrieve</a>(command) -> <a href="./src/pyopenwebui/types/shared/prompt_model.py">Optional</a></code>
- <code title="post /prompts/command/{command}/update">client.prompts.commands.<a href="./src/pyopenwebui/resources/prompts/commands.py">update</a>(\*, path_command, \*\*<a href="src/pyopenwebui/types/prompts/command_update_params.py">params</a>) -> <a href="./src/pyopenwebui/types/shared/prompt_model.py">Optional</a></code>
- <code title="delete /prompts/command/{command}/delete">client.prompts.commands.<a href="./src/pyopenwebui/resources/prompts/commands.py">delete</a>(command) -> <a href="./src/pyopenwebui/types/prompts/command_delete_response.py">CommandDeleteResponse</a></code>

# Memories

Types:

```python
from pyopenwebui.types import (
    MemoryModel,
    MemoryListResponse,
    MemoryDeleteResponse,
    MemoryDeleteUserResponse,
    MemoryQueryResponse,
    MemoryResetResponse,
)
```

Methods:

- <code title="post /memories/{memory_id}/update">client.memories.<a href="./src/pyopenwebui/resources/memories/memories.py">update</a>(memory_id, \*\*<a href="src/pyopenwebui/types/memory_update_params.py">params</a>) -> <a href="./src/pyopenwebui/types/memory_model.py">Optional</a></code>
- <code title="get /memories/">client.memories.<a href="./src/pyopenwebui/resources/memories/memories.py">list</a>() -> <a href="./src/pyopenwebui/types/memory_list_response.py">MemoryListResponse</a></code>
- <code title="delete /memories/{memory_id}">client.memories.<a href="./src/pyopenwebui/resources/memories/memories.py">delete</a>(memory_id) -> <a href="./src/pyopenwebui/types/memory_delete_response.py">MemoryDeleteResponse</a></code>
- <code title="post /memories/add">client.memories.<a href="./src/pyopenwebui/resources/memories/memories.py">add</a>(\*\*<a href="src/pyopenwebui/types/memory_add_params.py">params</a>) -> <a href="./src/pyopenwebui/types/memory_model.py">Optional</a></code>
- <code title="delete /memories/delete/user">client.memories.<a href="./src/pyopenwebui/resources/memories/memories.py">delete_user</a>() -> <a href="./src/pyopenwebui/types/memory_delete_user_response.py">MemoryDeleteUserResponse</a></code>
- <code title="post /memories/query">client.memories.<a href="./src/pyopenwebui/resources/memories/memories.py">query</a>(\*\*<a href="src/pyopenwebui/types/memory_query_params.py">params</a>) -> <a href="./src/pyopenwebui/types/memory_query_response.py">object</a></code>
- <code title="post /memories/reset">client.memories.<a href="./src/pyopenwebui/resources/memories/memories.py">reset</a>() -> <a href="./src/pyopenwebui/types/memory_reset_response.py">MemoryResetResponse</a></code>

## Ef

Types:

```python
from pyopenwebui.types.memories import EfRetrieveResponse
```

Methods:

- <code title="get /memories/ef">client.memories.ef.<a href="./src/pyopenwebui/resources/memories/ef.py">retrieve</a>() -> <a href="./src/pyopenwebui/types/memories/ef_retrieve_response.py">object</a></code>

# Files

Types:

```python
from pyopenwebui.types import (
    FileCreateResponse,
    FileListResponse,
    FileDeleteResponse,
    FileDeleteAllResponse,
)
```

Methods:

- <code title="post /files/">client.files.<a href="./src/pyopenwebui/resources/files/files.py">create</a>(\*\*<a href="src/pyopenwebui/types/file_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/file_create_response.py">object</a></code>
- <code title="get /files/{id}">client.files.<a href="./src/pyopenwebui/resources/files/files.py">retrieve</a>(id) -> <a href="./src/pyopenwebui/types/shared/file_model.py">Optional</a></code>
- <code title="get /files/">client.files.<a href="./src/pyopenwebui/resources/files/files.py">list</a>() -> <a href="./src/pyopenwebui/types/file_list_response.py">FileListResponse</a></code>
- <code title="delete /files/{id}">client.files.<a href="./src/pyopenwebui/resources/files/files.py">delete</a>(id) -> <a href="./src/pyopenwebui/types/file_delete_response.py">object</a></code>
- <code title="delete /files/all">client.files.<a href="./src/pyopenwebui/resources/files/files.py">delete_all</a>() -> <a href="./src/pyopenwebui/types/file_delete_all_response.py">object</a></code>

## Content

Methods:

- <code title="get /files/{id}/content">client.files.content.<a href="./src/pyopenwebui/resources/files/content/content.py">retrieve</a>(id) -> <a href="./src/pyopenwebui/types/shared/file_model.py">Optional</a></code>

### FileName

Methods:

- <code title="get /files/{id}/content/{file_name}">client.files.content.file_name.<a href="./src/pyopenwebui/resources/files/content/file_name.py">retrieve</a>(file_name, \*, id) -> <a href="./src/pyopenwebui/types/shared/file_model.py">Optional</a></code>

# Tools

Types:

```python
from pyopenwebui.types import (
    ToolModel,
    ToolResponse,
    ToolListResponse,
    ToolDeleteResponse,
    ToolExportResponse,
)
```

Methods:

- <code title="post /tools/create">client.tools.<a href="./src/pyopenwebui/resources/tools/tools.py">create</a>(\*\*<a href="src/pyopenwebui/types/tool_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/tool_response.py">Optional</a></code>
- <code title="get /tools/id/{id}">client.tools.<a href="./src/pyopenwebui/resources/tools/tools.py">retrieve</a>(id) -> <a href="./src/pyopenwebui/types/tool_model.py">Optional</a></code>
- <code title="post /tools/id/{id}/update">client.tools.<a href="./src/pyopenwebui/resources/tools/tools.py">update</a>(\*, path_id, \*\*<a href="src/pyopenwebui/types/tool_update_params.py">params</a>) -> <a href="./src/pyopenwebui/types/tool_model.py">Optional</a></code>
- <code title="get /tools/">client.tools.<a href="./src/pyopenwebui/resources/tools/tools.py">list</a>() -> <a href="./src/pyopenwebui/types/tool_list_response.py">ToolListResponse</a></code>
- <code title="delete /tools/id/{id}/delete">client.tools.<a href="./src/pyopenwebui/resources/tools/tools.py">delete</a>(id) -> <a href="./src/pyopenwebui/types/tool_delete_response.py">ToolDeleteResponse</a></code>
- <code title="get /tools/export">client.tools.<a href="./src/pyopenwebui/resources/tools/tools.py">export</a>() -> <a href="./src/pyopenwebui/types/tool_export_response.py">ToolExportResponse</a></code>

## Valve

Types:

```python
from pyopenwebui.types.tools import ValveListResponse
```

Methods:

- <code title="get /tools/id/{id}/valves">client.tools.valve.<a href="./src/pyopenwebui/resources/tools/valve.py">list</a>(id) -> <a href="./src/pyopenwebui/types/tools/valve_list_response.py">object</a></code>

## Valves

Types:

```python
from pyopenwebui.types.tools import ValveUpdateResponse
```

Methods:

- <code title="post /tools/id/{id}/valves/update">client.tools.valves.<a href="./src/pyopenwebui/resources/tools/valves/valves.py">update</a>(id, \*\*<a href="src/pyopenwebui/types/tools/valve_update_params.py">params</a>) -> <a href="./src/pyopenwebui/types/tools/valve_update_response.py">object</a></code>

### Spec

Types:

```python
from pyopenwebui.types.tools.valves import SpecRetrieveResponse
```

Methods:

- <code title="get /tools/id/{id}/valves/spec">client.tools.valves.spec.<a href="./src/pyopenwebui/resources/tools/valves/spec.py">retrieve</a>(id) -> <a href="./src/pyopenwebui/types/tools/valves/spec_retrieve_response.py">object</a></code>

### User

Types:

```python
from pyopenwebui.types.tools.valves import UserRetrieveResponse, UserUpdateResponse
```

Methods:

- <code title="get /tools/id/{id}/valves/user">client.tools.valves.user.<a href="./src/pyopenwebui/resources/tools/valves/user/user.py">retrieve</a>(id) -> <a href="./src/pyopenwebui/types/tools/valves/user_retrieve_response.py">object</a></code>
- <code title="post /tools/id/{id}/valves/user/update">client.tools.valves.user.<a href="./src/pyopenwebui/resources/tools/valves/user/user.py">update</a>(id, \*\*<a href="src/pyopenwebui/types/tools/valves/user_update_params.py">params</a>) -> <a href="./src/pyopenwebui/types/tools/valves/user_update_response.py">object</a></code>

#### Spec

Types:

```python
from pyopenwebui.types.tools.valves.user import SpecRetrieveResponse
```

Methods:

- <code title="get /tools/id/{id}/valves/user/spec">client.tools.valves.user.spec.<a href="./src/pyopenwebui/resources/tools/valves/user/spec.py">retrieve</a>(id) -> <a href="./src/pyopenwebui/types/tools/valves/user/spec_retrieve_response.py">object</a></code>

# Functions

Types:

```python
from pyopenwebui.types import (
    FunctionModel,
    FunctionResponse,
    FunctionModel,
    FunctionListResponse,
    FunctionDeleteResponse,
)
```

Methods:

- <code title="post /functions/create">client.functions.<a href="./src/pyopenwebui/resources/functions/functions.py">create</a>(\*\*<a href="src/pyopenwebui/types/function_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/function_response.py">Optional</a></code>
- <code title="get /functions/id/{id}">client.functions.<a href="./src/pyopenwebui/resources/functions/functions.py">retrieve</a>(id) -> <a href="./src/pyopenwebui/types/function_model.py">Optional</a></code>
- <code title="post /functions/id/{id}/update">client.functions.<a href="./src/pyopenwebui/resources/functions/functions.py">update</a>(\*, path_id, \*\*<a href="src/pyopenwebui/types/function_update_params.py">params</a>) -> <a href="./src/pyopenwebui/types/function_model.py">Optional</a></code>
- <code title="get /functions/">client.functions.<a href="./src/pyopenwebui/resources/functions/functions.py">list</a>() -> <a href="./src/pyopenwebui/types/function_list_response.py">FunctionListResponse</a></code>
- <code title="delete /functions/id/{id}/delete">client.functions.<a href="./src/pyopenwebui/resources/functions/functions.py">delete</a>(id) -> <a href="./src/pyopenwebui/types/function_delete_response.py">FunctionDeleteResponse</a></code>
- <code title="post /functions/id/{id}/toggle">client.functions.<a href="./src/pyopenwebui/resources/functions/functions.py">toggle</a>(id) -> <a href="./src/pyopenwebui/types/function_model.py">Optional</a></code>
- <code title="post /functions/id/{id}/toggle/global">client.functions.<a href="./src/pyopenwebui/resources/functions/functions.py">toggle_global</a>(id) -> <a href="./src/pyopenwebui/types/function_model.py">Optional</a></code>

## Export

Types:

```python
from pyopenwebui.types.functions import ExportRetrieveResponse
```

Methods:

- <code title="get /functions/export">client.functions.export.<a href="./src/pyopenwebui/resources/functions/export.py">retrieve</a>() -> <a href="./src/pyopenwebui/types/functions/export_retrieve_response.py">ExportRetrieveResponse</a></code>

## Valves

Types:

```python
from pyopenwebui.types.functions import ValveRetrieveResponse, ValveUpdateResponse
```

Methods:

- <code title="get /functions/id/{id}/valves">client.functions.valves.<a href="./src/pyopenwebui/resources/functions/valves/valves.py">retrieve</a>(id) -> <a href="./src/pyopenwebui/types/functions/valve_retrieve_response.py">object</a></code>
- <code title="post /functions/id/{id}/valves/update">client.functions.valves.<a href="./src/pyopenwebui/resources/functions/valves/valves.py">update</a>(id, \*\*<a href="src/pyopenwebui/types/functions/valve_update_params.py">params</a>) -> <a href="./src/pyopenwebui/types/functions/valve_update_response.py">object</a></code>

### Spec

Types:

```python
from pyopenwebui.types.functions.valves import SpecRetrieveResponse
```

Methods:

- <code title="get /functions/id/{id}/valves/spec">client.functions.valves.spec.<a href="./src/pyopenwebui/resources/functions/valves/spec.py">retrieve</a>(id) -> <a href="./src/pyopenwebui/types/functions/valves/spec_retrieve_response.py">object</a></code>

### User

Types:

```python
from pyopenwebui.types.functions.valves import UserRetrieveResponse, UserUpdateResponse
```

Methods:

- <code title="get /functions/id/{id}/valves/user">client.functions.valves.user.<a href="./src/pyopenwebui/resources/functions/valves/user/user.py">retrieve</a>(id) -> <a href="./src/pyopenwebui/types/functions/valves/user_retrieve_response.py">object</a></code>
- <code title="post /functions/id/{id}/valves/user/update">client.functions.valves.user.<a href="./src/pyopenwebui/resources/functions/valves/user/user.py">update</a>(id, \*\*<a href="src/pyopenwebui/types/functions/valves/user_update_params.py">params</a>) -> <a href="./src/pyopenwebui/types/functions/valves/user_update_response.py">object</a></code>

#### Spec

Types:

```python
from pyopenwebui.types.functions.valves.user import SpecRetrieveResponse
```

Methods:

- <code title="get /functions/id/{id}/valves/user/spec">client.functions.valves.user.spec.<a href="./src/pyopenwebui/resources/functions/valves/user/spec.py">retrieve</a>(id) -> <a href="./src/pyopenwebui/types/functions/valves/user/spec_retrieve_response.py">object</a></code>

# Utils

## Gravatar

Types:

```python
from pyopenwebui.types.utils import GravatarRetrieveResponse
```

Methods:

- <code title="get /utils/gravatar">client.utils.gravatar.<a href="./src/pyopenwebui/resources/utils/gravatar.py">retrieve</a>(\*\*<a href="src/pyopenwebui/types/utils/gravatar_retrieve_params.py">params</a>) -> <a href="./src/pyopenwebui/types/utils/gravatar_retrieve_response.py">object</a></code>

## Code

Types:

```python
from pyopenwebui.types.utils import CodeFormatResponse
```

Methods:

- <code title="post /utils/code/format">client.utils.code.<a href="./src/pyopenwebui/resources/utils/code.py">format</a>(\*\*<a href="src/pyopenwebui/types/utils/code_format_params.py">params</a>) -> <a href="./src/pyopenwebui/types/utils/code_format_response.py">object</a></code>

## Markdown

Types:

```python
from pyopenwebui.types.utils import MarkdownCreateResponse
```

Methods:

- <code title="post /utils/markdown">client.utils.markdown.<a href="./src/pyopenwebui/resources/utils/markdown.py">create</a>(\*\*<a href="src/pyopenwebui/types/utils/markdown_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/utils/markdown_create_response.py">object</a></code>

## Pdf

Types:

```python
from pyopenwebui.types.utils import PdfCreateResponse
```

Methods:

- <code title="post /utils/pdf">client.utils.pdf.<a href="./src/pyopenwebui/resources/utils/pdf.py">create</a>(\*\*<a href="src/pyopenwebui/types/utils/pdf_create_params.py">params</a>) -> <a href="./src/pyopenwebui/types/utils/pdf_create_response.py">object</a></code>

## DB

Types:

```python
from pyopenwebui.types.utils import DBDownloadResponse
```

Methods:

- <code title="get /utils/db/download">client.utils.db.<a href="./src/pyopenwebui/resources/utils/db.py">download</a>() -> <a href="./src/pyopenwebui/types/utils/db_download_response.py">object</a></code>

## Litellm

### Config

Types:

```python
from pyopenwebui.types.utils.litellm import ConfigRetrieveResponse
```

Methods:

- <code title="get /utils/litellm/config">client.utils.litellm.config.<a href="./src/pyopenwebui/resources/utils/litellm/config.py">retrieve</a>() -> <a href="./src/pyopenwebui/types/utils/litellm/config_retrieve_response.py">object</a></code>

# Root

Types:

```python
from pyopenwebui.types import RootRetrieveResponse
```

Methods:

- <code title="get /">client.root.<a href="./src/pyopenwebui/resources/root.py">retrieve</a>() -> <a href="./src/pyopenwebui/types/root_retrieve_response.py">object</a></code>
