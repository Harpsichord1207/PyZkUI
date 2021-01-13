import pathlib
from setuptools import setup, find_packages

read_me = pathlib.Path(__file__).parent.joinpath('README.md').read_text()

setup_args = {
    'name': 'PyZkUI',
    'version': '1.1.2',
    'description': 'A Python Zookeeper UI.',
    'long_description': read_me,
    'long_description_content_type': 'text/markdown',
    'author': 'Harpsichord',
    'author_email': 'tliu1217@163.com',
    'license': 'MPL 2.0',
    'packages': find_packages(),
    'url': 'https://github.com/Harpsichord1207/PyZkUI',
    'install_requires': ['flask', 'waitress', 'kazoo'],
    'classifiers': [
        'Programming Language :: Python :: 3.8',
    ],
    'keywords': 'Flask Zookeeper UI',
    'platforms': 'any',
    'package_data': {'': ['*', 'static/*', 'templates/*']},
    'entry_points': {'console_scripts': ['PyZkServer=PyZkUI:main']},
    'zip_safe': False
}

setup(**setup_args)
