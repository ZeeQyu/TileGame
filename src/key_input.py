#!/usr/bin/env python
# coding=utf-8
""" Module /src/key_input.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame

    Module for controlling input from the user. Note that the key rebinding happens separately in interface.py
"""
import os
import sys

import pygame
import pygame.locals as pgl

sys.path.append(os.path.join(os.getcwd(), "sys"))
import globals as g
import units
import interface
import constants as c
import entities

player_dirs = {
    (1, 0): False,
    (-1, 0): False,
    (0, 1): False,
    (0, -1): False
}

def event_check():
    for event in pygame.event.get():
        # Quit code
        if event.type == pgl.QUIT:
            sys.exit()
        if event.type == pgl.KEYDOWN or event.type == pgl.KEYUP:
            # Create beetle with (default) a
            if event.type == pgl.KEYDOWN and event.key == g.key_dict["spawn_beetle"][0]:
                g.entity_list.append(units.Beetle(g.special_entity_list["player"].x,
                                                  g.special_entity_list["player"].y))
            # Duplicate all beetles with (default) D
            elif event.type == pgl.KEYDOWN and event.key == g.key_dict["duplicate_beetles"][0]:
                # Make an empty list to temporarily store the added beetles, so no infinite loop appears
                temp_entity_list = []
                for entity in g.entity_list:
                    if type(entity) == units.Beetle:
                        temp_entity_list.append(units.Beetle(entity.x, entity.y))
                g.entity_list.extend(temp_entity_list)
            # Remove all beetles
            elif event.type == pgl.KEYDOWN and event.key == g.key_dict["remove_beetles"][0]:
                # Loop backwards through the g.entity_list
                for i in range(len(g.entity_list) - 1, -1, -1):
                    if type(g.entity_list[i]) == units.Beetle:
                        del g.entity_list[i]
                g.force_update = True
            # Key configuration
            elif event.type == pgl.KEYDOWN and event.key == c.CONFIG_KEYS_KEY:
                skip_cycle = g.force_update = True
                interface.key_reconfig()

            elif event.key == g.key_dict["move_up"][0]:
                _move(event, (0, -1))

            elif event.key == g.key_dict["move_down"][0]:
                _move(event, (0, 1))

            elif event.key == g.key_dict["move_left"][0]:
                _move(event, (-1, 0))

            elif event.key == g.key_dict["move_right"][0]:
                _move(event, (1, 0))

            elif event.key == g.key_dict["place_tile"][0]:
                g.special_entity_list["player"].placing_tile = _if_down(event.type)
            elif event.key == g.key_dict["remove_tile"][0]:
                g.special_entity_list["player"].removing_tile = _if_down(event.type)
            elif (event.key == g.key_dict["pick_up_tile"][0] and
                    event.type == pgl.KEYDOWN):
                # This is handled in g.special_entity_list["player"].update()
                if not g.special_entity_list["player"].browsing_menu:
                    g.special_entity_list["player"].toggle_grab = True

            elif (event.key == g.key_dict["build_menu"][0] and
                    event.type == pgl.KEYUP):
                # Shows the build menu
                if g.tile_target_selection is None:
                    g.force_update = True
                    g.special_entity_list["player"].y_minus = g.special_entity_list["player"].y_plus =\
                        g.special_entity_list["player"].x_minus = g.special_entity_list["player"].x_plus = False
                    if "menu" not in g.non_entity_list.keys():
                        g.non_entity_list["menu"] = interface.BuildMenu()
                        g.special_entity_list["player"].browsing_menu = True
                    else:
                        del g.non_entity_list["menu"]
                        g.special_entity_list["player"].browsing_menu = False

            elif (event.key == g.key_dict["select"][0] or event.key == g.key_dict["select2"][0] and
                    event.type == pgl.KEYDOWN):
                # Selects the current menu item
                if "menu" in g.non_entity_list.keys():
                    if g.non_entity_list["menu"].select():
                        del g.non_entity_list["menu"]
                        g.special_entity_list["player"].browsing_menu = False
                elif "tile_target" in g.special_entity_list:
                    if g.get_img(*g.special_entity_list["player"].get_aim_tile()).factory_output:
                        good_names = []
                        for good in g.get_img(*g.special_entity_list["player"].get_aim_tile()).factory_output:
                            good_names.append(good[0])
                        g.non_entity_list["menu"] = interface.TileTargetMenu(good_names)
                        g.force_update = True
                    else:
                        g.tile_target_selection = None
                        del g.special_entity_list["tile_target"]
                        g.special_entity_list["player"].browsing_menu = False

            elif (event.key == g.key_dict["change_target"][0] and
                    event.type == pgl.KEYDOWN):
                if not g.special_entity_list["player"].browsing_menu:
                    if g.get_img(*g.special_entity_list["player"].get_aim_tile()).factory_output:
                        g.menu_selection = [0, 0]
                        g.special_entity_list["player"].browsing_menu = True
                        g.special_entity_list["player"].y_minus = g.special_entity_list["player"].y_plus = \
                            g.special_entity_list["player"].x_minus = g.special_entity_list["player"].x_plus = False
                        g.tile_target_selection = list(g.special_entity_list["player"].get_aim_tile())
                        x, y = g.special_entity_list["player"].get_aim_tile()
                        g.special_entity_list["tile_target"] =\
                            entities.Entity(x*c.TILE_SIZE, y*c.TILE_SIZE, "tile_target_aim",
                                            0, rotates=False, collides=False)
                elif g.tile_target_selection is not None:
                    g.special_entity_list["player"].browsing_menu = False
                    g.tile_target_selection = None
                    del g.special_entity_list["tile_target"]
                    del g.non_entity_list["menu"]
                    g.force_update = True


def _if_down(down_or_up):
    """ Checks if down_or_up is equal to pgl.KEYDOWN. Returns true if it is, otherwise it returns false.
    """
    return down_or_up == pgl.KEYDOWN


def _move(event, direction):
    if not g.special_entity_list["player"].browsing_menu:
        player_dirs[direction] = _if_down(event.type)
        dirs = [0, 0]
        for key in player_dirs:
            if player_dirs[key]:
                dirs[0] += key[0]
                dirs[1] += key[1]
        g.special_entity_list["player"].dir = dirs

    else:
        if _if_down(event.type):
            if g.tile_target_selection is not None:
                if "menu" in g.non_entity_list:
                    g.non_entity_list["menu"].selection_queue.insert(0, direction)
                else:
                    g.tile_target_selection[0] += direction[0]
                    g.tile_target_selection[1] += direction[1]
            else:
                g.non_entity_list["menu"].selection_queue.insert(0, direction)
            g.force_update = True

            # if not g.special_entity_list["player"].browsing_menu:
            #     g.special_entity_list["player"].y_minus = _if_down(event.type)
            # else:
            #     if _if_down(event.type):
            #         if g.tile_target_selection is not None:
            #             if "menu" in g.non_entity_list:
            #                 g.tile_target_menu_selection[1] -= 1
            #             else:
            #                 g.tile_target_selection[1] -= 1
            #         else:
            #             g.build_menu_selection[1] -= 1
            #         g.force_update = True