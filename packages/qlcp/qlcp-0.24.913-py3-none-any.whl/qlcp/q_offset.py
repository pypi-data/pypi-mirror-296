# -*- coding: utf-8 -*-
"""
    v1 201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    v2 202101, Dr. Jie Zheng & Dr./Prof. Linqiao Jiang
    v3 202201, Zheng & Jiang
    v4 202304, Upgrade, restructure, Zheng & Jiang
    Quick_Light_Curve_Pipeline
"""


import numpy as np
import astropy.io.fits as fits
from qmatch import mean_xy, mean_offset1d
import matplotlib.pyplot as plt
from .u_conf import config
from .u_workmode import workmode
from .u_log import init_logger
from .u_utils import loadlist, rm_ix, hdr_dt, zenum, str2mjd, pkl_dump, fnbase, tqdm_bar


def offset(
        conf:config,
        raw_dir:str,
        red_dir:str,
        obj:str,
        band:str,
        base_img:int|str=0,
        mode:workmode=workmode(),
):
    """
    Calculate offset of images
    :param conf: config object
    :param raw_dir: raw files dir
    :param red_dir: red files dir
    :param obj: object
    :param band: band
    :param base_img: the offset base index or filename
    :param mode: input files missing or output existence mode
    :returns: Nothing
    """
    logf = init_logger("offset", f"{red_dir}/log/offset.log", conf)
    mode.reset_append(workmode.EXIST_OVER)

    # list file, and load list
    listfile = f"{red_dir}/lst/{obj}_{band}.lst"
    if mode.missing(listfile, f"{obj} {band} list", logf):
        return
    bf_fits_list = loadlist(listfile, base_path=red_dir,
                        suffix="bf.fits", separate_folder=True)
    offset_pkl = f"{red_dir}/offset_{obj}_{band}.pkl"
    offset_txt = f"{red_dir}/offset_{obj}_{band}.txt"
    offset_png = f"{red_dir}/offset_{obj}_{band}.png"

    # check file exists
    if mode.exists(offset_pkl, f"offset {obj} {band}", logf):
        return

    # check file missing
    mode.start_lazy()
    ix = []
    for i, (f,) in zenum(bf_fits_list):
        if mode.missing(f, "corrected image", None):
            ix.append(i)
    # remove missing file
    mode.end_lazy(logf)
    rm_ix(ix, bf_fits_list)
    nf = len(bf_fits_list)

    if nf == 0:
        logf.info(f"SKIP {obj} {band} Nothing")
        return

    # base image, type check, range check, existance check
    if isinstance(base_img, int):
        if 0 > base_img or base_img >= nf:
            base_img = 0
        base_img = bf_fits_list[base_img]
    elif not isinstance(base_img, str):
        base_img = bf_fits_list[0]
    # if external file not found, use 0th
    # special, fixed mode
    if workmode(workmode.MISS_SKIP).missing(base_img, "offset base image", logf):
        base_img = bf_fits_list[0]

    ###############################################################################

    logf.debug(f"{nf:3d} files")

    # load base image
    logf.debug(f"Loading base image: {base_img}")
    base_x, base_y = mean_xy(fits.getdata(base_img))

    # xy offset array
    offset_x = np.empty(nf, int)
    offset_y = np.empty(nf, int)
    obs_mjd = np.empty(nf)

    # load images and process
    pbar = tqdm_bar(nf, f"OFFSET {obj} {band}")
    for i, (bff,) in zenum(bf_fits_list):

        # process data
        bf_x, bf_y = mean_xy(fits.getdata(bff))
        offset_x[i] = int(mean_offset1d(base_x, bf_x, max_d=conf.offset_max_dis))
        offset_y[i] = int(mean_offset1d(base_y, bf_y, max_d=conf.offset_max_dis))

        # mjd of obs
        # hdr = fits.getheader(bff)
        # obs_dt = hdr_dt(hdr)[:19]
        # obs_mjd[i] = str2mjd(obs_dt) + hdr.get("EXPTIME", 0.0) / 2 / 86400
        obs_mjd[i] = fits.getval(bff, "MJD")

        logf.debug(f"{i+1:03d}/{nf:03d}: "
                   f"{obs_mjd[i]:12.7f}  {offset_x[i]:+5d} {offset_y[i]:+5d}  "
                   f"{fnbase(bff)}")
        pbar.update(1)
    pbar.close()

    # save new fits
    with open(offset_txt, "w") as ff:
        for d, x, y, bff in zip(obs_mjd, offset_x, offset_y, bf_fits_list):
            ff.write(f"{d:12.7f}  {x:+5d} {y:+5d}  {bff}\n")
    pkl_dump(offset_pkl, obs_mjd, offset_x, offset_y, bf_fits_list)
    logf.debug(f"Writing {offset_pkl}")

    # draw offset figure
    fig = plt.figure(figsize=(6, 6))
    ax_xy = fig.add_axes([0.05, 0.05, 0.60, 0.60])
    ax_xt = fig.add_axes([0.05, 0.70, 0.60, 0.25])
    ax_ty = fig.add_axes([0.70, 0.05, 0.25, 0.60])
    ax_xy.plot(offset_x, offset_y, "k.:")
    ax_xt.plot(offset_x, obs_mjd, "k.:")
    ax_ty.plot(obs_mjd, offset_y, "k.:")
    ax_xy.set_xlabel("X offset")
    ax_xy.set_ylabel("Y offset")
    ax_xt.set_ylabel("MJD")
    ax_ty.set_xlabel("MJD")
    ax_xt.set_title(f"Offset {obj} {band}")
    fig.savefig(offset_png)
