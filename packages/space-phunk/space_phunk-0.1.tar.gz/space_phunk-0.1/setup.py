# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phunk']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=6.0',
 'lmfit>=1.2.2',
 'matplotlib>=3.4.3',
 'pandas>=1.3.5',
 'requests>=2.26.0,<3.0.0',
 'sbpy>=0.3',
 'space-rocks>=1.9']

extras_require = \
{':python_version >= "3.11" and python_version < "4.0"': ['numpy>=1.24'],
 ':python_version >= "3.7" and python_version < "3.11"': ['numpy>=1.21']}

setup_kwargs = {
    'name': 'space-phunk',
    'version': '0.1',
    'description': 'Fit photometric phase curves of asteroids.',
    'long_description': '<p align="center">\n  <img width="260" src="https://raw.githubusercontent.com/maxmahlke/phunk/main/docs/gfx/logo_phunk.svg">\n</p>\n\n<p align="center">\n  <a href="https://github.com/maxmahlke/phunk#features"> Features </a> - <a href="https://github.com/maxmahlke/phunk#install"> Install </a> - <a href="https://github.com/maxmahlke/phunk#documentation"> Documentation </a>\n</p>\n\n<div align="center">\n  <a href="https://img.shields.io/pypi/pyversions/space-phunk">\n    <img src="https://img.shields.io/pypi/pyversions/space-phunk"/>\n  </a>\n  <a href="https://img.shields.io/pypi/v/space-phunk">\n    <img src="https://img.shields.io/pypi/v/space-phunk"/>\n  </a>\n  <a href="https://readthedocs.org/projects/phunk/badge/?version=latest">\n    <img src="https://readthedocs.org/projects/phunk/badge/?version=latest"/>\n  </a>\n</div>\n\n\n## Features\n\nObserve the phase curve of an asteroid, ...\n\n``` python\n>>> from phunk import PhaseCurve\n>>> # Observations of (20) Massalia from Gehrels 1956\n>>> phase = [0.57, 1.09, 3.20, 10.99, 14.69, 20.42]\n>>> mag = [6.555, 6.646, 6.793, 7.130, 7.210, 7.414]\n>>> pc = PhaseCurve(phase=phase, mag=mag)\n```\n\n..., fit it in one of multiple photometric models, ....\n\n``` python\n>>> pc.fit(["HG", "HG1G2", "sHG1G2"])\n```\n\n..., and plot / process the results.\n\n``` python\n>>> pc.HG1G2.H\n>>> pc.HG12.H\n>>> pc.plot()\n```\n\nProvide a target to ``PhaseCurve`` to have ``phunk`` compute the required ephemerides for you.\n\n``` python\n>>> epoch = [35193, 35194, 35198, 35214, 35223, 35242]  # in MJD\n>>> pc = PhaseCurve(epoch=epoch, mag=mag, target=\'massalia\')\n>>> pc.fit([\'sHG1G2\'])  # phunk computes required RA, Dec, and phase at epoch of observation\n>>> pc.sHG1G2.H\n```\n\n## Install\n\nInstall from PyPi using `pip`:\n\n     $ pip install space-phunk\n\nThe minimum required `python` version is 3.8.\n\n\n## Documentation\n\nCheck out the documentation at [phunk.readthedocs.io](https://phunk.readthedocs.io/en/latest/).\n\n## Acknowledgements\n\nThis package uses the photometric model implementations provided by [sbpy](https://sbpy.readthedocs.io/en/stable).\n',
    'author': 'Max Mahlke',
    'author_email': 'max.mahlke@oca.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://phunk.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
