#!/usr/bin/env python
# coding=utf-8
""" Module /src/interface.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module handling interfaces, menus and prompts
"""
import sys, time

import pygame
import pygame.locals as pgl

import constants as c
import globals as g
import tiles
import maps
import entities


def key_reconfig():
    """ Function for reconfiguring key mappings. Freezes the screen and darkens it and displays
        prompts for telling the user which key should be inputted next. Closes when done 
    """
    set_key = None
    screen_updated = True
    invalid_key_timer = 0
    new_keys = []
    
    transparent_surface = pygame.Surface((g.width*c.TILE_SIZE,
                                          g.height*c.TILE_SIZE)).convert_alpha()
    transparent_surface.fill((0, 0, 0, 150))
    
    font = pygame.font.Font("freesansbold.ttf", 20)
    welcome_surface = font.render(c.CONFIG_KEYS_MESSAGE, True, c.CONFIG_KEYS_FONT_COLOR)
    error_surface = font.render(c.CONFIG_KEYS_ERROR_MESSAGE, True, c.CONFIG_KEYS_FONT_COLOR)    
    
    while True:
        # Events
        for event in pygame.event.get():
            # Quit code
            if event.type == pgl.QUIT:
                sys.exit()
            # Cancel
            elif event.type == pgl.KEYDOWN and event.key == c.CONFIG_KEYS_KEY:
                return
            # Key configuration
            elif event.type == pgl.KEYDOWN:
                set_key = event.key
        # If the user pressed a key
        if set_key is not None:
            for key in new_keys:
                if set_key == key:
                    invalid_key_timer = c.CONFIG_KEYS_INVALID_TIMER
                    set_key = None
                    screen_updated = True
                    break
            if set_key is None:
                continue
            new_keys.append(set_key)
            screen_updated = True
            set_key = None

        # Count down the error timer and update the screen if the button disappeared
        if invalid_key_timer > 0:
            invalid_key_timer -= 1
            if invalid_key_timer == 0:
                screen_updated = True

        # Only update screen if something updated
        if screen_updated:
            screen_updated = False

            # If it's done
            if len(new_keys) == len(g.key_list):
                for i in range(len(new_keys)):
                    g.key_list[i][1] = new_keys[i]
                g.update_key_dict()
                return
            elif len(new_keys) > len(g.key_list):
                raise Exception("The new_keys dictionary somehow got larger than the old_keys dictionary")

            # The text that tells the user which key should be configured next.
            # Uses the length of the new_keys to figure out which message it should use
            text_surface = font.render(c.CONFIG_KEYS_TEXT_PREFIX +
                                       g.key_list[len(new_keys)][2],
                                       True, c.CONFIG_KEYS_FONT_COLOR)
            # Draw the map buffer
            g.screen.blit(g.map_screen_buffer, (0, 0))
            # Draw entities
            for entity in g.entity_list:
                entity.paint()
            # Darken the screen a bit
            g.screen.blit(transparent_surface, (0, 0))
            # Draw text
            g.screen.blit(welcome_surface, (200, 100))
            g.screen.blit(text_surface, (50, 200))
            # Draw error text only if the player pressed an invalid button
            if invalid_key_timer > 0:
                g.screen.blit(error_surface, (200, 300))
            pygame.display.flip()
        # Sleep by a fixed amount, because this loop doesn't need to update very constantly 
        time.sleep(c.TICK_FREQ)


class MenuButton(object):
    """ A class for use in menus, representing the various buttons in a menu that can be selected.
    """
    def __init__(self, text, image, function=False, variables=[], recommended=False, tile_filter=[]):
        """ "text" should be a short string showing what the button represents
            "image" should be a string identifier pointing to a Graphics object in the
                g.images dictionary, for the thumbnail
            "function" should be a function that is called when this button is selected.
            "vars" should be a list of parameters that should be passed to the function when it's called.
            "recommended" decides whether or not this tile should be one of the first to be displayed.
            "tile_filter" should be a list of tiles that can be marked when this button should appear.
                Leave empty to always display.
        """
        self.text = text
        self.image = image
        self.function = function
        self.vars = variables
        # Set recommended to True for it to be displayed at the top of the menu
        self.recommended = recommended
        # The tiles that can be marked for this button to appear.
        # Leave empty for no filtering = all tiles are accepted.
        self.tile_filter = tile_filter
        # Determines if the Button will be usable. If False, it will be grayed out and not usable.
        self.active = True

    def __call__(self, *args, **kwargs):
        """ Calls the predetermined function
        """
        if self.function:
            if self.active:
                if self.vars:
                    return self.function(*self.vars)
                else:
                    return self.function()
            else:
                return False

    def __str__(self):
        return self.text


class Menu(object):
    """ Base class for on-screen menus that won't pause the game.
    """
    def __init__(self, background, buttons):
        """ Creates a general-purpose menu.
        
            "background" should be a string identifier pointing
                towards a Graphics object in the g.images dictionary
                that should be used as a background.
            "target" should be a tuple with an x and y coordinate in pixels
                for where the menu's top left corner should be painted
        """
        self.background = background
        self.buttons = []
        buttons.reverse()
        # The buttons gets assigned to coordinates in self.buttons in the end of the init function.

        # Check if each button should stay by looking at the tile filter.
        filter_tile = (g.map[g.special_entity_list["player"].get_aim_tile()[0]]
                       [g.special_entity_list["player"].get_aim_tile()[1]].type)

        for i in range(len(buttons)-1, -1, -1):
            button = buttons[i]
            if button.tile_filter:
                if filter_tile not in button.tile_filter:
                    buttons[i].active = False

        # The last known g.selected variable
        self.old_selected = g.selected[:]

        self.button_places = []
        self.needs_scroll = False
        self.background_width, self.background_height = g.images["menu_background"].get_size()
        self.target = (g.build_menu_coords[0], g.build_menu_coords[1])
        # If the build menu should be painted

        # Note that this is a function
        self.update_position()

        # Defining where buttons can be put
        area_width = self.background_width - 2 * c.BUTTON_PADDING
        area_height = self.background_height - c.BUTTON_BOTTOM_PADDING - c.BUTTON_TOP_PADDING
        buttons_wide = area_width // (c.BUTTON_SIZE + c.BUTTON_SPACING)
        buttons_high = area_height // (c.BUTTON_SIZE + c.BUTTON_SPACING)

        # A distance from the edges of the background that is balanced to center the buttons in the menu
        self.margin = (area_width - buttons_wide * (c.BUTTON_SIZE + c.BUTTON_SPACING) + c.BUTTON_SPACING) / 2

        # Make an empty button array.
        for i in range(buttons_wide):
            self.buttons.append([])
            for j in range(buttons_high):
                self.buttons[i].append(None)

        spot = [0, 0]
        # Go through all buttons and paint those who are "recommended" first.
        any_recommended = False
        for i in range(len(buttons) - 1, -1, -1):
            button = buttons[i]
            if button.recommended:

                # put the button in the next coordinate in the buttons array
                if spot[0] >= buttons_wide:
                    spot[0] = 0
                    spot[1] += 1
                    if spot[1] >= buttons_high and not self.needs_scroll:
                        self.needs_scroll = True
                        raise "Too many buttons. Implement a fix"  # TODO: Remove this
                self.buttons[spot[0]][spot[1]] = button
                del buttons[i]
                spot[0] += 1

                any_recommended = True

        # Then leave a spot empty, if any of them were recommended
        if any_recommended:
            if spot[0] >= buttons_wide:
                spot[0] = 0
                spot[1] += 1
                if spot[1] >= buttons_high and not self.needs_scroll:
                    self.needs_scroll = True
                    raise "Too many buttons. Implement a fix"  # TODO: Remove this
            spot[0] += 1

        # Then add all the other buttons.
        for i in range(len(buttons) - 1, -1, -1):
            button = buttons[i]
            if spot[0] >= buttons_wide:
                spot[0] = 0
                spot[1] += 1
                if spot[1] >= buttons_high and not self.needs_scroll:
                    self.needs_scroll = True
                    raise "Too many buttons. Implement a fix"  # TODO: Remove this
            self.buttons[spot[0]][spot[1]] = button
            del buttons[i]
            spot[0] += 1

        # Create the buffer and update it.
        self.screen_buffer = pygame.Surface(g.images["menu_background"].get_size(), flags=pygame.SRCALPHA)
        self.update_buffer()

    def update_position(self):
        """ Updates the position of the Menu based on where the player is.
        """
        player_x = g.special_entity_list["player"].x
        player_y = g.special_entity_list["player"].y

        # Put the target variable in the end of the screen the player isn't in.
        # X Coordinate
        if player_x > g.width * c.TILE_SIZE / 3.0 * 2.0:
            g.build_menu_coords[0] = c.BORDER_MARGINS
        elif player_x < g.width * c.TILE_SIZE / 3.0:
            g.build_menu_coords[0] = g.width * c.TILE_SIZE - self.background_width - c.BORDER_MARGINS
        elif g.build_menu_coords[0] is "Empty":
            g.build_menu_coords[0] = c.BORDER_MARGINS

        # Y Coordinate
        if player_y > g.height * c.TILE_SIZE / 3.0 * 2.0:
            g.build_menu_coords[1] = c.BORDER_MARGINS
        elif player_y < g.height * c.TILE_SIZE / 3.0:
            g.build_menu_coords[1] = g.height * c.TILE_SIZE - self.background_height - c.BORDER_MARGINS
        elif g.build_menu_coords[1] is "Empty":
            g.build_menu_coords[1] = c.BORDER_MARGINS

        # Set the variable the outside refers to.
        self.target = (g.build_menu_coords[0], g.build_menu_coords[1])

    def update_buffer(self):
        """ Updates the buffer that is painted to the screen with the paint function.
            This middle step is to decrease load from painting each button each frame,
                similar to the painting of the map.
        """
        # Update the position and paint the background
        self.update_position()
        self.screen_buffer = pygame.Surface(g.images["menu_background"].get_size(), flags=pygame.SRCALPHA)
        self.screen_buffer.blit(g.images[self.background].get(), (0, 0))

        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[0])):
                button = self.buttons[i][j]
                if button is not None:
                    self.screen_buffer.blit(g.images[button.image].get(),
                                            (i * (c.BUTTON_SIZE + c.BUTTON_SPACING) +
                                             self.margin + c.BUTTON_PADDING,
                                             j * (c.BUTTON_SIZE + c.BUTTON_SPACING) +
                                             c.BUTTON_TOP_PADDING))
                    if not button.active:
                        self.screen_buffer.blit(g.images["button_shader"].get(),
                                                (i * (c.BUTTON_SIZE + c.BUTTON_SPACING) +
                                                 self.margin + c.BUTTON_PADDING,
                                                 j * (c.BUTTON_SIZE + c.BUTTON_SPACING) +
                                                 c.BUTTON_TOP_PADDING))

        border_img = g.images["button_border"]

        # Calculate the difference between the size of the border picture size and the button size
        button_border_margin_width = (border_img.get_size()[0] - c.BUTTON_SIZE) / 2
        button_border_margin_height = (border_img.get_size()[0] - c.BUTTON_SIZE) / 2

        # Make sure the selector is inside the bounds
        self.loop_selector()

        # Paint the button border that is the selected button identifier.
        self.screen_buffer.blit(border_img.get(),
                                (g.selected[0] * (c.BUTTON_SIZE + c.BUTTON_SPACING) +
                                 self.margin + c.BUTTON_PADDING - button_border_margin_width,
                                 g.selected[1] * (c.BUTTON_SIZE + c.BUTTON_SPACING) +
                                 c.BUTTON_TOP_PADDING - button_border_margin_height))

        # Tooltips
        # Render the tooltip only if the selected spot has a button.
        if self.buttons[g.selected[0]][g.selected[1]] is not None:
            # Generate the tooltip
            tooltip = pygame.font.Font("freesansbold.ttf", 20).render(self.buttons[g.selected[0]][g.selected[1]].text,
                                                                      True, c.MENU_FONT_COLOR)
            # Blit it onto the the buffer
            self.screen_buffer.blit(tooltip,
                                    # X coordinate is calculated such that the text is centered in the x-axis
                                    (c.BUTTON_PADDING +
                                     ((self.background_width - 2 * c.BUTTON_PADDING) - tooltip.get_size()[0]) / 2,
                                     # Y Coordinate is placed below buttons, and centered between the remaining space
                                     c.BUTTON_TOP_PADDING + (len(self.buttons[0])) *
                                     (c.BUTTON_SIZE + c.BUTTON_SPACING) - c.BUTTON_SPACING +
                                     (c.BUTTON_BOTTOM_PADDING - tooltip.get_size()[1]) // 2))

    def paint(self):
        """ Paints the screen buffer to the screen.
        """
        if g.selected != self.old_selected:
            self.update_buffer()
            self.old_selected = g.selected[:]
        g.screen.blit(self.screen_buffer, self.target)

    def select(self):
        """ The function that is called when the select button is pressed when this menu is opened.
            Executes the function of the selected button and closes the menu if a button is selected.

            Returns true if the menu closed
        """
        self.loop_selector()
        if (self.buttons[g.selected[0]][g.selected[1]] is not None and
                self.buttons[g.selected[0]][g.selected[1]].function is not False):

            if self.buttons[g.selected[0]][g.selected[1]]():
                self.show = False
                g.force_update = True
                # Returns that it is true that it closed
                return True
            else:
                pass  # TODO make sure there's an indicator of that the pressed button didn't work.
        return False

    def loop_selector(self):
        """ Makes sure the selector stays inside the bounds by putting it on the other end of the menu if it's outside.
        """
        # Loop the selector
        while g.selected[0] >= len(self.buttons):
            g.selected[0] -= len(self.buttons)
        while g.selected[0] < 0:
            g.selected[0] += len(self.buttons)

        while g.selected[1] >= len(self.buttons[0]):
            g.selected[1] -= len(self.buttons[0])
        while g.selected[1] < 0:
            g.selected[1] += len(self.buttons[0])


def _put_tile(tile_id):
    tiles.make_tile(tile_id, *g.special_entity_list["player"].get_aim_tile())
    return True


def _close():
    return True


def _regenerate_map():
    return_value = False
    if c.GEN_DEMO_MODE is False:
        maps.load_map(maps.generate_map())
        g.force_update = True
        return_value = True
    else:
        if g.map_generator is None:
            g.map_generator = maps.generate_map_generator()
        try:
            maps.load_map(g.map_generator.__next__())
        except StopIteration:
            g.map_generator = None
            return_value = True
        g.force_update = True

    for i in range(len(g.entity_list)-1, -1, -1):
        del g.entity_list[i]
    for key in list(g.special_entity_list.keys())[:]:
        if key != "player":
            del g.special_entity_list[key]
        g.special_entity_list["player"].x = g.player_start_x
        g.special_entity_list["player"].y = g.player_start_y
        g.special_entity_list["player"].following_entity = None

    return return_value


def _create_pather():
    x, y = g.special_entity_list["player"].get_aim_tile()
    entities.PathingEntity(x=x*c.TILE_SIZE, y=y*c.TILE_SIZE, image="robot_empty",
                           movement_speed=c.PATHER_MOVEMENT_SPEED, custom_name="pather")
    return True


def _set_pather_target():
    if "pather" in g.special_entity_list:
        x, y = g.special_entity_list["player"].get_aim_tile()
        g.special_entity_list["pather"].pathfind((x, y))
        return True
    else:
        return False


class BuildMenu(Menu):
    """ Subclass of Menu, used for choosing which building you want to build at a location.
    """
    def __init__(self):
        """ Sets the menu up. Contains the information for the building menu.
        """

        super().__init__("menu_background", [
            MenuButton("Build Ore Mine", "ore_mine_button", _put_tile, ["ore_mine"], recommended=True,
                       tile_filter=["ore-package"]),
            MenuButton("Build Furnace", "furnace_button", _put_tile, ["furnace"], recommended=True,
                       tile_filter=["package", "dirt-package"]),
            MenuButton("Build Package Factory", "package_gen_button", _put_tile, ["package_gen"], recommended=True,
                       tile_filter=["package", "dirt_package"]),
            MenuButton("Build Launcher", "launcher_button", _put_tile, ["launcher"], recommended=True,
                       tile_filter=["package", "dirt-package"]),
            MenuButton("Reload Map", "button", _regenerate_map),
            MenuButton("Create Pather", "button1", _create_pather, tile_filter=["grass"]),
            MenuButton("Set Pather Target", "button2", _set_pather_target,
                       tile_filter=["grass", "ore", "stump"]),
            MenuButton("Close", "button_close", _close)
        ])