from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import os
import re
import sys

from PIL import Image, ImageDraw


def parse_transparency(text):
    """
    Extract transparency from the text if available in format 'hex_color:transparency'.
    Returns hex color and transparency as a tuple.
    """
    match = re.match(
        r"^([0-9A-Fa-f]+):(0[0-9][0-9]|1[0-1][0-9]|12[0-7]|[0-9][0-9])$",
        text)
    if match:
        return match.group(1), int(match.group(2))
    return text, 255  # default transparency is 255 (opaque)


def parse_color(text):
    """
    Parse the color from the text in multiple formats (single hex, full RGB hex, octal, decimal).
    Returns an (R, G, B) tuple.
    """
    # Single hex digit to RGB mapping
    single_hex_map = {
        "0": (
            0, 0, 0), "1": (
            104, 104, 104), "2": (
                0, 18, 144), "3": (
                    0, 39, 251), "4": (
                        0, 143, 21), "5": (
                            0, 249, 44), "6": (
                                0, 144, 146), "7": (
                                    0, 252, 254), "8": (
                                        155, 23, 8), "9": (
                                            255, 48, 22), "A": (
                                                154, 32, 145), "B": (
                                                    255, 63, 252), "C": (
                                                        148, 145, 25), "D": (
                                                            255, 253, 51), "E": (
                                                                184, 184, 184), "F": (
                                                                    255, 255, 255)}

    # Check for single hex color
    if re.match(r"^[0-9A-Fa-f]$", text):
        return single_hex_map[text.upper()]

    # Check for 6-digit hex RGB color
    match = re.match(
        r"^([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})$",
        text)
    if match:
        return tuple(int(match.group(i), 16) for i in range(1, 4))

    # Check for octal format (000–377 for each channel)
    match = re.match(
        r"(000[0-9]|00[1-9][0-9]|01[0-9][0-9]|02[0-9][0-9]|03[0-6][0-9]|037[0-7])"
        r"(000[0-9]|00[1-9][0-9]|01[0-9][0-9]|02[0-9][0-9]|03[0-6][0-9]|037[0-7])"
        r"(000[0-9]|00[1-9][0-9]|01[0-9][0-9]|02[0-9][0-9]|03[0-6][0-9]|037[0-7])", text)
    if match:
        return tuple(int(match.group(i), 8) for i in range(1, 4))

    # Check for decimal RGB color (000–255)
    match = re.match(
        r"(00[0-9]|0[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
        r"(00[0-9]|0[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
        r"(00[0-9]|0[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])", text)
    if match:
        return tuple(int(match.group(i)) for i in range(1, 4))

    return (0, 0, 0)  # default to black if no match


def draw_image_from_text(
        text,
        imgtype="png",
        outputimage=True,
        resize=1,
        resizetype="nearest",
        outfile=None):
    """
    Draw an image based on text input. Supports various color and transparency formats.
    """
    text = re.sub("^#(.*?)\n", "", text)  # remove comments starting with #
    # remove comments starting with //
    text = re.sub("^\\/\\/(.*?)\n", "", text)

    # Parse resizing factor if specified
    resize_match = re.match(r"^([-]?[0-9]*[\.]?[0-9])x", text)
    if resize_match:
        resize = int(resize_match.group(1))
        text = re.sub(r"^([-]?[0-9]*[\.]?[0-9])x\n", "", text)

    # Prepare text data as pixel array
    text_lines = text.strip().split("\n")
    num_y = len(text_lines)
    num_x = max(len(line.split(" ")) for line in text_lines)

    pre_txt_img = Image.new("RGBA", (num_x, num_y))
    txt_img = ImageDraw.Draw(pre_txt_img)

    # Draw pixels based on the parsed text
    for count_y, line in enumerate(text_lines):
        pixels = line.split(" ")
        for count_x, pixel in enumerate(pixels):
            pixel, Transparency = parse_transparency(pixel)
            color = parse_color(pixel)
            txt_img.line(
                (count_x, count_y, count_x, count_y), fill=(
                    color[0], color[1], color[2], Transparency))

    # Resize the image if required
    resizetype_map = {
        "antialias": Image.ANTIALIAS,
        "bilinear": Image.BILINEAR,
        "bicubic": Image.BICUBIC,
        "nearest": Image.NEAREST
    }
    if resize > 1:
        new_txt_img = pre_txt_img.resize(
            (num_x * resize,
             num_y * resize),
            resizetype_map.get(
                resizetype,
                Image.NEAREST))
    else:
        new_txt_img = pre_txt_img

    # Save or return the image
    if outputimage:
        new_txt_img.save(outfile, imgtype)
        return True
    return new_txt_img


if __name__ == "__main__":
    sys.tracebacklimit = 0

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(conflict_handler="resolve", add_help=True)
    parser.add_argument("-i", "--input", default=None,
                        help="Enter name of input file")
    parser.add_argument("-t", "--outputtype", default=None,
                        help="Enter file type of output image")
    parser.add_argument("-o", "--output", default=None,
                        help="Enter name of output image")
    parser.add_argument(
        "-s",
        "--resize",
        default=1,
        help="Enter number to resize image",
        type=int)
    parser.add_argument(
        "-r",
        "--resizetype",
        default="nearest",
        help="Enter resize type")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="1.0.0 RC 1")

    getargs = parser.parse_args()

    with open(getargs.input, "r") as ftest:
        draw_image_from_text(
            ftest.read(),
            getargs.outputtype,
            True,
            getargs.resize,
            getargs.resizetype,
            getargs.output)
