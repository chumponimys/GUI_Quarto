# Quarto.py
# Sean Straw & Ari Cohen

from quarto_interface import *
from quarto_player import *
from quarto_state import *
from quarto_network import *
from quarto_engine import *

while True:
        interface_state = MainInterface()
        player_1 = GamePlayer()
        player_1.player_num = "1"
        player_2 = GamePlayer()
        player_2.player_num = "2"
        get_players_info(player_1, player_2, interface_state)
        [game_state, game_status, final_move, player_1, player_2] = quarto(player_1, player_2, interface_state)
        signal_end_of_game(game_status, game_state, player_1, player_2, final_move)
