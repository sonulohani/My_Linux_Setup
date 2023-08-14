import fontforge

def add_weight(input_font_path, output_font_path, weight_increment):
    font = fontforge.open(input_font_path)
    
    for glyph in font.glyphs():
        # Skip non-glyph characters
        if glyph.isWorthOutputting():
            glyph.changeWeight(weight_increment)
    
    font.generate(output_font_path)
    font.close()

if __name__ == "__main__":
    input_font = ""
    output_font = ""
    weight_increment = 10  # Adjust this value based on your needs
    
    add_weight(input_font, output_font, weight_increment)

