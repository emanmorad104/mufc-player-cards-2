import random
from PIL import Image, ImageDraw, ImageFont
import os
from players_info import players_info
from ascii_results import win_art, lose_art, draw_art

# Function to create a player card
def create_player_card(player_name, attributes, position, player_image_path, show_values=True, image_size=(300, 300)):
    # Open and resize the player's image
    player_image = Image.open(player_image_path)
    player_image = player_image.resize(image_size, Image.LANCZOS)

    # Define the size of the card (image height + extra space for text)
    card_width = image_size[0]
    card_height = image_size[1] + 150
    card = Image.new('RGB', (card_width, card_height), 'white')
    # Paste the player's image onto the card
    card.paste(player_image, (0, 0))

    draw = ImageDraw.Draw(card)

    # Draw a black rectangle for the player's position
    player_name_background_color = 'black'
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

    # Draw the player's position on the card
    draw.text((10, image_size[1]), position, fill='white', font=player_name_font)

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

    # Draw each attribute and its value (if show_values is True) on the card
    attribute_y = image_size[1] + player_name_background_height + 10
    for attribute, value in attributes.items():
        text = f"{attribute}: {value}" if show_values else f"{attribute}: ???"
        draw.text((14, attribute_y), text, fill='black', font=attribute_font)
        attribute_y += 20

    return card

# Select random football players ensuring they are not the same
def find_random_players(num_players=2):
    player_names = list(players_info.keys())
    random_player_names = random.sample(player_names, num_players)
    while len(set(random_player_names)) < num_players:
        random_player_names = random.sample(player_names, num_players)
    player_infos = [players_info.get(name) for name in random_player_names]
    # Returns a tuple containing the selected player names and their corresponding information.
    return random_player_names, player_infos

# Function to get user input for attribute selection
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

# Function to combine and show player cards side by side
def show_combined_cards(left_card, right_card):
    # Create a new image with enough width to hold both cards side by side
    combined_image = Image.new('RGB', (left_card.width + right_card.width, max(left_card.height, right_card.height)), 'white')
    combined_image.paste(left_card, (0, 0))
    combined_image.paste(right_card, (left_card.width, 0))
    combined_image.show()

# Function to compare attribute values and determine the result
def compare_attribute_values(attribute, left_player_attributes, right_player_attributes):
    # Convert attribute values from strings (with '%') to integers
    left_value = int(left_player_attributes[attribute].strip('%'))
    right_value = int(right_player_attributes[attribute].strip('%'))
    
    # Retrieve player names
    left_player_name = random_player_names[0]
    right_player_name = random_player_names[1]

     # Compare the attribute values and determine the result
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


# Run top trumps game

# Select random players and their information
random_player_names, random_player_infos = find_random_players()

left_player_card = None
right_player_card = None

# Create player cards for the selected players
for i, (player_name, player_info) in enumerate(zip(random_player_names, random_player_infos)):
    if player_info:
        player_image_path = player_info['image_path']
        player_position = player_info['Position']
        player_attributes = {key: value for key, value in player_info.items() if key not in ['image_path', 'Position']}
        
        if i == 0:
            left_player_card = create_player_card(player_name, player_attributes, player_position, player_image_path, show_values=True)
        else:
            right_player_card = create_player_card(player_name, player_attributes, player_position, player_image_path, show_values=False)

# If both player cards are created, display them side by side
if left_player_card and right_player_card:
    show_combined_cards(left_player_card, right_player_card)

# Get the attribute choice from the user
attribute = get_user_input()
print("Attribute:", attribute)

# Show the right player's card with values revealed
right_player_attributes = {key: value for key, value in random_player_infos[1].items() if key not in ['image_path', 'Position']}
right_player_card = create_player_card(random_player_names[1], right_player_attributes, random_player_infos[1]['Position'], random_player_infos[1]['image_path'], show_values=True)

# If both player cards are created, display them side by side again
if left_player_card and right_player_card:
    show_combined_cards(left_player_card, right_player_card)

# Extract left player's attributes
left_player_attributes = {key: value for key, value in random_player_infos[0].items() if key not in ['image_path', 'Position']}
print(f"{random_player_names[0]} - {attribute}: {left_player_attributes[attribute]}")
print(f"{random_player_names[1]} - {attribute}: {right_player_attributes[attribute]}")

# Compare the attribute values and determine the result
result = compare_attribute_values(attribute, left_player_attributes, right_player_attributes)
print(result)
