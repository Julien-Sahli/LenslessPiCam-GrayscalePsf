# CHANGELOG.md

## Unreleased

#### Added

- Support of 3D data
	- Support of 3D psfs, which have to be provided as .npy files.
	- Support of 3D reconstruction for vanilla Gradient Descent (APGD ? todo check)
	- Support of 3D data in lensless/plot.py. All methods are still compatible with 2D data. Able to tell apart grayscale 3D data from rgb 2D data (which both have 3 dimensions) according to shape of the data.

- Camera Simulator (scripts/simulator)
	- scripts/simulator/psf_generator.py : Script that generates 3D PSFs from 2D height maps / normal maps or masks.
	- scripts/simulator/simulator.py : Script that takes a 3D PSF and a scene as an input to generate lensless data using raytracing. A scene is the combination of two 2D images : an irradiance map and a depth map
	- scripts/simulator/

- New scripts
	- scripts/conversion/mat_to_npy.py : Script to export mat data for `https://github.com/Waller-Lab/DiffuserCam` to usable .npy
	- scripts/conversion/npy_to_obj.py : Script to export npy data to wavefront .obj scatter plots for quick viewing purposes
	- scripts/recon/gradmm.py : Script that reconstructs image by applying a few iterations of ADMM to quickly get a general shape of the recon and then applies gradient descent on it to make it more precise. Inconclusive results yet.
	- scripts/recon/save_recon.py : new method used by recon scripts to create a new folder for output if a folder of the same name already exists

#### Changed

- The data of images and psfs are now always stored as (depth, width, height, color) arrays in memory. Each reconstruction algorithm was adapted accordingly.
- Fixed a typo the GradientDescent class

#### Bugfix

- Loading grayscale PSFs would cause an dimension error when removing the background pixels

## 1.0.2 - (2022-05-31)

#### Added

- Example of RGB reconstruction with complex-valued FFT: `scripts/recon/apgd_pycsou.py`

#### Bugfix

- Possible shape mismatch when using the real-valued FFT: forward and backward.

## 1.0.1 - (2022-04-26)

#### Added

- Scripts for collecting MNIST.
- Option to collect grayscale data.

#### Changed

- Restructure example scripts, i.e. subfolder `recon` for reconstructions.
- Remove heavy installs from setup (e.g. pycsou, lpips, skikit-image).


## 1.0.0 - (2022-03-21)

First version!
