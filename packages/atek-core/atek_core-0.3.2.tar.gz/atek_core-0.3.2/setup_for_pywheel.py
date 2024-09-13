# Copyright (c) Meta Platforms, Inc. and affiliates.
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

from setuptools import find_packages, setup


def main():
    setup(
        name="atek-core",
        version="0.3.2",
        description="Aria train and evaluation kits",
        author="Meta Reality Labs Research",
        packages=find_packages(),  # automatically discover all packages and subpackages
        install_requires=[
            "torch==2.4.1",  # Assuming 'pytorch=2' corresponds to this version
            "torchvision",
            "fvcore",
            "iopath",
            "tqdm",
            "scipy",
            "webdataset",
            "trimesh",
            "pybind11",
            "toolz",
            "opencv-python",
            # Add other dependencies that can be resolved by pip here
        ],
        dependency_links=[
            "git+https://github.com/facebookresearch/pytorch3d.git@stable#egg=pytorch3d",
            "git+https://github.com/facebookresearch/detectron2.git#egg=detectron2",
        ],
        extras_require={
            "dev": [
                "projectaria-tools==1.5.4",
            ]
        },
    )


if __name__ == "__main__":
    main()
