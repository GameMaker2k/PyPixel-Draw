from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import os
import re
import sys

from PIL import Image, ImageDraw

if (__name__ == "__main__"):
    sys.tracebacklimit = 0
__version_info__ = (1, 0, 0, "RC 1")
if (__version_info__[3] is not None):
    __version__ = str(__version_info__[0]) + "." + str(__version_info__[1]) + "." + str(
        __version_info__[2]) + " " + str(__version_info__[3])
if (__version_info__[3] is None):
    __version__ = str(__version_info__[
        0]) + "." + str(__version_info__[1]) + "." + str(__version_info__[2])

parser = argparse.ArgumentParser(conflict_handler="resolve", add_help=True)
parser.add_argument("-i", "--input", default=None,
                    help="enter name of input file")
parser.add_argument("-t", "--outputtype", default=None,
                    help="enter file type of output image")
parser.add_argument("-o", "--output", default=None,
                    help="enter name of output image")
parser.add_argument("-s", "--resize", default=1,
                    help="enter number to resize image")
parser.add_argument("-r", "--resizetype", default="nearest",
                    help="enter resize type")
parser.add_argument("-v", "--version", action="version", version=__version__)
getargs = parser.parse_args()


def text_draw_image(
        text,
        imgtype="png",
        outputimage=True,
        resize=1,
        resizetype="nearest",
        outfile=None):
    if (not str(resize).isdigit() or resize < 1):
        resize = 1
    resizetype = resizetype.lower()
    if (resizetype != "antialias" and resizetype !=
            "bilinear" and resizetype != "bicubic" and resizetype != "nearest"):
        resizetype = "nearest"
    text = re.sub("^#(.*?)\n", "", text)
    text = re.sub("^\\/\\/(.*?)\n", "", text)
    if (re.findall("^([-]?[0-9]*[\\.]?[0-9])x", text)):
        resize_match = re.findall("^([-]?[0-9]*[\\.]?[0-9])x", text)
        resize = resize_match[0]
        '''if(resize<1):
      resize = 1;'''
        text = re.sub("^([-]?[0-9]*[\\.]?[0-9])x\n", "", text)
    text = text.strip(' \t\n\r')
    text_y = text.split("\n")
    num_y = len(text_y)
    if (num_y < 1):
        text_y[0] = text_y
    num_x = len(text_y[0].split(" "))
    pre_txt_img = Image.new("RGBA", (num_x, num_y))
    txt_img = ImageDraw.Draw(pre_txt_img)
    txt_img.rectangle([(0, 0), (num_x, num_y)], fill=(255, 255, 255))
    count_y = 0
    while (count_y < num_y):
        text_x = text_y[count_y].split(" ")
        count_x = 0
        while (count_x < num_x):
            pixeldone = False
            try:
                text_x[count_x]
            except IndexError:
                text_x[count_x] = "FFFFFF"
            text_x[count_x] = text_x[count_x].strip(' \t\n\r')
            Transparency = 255
            if (re.findall(
                    "^([0-9A-Fa-f]+):(0[0-9][0-9]|1[0-1][0-9]|12[0-7]|[0-9][0-9])$", text_x[count_x])):
                getTransparent = re.findall(
                    "^([0-9A-Fa-f]+):(0[0-9][0-9]|1[0-1][0-9]|12[0-7]|[0-9][0-9])$",
                    text_x[count_x])
                text_x[count_x] = re.sub(
                    "^([0-9A-Fa-f]+):(0[0-9][0-9]|1[0-1][0-9]|12[0-7]|[0-9][0-9])$",
                    "\\1",
                    text_x[count_x])
                Transparency = getTransparent[2]
            if (re.findall("^([0-9A-Fa-f]{2})$",
                           text_x[count_x]) and pixeldone is False):
                color_matches = re.findall(
                    "^([0-9A-Fa-f]{2})$", text_x[count_x])
                c8bitX = 32
                c8bitXnum = 0
                c8bitY = 8
                c8bitYnum = 0
                c8bitBlue = 0
                c8bitRed = 0
                c8bitGreen = 0
                c8bitNum = 0
                if (int(color_matches[0], 16) >=
                        32 and int(color_matches[0], 16) < 64):
                    c8bitBlue = 0
                    c8bitRed = 0
                    c8bitYnum = 1
                if (int(color_matches[0], 16) >=
                        64 and int(color_matches[0], 16) < 96):
                    c8bitBlue = 0
                    c8bitRed = 0
                    c8bitYnum = 2
                if (int(color_matches[0], 16) >= 96 and int(
                        color_matches[0], 16) < 128):
                    c8bitBlue = 0
                    c8bitRed = 0
                    c8bitYnum = 3
                if (int(color_matches[0], 16) >= 128 and int(
                        color_matches[0], 16) < 160):
                    c8bitBlue = 0
                    c8bitRed = 0
                    c8bitYnum = 4
                if (int(color_matches[0], 16) >= 160 and int(
                        color_matches[0], 16) < 192):
                    c8bitBlue = 0
                    c8bitRed = 0
                    c8bitYnum = 5
                if (int(color_matches[0], 16) >= 192 and int(
                        color_matches[0], 16) < 224):
                    c8bitBlue = 0
                    c8bitRed = 0
                    c8bitYnum = 6
                if (int(color_matches[0], 16) >= 224):
                    c8bitBlue = 0
                    c8bitRed = 0
                    c8bitYnum = 7
                if (int(color_matches[0], 16) >= 32):
                    c8bitGreen = 36 * c8bitYnum
                    c8bitNum = 32 * c8bitYnum
                while (c8bitYnum < c8bitY):
                    c8bitXnum = 0
                    while (c8bitXnum < c8bitX):
                        if (int(color_matches[0], 16) == 255):
                            txt_img.line(
                                (count_x, count_y, count_x, count_y), fill=(
                                    255, 255, 255, Transparency))
                            pixeldone = True
                            break
                        if (int(color_matches[0], 16) == c8bitNum):
                            txt_img.line(
                                (count_x, count_y, count_x, count_y), fill=(
                                    c8bitRed, c8bitGreen, c8bitBlue, Transparency))
                            pixeldone = True
                            break
                        ''' Blue = 85|255 Red = 36|252 Green = 36|252 '''
                        c8bitBlue = 85 + c8bitBlue
                        if (c8bitBlue >= 340):
                            c8bitRed += 36 + c8bitRed
                            c8bitBlue = 0
                        if (c8bitRed >= 288):
                            c8bitGreen += 36 + c8bitGreen
                            c8bitRed = 0
                        c8bitXnum = c8bitXnum + 1
                        c8bitNum = c8bitNum + 1
                    c8bitYnum = c8bitYnum + 1
            if (re.findall("^([0-9A-Fa-f])$",
                           text_x[count_x]) and pixeldone == False):
                color_matches = re.findall("^([0-9A-Fa-f])$", text_x[count_x])
                if (color_matches[0] == "0"):
                    text_x[count_x] = "000000000"
                if (color_matches[0] == "1"):
                    text_x[count_x] = "104104104"
                if (color_matches[0] == "2"):
                    text_x[count_x] = "000018144"
                if (color_matches[0] == "3"):
                    text_x[count_x] = "000039251"
                if (color_matches[0] == "4"):
                    text_x[count_x] = "000143021"
                if (color_matches[0] == "5"):
                    text_x[count_x] = "000249044"
                if (color_matches[0] == "6"):
                    text_x[count_x] = "000144146"
                if (color_matches[0] == "7"):
                    text_x[count_x] = "000252254"
                if (color_matches[0] == "8"):
                    text_x[count_x] = "155023008"
                if (color_matches[0] == "9"):
                    text_x[count_x] = "255048022"
                if (color_matches[0] == "A"):
                    text_x[count_x] = "154032145"
                if (color_matches[0] == "B"):
                    text_x[count_x] = "255063252"
                if (color_matches[0] == "C"):
                    text_x[count_x] = "148145025"
                if (color_matches[0] == "D"):
                    text_x[count_x] = "255253051"
                if (color_matches[0] == "E"):
                    text_x[count_x] = "184184184"
                if (color_matches[0] == "F"):
                    text_x[count_x] = "255255255"
            if (
                re.findall(
                    "(000[0-9]|00[1-9][0-9]|01[0-9][0-9]|02[0-9][0-9]|03[0-6][0-9]|037[0-7])(000[0-9]|00[1-9][0-9]|01[0-9][0-9]|02[0-9][0-9]|03[0-6][0-9]|037[0-7])(000[0-9]|00[1-9][0-9]|01[0-9][0-9]|02[0-9][0-9]|03[0-6][0-9]|037[0-7])",
                    text_x[count_x]) and pixeldone == False):
                color_matches = re.findall(
                    "(000[0-9]|00[1-9][0-9]|01[0-9][0-9]|02[0-9][0-9]|03[0-6][0-9]|037[0-7])(000[0-9]|00[1-9][0-9]|01[0-9][0-9]|02[0-9][0-9]|03[0-6][0-9]|037[0-7])(000[0-9]|00[1-9][0-9]|01[0-9][0-9]|02[0-9][0-9]|03[0-6][0-9]|037[0-7])",
                    text_x[count_x])
                color_matches = color_matches[0]
                color_matches = [int(i) for i in color_matches]
                txt_img.line(
                    (count_x, count_y, count_x, count_y), fill=(
                        int(
                            color_matches[0], 8), int(
                            color_matches[1], 8), int(
                            color_matches[2], 8), Transparency))
                pixeldone = True
            if (
                re.findall(
                    "(00[0-9]|0[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(00[0-9]|0[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(00[0-9]|0[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])",
                    text_x[count_x]) and pixeldone == False):
                color_matches = re.findall(
                    "(00[0-9]|0[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(00[0-9]|0[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(00[0-9]|0[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])",
                    text_x[count_x])
                color_matches = color_matches[0]
                color_matches = [int(i) for i in color_matches]
                txt_img.line((count_x, count_y, count_x, count_y), fill=(
                    color_matches[0], color_matches[1], color_matches[2], Transparency))
                pixeldone = True
            if (
                re.findall(
                    "([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})",
                    text_x[count_x]) and pixeldone == False):
                color_matches = re.findall(
                    "([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})",
                    text_x[count_x])
                color_matches = color_matches[0]
                txt_img.line(
                    (count_x, count_y, count_x, count_y), fill=(
                        int(
                            color_matches[0], 16), int(
                            color_matches[1], 16), int(
                            color_matches[2], 16), Transparency))
                pixeldone = True
            count_x = count_x + 1
        count_y = count_y + 1
    if (resizetype != "antialias"):
        new_txt_img = pre_txt_img.resize(
            ((num_x) * int(resize), (num_y) * int(resize)), Image.ANTIALIAS)
    if (resizetype != "bilinear"):
        new_txt_img = pre_txt_img.resize(
            ((num_x) * int(resize), (num_y) * int(resize)), Image.BILINEAR)
    if (resizetype != "bicubic"):
        new_txt_img = pre_txt_img.resize(
            ((num_x) * int(resize), (num_y) * int(resize)), Image.BICUBIC)
    if (resizetype != "nearest"):
        new_txt_img = pre_txt_img.resize(
            ((num_x) * int(resize), (num_y) * int(resize)), Image.NEAREST)
    del (txt_img)
    del (pre_txt_img)
    txt_img = ImageDraw.Draw(new_txt_img)
    new_txt_img.save(outfile, imgtype)
    return True


ftest = open(getargs.input, "r")
text_draw_image(ftest.read(), getargs.outputtype, True,
                getargs.resize, getargs.resizetype, getargs.output)
ftest.close()
