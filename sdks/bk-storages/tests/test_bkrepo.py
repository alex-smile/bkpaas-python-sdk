# -*- coding: utf-8 -*-
"""
 * TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-蓝鲸 PaaS 平台(BlueKing-PaaS) available.
 * Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
 * Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at http://opensource.org/licenses/MIT
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 * an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations under the License.
"""
import io
from unittest import mock

import pytest
import requests
import requests_mock
from six.moves.urllib_parse import urljoin

from bkstorages.backends.bkrepo import BKGenericRepoClient, BKRepoFile, BKRepoStorage
from tests.utils import generate_random_string


@pytest.fixture
def username():
    return generate_random_string()


@pytest.fixture
def password():
    return generate_random_string()


@pytest.fixture
def endpoint():
    return "http://dummy.com"


@pytest.fixture
def session():
    return requests.session()


@pytest.fixture()
def adapter(session):
    adapter = requests_mock.Adapter()
    session.mount('http://', adapter)
    return adapter


@pytest.fixture
def bk_repo_cli(session, username, password, endpoint):
    bk_repo_cli = BKGenericRepoClient(
        bucket="dummy-bucket", username=username, password=password, project="dummy-project", endpoint_url=endpoint
    )
    with mock.patch("bkstorages.backends.bkrepo.requests.session", lambda: session):
        yield bk_repo_cli


@pytest.fixture
def make_dummy_file(adapter, endpoint):
    def core(key, content):
        def fake_upload(request):
            g._responses[0]._params["body"] = io.BytesIO(request.text.read())
            return True

        g = adapter.register_uri(
            'GET', urljoin(endpoint, f'/generic/dummy-project/dummy-bucket/{key}'), body=io.BytesIO(content)
        )
        adapter.register_uri(
            'PUT',
            urljoin(endpoint, f'/generic/dummy-project/dummy-bucket/{key}'),
            json={"code": 0, "message": ""},
            additional_matcher=fake_upload,
        )

    return core


@pytest.fixture
def bk_repo_storage(bk_repo_cli):
    storage = BKRepoStorage()
    storage.client = bk_repo_cli
    return storage


class TestBKRepoFile:
    def test_read(self, make_dummy_file, bk_repo_storage):
        key = "dummy-key"
        content = generate_random_string().encode()
        make_dummy_file(key, content)
        file = BKRepoFile(key, bk_repo_storage)
        assert file.read() == content

    def test_write(self, make_dummy_file, bk_repo_storage):
        key = "dummy-key"
        content = generate_random_string().encode()
        overwrite = generate_random_string().encode()
        make_dummy_file(key, content)
        file = BKRepoFile(key, bk_repo_storage)
        file.write(overwrite)
        file.flush()

        assert BKRepoFile(key, bk_repo_storage).read() == overwrite


def folder(name):
    return {"folder": True, "name": name}


def file(name):
    return {"folder": False, "name": name}


class TestBKRepoStorage:
    @pytest.mark.parametrize(
        "mock_responses, expect_directories, expect_files",
        [
            (([folder("d-a"), folder("d-b"), file("f-a")],), ["d-a", "d-b"], ["f-a"]),
            (
                ([folder("d-a"), folder("d-b"), file("f-a")], [folder("d-c"), folder("d-d"), file("f-b")]),
                ["d-a", "d-b", "d-c", "d-d"],
                ["f-a", "f-b"],
            ),
        ],
    )
    def test_list_dir(self, bk_repo_storage, adapter, endpoint, mock_responses, expect_directories, expect_files):
        path = "dummy-key"
        for idx, records in enumerate(mock_responses):
            adapter.register_uri(
                'GET',
                urljoin(
                    endpoint,
                    f'/repository/api/node/page/dummy-project/dummy-bucket/'
                    f'{path}?pageSize=1000&PageNumber={idx + 1}&includeFolder=True',
                ),
                json={"code": 0, "message": 0, "data": {"totalPages": len(mock_responses), "records": records}},
            )
        directories, files = bk_repo_storage.listdir(path)

        assert adapter.call_count == len(mock_responses)
        assert expect_directories == directories
        assert expect_files == files
