import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

CACHE_DIR = "cache"
IMAGE_PATH = os.path.join(CACHE_DIR, "summary.png")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.path.join(BASE_DIR, "assets", "DejaVuSans-Bold.ttf")

def generate_summary_image(total_countries: int, top_5_countries: list, timestamp: datetime):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    img_width, img_height = 800, 400
    bg_color = (20, 30, 40)
    text_color = (255, 255, 255)
    highlight_color = (70, 130, 180)

    image = Image.new("RGB", (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(image)

    try:
        title_font = ImageFont.truetype(FONT_PATH, 32)
        text_font = ImageFont.truetype(FONT_PATH, 18)
        small_font = ImageFont.truetype(FONT_PATH, 14)
    except IOError:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        print("Warning: Custom font not found. Using default.")

    # Title
    draw.text((30, 20), "Country Data Summary", font=title_font, fill=highlight_color)
    
    # Stats
    draw.text((30, 80), f"Total Countries Cached: {total_countries}", font=text_font, fill=text_color)
    draw.text((30, 110), f"Last Refresh: {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}", font=text_font, fill=text_color)
    
    # Top 5 Countries
    draw.text((30, 160), "Top 5 Countries by Estimated GDP (USD):", font=text_font, fill=highlight_color)
    y_pos = 190
    for i, country in enumerate(top_5_countries):
        gdp_billions = country.estimated_gdp / 1_000_000_000 if country.estimated_gdp else 0
        text = f"{i+1}. {country.name}: ${gdp_billions:,.2f} Billion"
        draw.text((40, y_pos), text, font=text_font, fill=text_color)
        y_pos += 30

    image.save(IMAGE_PATH)
    print(f"Summary image saved to {IMAGE_PATH}")