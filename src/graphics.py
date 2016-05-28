#!/usr/bin/env python
# coding=utf-8
""" Module /src/graphics.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module containing the Graphics class.
    Uses pygame image objects.
"""
import os

import pygame

from src import constants as c


class MissingMicrotileQuartetError(Exception):
    pass


class Graphics(object):
    """ Graphics object containing an image. Loads the image by itself.
    """
 
    def __init__(self, name):
        """ "name" should be one of these two things, which determines what the image should be:
            - A pygame.Surface
                If so, the image will be that surface
            - A path, and in that case name_is_path should be True
                If so, the image will be that exact image
        """
        if type(name) == str:
            self.image = pygame.image.load(name)
            # if c.NORMAL_DEBUG:
            #     print(os.path.join(os.getcwd(), c.RES_FOLDER, c.IMAGES[name].png))
        elif type(name) == pygame.Surface:
            self.image = name 
    
    def get(self):
        """ returns the contained image
        """
        return self.image
    
    def get_size(self):
        """ returns a tuple containing the width and height of the image 
        """
        return self.get().get_width(), self.get().get_height()


def load_graphics():
    """ Creates a dictionary with the keys from the constants.py IMAGES dictionary keys
        and a Graphics object created using that key, as well as associated resource files.

        The bulk of the code checks the c.GEN_RES_FOLDER for each image before the c.RES_FOLDER.
        
        returns that dictionary
    """
    images = {}

    # Add all images in the c.RES_FOLDER to a list for quicker searching
    res_images = [image_file for image_file in os.listdir(os.path.join(os.getcwd(), c.RES_FOLDER))
                  if os.path.isfile(os.path.join(os.getcwd(), c.RES_FOLDER, image_file)) and
                  image_file[0] != "%"]

    gen_res_images = []
    # Do the same for c.GEN_RES_FOLDER if generated images are used.
    if c.DEACTIVATE_IMAGE_PREPARATION is False:
        gen_res_images = [image_file for image_file in os.listdir(os.path.join(os.getcwd(), c.GEN_RES_FOLDER))
                          if os.path.isfile(os.path.join(os.getcwd(), c.GEN_RES_FOLDER, image_file)) and
                          image_file[0] != "%"]  # Exclude files which should be processed by prepare_images().

    # Loop through all images of c.IMAGES
    for key in list(c.IMAGES.keys()):
        # Load the primary image
        if c.IMAGES[key].png in gen_res_images:
            images[key] = Graphics(os.path.join(os.getcwd(), c.GEN_RES_FOLDER, c.IMAGES[key].png))
        else:
            images[key] = Graphics(os.path.join(os.getcwd(), c.RES_FOLDER, c.IMAGES[key].png))

        # Load random images, that is, images that are named the same but with a digit at the end.
        if not c.DEACTIVATE_RANDOM_TEXTURES and c.IMAGES[key].random is True:
            added_random_images = False
            primary_image_file = c.IMAGES[key].png
            for random_image_file in gen_res_images:
                # Single out the part of the file name that should be a digit
                digit = "".join(random_image_file.split(".")[:-1])[len("".join(primary_image_file.split(".")[:-1])):]
                # If the image follows the format
                if digit.isdigit() and random_image_file == \
                        "".join(primary_image_file.split(".")[:-1]) + digit + "." + primary_image_file.split(".")[-1]:
                    # Add it to the images dict
                    added_random_images = True
                    images[key+digit] = Graphics(os.path.join(os.getcwd(), c.GEN_RES_FOLDER, random_image_file))
            # If no images were added during the previous step
            if not added_random_images:
                # Do it again with the
                for random_image_file in res_images:
                    digit = "".join(random_image_file.split(".")[:-1])[
                            len("".join(primary_image_file.split(".")[:-1])):]

                    # If the image follows the format
                    if digit.isdigit() and random_image_file == "".join(primary_image_file.split(".")[:-1]) + digit + \
                            "." + primary_image_file.split(".")[-1]:
                        # Add it to the images dict
                        images[key + digit] = Graphics(os.path.join(os.getcwd(), c.RES_FOLDER, random_image_file))

        # Load microtiles, that is, images that start with the same name as the
        if c.DEACTIVATE_MICROTILES is False and c.IMAGES[key].microtiles is not None:
            primary, ext = c.IMAGES[key].png.rsplit(".")
            ext = "." + ext
            for microtile in ["Full", "Corner", "Side", "Top", "End"]:
                found_microtiles = 0
                for i in range(4):
                    # Make sure we have the entire set
                    if primary + microtile + str(i) + ext in gen_res_images or \
                            primary + microtile + str(i) + ext in gen_res_images:
                        found_microtiles += 1
                if found_microtiles == 4:
                    # If the entire set is found
                    for i in range(4):
                        if primary + microtile + str(i) + ext in gen_res_images:
                            images[key + "_" + microtile.lower() + str(i)] = \
                                Graphics(os.path.join(os.getcwd(), c.GEN_RES_FOLDER, primary + microtile + str(i) + ext))
                        elif primary + microtile + str(i) + ext in res_images:
                            images[key + "_" + microtile.lower() + str(i)] = \
                                Graphics(os.path.join(os.getcwd(), c.RES_FOLDER, primary + microtile + str(i) + ext))
                elif found_microtiles == 0:
                    # If no microtiles with a number is found, check if there is one without a number
                    if primary + microtile + ext in gen_res_images:
                        images[key + "_" + microtile.lower()] = \
                            Graphics(os.path.join(os.getcwd(), c.GEN_RES_FOLDER, primary + microtile + ext))
                    elif primary + microtile + ext in res_images:
                        images[key + "_" + microtile.lower()] = \
                            Graphics(os.path.join(os.getcwd(), c.RES_FOLDER, primary + microtile + ext))
                    else:
                        if microtile == "Top":
                            if primary + microtile + ext in images:
                                image = images[primary + microtile + ext].get()
                            elif primary + microtile + "0" + ext in images:
                                image = images[primary + microtile + "0" + ext].get()
                            else:
                                raise MissingMicrotileQuartetError(
                                    "Microtile corner " + primary + "_" + microtile.lower() +
                                    " not found. Please make sure the file " + primary + microtile + ext +
                                    " exists in the folder " + c.RES_FOLDER + ".")
                            image = pygame.transform.flip(image, 1, 0)
                            image = pygame.transform.rotate(image, 90)
                            images[key + "_" + microtile.lower()] = Graphics(image)
                        else:
                            raise MissingMicrotileQuartetError(
                                "Microtile corner " + primary + "_" + microtile.lower() +
                                " not found. Please make sure the file " + primary + microtile + ext +
                                " exists in the folder " + c.RES_FOLDER + ".")
                else:
                    for i in range(4):
                        if primary + microtile + str(i) + ext in gen_res_images:
                            images[key + "_" + microtile.lower()] = Graphics(
                                os.path.join(os.getcwd(), c.GEN_RES_FOLDER, primary + microtile + str(i) + ext))
                        if primary + microtile + str(i) + ext in res_images:
                            images[key + "_" + microtile.lower()] = \
                                Graphics(os.path.join(os.getcwd(), c.RES_FOLDER, primary + microtile + str(i) + ext))

                        #"water_full", "water_corner",
                             #"water_side", "water_end"
    return images


def prepare_images():
    """ File modifying script. Takes images from res beginning with the % symbol, processes them depending
        on their naming patterns and puts the generated images in the /gen_res folder.

        The gen_res folder is cleared with every new run of this script.

        All files containing a + will be overlayed over the tiles following the +.
            For example, %package+grass+dirt+ore.png will use one of the tiles of grass.png or grass(number).png and
            overlay the image (which should be a package) over one of the grass tiles and save it as packageGrass.png
            in gen_res and then repeat the process for dirt and ore.
        All files starting with atlas- will be split in even 16x16 tiles and be named with numbers in gen_res.
            For example, %atlas-grass, which might be a 48x48 image, will be split in 16 pieces, and named grass.png,
            grass2.png and so on up to grass16.png.
        All files starting with microtile- will be split into 8x8 microtile quartets and be named appropriately to
            which tile it represents, provided that the atlas is constructed as a 48x48 with an image filled in as
            a f.ex. lake with the shape depicted in the file res/example_microtile_atlas.jpg
            For example, %microtile-water
        All files with no special formatting will simple be copied over to gen_res
            For example, %entityPlayer

        Formattings can be combined, but additions (+) must be specified last in the file. atlas- and microtile- can
            not be combined
            For example: %atlas-sapling+grass+dirt

        If a tile requires another tile (%sapling+grass requires grass) it will be processed after the required tile.
        If a required tile exists in res as both a tile prepended with % and without, the one prepended with % will be
            used. Tiles prepended with % will also take priority over tiles without when graphics are loaded.
    """
    pass