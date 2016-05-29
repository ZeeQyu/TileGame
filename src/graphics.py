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
import heapq
import random

import pprint
import time

import pygame

from src import constants as c


class MissingMicrotileQuartetError(Exception):
    pass


class RequiredImageNotFoundError(Exception):
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
                digit = random_image_file.rsplit(".", 1)[0][len(primary_image_file.rsplit(".", 1)[0]):]
                # If the image follows the format
                if digit.isdigit() and random_image_file == \
                        primary_image_file.rsplit(".", 1)[0] + digit + "." + primary_image_file.rsplit(".", 1)[1]:
                    # Add it to the images dict
                    added_random_images = True
                    images[key+digit] = Graphics(os.path.join(os.getcwd(), c.GEN_RES_FOLDER, random_image_file))
            # If no images were added during the previous step
            if not added_random_images:
                # Do it again with the
                for random_image_file in res_images:
                    digit = random_image_file.rsplit(".", 1)[0][
                            len(primary_image_file.rsplit(".", 1)[0]):]

                    # If the image follows the format
                    if digit.isdigit() and random_image_file == primary_image_file.rsplit(".", 1)[0] + digit + \
                            "." + primary_image_file.rsplit(".", 1)[1]:
                        # Add it to the images dict
                        images[key + digit] = Graphics(os.path.join(os.getcwd(), c.RES_FOLDER, random_image_file))

        # Load microtiles, that is, images that start with the same name as the
        if c.DEACTIVATE_MICROTILES is False and c.IMAGES[key].microtiles is not None:
            primary, ext = c.IMAGES[key].png.rsplit(".", 1)
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
                            if primary + "_" + "side" in images:
                                image = images[primary + "_" + "side"].get()
                            elif primary + "_" + "side" + "0" in images:
                                image = images[primary + "_" + "side" + "0"].get()
                            else:
                                if c.SPECIAL_DEBUG: print("Locals: "); pprint.pprint(locals()); time.sleep(0.01)
                                raise MissingMicrotileQuartetError(
                                    "Microtile corner " + primary + "_" + microtile.lower() +
                                    " not found. Please make sure the file " + primary + microtile + ext +
                                    " exists in the folder " + c.RES_FOLDER + ".")
                            image = pygame.transform.flip(image, 1, 0)
                            image = pygame.transform.rotate(image, 90)
                            images[key + "_" + microtile.lower()] = Graphics(image)
                        else:
                            #images[key + "_" + microtile.lower()] = Graphics(image)

                            if c.SPECIAL_DEBUG: print("Locals: "); pprint.pprint(locals()); time.sleep(0.01)

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
    return images


def prepare_images():
    """ File modifying script. Takes images from res beginning with the % symbol, processes them depending
        on their naming patterns and puts the generated images in the /gen_res folder.

        The gen_res folder is cleared of png files with every new run of this script.

        All files containing a + specify backgrounds. The image will be overlayed over the tiles following the +.
            For example, %package+grass+dirt+ore.png will use one of the tiles of grass.png or a random of the tiles in
            an atlas of grass tiles and overlay the image (which should be a package)
            over one of the grass tiles and save it as packageGrass.png in gen_res and then
            repeat the process for dirt and ore.

            Tiles will not be put into gen_res without a background unless a trailing + is added.
            For example, %package+grass+dirt.png will not be put in gen_res without a grass or dirt background,
            but %package+grass+dirt+.png will be.

        All files starting with atlas- will be split in even 16x16 (f.ex, specified in c.ATLAS_TILE_SIZE)
            tiles and be named with numbers in gen_res.
            For example, %atlas-grass, which might be a 32x32 image, will be split in 4 pieces, and named grass.png,
            grass2.png and so on up to grass16.png.

            Tiles from atlasses will be put in gen_res without trailing + if no + at all is specified.
            Sizes of atlases must be multiples of 16, but need not be quadratic.

        All files starting with microtile- will be split into 8x8 microtile quartets and be named appropriately to
            which tile it represents, provided that the atlas is constructed as a 48x48 with an image filled in as
            a f.ex. lake with the shape depicted in the file res/example_microtile_atlas.jpg
            For example, %microtile-water.png
            Microtiles will be put in gen_res without trailing +.

            If a background is specified, it will be added before splitting.
                - If there's an atlas with the exact same size, put that unsplit behind the microtile.
                - If there's an atlas with other sizes, use the resulting tiles randomly as backgrounds.
                - If there's only simple images, repeatedly put it in the background.

        All files with no special formatting will not be copied to gen_res. It will only be prioritized as a
            background, unless a trailing + is specified, as specified above
            For example, %grass.png (will not be copied)

            If a image is formatted with leading % and trailing +, it will replace all tiles with the same name
            without % as a texture in the game.

        Formattings can be combined, but additions (+) must be specified last in the file. atlas- and microtile- can
            not be combined.
            For example: %atlas-sapling+grass+dirt.png

        If a tile requires another tile (%sapling+grass.png requires grass) it will be processed after the required tile
    """
    # Empty the folder of png's
    [os.remove(os.path.join(os.getcwd(), c.GEN_RES_FOLDER, f))
     for f in os.listdir(os.path.join(os.getcwd(), c.GEN_RES_FOLDER)) if f.rsplit(".", 1)[1] == "png"]

    # List of image keys that need to exist to fulfill all requirements
    required_images = []
    # Images loaded solely to fulfill requirements. {"image_key": "filename"}
    providied_images = {}
    # {"image_key": ["atlas/microtile/empty_string", ["requirement1", "requirement2"], "filename"]}
    source_files = {}

    # ========================================
    # Load the names of the textures to be processed, and how they should be processed.
    for f in os.listdir(os.path.join(os.getcwd(), c.RES_FOLDER)):
        if f[0] == "%":
            if "-" in f:
                # If there is a prefix
                image_key = f[1:].rsplit(".", 1)[0].split("-")[1].split("+")[0]
                prefix = f[1:].rsplit(".", 1)[0].split("-")[0]
                requirements = f[1:].rsplit(".", 1)[0].split("-")[1].split("+")[1:]
            else:
                image_key = f[1:].rsplit(".", 1)[0].split("+")[0]
                prefix = ""
                requirements = f[1:].rsplit(".", 1)[0].split("+")[1:]

            source_files[image_key] = [
                prefix,
                requirements,
                f  # The entire filename
            ]
            required_images.extend(requirements)

    # ========================================
    # Make sure each requirement is included
    for required_image in required_images:
        # If it can't be found in the loaded images already
        if required_image not in source_files and required_image is not "" and \
                required_image not in providied_images:
            # Try to load it
            if required_image + ".png" in os.listdir(os.path.join(os.getcwd(), c.RES_FOLDER)):
                providied_images[required_image] = os.path.join(os.getcwd(), c.RES_FOLDER, required_image + ".png")
            else:
                # If it isn't found anywhere, remove it from the requirements of the files to be processed
                for key in source_files:
                    for i in range(len(source_files[key][1]) - 1, -1, -1):
                        if source_files[key][1][i] == required_image:
                            del source_files[key][1][i]

    # ========================================
    # Order the images to be processed

    # [(priority, count, sources_key)]
    heap = []
    # For easier searching of added tiles
    images_in_heap = []
    remaining_images = list(source_files.keys())
    # Add tiles to the heap, making sure requirements are added first, with earlier priorities
    count = 0
    last_remaining_images = []
    while remaining_images:
        for i in range(len(remaining_images)-1, -1, -1):
            requirements = source_files[remaining_images[i]][1]
            is_ready = True
            priority = -1
            for requirement in requirements:
                if requirement != "":
                    if requirement in providied_images:
                        pass
                    else:
                        found_requirement = False
                        for heap_entry in heap:
                            if heap_entry[2] == requirement:
                                if priority < heap_entry[0]:
                                    priority = heap_entry[0]
                                found_requirement = True
                        if not found_requirement:
                            is_ready = False
            if is_ready:
                # Each element in the heap is (priority, count, sources_key)
                # count is used as a tie-breaker for priority.
                heapq.heappush(heap, (priority + 1, count, remaining_images[i]))
                count += 1
                del remaining_images[i]
        if last_remaining_images == remaining_images and remaining_images != []:
            print("A loop of tiles who reference each other has been found. "
                  "Please check the res folder for the format of the following images,"
                  "and make sure they don't refernce each other: " + str(remaining_images))
            break
        last_remaining_images = remaining_images
    # source_files = {"image_key": ["atlas/microtile/empty_string", ["requirement1", "requirement2"], "filename"]}
    # heap = [(priority, count, sources_key)]
    # {"image_key": [loaded_Surface_1, loaded_Surface_2}

    # ========================================
    #  Load images that aren't prefixed by % but is required for another tile.
    loaded_images = {}
    for provided_image in providied_images:
        loaded_images[provided_image] = \
            [pygame.image.load(os.path.join(os.getcwd(), c.RES_FOLDER, providied_images[provided_image]))]

    # ========================================
    # Go through the heap in priority order
    while heap:
        image_key = heapq.heappop(heap)[2]
        src_image = pygame.image.load(os.path.join(os.getcwd(), c.RES_FOLDER, source_files[image_key][2]))
        if source_files[image_key][0] == "atlas":
            loaded_images[image_key] = []
            for j in range(int(src_image.get_height() / c.ATLAS_TILE_SIZE)):
                for i in range(int(src_image.get_width() / c.ATLAS_TILE_SIZE)):
                    loaded_images[image_key].append(src_image.subsurface(pygame.Rect(
                        i*c.ATLAS_TILE_SIZE, j*c.ATLAS_TILE_SIZE, c.ATLAS_TILE_SIZE, c.ATLAS_TILE_SIZE)))

            if loaded_images[image_key] is []:
                # If the image is too small to divide, no image will have been added now.
                loaded_images[image_key] = [src_image]
            # Make sure the generated files are saved to gen_res
            if len(source_files[image_key][1]) == 0:
                source_files[image_key][1].append("")

        elif source_files[image_key][0] == "microtile":
            # Microtiles are not compatible with overlaying
            # TODO
            continue
        else:
            loaded_images[image_key] = [src_image]

        for background_name in source_files[image_key][1]:
            if background_name == "":
                # If it's the special case empty string, save the textures to gen_res
                for i, loaded_image in enumerate(loaded_images[image_key], 1):
                    _save_image(image_key, loaded_image, i)
            else:
                # For all other values, the value is a background. Overlay each random variation of the image on
                # the background and save it to gen_res
                for i, loaded_image in enumerate(loaded_images[image_key], 1):
                    image = random.choice(loaded_images[background_name])
                    image.blit(loaded_image, (0, 0))
                    _save_image(image_key + background_name.capitalize(), image, i)


def _save_image(image_name, image, i=0):
    """ Saves the provided image as image_name, with a number i, .png, in gen_res
        For example, grass2.png or grass.png

        If i is 1, no number is saved
    """
    if i == 1:
        pygame.image.save(image, os.path.join(os.getcwd(), c.GEN_RES_FOLDER, image_name + ".png"))
    else:
        pygame.image.save(image, os.path.join(os.getcwd(), c.GEN_RES_FOLDER, image_name + str(i) + ".png"))
