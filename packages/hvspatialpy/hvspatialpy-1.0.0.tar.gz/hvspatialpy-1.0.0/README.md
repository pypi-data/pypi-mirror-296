<!-- Our title -->
<div align="center">
  <h3 style="font-size: 25px;">hvspatialpy</h3>
</div>

<!-- Short description -->
<p align="center">
   A python package that evaluates the spatial variability of a site utilizing HVSR.
</p>

[![DOI](https://zenodo.org/badge/857518332.svg)](https://zenodo.org/doi/10.5281/zenodo.13770431)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/80fc3884310249019b8508415f516f53)](https://app.codacy.com/gh/fjornelas/hvspatialpy/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
![pypi - version](https://img.shields.io/pypi/v/hvspatialpy)
[![Pages](https://github.com/fjornelas/hvspatialpy/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/fjornelas/hvspatialpy/actions/workflows/pages/pages-build-deployment)
![GitHub License](https://img.shields.io/github/license/fjornelas/hvspatialpy)
[![Report Issues!](https://img.shields.io/badge/Report%20Issues-Here-1abc9c.svg)](https://github.com/fjornelas/hvspatialpy/issues)
[![Open Source?
Yes!](https://img.shields.io/badge/Open%20Source-Yes-green.svg)](https://github.com/fjornelas/hvspatialpy)

<div align="center">
    <h3 style=" font-size: 25px;">Authors</h3>
</div>

<!-- Short description -->

<p align="center">
   Francisco Javier G. Ornelas<sup>1</sup>, Scott J. Brandenberg<sup>1</sup>, Jonathan P. Stewart<sup>1</sup>
</p>

<sup>1</sup> University of California, Los Angeles (UCLA) <br>

<div style="text-align: center;">
    <h3 style=" font-size: 25px;">Table of Contents</h3>
</div>


 - [Introduction](#introduction)                                                      
 - [Background](#Background)   
 - [Getting started](#Getting-started) 
 - [Citation](#Citation)       
 - [Issues](#Issues)  

# Introduction

---

A python package that can evaluate the spatial variability of a site utilizing the Horizontal-to-Vertical Spectral Ratio (HVSR). 
This package works by taking multiple HVSR curves that were evalautes around a site, and compares them to a reference curve.
These curves are then separated further by frequency interval to evalaute the variability in terms of resonant peaks. 
This package was developed by Francisco Javier G. Ornelas under the supervision
of Dr. Jonathan P. Stewart and Dr. Scott J. Brandenberg at the University of California, Los Angeles (UCLA). 

# Background

---

HVSR is derived from ratios of the horizontal and vertical components
of a Fourier Amplitude Spectrum (FAS) from a 3-component recording of
microtremors or earthquakes. This is done by recording ground vibrations either from
temporarily-deployed or permanently-installed seismometers, for a relatively short
period of time (~1-2 hrs) or a longer period of time.

This method or technique was first proposed by Nogoshi and Igarashi (1971) 
<a href="https://www.scirp.org/reference/referencespapers?referenceid=3100696" target="_blank">[ABSTRACT]</a> and 
later popularized by Nakamura (1989) <a href="https://trid.trb.org/View/294184" target="_blank">[ABSTRACT]</a>.
The method works by assuming that the horizontal wavefield is amplified as seismic waves propagate
through the soil deposits compared to the vertical wavefield.

HVSR can be useful in site characterization since it can identify resonant frequencies at sites, through peaks in
an HVSR spectrum. Studies have also found that the lowest peak in HVSR spectra can be associated with the fundamental
frequency of a site (e.g., <a href="https://link.springer.com/article/10.1007/s10518-012-9413-4" target="_blank">[ABSTRACT]</a>).
The identification of these peaks is significant because they correlate with impedance contrasts at a given site. When multiple HVSR 
surveys are conducted at the same location, it becomes possible to illustrate the spatial variability of impedance contrasts across the site. Consequently, 
HVSR is a valuable tool for assessing and understanding the spatial heterogeneity of site characteristics

# Getting started

---

## Installation


hvspatialpy is available using pip and can be installed with:

- Jupyter Notebook
`pip install hvspatialpy`
- PyPI
`py -m pip install hvspatialpy`
## Usage


`hvspatialpy` is a python package that evaluates spatial variability at a site utilizing HVSR. 
The library contains various features, such as:
- A graphical user interface (GUI) to use in inputting parameters.
- The ability to vary the frequency interval of interest, to narrow down which peaks one wants to evaluate.
- A plot showing the approximate location of the site with all the tests done. These tests are color coded based on the
correlation type used (e.g., LCSS).

Examples of these can be found under the examples folder in the Github repository <a href="https://github.com/fjornelas/hvspatialpy" target="_blank">[GIT]</a>

### Example of Frequency Interval Selection and Test Locations

<img src="https://github.com/fjornelas/hvspatialpy/blob/main/fig/spatial_figure.png?raw=true" width="775">

# Citation

---

If you use hvspatialpy (directly or as a dependency of another package) for work resulting in an academic publication or
other instances, we would appreciate if you cite the following:

> Ornelas, F. J. G., Brandenberg, S. J., & Stewart, J. P. (2024). hvspatialpy (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.13770432.

# Issues

---

Please report any issues or leave comments on the <a href="https://github.com/fjornelas/hvspatialpy/issues" target="_blank">Issues</a> page.

## License

This project has been licensed under [![The GNU General Public License v3.0](https://www.gnu.org/graphics/gplv3-88x31.png "The GNU General Public License v3.0")](https://www.gnu.org/licenses/gpl-3.0.en.html)
more information about the license can be found here <a href="https://github.com/fjornelas/hvsrprocpy/blob/main/LICENSE" target="_blank">[LICENSE]</a>.
