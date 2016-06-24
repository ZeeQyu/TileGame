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
from src import globals as g


# This is a lookup-table for constructing microtiles. It specifies how the quartets should be used to be constructed
# See doc/microtiles.txt for more information
# "binary_neighbour_combination": ["quartet_name"]
MICROTILE_LEGEND = {
    "111": "full",
    "101": "corner",
    "001": "side",
    "100": "top",
    "000": "end"
}
# Prefix to let microtiles and atlases exist with the same name
MICROTILE_ATLAS_PREFIX = "+-+"
# Table for determining what position results in which kind of microtile in a microtile atlas.
# Uses MICROTILE_LEGEND keys for identifying which kind of quarter it is, plus a number 0-3 for what quarter
# position it's in (clockwise, starting with top left). None means "do not use this square".
MICROTILE_ATLAS_TABLE = [
    [ None,  None, "0000",  None,   None,   None,  None,  None],
    [ None,  None,  None,   None,   None,   None,  None,  None],
    [ None,  None, "0010", "1011", "1000", "0011", None, "0001"],
    [ None,  None, "1003", "1112", "1113", "1012", None,  None],
    [ None,  None, "1010", "1111", "1110", "1001", None,  None],
    ["0003", None, "0013", "1002", "1013", "0012", None,  None],
    [ None,  None,  None,   None,   None,   None,  None,  None],
    [ None,  None,  None,   None,   None,  "0002", None,  None]
]

class MissingMicrotileQuartetError(Exception):
    pass


class RequiredImageNotFoundError(Exception):
    pass


class Graphics(object):
    """ Graphics object containing an image. Loads the image by itself.
    """

    def __init__(self, name, rotation=0):
        """ "name" should be one of these two things, which determines what the image should be:
            - A pygame.Surface
                If so, the image will be that surface
            - A path, and in that case name_is_path should be True
                If so, the image will be that exact image

            "rotation" should be the rotation in degrees the image should be rotated conterclockwise before being saved
        """
        if type(name) == str:

            self.image = self._rotate(pygame.image.load(name), rotation)
        elif type(name) == pygame.Surface:
            self.image = self._rotate(name, rotation)

    @staticmethod
    def _rotate(image, rotation):
        if rotation != 0:
            return pygame.transform.rotate(image, rotation)
        else:
            return image

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

        # Load microtiles, that is, images that start with the same name as the key, but with endings sucha as Corner0
        if c.DEACTIVATE_MICROTILES is False and c.IMAGES[key].microtiles is not None:
            if type(c.IMAGES[key].microtiles) == str:
                microtile_name = c.IMAGES[key].microtiles
            else:
                microtile_name = c.IMAGES[key].png
            # Check if there's an extension
            if "." in microtile_name:
                primary, ext = microtile_name.rsplit(".", 1)
            else:
                # If there's no extension in the file name, use png as a default
                primary = microtile_name
                microtile_name += ".png"
                ext = "png"
            ext = "." + ext
            for microtile in [name.capitalize() for name in MICROTILE_LEGEND.values()]:
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
                        # Otherwise, try to mirror the side to look like the top.
                        if microtile == "Top":
                            if primary + "_" + "side" in images:
                                image = images[primary + "_" + "side"].get()
                            elif primary + "_" + "side" + "0" in images:
                                image = images[primary + "_" + "side" + "0"].get()
                            else:
                                # If all else fails, raise an exception that the file wasn't found
                                raise MissingMicrotileQuartetError(
                                    "Microtile corner " + primary + "_" + microtile.lower() +
                                    " not found. Please make sure the file " + primary + microtile + ext +
                                    " exists in the folder " + os.path.join(os.getcwd(), c.RES_FOLDER) + ".")
                            image = pygame.transform.flip(image, 1, 0)
                            image = pygame.transform.rotate(image, 90)
                            images[key + "_" + microtile.lower()] = Graphics(image)
                        else:
                            raise MissingMicrotileQuartetError(
                                "Microtile corner " + primary + "_" + microtile.lower() +
                                " not found. Please make sure the file " + primary + microtile + ext +
                                " exists in the folder " + os.path.join(os.getcwd(), c.RES_FOLDER) + ".")
                else:
                    # If 1 to 3 tiles were found, pick one, rotate it and use it as the top left one.
                    for i in range(4):
                        if primary + microtile + str(i) + ext in gen_res_images:
                            images[key + "_" + microtile.lower()] = Graphics(
                                os.path.join(os.getcwd(), c.GEN_RES_FOLDER, primary + microtile + str(i) + ext), i * 90)
                        if primary + microtile + str(i) + ext in res_images:
                            images[key + "_" + microtile.lower()] = \
                                Graphics(os.path.join(os.getcwd(), c.RES_FOLDER, primary + microtile + str(i) + ext),
                                         i * 90)
    return images


def construct_microtile(tile_type, image_name, shape):
    # If the tile doesn't exist, create it
    new_image = pygame.Surface((c.TILE_SIZE, c.TILE_SIZE))
    # Defines which quartet is being manipulated, clockwise, starting with top left
    pos = -1
    for j in range(0, 7, 2):
        pos += 1
        corner = shape[j - 1] + shape[j] + shape[j + 1]
        quartet_name = MICROTILE_LEGEND[corner]
        # Find the corresponding quartet
        quartet = None
        if tile_type + "_" + quartet_name + str(pos) in g.images:
            quartet = g.images[tile_type + "_" + quartet_name + str(pos)].get()
        elif tile_type + "_" + quartet_name in g.images:
            if pos != 0:
                quartet = pygame.transform.rotate(
                    g.images[tile_type + "_" + quartet_name].get(), pos * -90)
            else:
                quartet = g.images[tile_type + "_" + quartet_name].get()
        new_image.blit(quartet, (0, 0))
    g.images[image_name] = Graphics(new_image)
    return image_name


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
            which tile it represents, provided that the atlas is constructed as a 64x64 with an image filled in as
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

        Silently skips not found backgrounds.
    """
    # Empty the folder of png's
    [os.remove(os.path.join(os.getcwd(), c.GEN_RES_FOLDER, f))
     for f in os.listdir(os.path.join(os.getcwd(), c.GEN_RES_FOLDER)) if f.rsplit(".", 1)[1] == "png"]

    # Load the names of the files and parse them.
    implicit_backgrounds, required_images, source_files = _parse_files()

    # Make sure each requirement is included
    provided_images = _check_requirements(implicit_backgrounds, required_images, source_files)

    # Order the images to be processed
    heap = _create_heap(provided_images, source_files)
    # source_files = {"image_key": ["atlas/microtile/empty_string", ["requirement1", "requirement2"], "filename"]}
    # heap = [(priority, count, sources_key)]
    # {"image_key": [loaded_Surface_1, loaded_Surface_2}

    #  Load images that aren't prefixed by % but is required for another tile.
    loaded_images = {}
    for provided_image in provided_images:
        loaded_images[provided_image] = \
            [pygame.image.load(os.path.join(os.getcwd(), c.RES_FOLDER, provided_images[provided_image]))]

    # Go through the heap in priority order and create the files
    _process_heap(heap, loaded_images, source_files, implicit_backgrounds)


def _parse_files():
    """ Subfunction of prepare_images()
        Search through the c.RES_FOLDER for all files beginning with %, find the format of each file and
        construct a list of strings for what images are needed (required_images), what images there are (source_files)
        and what images will be created (implicit_backgrounds)
    """
    # List of image keys that need to exist to fulfill all requirements
    required_images = []
    # Images that exist
    # {"image_key": ["atlas/microtile/empty_string", ["requirement1", "requirement2"], "filename"]}
    source_files = {}
    # Requirements that are generated, f.ex. dirtGrass, from %dirt+grass.png
    implicit_backgrounds = []
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

            if prefix == "microtile":
                # Make sure an atlas and a microtile atlas can be loaded for the same tile, f.ex. water
                image_key = MICROTILE_ATLAS_PREFIX + image_key
            else:
                # Add the requirements to the array of derived images if it isn't a microtile atlas
                for requirement in requirements:
                    if requirement is not "":
                        implicit_backgrounds.append(image_key + requirement[0].capitalize() + requirement[1:])

            source_files[image_key] = [
                prefix,
                requirements,
                f  # The entire filename
            ]
            required_images.extend(requirements)

    return implicit_backgrounds, required_images, source_files


def _check_requirements(implicit_backgrounds, required_images, source_files):
    """ Use the lists created in _parse_files() and check them against each other so that each
        image name in required_images turns up in either source_files or amongst the implicit_backgrounds.
        If a requirement is not found, first attempt to load it from the res folder, even if it's without a %, and
        put it in the dictionary provided_images as {"file_name": pygame.Surface}

        If it's still not found, remove it from all images that requests it, without throwing an error. Notify
        the user through the console if c.NORMAL_DEBUG is on. If it's an important image, it will crash when
        graphics are loaded in load_graphics().
    """
    # Images loaded solely to fulfill requirements. {"image_key": "filename"}
    provided_images = {}
    for required_image in required_images:
        # If it can't be found in the loaded images already
        if required_image not in source_files and required_image is not "" and \
                        required_image not in provided_images and required_image not in implicit_backgrounds:

            # Try to load it
            if required_image + ".png" in os.listdir(os.path.join(os.getcwd(), c.RES_FOLDER)):
                provided_images[required_image] = os.path.join(os.getcwd(), c.RES_FOLDER, required_image + ".png")
            else:
                # If it isn't found anywhere, remove it from the requirements of the files to be processed
                for key in source_files:
                    for i in range(len(source_files[key][1]) - 1, -1, -1):
                        if source_files[key][1][i] == required_image:
                            del source_files[key][1][i]
                            if c.NORMAL_DEBUG:
                                print("Removed background requirement " + required_image +
                                      " because it wasn't found. Please add such an image to the res folder.")

    return provided_images


def _create_heap(provided_images, source_files):
    """ Order the elements of source_files to make sure each requirement is processed before the tile itself.
        If a loop, where several tiles reference themselves in a circle is found, notify the user (if c.NORMAL_DEBUG)
        and continue without crashing. If it's an important image, it will crash when load_graphics() is run.
    """
    # [(priority, count, sources_key)]
    heap = []

    remaining_images = list(source_files.keys())
    # Add tiles to the heap, making sure requirements are added first, with earlier priorities
    count = 0
    last_remaining_images = []
    while remaining_images:
        for i in range(len(remaining_images) - 1, -1, -1):
            requirements = source_files[remaining_images[i]][1]
            is_ready = True
            priority = -1
            for requirement in requirements:
                if requirement != "":
                    if requirement in provided_images:
                        pass
                    else:
                        found_requirement = False
                        for heap_entry in heap:
                            if heap_entry[2] == requirement:
                                if priority < heap_entry[0]:
                                    priority = heap_entry[0]
                                found_requirement = True
                            else:
                                for second_level_requirement in source_files[heap_entry[2]][1]:
                                    if second_level_requirement is not "" and requirement == heap_entry[2] + \
                                            second_level_requirement[0].capitalize() + second_level_requirement[1:]:
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
            if c.NORMAL_DEBUG:
                print("A loop of tiles who reference each other has been found. "
                      "Please check the res folder for the format of the following images,"
                      "and make sure they don't refernce each other in a circle: " + str(remaining_images))

                c.debug_print(locals())
            break
        last_remaining_images = remaining_images

    return heap


def _process_heap(heap, loaded_images, source_files, implicit_backgrounds):
    while heap:
        image_key = heapq.heappop(heap)[2]
        src_image = pygame.image.load(os.path.join(os.getcwd(), c.RES_FOLDER, source_files[image_key][2]))

        if source_files[image_key][0] == "atlas":
            loaded_images[image_key] = []
            for j in range(int(src_image.get_height() / c.ATLAS_TILE_SIZE)):
                for i in range(int(src_image.get_width() / c.ATLAS_TILE_SIZE)):
                    loaded_images[image_key].append(src_image.subsurface(pygame.Rect(
                        i * c.ATLAS_TILE_SIZE, j * c.ATLAS_TILE_SIZE, c.ATLAS_TILE_SIZE, c.ATLAS_TILE_SIZE)))
            if loaded_images[image_key] is []:
                # If the image is too small to divide, no image will have been added now.
                loaded_images[image_key] = [src_image]
            # Make sure the generated files are saved to gen_res
            if len(source_files[image_key][1]) == 0:
                source_files[image_key][1].append("")
        else:
            loaded_images[image_key] = [src_image]

        if source_files[image_key][0] != "microtile":
            # For normal tiles or normal atlases
            for background_name in source_files[image_key][1]:
                if background_name == "":
                    # If it's the special case empty string, save the textures to gen_res
                    for i, loaded_image in enumerate(loaded_images[image_key], 1):
                        _save_image(image_key, loaded_image, i)
                else:
                    # For all other values, the value is a background.
                    for i, loaded_image in enumerate(loaded_images[image_key], 1):
                        # Overlay each random variation of the image on the background and save it to gen_res
                        image = pygame.Surface((c.ATLAS_TILE_SIZE, c.ATLAS_TILE_SIZE), pygame.SRCALPHA)
                        image.blit(random.choice(loaded_images[background_name]), (0, 0))
                        image.blit(loaded_image, (0, 0))
                        _save_image(image_key + background_name[0].capitalize() + background_name[1:], image, i)
                        # Take the random variations of the backgrounded image and make it available for other tiles
                        if i == 1:
                            loaded_images[image_key + background_name[0].capitalize() + background_name[1:]] = [image]
                        else:
                            loaded_images[image_key + background_name[0].capitalize() + background_name[1:]].append(image)

        else:
            # For microtile atlases
            if loaded_images[image_key][0].get_width() == c.ATLAS_TILE_SIZE * 4 and \
                    loaded_images[image_key][0].get_height() == c.ATLAS_TILE_SIZE * 4:
                if "" not in source_files[image_key][1]:
                    source_files[image_key][1].append("")
                # Put each background behind the atlas
                for background_name in source_files[image_key][1]:
                    if background_name is not "":
                        microtile_atlas = pygame.Surface((c.ATLAS_TILE_SIZE*4, c.ATLAS_TILE_SIZE*4), pygame.SRCALPHA)
                        # Use an entire atlas if possible
                        atlas_background_successful = False
                        if background_name in source_files and source_files[background_name][0] == "atlas":
                            background_image = pygame.image.load(os.path.join(os.getcwd(),
                                                                 c.RES_FOLDER, source_files[background_name][2]))
                            if background_image.get_width() == c.ATLAS_TILE_SIZE * 4 and \
                                    background_image.get_height() == c.ATLAS_TILE_SIZE * 4:
                                # If there is such an atlas with the exact same size, use it.
                                microtile_atlas.blit(background_image, (0, 0))
                                atlas_background_successful = True
                        if not atlas_background_successful:
                            # If there isn't such an atlas, use single tiles, randomly chosen, over the entire background.
                            for j in range(4):
                                for i in range(4):
                                    microtile_atlas.blit(random.choice(loaded_images[background_name]),
                                                         (i*c.ATLAS_TILE_SIZE, j*c.ATLAS_TILE_SIZE))
                        del atlas_background_successful
                        microtile_atlas.blit(loaded_images[image_key][0], (0, 0))
                    else:
                        microtile_atlas = loaded_images[image_key][0]

                    # Create the name of the new image by appending the background to the image name
                    if background_name is "":
                        image_save_name = image_key[len(MICROTILE_ATLAS_PREFIX):]
                    else:
                        image_save_name = image_key[len(MICROTILE_ATLAS_PREFIX):] +\
                                          background_name[0].capitalize() + background_name[1:]

                    # Split the microtile atlas
                    if not c.DEACTIVATE_MICROTILES:
                        for j in range(8):
                            for i in range(8):
                                if MICROTILE_ATLAS_TABLE[j][i] is not None:
                                    # Create a transparent surface
                                    quarter = pygame.Surface((c.ATLAS_TILE_SIZE, c.ATLAS_TILE_SIZE), pygame.SRCALPHA)
                                    # Decide which quarter of said surface the quarter should be blitted onto
                                    x = 0
                                    y = 0
                                    if int(MICROTILE_ATLAS_TABLE[j][i][3]) is 1 or \
                                            int(MICROTILE_ATLAS_TABLE[j][i][3]) is 2:
                                        x = c.ATLAS_TILE_SIZE / 2
                                    if int(MICROTILE_ATLAS_TABLE[j][i][3]) is 2 or \
                                            int(MICROTILE_ATLAS_TABLE[j][i][3]) is 3:
                                        y = c.ATLAS_TILE_SIZE / 2

                                    quarter.blit(microtile_atlas.subsurface(pygame.Rect(
                                        i*c.ATLAS_TILE_SIZE/2, j*c.ATLAS_TILE_SIZE/2,
                                        c.ATLAS_TILE_SIZE/2, c.ATLAS_TILE_SIZE/2)),
                                        (x, y))
                                    _save_image(image_save_name +  # Image name and background name
                                                MICROTILE_LEGEND[MICROTILE_ATLAS_TABLE[j][i][:3]].capitalize() +  # Quarter name
                                                MICROTILE_ATLAS_TABLE[j][i][3],  # Quarter position
                                                quarter)

                    # Find out if there's a default tile.
                    found_microtile_default = (image_save_name in loaded_images or
                                               image_save_name in implicit_backgrounds)
                    for heap_entry in heap:
                        if heap_entry[2] == image_save_name:
                            found_microtile_default = True
                    if not found_microtile_default:
                        # If a default tile isn't found anywhere, create one from the center of the microtile atlas
                        default_image = pygame.Surface((16, 16))
                        # But make sure the surface fits in with the edges of other tiles, so put the top left quarter
                        # on the bottom right quarter and so on.
                        for i in (0, 1):
                            for j in (0, 1):
                                # For each quarter, blit it in the opposite square
                                default_image.blit(
                                    microtile_atlas.subsurface(pygame.Rect(
                                        c.ATLAS_TILE_SIZE*1.5 + i*c.ATLAS_TILE_SIZE*0.5,  # Position of source, x
                                        c.ATLAS_TILE_SIZE*1.5 + j*c.ATLAS_TILE_SIZE*0.5,  # Position of source, y
                                        c.ATLAS_TILE_SIZE*0.5, c.ATLAS_TILE_SIZE*0.5)),  # Size of
                                    ((1-i)*c.ATLAS_TILE_SIZE*0.5, (1-j)*c.ATLAS_TILE_SIZE*0.5))  # Pygame blit coordinate
                        _save_image(image_save_name,
                                    default_image)


def _save_image(image_name, image, i=1):
    """ Saves the provided image as image_name, with a number i, .png, in gen_res
        For example, grass2.png or grass.png

        If i is 1, no number is saved
    """
    if i == 1:
        number = ""
    else:
        number = str(i)
    if not os.path.isfile(os.path.join(os.getcwd(), c.GEN_RES_FOLDER, image_name + number + ".png")):
        pygame.image.save(image, os.path.join(os.getcwd(), c.GEN_RES_FOLDER, image_name + number + ".png"))
