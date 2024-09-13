# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['majormode',
 'majormode.xebus',
 'majormode.xebus.constant',
 'majormode.xebus.model',
 'majormode.xebus.utils']

package_data = \
{'': ['*']}

install_requires = \
['perseus-core-library>=1.20.5,<2.0.0',
 'unidecode>=1.3.8,<2.0.0',
 'xebus-core-library>=1.4.10,<2.0.0']

setup_kwargs = {
    'name': 'xebus-family-data-library',
    'version': '1.0.8',
    'description': 'Python library for loading family data from sheets',
    'long_description': '# Xebus Family Data Python Library\nPython library for loading family data from different sheet sources.\n',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel.caune@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xebus/xebus-family-data-python-library',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
