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


class Users:

    def __init__(self):
        self.client = openwebui.OpenWebUI(
            base_url=config.OPENWEBUI_BASE_URL, token=config.OPENWEBUI_JWT)

    def show(self, limit: int = 50, skip: int = 0):
        users = []
        for _user in self.client.users_list(limit=limit, skip=skip):
            users.append([
                _user.id,
                _user.name,
                _user.email,
                _user.role,
                _user.settings.ui.get('system') if _user.settings else '-',
                utils.timestamp_to_dateformat(_user.created_at),
                utils.timestamp_to_dateformat(_user.last_active_at),
            ])

        utils.pretty_output(
            field_names=['ID', 'name', 'email', 'role', 'system', 'created_at', 'last_active_at'],
            rows=users
        )
