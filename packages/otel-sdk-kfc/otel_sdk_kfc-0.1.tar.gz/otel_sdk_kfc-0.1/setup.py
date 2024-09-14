#!/usr/bin/python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('requirements.txt') as fp:
    install_requires = fp.read()
setup(
    name="otel_sdk_kfc",
    version="0.1",
    long_description="".join(open("README.md", encoding="utf-8").readlines()),
    long_description_content_type="text/markdown",
    license="MIT",
    # packages=["infrastack", "infrastack.tracer", "infrastack.logs", "infrastack.flask"],
    packages=find_packages(),
    install_requires=install_requires,
    python_requires=">= 3",
    zip_safe=False,
)



