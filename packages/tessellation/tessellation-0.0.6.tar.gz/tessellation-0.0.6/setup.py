# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tessellation',
 'tessellation.procgen',
 'tessellation.procgen.ga',
 'tessellation.procgen.rng']

package_data = \
{'': ['*']}

install_requires = \
['leap-ec>=0.8.1,<0.9.0',
 'matplotlib>=3.9.0,<4.0.0',
 'numpy>=2.0.1,<3.0.0',
 'scikit-image>=0.24.0,<0.25.0']

setup_kwargs = {
    'name': 'tessellation',
    'version': '0.0.6',
    'description': 'A service for procedurally generating tessellations.',
    'long_description': '# tessellation\nThis repository holds code to procedurally generate tessellations.\n',
    'author': "Anthony D'Achille",
    'author_email': 'adachille15@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/adachille/tessellation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
