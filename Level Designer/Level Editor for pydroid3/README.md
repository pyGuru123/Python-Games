# Level Designer for pydroid3

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-swag.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

This is a simple python script to design levels for your games on pydroid3. It works best when your coding vertical non-scrollable platformer games using pydroid3. This level editor was used to create levels for this game [Cave Story](https://github.com/pyGuru123/Python-Games/tree/master/Cave%20Story). Download and play it on pydroid3.

![Alt text](app.png?raw=true "Level Designer")

The Level Editor Is A Non Scrollable And Works Best With 16x16 Tiles.

## How to Download

Download this project from here [Download Level Designer](https://downgit.github.io/#/home?url=https://github.com/pyGuru123/Python-Games/tree/master/Level%20Designer/Level%20Editor%20for%20pydroid3)

## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following packages :-
* Pygame

```bash
pip install pygame
```

Note :- pygame is already installed on pydroid3. No need to install it, just import it.

## Usage

Run the main.py file to open the level editor. Click load to load prevoisuly designed levels. Click save to save your current level. Click cross to remove a tile from certain place. This tile editor can be used to create non scrollable games.

Instructions for using the Level Editor with your own tilemaps.

* Split the tilemap and put all the tile images in the tiles folder. Make sure you have less than 90 tiles.
* Set the number of tiles in NUM_TILES variable at line 29 in main.py 
* Set level in current_level variable at line 30 in main.py. This should be a integer representing the level which you want to create / edit.
* Run the main.py file, click load to load level data ( currently empty ), click anywhere on the empty screen to highlight the tile.
* Now click any asset tile to set the tile, and start creating your level.
* Finally click save to save the level data in a pickle file.
* press back on pydroid3 or ESC on pc to quit the program.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.