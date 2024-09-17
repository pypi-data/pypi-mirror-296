# Copyright 2024 xiexianbin.cn
# All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#        http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

""" open-webui API for https://ai.80.xyz/api/v1/docs """

from pyopenwebui import Pyopenwebui, DefaultHttpxClient


class OpenWebUI:

    def __init__(self, base_url: str, token: str) -> None:
        self.client = Pyopenwebui(
          # Or use the `PYOPENWEBUI_BASE_URL` env var
          base_url=base_url,
          max_retries=3,
          default_headers={
            'Authorization': f'Bearer {token}'},
          http_client=DefaultHttpxClient(),
      )

    def chats_list(self, page: int = 1):
        """Get Session User Chat List"""
        return self.client.chats.list(page=page)

    def chats_retrieve(self, id: str):
        """Get Chat By Id"""
        return self.client.chats.retrieve(id=id)

    def chats_tags_list(self, id: str):
        """Get Chat Tags By Id"""
        return self.client.chats.tags.list(id=id)

    def chats_tags_create(self, chat_id: str, tag_name: str):
        """Add Chat Tag By Id"""
        return self.client.chats.tags.create(id=id, chat_id=id, tag_name=tag_name)

    def users_list(self, limit: int = 50, skip: int = 0):
        """Get Users"""
        return self.client.users.list(limit=limit, skip=skip)
