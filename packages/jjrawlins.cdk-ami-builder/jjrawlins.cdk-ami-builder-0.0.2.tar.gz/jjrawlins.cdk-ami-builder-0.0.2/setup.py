import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "jjrawlins.cdk-ami-builder",
    "version": "0.0.2",
    "description": "Creates an EC2 AMI using an Image Builder Pipeline and returns the AMI ID.",
    "license": "Apache-2.0",
    "url": "https://github.com/jjrawlins/cdk-ami-builder-construct.git",
    "long_description_content_type": "text/markdown",
    "author": "Jayson Rawlins<jayson.rawlins@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/jjrawlins/cdk-ami-builder-construct.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "jjrawlins.cdk_ami_builder",
        "jjrawlins.cdk_ami_builder._jsii"
    ],
    "package_data": {
        "jjrawlins.cdk_ami_builder._jsii": [
            "cdk-ami-builder@0.0.2.jsii.tgz"
        ],
        "jjrawlins.cdk_ami_builder": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.141.0, <3.0.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.98.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
