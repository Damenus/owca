#!/bin/python3.6
# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os.path
import kaggle

'''
Downloads Moltean's fruits dataset using kaggle module
(install with 'pip install -r requirements.txt')
if dataset zip file is not found.
'''

dataset = 'moltean/fruits'
dataset_dir = 'tensorflow-inference/fruits-360'
if os.path.isdir(dataset_dir):
    print("Found dataset directory, exiting")
    exit(0)
print("Dataset not found, using kaggle-api tool for download")
kaggle.api.dataset_download_files(dataset, path="./tensorflow-inference/", unzip=True)
