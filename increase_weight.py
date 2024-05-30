import fontforge
import os
import glob

def get_ttf_files(directory):
    # Ensure the directory path ends with a slash or backslash
    if not directory.endswith(os.path.sep):
        directory += os.path.sep
    
    # Use glob to find all .ttf files in the directory
    ttf_files = glob.glob(os.path.join(directory, '*.ttf'))
    
    return ttf_files

directory = '/home/sonul/Downloads/build-3a85a7679/build/ttf/'
ttf_files = get_ttf_files(directory)

for file in ttf_files:
    # Open the font file
    font = fontforge.open(file)

    # Increase the weight of the font
    font.selection.all()
    font.changeWeight(15, "auto", 0, 0, "auto")

    # Generate a new font file with increased weight
    font.generate(file)

    # Close the font
    font.close()

