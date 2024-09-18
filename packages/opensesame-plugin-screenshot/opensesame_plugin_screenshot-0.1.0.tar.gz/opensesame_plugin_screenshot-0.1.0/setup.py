# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensesame_plugins',
 'opensesame_plugins.screenshot',
 'opensesame_plugins.screenshot.screenshot']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'opensesame-plugin-screenshot',
    'version': '0.1.0',
    'description': 'An OpenSesame Plugin for saving screenshots of stimuli and other screens within an experiment.',
    'long_description': "OpenSesame Plug-in: Screenshot\n==========\n\n*An OpenSesame plug-in for saving screenshots of stimuli and other screens within an experiment.*  \n\nCopyright, 2024, Bob Rosbag  \n\n\n## 1. About\n--------\n\nThis plug-in can make screenshots of stimuli and other screens and save it to png in the folder 'screenshots/subject-*/filename'. \n\nThis plug-in has two options:\n\n- *Verbose mode* for testing experiments.\n- *Screenshot file name*.\n\n\n## 2. LICENSE\n----------\n\nThe Screenshot plug-in is distributed under the terms of the GNU General Public License 3.\nThe full license should be included in the file COPYING, or can be obtained from\n\n- <http://www.gnu.org/licenses/gpl.txt>\n\nThis plug-in contains works of others. Icons are derivatives of the Faenza icon theme.\n  \n  \n## 3. Documentation\n----------------\n\nInstallation instructions and documentation on OpenSesame are available on the documentation website:\n\n- <http://osdoc.cogsci.nl/>\n",
    'author': 'Bob Rosbag',
    'author_email': 'debian@bobrosbag.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dev-jam/opensesame-plugin-screenshot',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
