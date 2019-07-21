#!/usr/bin/env python

import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import nibabel as nib


def isinteger(x):
    return np.equal(np.mod(x, 1), 0)

def bounding_box_3D(img):
    x = np.any(img, axis=(1, 2))
    y = np.any(img, axis=(0, 2))
    z = np.any(img, axis=(0, 1))
    xmin, xmax = np.where(x)[0][[0, -1]]
    ymin, ymax = np.where(y)[0][[0, -1]]
    zmin, zmax = np.where(z)[0][[0, -1]]
    return xmin, xmax, ymin, ymax, zmin, zmax

def crop_img(img, crop_coords=None):
    print(f"Original dimensions shape: {img.shape}")
    if crop_coords is None:
        crop_coords = bounding_box_3D(img)
    xmin = crop_coords[0]
    xmax = crop_coords[1]
    ymin = crop_coords[2]
    ymax = crop_coords[3]
    zmin = crop_coords[4]
    zmax = crop_coords[5]
    cropped_img = img[xmin:xmax, ymin:ymax, zmin:zmax]
    print(f"Cropped dimensions shape: {cropped_img.shape}")
    return cropped_img, crop_coords

def pick_slices(x, y, ax_slices):
    n_slices = x*y
    slices_per_half = n_slices // 2
    step_sz = ax_slices // n_slices
    mid_ax = ax_slices // 2
    first_ax = mid_ax - slices_per_half * step_sz
    last_ax = mid_ax + slices_per_half * step_sz
    bottom_half = list(range(first_ax, mid_ax, step_sz))
    top_half = list(range(mid_ax+step_sz, last_ax, step_sz))
    slices = bottom_half + [mid_ax] + top_half
    while len(slices) != n_slices:
        slices += [slices[-1] + step_sz]
    print(f'Slices to take are: {slices}')
    return slices

def slice_img(img, slice_num, slice_axis):
    sliced_img = np.take(img, slice_num, axis=slice_axis)
    oriented_slice = np.flipud(sliced_img.T)
    return oriented_slice

def stack_slices(img, slices, x, y, slice_axis):
    ind = 0
    for i in range(y):
        for j in range(x):
            slice_num = slices[ind]
            if j == 0:
                row_img = slice_img(img, slice_num, slice_axis)
            else:
                row_img = np.hstack((row_img,
                                     slice_img(img, slice_num, slice_axis)))
            ind += 1
        if i == 0:
            col_img = row_img
        else:
            col_img = np.vstack((col_img, row_img))
    return col_img

def scale_range(input, min, max):
    input += -(np.min(input))
    input /= np.max(input) / (max - min)
    input += min
    return input

def save_figure(filename, quality):
    if quality == "low":
        output_dpi = 100
    elif quality == "high":
        output_dpi = 300
    else:
        output_dpi = 200
    plt.savefig(filename, dpi=output_dpi, bbox_inches="tight", pad_inches=0)


def io_stream(base_file, overlay_file, save_file, x_imgs, y_imgs, quality):
    print(f"Loading {overlay_file} as overlay...")
    overlay = nib.load(overlay_file)
    base_cropped, overlay_cropped = crop_img(base.get_data(),
                                             overlay.get_data())
    slices = pick_slices(x_imgs, y_imgs, base_cropped.shape[slice_axis])
    base_img = stack_slices(base_cropped, slices, x_imgs, y_imgs, slice_axis)
    overlay_img = stack_slices(overlay_cropped, slices, x_imgs, y_imgs,
                               slice_axis)
    base_cmap = "gray"
    plt.imshow(base_img, cmap=base_cmap)
    mask_vals = len(np.unique(overlay_cropped))
    if mask_vals > 2:
        desikan_cmap = build_lut()
        plt.imshow(overlay_img, cmap=desikan_cmap, alpha=0.35)
    else:
        overlay_cmap = "plasma"
        plt.imshow(overlay_img, cmap=overlay_cmap, alpha=0.35)
    plt.axis("off")
    # plt.show()
    if args.s.endswith(".png"):
        image_fname = save_file
    else:
        image_fname = save_file + ".png"
    print(f"Saving layered image as {image_fname}...")
    save_figure(image_fname, quality)

def load_layer(layer_path):
    layer_path_abs = os.path.abspath(layer_path) 
    print(f"Loading {layer_path_abs} as layer...")
    layer_img = nib.load(layer_path_abs).get_data()
    return layer_img

def load_base(base_path):
    base_path_abs = os.path.abspath(base_path)
    print(f"Loading {base_path_abs} as base...")
    base_img = nib.load(base_path_abs)
    if isinstance(base_img, nib.freesurfer.MGHImage):
        slice_axis = 1
        print(f"MGH format detected, assuming slice axis = 1")
    else:
        slice_axis = 2
        print(f"Nifti format detected, assuming slice axis = 2")
    return base_img.get_data(), slice_axis


def guess_layer_type(layer_img):
    unique_vals = np.unique(layer_img)
    if all(isinteger(unique_vals)):
        if len(unique_vals) > 2:
            guess = 'parc'
        else:
            guess = 'mask'
    else:
        guess = 'cont'
    print(f'Guessing the layer is a {guess}')
    return guess


def load_desikan():
    script_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_path)
    lut_file = os.path.abspath('../freesurfer_utils/info/desikan.txt')
    print(f"Reading {lut_file} for custom colormap...")
    desikan = np.loadtxt(lut_file, delimiter=',', skiprows=1, usecols=(2, 3, 4))
    desikan = np.unique(desikan, axis=0)  # eliminate doubled colors
    desikan = desikan / 255
    print(desikan)

def read_input():
    if len(sys.argv) < 4:
        print("Error, not enough arguments.")
        sys.exit(1)
    base_path = sys.argv[1]
    layers = sys.argv[2:-1]
    output = sys.argv[-1]
    if not output.endswith(".png"):
        output = '.'.join([output, 'png'])
    return base_path, layers, output

if __name__ == "__main__":
    output_x, output_y = 10, 5
    base_path, layers, output = read_input()
    base_img, slice_axis = load_base(base_path)
    base_cropped, cropped_coords = crop_img(base_img)
    slices = pick_slices(output_x, output_y, base_cropped.shape[slice_axis])
    base_stack = stack_slices(base_cropped, slices, output_x, output_y, slice_axis)
    # colours = {'parc': 


        # vals = np.unique(layer_cropped)
        # print(vals)
    # overlay_img = stack_slices(overlay_cropped, slices, x_imgs, y_imgs,
    #                            slice_axis)
    load_desikan()
    # fig,ax = plt.subplots(1)
    # fig = plt.figure(figsize=[6,6])
    # ax = fig.add_subplot(111)
    # ax.imshow(base_stack, cmap='gray')
    # for layer in layers:
    #     layer_img = load_layer(layer)
    #     layer_cropped, coords = crop_img(layer_img, cropped_coords)
    #     layer_stack = stack_slices(layer_cropped, slices, output_x, output_y, slice_axis)
    #     guess = guess_layer_type(layer_cropped)
    #     print(layer_stack.shape)
    #     ax.imshow(layer_stack, cmap='tab20b', alpha=0.35)
    # ax.axes.get_xaxis().set_visible(False)
    # ax.axes.get_yaxis().set_visible(False)
    # ax.set_frame_on(False)
    # plt.savefig('data.png', dpi=400, bbox_inches='tight',pad_inches=0)
