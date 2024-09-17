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

from aigc2md.api import openwebui
from aigc2md import config
from aigc2md import utils


class Chats:

    def __init__(self):
        self.client = openwebui.OpenWebUI(
            base_url=config.OPENWEBUI_BASE_URL, token=config.OPENWEBUI_JWT)

    def list(self, page: int = 1):
        """Get Session User Chat List

        Args:
            page (int, optional): page number. Defaults to 1.
        """
        chats = []
        for _chat in self.client.chats_list(page):
            chats.append([
                _chat.id,
                _chat.title,
                utils.timestamp_to_dateformat(_chat.updated_at),
                utils.timestamp_to_dateformat(_chat.created_at),
            ])

        utils.pretty_output(
            field_names=['ID', 'title', 'updated_at', 'created_at',],
            rows=chats
        )

    def chat_by_id(self, id: str):
        """Get Chat By Id

        Args:
            id (str): chat id
        """

    def chat_tags_by_id(self, id: str):
        """Get Chat Tags By Id

        Args:
            id (str): chat id
        """
