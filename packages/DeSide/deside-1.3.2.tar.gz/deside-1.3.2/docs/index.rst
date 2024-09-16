.. DeSide documentation master file, created by
   sphinx-quickstart on Mon Apr 19 18:23:58 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DeSide's documentation!
==================================

The usage of DeSide as a Python package is described in this documentation.

----

What is DeSide?
---------------

DeSide is a deep-learning and single-cell-based deconvolution method for solid tumors.
It enables the inference of cellular proportions of different cell types from bulk RNA-seq data.
DeSide was developed by Xin Xiong and Yerong Liu under the guidance and collaboration of
the `Li(X) Lab <https://isynbio.siat.ac.cn/Li(x)lab/>`_ at the Institute for Synthetic Biology Research (iSynBio), Chinese Academy of Sciences,
and the `Tian Lab <https://physics.hkbu.edu.hk/people/tian-liang>`_ at Hong Kong Baptist University (HKBU).

Contents
------------------------------
- `Installation <https://deside.readthedocs.io/en/latest/installation.html>`_
- `Usage <https://deside.readthedocs.io/en/latest/usage.html>`_
- `Datasets <https://deside.readthedocs.io/en/latest/datasets.html>`_
- `Functions <https://deside.readthedocs.io/en/latest/functions.html>`_


`Our manuscript <https://www.biorxiv.org/content/10.1101/2023.05.11.540466v1>`_ consists of the following four parts (see figure below):

- DNN Model
- Single Cell Dataset Integration
- Cell Proportion Generation
- Bulk Tumor Synthesis

.. image:: https://raw.githubusercontent.com/OnlyBelter/DeSide/main/Fig.1a_b.svg
   :alt: Overview of DeSide
   :width: 800

Please check `Usage <https://deside.readthedocs.io/en/latest/usage.html>`_ for more details of each part.


.. toctree::
   :maxdepth: 2
   :hidden:

   installation.md
   usage.md
   datasets.md
   functions.rst
   changelog.md
   contact.md
   GitHub repository <https://github.com/OnlyBelter/DeSide>




Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
