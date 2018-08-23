#!/usr/bin/env python3

import json
import os
import sys
import collections

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import figtools


HMRunsData = collections.namedtuple(
    "HMRunsData",
    "kmatrix cprops radii theta theta_kmax radii_kmax theta_kmed radii_kmed theta_kmin radii_kmin kmax kmed kmin",
)


def parse_array(data, key):
    return np.array(data[key])


def parse_hmruns_data(data):
    kmatrix = data["kmatrix"]
    cprops = data["cprops"]
    radii = parse_array(data, "radii")
    theta = parse_array(data, "theta")
    theta_kmax = parse_array(data, "theta_kmax")
    radii_kmax = parse_array(data, "radii_kmax")
    theta_kmed = parse_array(data, "theta_kmed")
    radii_kmed = parse_array(data, "radii_kmed")
    theta_kmin = parse_array(data, "theta_kmin")
    radii_kmin = parse_array(data, "radii_kmin")
    kmax = parse_array(data, "kmax")
    kmed = parse_array(data, "kmed")
    kmin = parse_array(data, "kmin")
    return HMRunsData(
        kmatrix,
        cprops,
        radii,
        theta,
        theta_kmax,
        radii_kmax,
        theta_kmed,
        radii_kmed,
        theta_kmin,
        radii_kmin,
        kmax,
        kmed,
        kmin,
    )


def parse_contactarea_data(data):
    areas = data["areas"]
    return [np.array(a) for a in areas]


if __name__ == "__main__":
    
    with open(os.path.join(".", "data", "hmruns.json")) as f:
        data = parse_hmruns_data(json.load(f))

    kmax_n = data.kmax / data.kmatrix
    kmed_n = data.kmed / data.kmatrix
    kmin_n = data.kmin / data.kmatrix
    ah_prime = np.array(data.cprops['ah'])/(2*np.array(data.cprops['radius']))

    if 0:
        figtools.hemisphere.plot(
            data.theta_kmax,
            data.radii_kmax,
            np.log10(kmax_n),
            label=r"log$_{10}\mathit{k_{max}^\prime}$",
            cbformat="%.1f",
            save_as=os.path.join(".", "figures", "hemisphere_kmax.png"),
            nbars=8,
            alpha=0.8
        )
        figtools.hemisphere.plot(
            data.theta,
            data.radii,
            ah_prime,
            label=r'$\mathit{a_{h}^\prime}$',
            cbformat='%.4f',
            save_as=os.path.join(".", "figures", "hemisphere_ahprime.png"),
            nbars=9,
            alpha=0.8
        )


    with open(os.path.join(".", "data", "contactareas.json")) as f:
        allareas = parse_contactarea_data(json.load(f))
    
    lsim = len(allareas) - 1
    colors, alphas = ['blue'] + ['red'] * lsim, [1.0] + [0.3] * lsim
    def hook(ax):
        blue_line = mpl.lines.Line2D([], [], color='blue', label='Nemoto et al., 2009')
        red_line = mpl.lines.Line2D([], [], color='red', alpha=0.3, label='Numerical')
        plt.legend(handles=[blue_line,red_line])
        i, k = 90, -5.6E-6
        def line(x):
            return i + k * x
        slopeAx =  np.array([1.6E5, 1.5E7])
        slopeAy = line(slopeAx)
        #ax.plot(slopeAx, slopeAy, linestyle='--', lw=3, color="black")
    figtools.contactdistribution.plot(allareas, figsize=(8,4), colors=colors, alphas=alphas, hook=hook)
