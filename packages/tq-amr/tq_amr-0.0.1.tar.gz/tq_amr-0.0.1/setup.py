from setuptools import setup, find_packages
import os.path

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Some simple utils.'

setup(
    name='tq_amr',
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://gitee.com/torchW/tq_amr.git',
    author='TripleQuiz',
    author_email='triple_quiz@163.com',
    license='MIT',
    keywords=['python', 'util', 'analyze module relationship', 'graph', 'dot'],
    python_requires='>=3.8, <3.12',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Natural Language :: Chinese (Simplified)',
    ],
    packages=find_packages(include=['tq_amr', 'tq_amr.*']),
    install_requires=[
        'pydot==3.0.1',
        'pygraphviz==1.11',
        'tq_utils>=0.1.3.post1',
    ],
    include_package_data=True,
    exclude_package_data={},
    zip_safe=False,
)

"""
打包发布步骤：
1. 测试代码
2. commit & create tag
3. 打包源分发包和轮子，命令：python setup.py sdist bdist_wheel
4. PyPI发布，命令：twine upload -r tq_amr dist/*
"""
