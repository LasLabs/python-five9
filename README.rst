|License MIT| | |Build Status| | |Coverage| | |Code Climate|

============
Python Five9
============

This library allows you to interact with the Five9 Settings and Statistics Web
Services using Python.

* `Read The API Documentation <https://laslabs.github.io/python-five9>`_

Installation
============

Installation is easiest using Pip and PyPi::

   pip install five9

If you would like to contribute, or prefer Git::

   git clone https://github.com/LasLabs/python-five9.git
   cd python-five9
   pip install -r requirements.txt
   pip install .

Usage
=====

Connect
-------

.. code-block:: python

   from five9 import Five9

   client = Five9('user', 'password')

Configuration Web Services
--------------------------

Documentation:

* `Five9 <http://webapps.five9.com/assets/files/for_customers/documentation/apis/config-webservices-api-reference-guide.pdf>`_
* `API Docs <https://laslabs.github.io/python-five9/AdminWebService.html>`_

Example Use:

.. code-block:: python

   client.configuration.getSkills()
   # Returns
   [{
       'description': None,
       'id': 266184L,
       'messageOfTheDay': None,
       'name': 'TestSkill',
       'routeVoiceMails': False
   }]

Statistics Web Services
-----------------------

Documentation:

* `Five9 <http://webapps.five9.com/assets/files/for_customers/documentation/apis/statistics-webservices-api-reference-guide.pdf>`_
* `API Docs <https://laslabs.github.io/python-five9/SupervisorWebService.html>`_

A supervisor session is required in order to perform most actions provided in the
Supervisor Web Service. Due to this, a session is implicitly created before the
supervisor is used.

The session is created with the following defaults. You can change the parameters
by changing the proper instance variable on the `Five9` object:

+----------------------+------------------------+---------------+
| Five9 Parameter      | Instance Variable      | Default       |
+======================+========================+===============+
| `forceLogoutSession` | `force_logout_session` | `True`        |
| `rollingPeriod`      | `rolling_period`       | `Minutes30`   |
| `statisticsRange`    | `statistics_range`     | `CurrentWeek` |
| `shiftStart`         | `shift_start_hour`     | `8`           |
| `timeZone`           | `time_zone_offset`     | `-7`          |
+----------------------+------------------------+---------------+

Example Use:

.. code-block:: python

   # Setup a session - required for most things
   client.supervisor.getUserLimits()
   # Returns
   {
       'mobileLimit': 0L,
       'mobileLoggedin': 0L,
       'supervisorLimit': 1L,
       'supervisorsLoggedin': 1L
   }

Known Issues / Roadmap
======================

* The supervisor session options should be represented in a class and documented,
  instead of the mostly undocumented free-form dictionary mapped to instance
  variables.

Credits
=======

Images
------

* LasLabs: `Icon <https://repo.laslabs.com/projects/TEM/repos/odoo-module_template/browse/module_name/static/description/icon.svg?raw>`_.

Contributors
------------

* Dave Lasley <dave@laslabs.com>

Maintainer
----------

.. image:: https://laslabs.com/logo.png
   :alt: LasLabs Inc.
   :target: https://laslabs.com

This module is maintained by LasLabs Inc.

.. |Build Status| image:: https://api.travis-ci.org/LasLabs/python-five9.svg?branch=master
   :target: https://travis-ci.org/LasLabs/python-five9
.. |Coverage| image:: https://codecov.io/gh/LasLabs/python-five9/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/LasLabs/python-five9
.. |Code Climate| image:: https://codeclimate.com/github/LasLabs/python-five9/badges/gpa.svg
   :target: https://codeclimate.com/github/LasLabs/python-five9
.. |License MIT| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT
