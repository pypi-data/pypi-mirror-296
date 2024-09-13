# MIT License
#
# Copyright (c) 2024 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests


class Client:

    def __init__(self, base_url):
        self.base_url = base_url

    def create_document(self, content, metadata):
        url = f"{self.base_url}/api/v1/document"

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        data = {
            'content': content,
            'metadata': metadata
        }

        response = requests.post(url, json=data, headers=headers)

        return response.json()

    def search_documents(self, text, metadata, limit):
        url = f"{self.base_url}/api/v1/document/search"

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        data = {
            'text': text,
            'limit': limit,
            'metadata': metadata
        }

        response = requests.post(url, json=data, headers=headers)

        return response.json()
