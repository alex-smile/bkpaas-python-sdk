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

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = ''

setup(
    long_description=readme,
    name='bkstorages',
    version='1.0.1',
    description='File storage backends for blueking PaaS platform',
    python_requires='<3.8,>=3.6',
    author='blueking',
    author_email='blueking@tencent.com',
    classifiers=['Programming Language :: Python', 'Programming Language :: Python :: 3', 'Framework :: Django'],
    packages=['bkstorages', 'bkstorages.backends'],
    package_dir={"": "."},
    package_data={},
    install_requires=['boto3>=1.4.1', 'curlify==2.*,>=2.2.1', 'requests', 'six>=1.14'],
    extras_require={
        "dev": ["django<3.0.0,>=1.7", "pytest>=3.0.4", "pytest-django>=3.1.2", "requests-mock==1.*,>=1.8.0"]
    },
)
