from PIL import Image, ImageDraw, ImageFont

# Function to draw ovals for face features
def draw_oval(draw, color, x_radius, y_radius, x, y, angle=0):
    # Create a blank image with transparent background
    temp_image = Image.new("RGBA", (x_radius * 2, y_radius * 2), (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_image)

    # Draw the oval on the temporary image
    temp_draw.ellipse((0, 0, x_radius * 2, y_radius * 2), fill=color)

    # Rotate the temporary image
    rotated_image = temp_image.rotate(angle, expand=True)

    # Paste the rotated oval onto the main image
    draw.bitmap((x - x_radius, y - y_radius), rotated_image, fill=color)

# Function to create a player card with a custom face image
def create_custom_player_card(player_name, attributes, face_image_path):
    # Load face image
    face_image = Image.open(face_image_path)

    # Create a blank image for the player card
    card_width = face_image.width
    card_height = face_image.height + 150  # Adjust height for attributes
    card = Image.new('RGB', (card_width, card_height), 'white')

    # Paste face image onto the card
    card.paste(face_image, (0, 0))

    # Draw player name background
    draw = ImageDraw.Draw(card)
    player_name_background_color = 'lightblue'  
    player_name_background_height = 40
    draw.rectangle([(0, face_image.height), (card_width, face_image.height + player_name_background_height)], fill=player_name_background_color)

    # Load font for player name
    player_name_font = ImageFont.truetype("Verdana.ttf", size=24)  # Adjust the font file and size as needed
    
    # Draw player name
    draw.text((10, face_image.height), player_name, fill='black', font=player_name_font)

    # Draw attributes background
    attribute_background_color = 'lightgreen'  
    attribute_background_height = 110
    draw.rectangle([(0, face_image.height + player_name_background_height), (card_width, card_height)], fill=attribute_background_color)

    # Load font for attributes
    attribute_font = ImageFont.truetype("Arial.ttf", size=16)  # Adjust the font file and size as needed
    
    # Draw player attributes
    attribute_y = face_image.height + player_name_background_height + 10
    for attribute, value in attributes.items():
        draw.text((10, attribute_y), f"{attribute}: {value}", fill='black', font=attribute_font)
        attribute_y += 20  # Adjust vertical spacing

    return card

# Example usage
if __name__ == "__main__":
    player_name = "Bob example"
    player_attributes = {"Strength": 8, "Speed": 9, "Skill": 7}  # Example attributes
    face_image_path = "face_image.png"  # Path to the face image created using face_image.py
    player_card = create_custom_player_card(player_name, player_attributes, face_image_path)
    player_card.show()  # Show the player card
