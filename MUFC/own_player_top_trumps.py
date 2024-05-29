import random
from PIL import Image, ImageDraw, ImageFont
import os
from players_info import players_info
from ascii_results import win_art, lose_art, draw_art

# Function to create a player card for existing players
def create_player_card(player_name, attributes, position, player_image_path, show_values=True, image_size=(300, 300)):
    # Load player image and resize it
    player_image = Image.open(player_image_path)
    player_image = player_image.resize(image_size, Image.LANCZOS)

    # Create a blank image for the player card
    card_width = image_size[0]
    card_height = image_size[1] + 150  # Adjust height for attributes
    card = Image.new('RGB', (card_width, card_height), 'white')

    # Paste player image onto the card
    card.paste(player_image, (0, 0))

    # Draw player name background
    draw = ImageDraw.Draw(card)
    player_name_background_color = 'black'  # Change this color as desired
    player_name_background_height = 40
    draw.rectangle([(0, image_size[1]), (card_width, image_size[1] + player_name_background_height)], fill=player_name_background_color)

    # Load font for player name
    font_path = "./fonts/Bebas.ttf"  # Adjust the font file path as needed
    if not os.path.isfile(font_path):
        raise FileNotFoundError(f"Font file '{font_path}' not found.")
    
    try:
        player_name_font = ImageFont.truetype(font_path, size=40)  # Adjust the font file and size as needed
    except Exception as e:
        raise Exception(f"Failed to load font '{font_path}': {e}")
    
    # Draw player position
    draw.text((10, image_size[1]), position, fill='white', font=player_name_font)

    # Draw attributes background
    attribute_background_color = '#E74C3C'  # Change this color as desired
    attribute_background_height = 110
    draw.rectangle([(0, image_size[1] + player_name_background_height), (card_width, card_height)], fill=attribute_background_color)

    # Load font for attributes
    try:
        attribute_font = ImageFont.truetype(font_path, size=16)  # Adjust the font file and size as needed
    except Exception as e:
        raise Exception(f"Failed to load font '{font_path}': {e}")
    
    # Draw player attributes
    attribute_y = image_size[1] + player_name_background_height + 10
    for attribute, value in attributes.items():
        if show_values:
            draw.text((14, attribute_y), f"{attribute}: {value}", fill='black', font=attribute_font)
        else:
            draw.text((14, attribute_y), f"{attribute}: ???", fill='black', font=attribute_font)
        attribute_y += 20  # Adjust vertical spacing

    return card

# Select a random player
def find_random_player(exclude_player_name=None):
    player_names = list(players_info.keys())
    if exclude_player_name:
        player_names.remove(exclude_player_name)
    random_player_name = random.choice(player_names)
    random_player_info = players_info[random_player_name]
    return random_player_name, random_player_info

# Function to combine and show player cards side by side
def show_combined_cards(left_card, right_card):
    combined_image = Image.new('RGB', (left_card.width + right_card.width, max(left_card.height, right_card.height)), 'white')
    combined_image.paste(left_card, (0, 0))
    combined_image.paste(right_card, (left_card.width, 0))
    combined_image.show()

# Function to get user input for attribute
def get_user_input():
    options = ["Shooting accuracy", "Passing accuracy", "Appearances"]
    print("Choose an attribute:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    choice = input("Enter the number of your choice: ").strip()
    
    while not choice.isdigit() or int(choice) not in range(1, len(options) + 1):
        print("Invalid choice. Please try again.")
        choice = input("Enter the number of your choice: ").strip()

    return options[int(choice) - 1]

# Function to compare attribute values and determine the result
def compare_attribute_values(attribute, left_player_attributes, right_player_attributes, left_player_name, right_player_name):
    left_value = int(left_player_attributes[attribute].strip('%'))
    right_value = int(right_player_attributes[attribute].strip('%'))
    
    if left_value > right_value:
        print(win_art)
        print(f"You won! Your player's {left_player_name} {attribute} value ({left_value}%) is higher than your opponent's {right_player_name} ({right_value}%).")
        return "You won!"
    elif left_value == right_value:
        print(draw_art)
        return "It is a draw"
    else:
        print(lose_art)
        print(f"You lost! Your player's {left_player_name} {attribute} value ({left_value}%) is lower than your opponent's {right_player_name} ({right_value}%).")
        return "You lose"

# Manual selection of player for the left card
left_player_name = "Marcus Rashford"  # Enter the name of the player you want for the left card

# Retrieve player info for the manually selected left player
left_player_info = players_info.get(left_player_name)
left_player_card = None

# Create the card for the left player
if left_player_info:
    player_image_path = left_player_info['image_path']
    player_position = left_player_info['Position']
    player_attributes = {key: value for key, value in left_player_info.items() if key not in ['image_path', 'Position']}
    left_player_card = create_player_card(left_player_name, player_attributes, player_position, player_image_path, show_values=True)

# Select a random player for the right card, excluding the left player
random_player_name, random_player_info = find_random_player(exclude_player_name=left_player_name)
right_player_card = None

# Create the card for the right player
if random_player_info:
    player_image_path = random_player_info['image_path']
    player_position = random_player_info['Position']
    player_attributes = {key: value for key, value in random_player_info.items() if key not in ['image_path', 'Position']}
    right_player_card = create_player_card(random_player_name, player_attributes, player_position, player_image_path, show_values=False)

# Combine and display the player cards side by side
if left_player_card and right_player_card:
    show_combined_cards(left_player_card, right_player_card)

# Get user input
attribute = get_user_input()
print("Attribute:", attribute)

# Update the right player card to reveal the values
right_player_attributes = {key: value for key, value in random_player_info.items() if key not in ['image_path', 'Position']}
right_player_card = create_player_card(random_player_name, right_player_attributes, random_player_info['Position'], random_player_info['image_path'], show_values=True)

# Combine player cards side by side again to show updated card
if left_player_card and right_player_card:
    show_combined_cards(left_player_card, right_player_card)

# Print both players' names and attribute values
left_player_attributes = {key: value for key, value in left_player_info.items() if key not in ['image_path', 'Position']}
print(f"{left_player_name} - {attribute}: {left_player_attributes[attribute]}")
print(f"{random_player_name} - {attribute}: {right_player_attributes[attribute]}")

# Compare the values of the selected attribute
result = compare_attribute_values(attribute, left_player_attributes, right_player_attributes, left_player_name, random_player_name)
print(result)
