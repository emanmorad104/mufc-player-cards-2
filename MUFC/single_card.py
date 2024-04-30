import random
from PIL import Image, ImageDraw, ImageFont
from players_info_for_vs import players_info
from own_card import create_custom_player_card

# Function to create a player card for existing players
def create_player_card(player_name, attributes, player_image_path):
    # Load player image
    player_image = Image.open(player_image_path)

    # Create a blank image for the player card
    card_width = player_image.width
    card_height = player_image.height + 150  # Adjust height for attributes
    card = Image.new('RGB', (card_width, card_height), 'white')

    # Paste player image onto the card
    card.paste(player_image, (0, 0))

    # Draw player name background
    draw = ImageDraw.Draw(card)
    player_name_background_color = 'lightblue'  # Change this color as desired
    player_name_background_height = 40
    draw.rectangle([(0, player_image.height), (card_width, player_image.height + player_name_background_height)], fill=player_name_background_color)

    # Load font for player name
    player_name_font = ImageFont.truetype("Verdana.ttf", size=24)  # Adjust the font file and size as needed
    
    # Draw player name
    draw.text((10, player_image.height), player_name, fill='black', font=player_name_font)

    # Draw attributes background
    attribute_background_color = 'lightgreen'  # Change this color as desired
    attribute_background_height = 110
    draw.rectangle([(0, player_image.height + player_name_background_height), (card_width, card_height)], fill=attribute_background_color)

    # Load font for attributes
    attribute_font = ImageFont.truetype("Arial.ttf", size=16)  # Adjust the font file and size as needed
    
    # Draw player attributes
    attribute_y = player_image.height + player_name_background_height + 10
    for attribute, value in attributes.items():
        draw.text((10, attribute_y), f"{attribute}: {value}", fill='black', font=attribute_font)
        attribute_y += 20  # Adjust vertical spacing

    return card

# Select random football player
def find_random_player():
    player_names = list(players_info.keys())
    # Randomly select a player name
    random_player_name = random.choice(player_names)
    # Get player info based on random player name
    player_info = players_info.get(random_player_name)
    return random_player_name, player_info

# Example usage
random_player_name, random_player_info = find_random_player()
if random_player_info:
    player_image_path = random_player_info['image_path']
    player_attributes = {key: value for key, value in random_player_info.items() if key != 'image_path'}
    existing_player_card = create_player_card(random_player_name, player_attributes, player_image_path)
    existing_player_card.show()  # Show the player card
else:
    print("No existing player found.")

# # Create custom player card with face image
# player_name = "Jessie example"
# player_attributes = {"Strength": 8, "Speed": 9, "Skill": 8}  
# face_image_path = "face_image.png"  # Path to the face image created using face_image.py
# custom_player_card = create_custom_player_card(player_name, player_attributes, face_image_path)

# # Combine both player cards side by side
# total_width = existing_player_card.width + custom_player_card.width + 20  # Add some padding
# max_height = max(existing_player_card.height, custom_player_card.height)

# combined_card = Image.new('RGB', (total_width, max_height), 'white')
# combined_card.paste(existing_player_card, (0, 0))
# combined_card.paste(custom_player_card, (existing_player_card.width + 20, 0))

# # Display the combined player cards
# combined_card.show()
