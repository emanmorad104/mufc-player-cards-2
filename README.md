# MUFC player cards
- Programmes creating football player cards.

cd into the MUFC directory to run the python files

- top_trumps.py
    - Randomly selects 2 players. 
    - Players are displayed side by side. The attributes of the right player will be hidden.
    - User is prompted to select an attribute of their player (left hand side player) to play.
    - Selected attributed is compared against the corresponding attribute for the right player.
    - If the player's selected attribute is high than the right hand player they win. 
    - Results are printed on the terminal.
    - Player cards are displayed again at the end, this time the right players attributes are revealed. 

- own_player_top_trumps.py
    - Same process as above but the left hand side player is not random. 
    - The user can set a specific player they want. 
    - The user can add their own player and set this to be used in the programme (line 111)
        - To add own details user just needs to add their own information in "player_info.py" file.
        - If the user wants to use their own image, then the photo has to be added to the "images" folder. Otherwise they can use the "stock.png" photo.

- single_card.py
    - Used to create a custom player card. 
    - User adds their own information to players_info.py
    - User then updates line 99 and enters their own name. 
    - User's photo gets resized in the create_player_card function. 
        - Default dimensions are set with portrait selfies in mind. 
        - Can change the dimensions by passing a value for the image_size parameter when calling the create_player_card function on line 103. 
        - Alternatively can change dimensions for the default values on line 29

## Pre-Requisites
- Pillow python library (pip install pillow)
