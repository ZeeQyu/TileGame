TileGame
========
Test
An experimental tile-based game

Requires Python 3.2 and Pygame for Python 3.2.
**INSTALL.txt** has installation instructions.

Consider reading **concept.txt** for more context on the project

Generates a game world and lets you move a character with collision and turning.

- **Arrow keys** to move.

- **A** summons a beetle minion at your feet that randomly roams around.
- Press **S** to duplicate all beetles.
- Press **W** to remove all beetles.
- Press and hold **F** to destroy a tile, for example, trees and buildings.
 
        Rocks can't be destroyed, nor can packages and ores. Pretty much everything else can.

- Press **D** to place a sapling.
- Press **E** to pick up or place down a package

        (Spawns in the middle of the map. The one with a red line is an infinite package).

- Press **Q** to open a menu that is context-sensitive, depending on the tile you're aiming at.

        (Aiming at a package (not an endless package) will let you build a launcher and aiming at a package on a
        piece of ore (which currently has a green placeholder texture) will let you build an ore miner.
        None of the structures currently do anything.    
        Aiming at grass lets you play around with my test version of pathfinding with a small robot, which you can
        set targets for with the menu button
   
- Press **Space** to select the button you're currently aiming at. (Because Enter is too far away on the keyboard.)
- Press **Insert** to rebind all keys other than Insert.

The game has randomly generated maps that can be rerolled with a button in the **Q**-menu.

    Doing this can cause instabilities like being able to walk around on the trees. Use with caution


//ZeeQyu