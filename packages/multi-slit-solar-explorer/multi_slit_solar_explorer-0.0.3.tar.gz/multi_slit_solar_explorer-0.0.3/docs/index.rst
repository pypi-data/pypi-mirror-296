Introduction
============

The Multi-slit Solar Explorer (MUSE) is a NASA satellite
designed to measure line profiles in the solar corona,
over a wide field of view,
with high temporal, spatial, and spectral resolution
:cite:p:`DePontieu2020`.
It achieves this using 37 spectrographic slits and a narrow
passband to simultaneously measure line profiles over
a 2D field of view.
MUSE is set to launch in 2027.

This package aims to provide a raytrace model of the MUSE
optical system to understand the distortion inherent in the
design of the optics.
The Python package :mod:`optika` is used to represent the
optical system and propagate rays through the system.

Installation
============

This package is published to PyPI and can be installed using pip:

.. code-block::

    pip install multi-slit-solar-explorer

API Reference
=============

.. autosummary::
    :toctree: _autosummary
    :template: module_custom.rst
    :recursive:

    muse


Bibliography
============

.. bibliography::

|


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
