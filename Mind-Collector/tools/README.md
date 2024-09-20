## Tools

### For Statistics Triggered Markers

```bash
cd tools
```

#### [Screen Coordinates Finder](./ss_coordinates_finder.py) - A tool to find desired screen region coordinates. 

**How to use**: Open Your application (ex. League of Legends match), start the script by running `python ss_coordinates_finder.py`. Follow printed instructions. Then a mouse LPM click on the screen will print the coordinates of the clicked point. In this way you may find TOP (left-top) and BOTTOM (right-bottom) coordinates of the desired screen region.

#### [Preview Region](./preview_selected_ss_area.py) - A tool to preview selected screen for a given left-top and right-bottom coordinates.

**How to use**: Open Your application (ex. League of Legends match), start the script by running `python preview_selected_ss_area.py --top=1637,0 --bottom=1730,25` and follow printed instructions.


#### [SS Annotation Tweaker](./ss_annotation_tweaker.ipynb) - For cleaning annotations based on taken screenshots.
