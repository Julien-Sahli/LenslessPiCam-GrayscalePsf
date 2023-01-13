"""
Apply a few ADMM iterations to quiclky converge to an avanced result, then refines it with gradient descent.

```
python scripts/recon/gradmm.py --psf_fp data/psf/tape_rgb.png \
--data_fp data/raw_data/thumbs_up_rgb.png --n_iter 5
```

"""

import os
import time
import pathlib as plib
import click
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from lensless.io import load_data
from lensless import ADMM
from lensless import GradientDescent
from save_recon import make_dir


@click.command()
@click.option(
    "--psf_fp",
    type=str,
    help="File name for recorded PSF.",
)
@click.option(
    "--data_fp",
    type=str,
    help="File name for raw measurement data.",
)
@click.option(
    "--n_iter_admm",
    type=int,
    default=5,
    help="Number of iterations for the ADMM part.",
)
@click.option(
    "--n_iter_grad",
    type=int,
    default=5,
    help="Number of iterations for the gradient descent part.",
)
@click.option(
    "--downsample",
    type=float,
    default=4,
    help="Downsampling factor.",
)
@click.option(
    "--shape",
    default=None,
    nargs=2,
    type=int,
    help="Image shape (height, width) for reconstruction.",
)
@click.option(
    "--disp",
    default=1,
    type=int,
    help="How many iterations to wait for intermediate plot. Set to negative value for no intermediate plots.",
)
@click.option(
    "--flip",
    is_flag=True,
    help="Whether to flip image.",
)
@click.option(
    "--save",
    is_flag=True,
    help="Whether to save intermediate and final reconstructions.",
)
@click.option(
    "--gray",
    is_flag=True,
    help="Whether to perform construction with grayscale.",
)
@click.option(
    "--bayer",
    is_flag=True,
    help="Whether image is raw bayer data.",
)
@click.option(
    "--no_plot",
    is_flag=True,
    help="Whether to no plot.",
)
@click.option(
    "--bg",
    type=float,
    help="Blue gain.",
)
@click.option(
    "--rg",
    type=float,
    help="Red gain.",
)
@click.option(
    "--gamma",
    default=None,
    type=float,
    help="Gamma factor for plotting.",
)
@click.option(
    "--single_psf",
    is_flag=True,
    help="Same PSF for all channels (sum) or unique PSF for RGB.",
)
def gradmm(
    psf_fp,
    data_fp,
    n_iter_admm,
    n_iter_grad,
    downsample,
    disp,
    flip,
    gray,
    bayer,
    bg,
    rg,
    gamma,
    save,
    no_plot,
    single_psf,
    shape,
):
    psf, data = load_data(
        psf_fp=psf_fp,
        data_fp=data_fp,
        downsample=downsample,
        bayer=bayer,
        blue_gain=bg,
        red_gain=rg,
        plot=not no_plot,
        flip=flip,
        gamma=gamma,
        gray=gray,
        single_psf=single_psf,
        shape=shape,
    )

    if disp < 0:
        disp = None
    if save:
        save = make_dir("gradmm_", data_fp)

    start_time = time.time()
    recon = ADMM(psf)
    recon.set_data(data)
    print(f"Setup time (ADMM) : {time.time() - start_time} s")

    start_time = time.time()
    tmp = recon.apply(n_iter=n_iter_admm, disp_iter=disp, save=save, gamma=gamma, plot=not no_plot)
    print(f"Processing time (ADMM) : {time.time() - start_time} s")

    start_time = time.time()
    recon = GradientDescent(psf=psf, initial_est=np.array(tmp[0]))
    recon.set_data(data)
    print(f"Setup time (Gradient Descent) : {time.time() - start_time} s")

    start_time = time.time()
    res = recon.apply(n_iter=n_iter_grad, disp_iter=disp, save=save, gamma=gamma, plot=not no_plot)
    print(f"Processing time (Gradient Descent) : {time.time() - start_time} s")

    if not no_plot:
        plt.show()
    if save:
        np.save(str(plib.Path(save) / "final_reconstruction.npy"), res[0])
        print(f"Files saved to : {save}")


if __name__ == "__main__":
    gradmm()