from typing import Union, Tuple

def hvr_clr_g(colors: Union[Tuple[str, ...], str], modes: str, gain=20):
    result = []
    if isinstance(colors, str):
        colors = [colors]

    for color, mode in zip(colors, modes):

        hvr_clr = "#"
        if len(color) == 7 and color[0]=="#":
            color = color [1:]

        if mode == "l":
            for i in range(0, 6, 2): #generate hover color for light mode
                lit_255 = color[i:i+2]    # FF
                if lit_255 == "00":
                    hvr_clr += lit_255
                    continue
                num_255 = int(lit_255, 16)  # 255
                if num_255-gain < 0 :
                    hex_255 = "0x00"
                else:
                    hex_255 = hex(num_255-gain)    # 254 -> 0xFE    ,minus 1 to get darker color, then convert it back to hex 
                if len(hex_255[2:]) == 1:
                    hex_255 = "0"+hex_255[2:]
                    hvr_clr += hex_255
                else:
                    hex_255 = hex_255[2:]
                    hvr_clr += hex_255
                        
        elif mode == "d":
            for i in range(0, 6, 2): #generate hover color for dark mode
                lit_255 = color[i:i+2]    # 38
                if lit_255 == "FF" or lit_255 == "ff":
                    hvr_clr += lit_255
                    continue
                num_255 = int(lit_255, 16)  # 56
                if num_255+gain > 255:
                    hex_255 = "0xff"
                else:
                    hex_255 = hex(num_255+gain)    # 57 -> 0x39    ,plus 1 to get lighter color, then convert it back to hex 
                if len(hex_255[2:]) == 1:
                    hex_255 = "0"+hex_255[2:]
                    hvr_clr += hex_255
                else:
                    hex_255 = hex_255[2:]
                    hvr_clr += hex_255    

        result.append(hvr_clr)
    
    return tuple(result) if len(result) > 1 else result[0]

########################################################################################

import numpy as np
import os, copy
from PIL import Image
from methodtools import lru_cache
from typing import Tuple, Union

@lru_cache(maxsize=50)
def change_pixel_color(icon: Union[str, Image.Image], colors: Tuple[str, ...]):
    # print("Changing")
    """change the color of a filled icon to the target color

    Args:
        icon (raw string): the path of the icon
        color (Tuple): the target color/s in hex(str) format
    """
    finished_images = []
    if isinstance(icon, str):
        img = Image.open(icon).convert("RGBA")
    elif isinstance(icon, Image.Image):
        img = icon.convert("RGBA")
    else:
        raise TypeError("icon should be a path to an image or an Image object.")

    # Convert the image to a NumPy array
    img_array = np.array(img)
    for clr in colors:
        clr = tuple(int(clr[xx:xx+2], 16) for xx in (1, 3, 5))

        # Apply the target color to non-transparent pixels
        img_array[img_array[..., 3] != 0, :3] = clr

        # Create a new image from the modified array
        modified_img = Image.fromarray(img_array, "RGBA")

        finished_images.append(copy.copy(modified_img))
        
        # if not return_img:
        #     # Save the modified image
        #     folder = os.path.dirname(icon_path)
        #     file = os.path.basename(icon_path)
        #     modified_img.save(os.path.join(folder, f"{os.path.splitext(file)[0]}{clr}{os.path.splitext(file)[1]}"))

    return finished_images if len(finished_images) > 1 else finished_images[0]
    
########################################################################################

def color_finder(widget):
    while True:
        if widget._fg_color == "transparent":
            widget = widget.master
        else:
            return widget._fg_color
        
