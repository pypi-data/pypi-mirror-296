# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yt_supercut']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'datasette-youtube-embed[datasette]>=0.1,<0.2',
 'datasette[datasette]>=0.64.3,<0.65.0',
 'sqlite-utils>=3.32.1,<4.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'tqdm>=4.65.0,<5.0.0',
 'typer>=0.9.0,<0.10.0',
 'webvtt-py>=0.4.6,<0.5.0',
 'yt-dlp']

entry_points = \
{'console_scripts': ['yt-supercut = yt_supercut.main:cli']}

setup_kwargs = {
    'name': 'yt-supercut',
    'version': '0.1.5',
    'description': '',
    'long_description': '# yt-supercut\n',
    'author': 'redraw',
    'author_email': 'redraw@sdf.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
