# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eta_utility',
 'eta_utility.connectors',
 'eta_utility.eta_x',
 'eta_utility.eta_x.agents',
 'eta_utility.eta_x.common',
 'eta_utility.eta_x.envs',
 'eta_utility.servers',
 'eta_utility.simulators',
 'eta_utility.timeseries',
 'eta_utility.type_hints']

package_data = \
{'': ['*'],
 'eta_utility': ['ju_extensions/*',
                 'ju_extensions/src/*',
                 'ju_extensions/src/etax/agents/*',
                 'ju_extensions/test/*',
                 'ju_extensions/test/etax/agents/*']}

install_requires = \
['asyncua-fork-for-eta-utility==1.0.7',
 'attrs>=23.1.0,<24.0.0',
 'cryptography>=41.0.4,<42.0.0',
 'fmpy>=0.3.5,<0.4.0',
 'lxml>=4.9.3,<5.0.0',
 'numpy>=1.26.0,<1.27.0',
 'pandas>=2.2.2,<2.3.0',
 'pymodbustcp==0.2.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests-cache>=1.2.0,<2.0.0',
 'requests>=2.31.0,<3.0.0',
 'wetterdienst>=0.88.0,<0.89.0',
 'xlrd>=2.0.1,<3.0.0']

extras_require = \
{'develop': ['gymnasium==0.29.1',
             'torch==2.0.0',
             'stable-baselines3==2.2.1',
             'tensorboard>=2.14.0,<2.15.0',
             'pyomo>=6.6.2,<6.7.0',
             'toml>=0.10.2,<0.11.0',
             'matplotlib>=3.7.0,<3.8.0',
             'keyboard>=0.13.5,<0.14.0',
             'pygame>=2.5.2,<3.0.0',
             'pyglet<2',
             'onnxruntime>=1.16.0,<2.0.0',
             'pytest>=7.4.2,<8.0.0',
             'pytest-cov>=4.1.0,<5.0.0',
             'openpyxl>=3.1.2,<4.0.0',
             'sphinx>=7.1.2,<8.0.0',
             'sphinx-rtd-theme>=1.3.0,<2.0.0',
             'sphinx-copybutton>=0.5.2,<0.6.0',
             'pre-commit>=3.4.0,<4.0.0',
             'black>=23.7,<23.8',
             'blacken_docs>=1.16,<1.17',
             'mypy>=1.9,<1.10',
             'types-python-dateutil>=2.8.19.14,<3.0.0.0',
             'types-requests>=2.31.0.4,<3.0.0.0',
             'types-pytz>=2024.1.0.20240203,<2025.0.0.0',
             'ruff>=0.6.0,<0.7.0'],
 'eta-x': ['gymnasium==0.29.1',
           'torch==2.0.0',
           'stable-baselines3==2.2.1',
           'tensorboard>=2.14.0,<2.15.0',
           'pyomo>=6.6.2,<6.7.0',
           'toml>=0.10.2,<0.11.0'],
 'examples': ['matplotlib>=3.7.0,<3.8.0',
              'keyboard>=0.13.5,<0.14.0',
              'pygame>=2.5.2,<3.0.0',
              'pyglet<2',
              'onnxruntime>=1.16.0,<2.0.0']}

entry_points = \
{'console_scripts': ['install-julia = eta_utility:install_julia',
                     'update-julia-agent = eta_utility:update_agent']}

setup_kwargs = {
    'name': 'eta-utility',
    'version': '3.2.2.post1',
    'description': 'A framework for researching energy optimization of factory operations',
    'long_description': 'ETA Utility Functions\n======================\n\nWhile there are many tools which are useful in the area of energy optimized factory operations, at the\n`ETA-Fabrik <https://www.ptw.tu-darmstadt.de>`_ at Technical University of Darmstadt we have recognized a lack of\ncomprehensive frameworks which combine functionality for optimization, simulation and communication with\ndevices in the factory.\n\nTherefore, we developed the *eta_utility* framework, which provides a standardized interface for the development\nof digital twins of factories or machines in a factory. The framework is based on the Gymnasium environment\nand follows a rolling horizon optimization approach. It provides standardized connectors for multiple\ncommunication protocols, including OPC UA and Modbus TCP. These facilities can be utilized to easily implement\nrolling horizon optimizations for factory systems and to directly control devices in the factory with the\noptimization results.\n\nFull Documentation can be found on the\n`Documentation Page <https://eta-utility.readthedocs.io/>`_.\n\nYou can find the `source code on github <https://github.com/PTW-TUDa/eta_utility/>`_. If you would like to contribute, please\ncheck our `working repository <https://git.ptw.maschinenbau.tu-darmstadt.de/eta-fabrik/public/eta-utility/>`_.\n\n\n.. warning::\n    This is beta software. APIs and functionality might change without prior notice. Please fix the version you\n    are using in your requirements to ensure your software will not be broken by changes in *eta_utility*.\n\nThe package *eta_utility* consists of five main modules and some additional functionality:\n\n- *eta_x* is the rolling horizon optimization module which combines the functionality of the\n  other modules. It is based on the *gymnasium* framework and utilizes\n  algorithms and functions from the *stable_baselines3* package. *eta_x* also contains extended base classes for\n  environments and additional agents (or algorithms).\n- The *connectors* module provides a standardized way to connect to machines and devices in a\n  factory or other factory systems (such as energy management systems). The **connectors** can also\n  handle subscriptions, for example to regularly store values in a database.\n- The *servers* module can be used to easily instantiate servers, for example to publish optimization\n  results.\n- *simulators* are interfaces based on the *fmpy* package which provide a way to simulate FMU\n  (Functional Mockup Unit) models.\n  The  *simulators* can be used to perform quick complete simulations or to step through simulation\n  models, as would be the case in rolling horizons optimization.\n- *timeseries* is an interface based on the *pandas* package to load and manipulate timeseries data\n  from CSV files. It can for example rename columns, resample data in more complex ways such as\n  multiple different resampling intervals or select random time slices from data. The *scenario_from_csv* function combines much of this functionality.\n- Other functionality includes some general utilities which are available on the top level of the\n  package.\n\nSome particularities\n----------------------\n\nIf you want to have logging output from eta utility, call:\n\n.. code-block::\n\n    from eta_utility import get_logger\n    get_logger()\n\n**eta_utility** uses dataframes to pass timeseries data and the dataframes are ensured to\ncontain timezone information where sensible.\n\nCiting this project\n--------------------\n\nPlease cite this project using our publication:\n\n.. code-block::\n\n    Grosch, B., Ranzau, H., Dietrich, B., Kohne, T., Fuhrländer-Völker, D., Sossenheimer, J., Lindner, M., Weigold, M.\n    A framework for researching energy optimization of factory operations.\n    Energy Inform 5 (Suppl 1), 29 (2022). https://doi.org/10.1186/s42162-022-00207-6\n\nWe would like to thank the many contributors who developed functionality for the package, helped with\ndocumentation or provided insights which helped to create the framework architecture.\n\n- *Niklas Panten* for the first implementation of the rolling horizon optimization now available in\n  *eta_x*,\n- *Nina Strobel* for the first implementation of the connectors,\n- *Thomas Weber* for contributions to the rolling horizon optimization with MPC algorithms,\n- *Guilherme Fernandes*, *Tobias Koch*, *Tobias Lademann*, *Saahil Nayyer*, *Magdalena Patyna*, *Jerome Stock*,\n- and all others who made small and large contributions.\n\nContributions\n--------------------\n\nIf you would like to contribute, please create an issue in the repository to discuss you suggestions.\nOnce the general idea has been agreed upon, you can create a merge request from the issue and\nimplement your changes there.\n',
    'author': 'Technical University of Darmstadt, Institute for Production Management, Technology and Machine Tools (PTW).',
    'author_email': 'info@ptw.tu-darmstadt.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.ptw.tu-darmstadt.de',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
