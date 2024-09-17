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
import sys
import time
from typing import List

from jinja2 import Template
import pydantic

from aigc2md.api import openwebui
from aigc2md import config
from aigc2md import utils


post_archetype = """---
title: "{{ post.title }}"
author:
date: {{ post.date }}
deprecated:
  enable: false
  reference: []
draft: false
layout: single
mathjax: false
comment: true
keywords: {{ post.keywords }}
description:
aliases: []
categories: {{ post.categories }}
tags: {{ post.tags }}
original: true
reference: []
---

> {{ post.content }}

"""


class Post(pydantic.BaseModel):
    title: str
    author: str = ''
    date: str
    keywords: List[str] = []
    categories: List[str] = []
    tags: List[str] = []
    content: str


class Render:

    def __init__(self, force: bool = False):
        self.author_list = {
            'bge': 'b',
            'gemma': 'g',
            'hunyuan': 't',
            'llama3': 'l3',
            'qwen': 'a',
            'SparkDesk': 's',
        }
        self.rendered_flag = 'posted'
        self.client = openwebui.OpenWebUI(
            base_url=config.OPENWEBUI_BASE_URL, token=config.OPENWEBUI_JWT)

        self.force = force

    def _parse_tags(self, tags: List[dict]) -> List[str]:
        result = []
        for tag in tags:
            if tag:
              result.append(tag.get('name', ''))
        return result

    def _parse_author(self, model_name: str):
        for author in self.author_list:
            if author in model_name:
                return self.author_list[author]
        return ''

    def _parse_to_posts(self, messages: List[any]) -> List[Post]:
        result = []
        title: str
        for message in messages:
            if message.get('role', '') == 'user':
                title = message.get('content')
            elif message.get('role', '') == 'assistant':
                post = Post(
                    title=title,
                    author=self._parse_author(message.get('modelName')),
                    date=utils.timestamp_to_dateformat(
                        int(message.get('timestamp')),
                        format='%Y-%m-%d %H:%M:%S+0800',
                    ),
                    keywords=[],
                    categories=[],
                    tags=[],
                    content=message.get('content'),
                )
                result.append(post)
        return result

    def one(self, chat_id: str, output: str):
        """Render Chat by id

        Args:
            chat_id (str): chat id
        """
        # output directory
        if os.path.exists(output) is False:
            print(f'output directory not exists. auto create ...')
            os.makedirs(output)

        if os.path.isdir(output) is False:
            print(f'{output} is file, expect is dir')
            sys.exit(1)

        # Get Chat By Id
        chat = self.client.chats_retrieve(id=chat_id)

        if self.rendered_flag in self._parse_tags(chat.chat.get('tags', [])):
            print(f'chat: {chat.title}({chat_id}) already render with flag({self.rendered_flag}), please use `--force` flag to force render again')
            sys.exit(1)

        posts = self._parse_to_posts(chat.chat.get('messages', {}))
        for post in posts:
            file_path = os.path.join(output, f'{post.title.replace(" ", "").replace("/", "-")}.md')
            if os.path.exists(file_path) and self.force is False:
                file_path = file_path.replace(
                    '.md',
                    f'-{time.strftime("%Y%m%d-%H%M%S-%s", time.localtime(time.time()))}.md')

            with open(file_path, 'w', encoding='utf8') as out_file:
                tmle = Template(post_archetype)
                out_file.write(tmle.render({'post': post}))
                print(f'{post.title} render to {file_path} ...')

        # utils.pretty_output(
        #     field_names=['ID', 'title', 'updated_at', 'created_at',],
        #     rows=chats
        # )
