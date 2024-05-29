import random
from PIL import Image, ImageDraw, ImageFont, ExifTags
import os
from players_info import players_info

# Function to correct image orientation based on EXIF data
def correct_image_orientation(image):
    try:
        # Find the key corresponding to the 'Orientation' tag in the EXIF data
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        # Extract EXIF data from the image
        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation)
            # Rotate the image based on the orientation value
            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
    except Exception as e:
        print(f"Error correcting image orientation: {e}")
    return image

# Function to create a player card for a specific player with a football club logo
def create_player_card(player_name, player_info, logo_image_path, image_size=(300, 300)):
    # Extract player information
    player_image_path = player_info['image_path']
    player_position = player_info['Position']
    player_attributes = {key: value for key, value in player_info.items() if key not in ['image_path', 'Position']}
    
    # Load and resize player image
    player_image = Image.open(player_image_path)
    player_image = correct_image_orientation(player_image)
    player_image = player_image.resize(image_size, Image.LANCZOS)

    # Load logo image 
    logo_image = Image.open(logo_image_path).convert("RGBA")

    # Create a blank image for the player card
    card_width = image_size[0]
    card_height = image_size[1] + 150  # Adjust height for attributes
    card = Image.new('RGB', (card_width, card_height), 'white')

    # Paste player image onto the card
    card.paste(player_image, (0, 0))

    # Resize logo image to fit within 1/4th of the card width
    max_logo_width = card_width // 4
    max_logo_height = logo_image.height * max_logo_width // logo_image.width
    logo_image = logo_image.resize((max_logo_width, max_logo_height))

    # Paste logo image onto the card (top right corner)
    logo_width, logo_height = logo_image.size
    card.paste(logo_image, (card_width - logo_width, 0), logo_image)

    # Draw player name background
    draw = ImageDraw.Draw(card)
    player_name_background_color = 'black'  # Change this color as desired
    player_name_background_height = 40
    draw.rectangle([(0, image_size[1]), (card_width, image_size[1] + player_name_background_height)], fill=player_name_background_color)

    # Load the font for the player's position
    position_font_path = "./fonts/Bebas.ttf"
    if not os.path.isfile(position_font_path):
        raise FileNotFoundError(f"Font file '{position_font_path}' not found.")

    try:
        player_name_font = ImageFont.truetype(position_font_path, size=40)
    except Exception as e:
        raise Exception(f"Failed to load font '{position_font_path}': {e}")
    
    # Draw player position
    draw.text((10, image_size[1]), player_position, fill='white', font=player_name_font)

    # Draw a red rectangle for the attributes section
    attribute_background_color = '#E74C3C'
    attribute_background_height = 110
    draw.rectangle([(0, image_size[1] + player_name_background_height), (card_width, card_height)], fill=attribute_background_color)

    # Load the font for the attributes
    attribute_font_path = "./fonts/Bebas.ttf"
    try:
        attribute_font = ImageFont.truetype(attribute_font_path, size=16)
    except Exception as e:
        raise Exception(f"Failed to load font '{attribute_font_path}': {e}")
    # Draw player attributes
    attribute_y = image_size[1] + player_name_background_height + 10
    for attribute, value in player_attributes.items():
        draw.text((14, attribute_y), f"{attribute}: {value}", fill='black', font=attribute_font)
        attribute_y += 20  # Adjust vertical spacing

    return card

# Create your player card
specific_player_name = "Marcus Rashford"  # Change this to the player you want
specific_player_info = players_info.get(specific_player_name)
if specific_player_info:
    logo_image_path = "./images/logo.png" 
    specific_player_card_with_logo = create_player_card(specific_player_name, specific_player_info, logo_image_path)
    specific_player_card_with_logo.show()  
else:
    print(f"No information found for player: {specific_player_name}")
