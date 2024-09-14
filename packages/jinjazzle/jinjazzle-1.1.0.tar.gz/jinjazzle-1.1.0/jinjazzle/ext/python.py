"""
Description
-----------

PythonExtension provides the capability to do actions on the python version string.

.. autoclass: PythonExtension


Example
-------

.. code-block:: jinja

  # scaffold.python_min_version is "3.9" for example
  {% if (scaffold.python_min_version | pyversion)[1] <= 9 %}
  ...
  {% endif %}

  # the following would generate:
  # 3.9 3.10 3.11 3.12
  {{ scaffold.python_min_version | pyversion_sequence(12) }}

  # 3.9-dev, 3.10-dev, 3.11-dev, 3.12-dev
  {{ scaffold.python_min_version | pyversion_sequence(12, sep=", ", fmt="{major}.{minor}-dev") }}

"""

from jinja2.ext import Extension


def _pyversion(lhs):
    """
    Take a format value and return it formatted as tuple (Major, Minor)
    """
    values = str(lhs).split(".")
    return int(values[0]), int(values[1])


def _pyversion_format(lhs, fmt):
    """
    Take a format lhs and return it formatted according to `fmt`
    """
    values = _pyversion(lhs)
    return fmt.format(major=values[0], minor=values[1])


def _pyversion_sequence(lhs, stop, sep=" ", fmt="{major}.{minor}"):
    """
    Take a format value and return it formatted according to `fmt` for the
    range from minor lfs to minor stop
    """
    major, minor = _pyversion(lhs)
    values = list(range(minor, stop + 1))
    values = [fmt.format(major=major, minor=i) for i in values]
    values = sep.join(values)
    return values


# pylint: disable=abstract-method
class PythonExtension(Extension):
    """
    Jinja2 extension for python manipulation.
    """

    def __init__(self, environment):
        """
        Jinja2 Extension constructor.
        """
        super().__init__(environment)

        environment.filters["pyversion"] = _pyversion
        environment.filters["pyversion_format"] = _pyversion_format
        environment.filters["pyversion_sequence"] = _pyversion_sequence
