from setuptools import setup, find_packages

setup_args = {
    'name': 'PyZkUI',
    'version': '1.0.0',
    'description': 'A Python Zookeeper UI.',
    'long_description': 'A Zookeeper UI tool, base on Python/Flask.',
    'author': 'Derek Liu',
    'author_email': 'tliu1217@163.com',
    'license': 'MPL 2.0',
    'packages': find_packages(),
    'url': 'https://github.com/Harpsichord1207/PyZkUI',
    'install_requires': ['flask', 'waitress'],
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
