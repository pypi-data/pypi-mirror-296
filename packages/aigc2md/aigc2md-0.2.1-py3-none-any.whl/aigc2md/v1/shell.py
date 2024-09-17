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

import os

from aigc2md import utils
from aigc2md.v1.chats import Chats
from aigc2md.v1.render import Render
from aigc2md.v1.users import Users


@utils.arg(
    '--limit', dest='limit', metavar='<integer>', type=int, default=50,
    help='page size.')
@utils.arg(
    '--skip', dest='skip', metavar='<integer>', type=int, default=0,
    help='skip.')
def do_users(args):
    """list users."""
    Users().show(limit=args.limit, skip=args.skip)


@utils.arg(
    '--page', dest='page', metavar='<integer>', type=int, default=1,
    help='page number.')
@utils.arg(
    '--skip', dest='skip', metavar='<integer>', type=int, default=0,
    help='skip.')
def do_chats(args):
    """chats actions."""
    Chats().list(page=args.page)


@utils.arg(
    '-i',
    '--id', dest='chat_id', metavar='<str>', help='chat id.',
    default="")
@utils.arg(
    '-f',
    '--force',
    dest='force',
    action="store_true",
    default=False,
    help='force render model(default is %(default)s)')
@utils.arg(
    '-o',
    '--output',
    dest='output', metavar='<str>', help='markdown post output directory.(default is %(default)s)',
    default=f'{os.getcwd()}/output')
def do_render(args):
    """render actions."""
    Render(force=args.force).one(chat_id=args.chat_id, output=args.output)
