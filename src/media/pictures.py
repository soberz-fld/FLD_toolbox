import cv2
import numpy
import re
import os

from ..fldlogging import log
from ..calcs.numbers import round_to_multiple_of_x as xround


def create_picture_in_size_from_image(src_file: str, dst_file: str, size_x: int, size_y: int, pick_fill_color_by_rgb_true_r_g_b_false: bool = True) -> bool:
    if re.match('.*\\.png$|.*\\.jpg$', src_file) and re.match('.*\\.png$|.*\\.jpg$', dst_file) and size_x > 0 and size_y > 0:
        if os.path.isfile(src_file):
            # Check source image and prepare
            img = cv2.imread(src_file)
            img_width = img.shape[1]
            img_height = img.shape[0]
            if not (img_width == size_x and img_height == size_y):
                # Need to resize
                if round(img_width / size_x, 3) == round(img_height / size_y, 3):
                    # Same size ratio
                    img = cv2.resize(img, (size_x, size_y))
                elif round(img_width / size_x, 3) > round(img_height / size_y, 3):
                    # Wider, therefore a rim at the top and bottom
                    new_height = int(img_height / (img_width / size_x))
                    img = cv2.resize(img, (size_x, new_height))
                else:
                    # Narrower, therefore a border on the left and right
                    new_width = int(img_width / (img_height / size_y))
                    img = cv2.resize(img, (new_width, size_y))

            # Update img_width and img_height to size of resized image
            img_width = img.shape[1]
            img_height = img.shape[0]

            # if fill needed, calculate RGB-histogram, take the most occurring color and create new image with that color as fill
            if img_width != size_x or img_height != size_y:
                # Fill needed

                if pick_fill_color_by_rgb_true_r_g_b_false:

                    # Histogram for combined rgb
                    histogram = dict()
                    for y in img:
                        for x in y:
                            try:
                                histogram[str(x)] += 1
                            except KeyError:
                                histogram[str(x)] = 1

                    maximum = 0
                    max_val = ''  # Color value of most occurring color
                    for key in histogram.keys():
                        if histogram[key] > maximum:
                            maximum = histogram[key]
                            max_val = str(key)
                    fill_color = numpy.fromstring(max_val.replace('[', '').replace(']', ''), dtype=int, sep=' ')

                else:

                    # Histogram for r, g and b separately
                    histogram_r = dict()
                    histogram_g = dict()
                    histogram_b = dict()
                    base = 10
                    for y in img:
                        for x in y:
                            # Create histogram red
                            try:
                                histogram_r[str(xround(base, x[2]))] += 1
                            except KeyError:
                                histogram_r[str(xround(base, x[2]))] = 1
                            # Create histogram green
                            try:
                                histogram_g[str(xround(base, x[1]))] += 1
                            except KeyError:
                                histogram_g[str(xround(base, x[1]))] = 1
                            # Create histogram blue
                            try:
                                histogram_b[str(xround(base, x[0]))] += 1
                            except KeyError:
                                histogram_b[str(xround(base, x[0]))] = 1

                    max_r, max_g, max_b = 0, 0, 0
                    maxval_r, maxval_g, maxval_b = '', '', ''
                    for key in histogram_r.keys():
                        if histogram_r[key] > max_r:
                            max_r = histogram_r[key]
                            maxval_r = str(key)
                    for key in histogram_g.keys():
                        if histogram_g[key] > max_g:
                            max_g = histogram_g[key]
                            maxval_g = str(key)
                    for key in histogram_b.keys():
                        if histogram_b[key] > max_b:
                            max_b = histogram_b[key]
                            maxval_b = str(key)
                    max_val = f'[{maxval_b} {maxval_g} {maxval_r}]'
                    fill_color = numpy.fromstring(max_val.replace('[', '').replace(']', ''), dtype=int, sep=' ')

                # Create new emtpy image to migrate to
                new_img = numpy.zeros((size_y, size_x, 3), int)

                # Get size of new image
                new_image_width = new_img.shape[1]
                new_img_height = new_img.shape[0]

                # Calculate pixels to fill each side
                fill_x = new_image_width - img_width
                fill_y = new_img_height - img_height
                fill_left = int(fill_x / 2)
                fill_top = int(fill_y / 2)

                # Migrate to new image
                for i_y in range(0, size_y):
                    for i_x in range(0, size_x):
                        if i_x < fill_left or i_x > fill_left + img_width:
                            # If fill needed top or bottom
                            new_img[i_y, i_x] = fill_color
                        elif i_y < fill_top or i_y > fill_top + img_height:
                            # If fill needed left or right
                            new_img[i_y, i_x] = fill_color
                        else:
                            try:
                                new_img[i_y, i_x] = img[i_y - fill_top, i_x - fill_left]
                            except IndexError:
                                new_img[i_y, i_x] = fill_color

                img = new_img

            cv2.imwrite(dst_file, img)
            return True
    log(error='Could not convert src_file for any reason')
    return False
