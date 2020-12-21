from setuptools import setup, find_packages


setup_args = {
    'name': 'PyZkUI',
    'version': '1.0.0',
    'description': 'A Python Zookeeper UI.',
    'long_description': 'A Zookeeper UI tool, base on Python/Flask.',
    'author': 'Derek Liu',
    'author_email': 'tliu1217@163.com',
    'license': 'MPL 2.0',
    'packages': find_packages('src'),
    'package_dir': {'': 'src'},
    # 'scripts': ['bin/PyZkServer'],
    'url': 'https://github.com/Harpsichord1207/PyZkUI',
    'install_requires': ['flask'],
    'classifiers': [
        'Programming Language :: Python :: 3.8',
    ],
    'keywords': 'Flask Zookeeper UI',
    'platforms': 'any',
    # 'package_data': {'PyZkUI': ['*']},  # TODO: no work
    'entry_points': {'console_scripts': ['PyZkServer=PyZkUI.cli:main']}
}

setup(**setup_args)
