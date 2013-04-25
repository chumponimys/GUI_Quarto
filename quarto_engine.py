# Sean Straw & Ari Cohen

from quarto_interface import *
from quarto_player import *
from quarto_state import *
from quarto_network import *

pygame.init()
WHITE = (0, 0, 0)

def quarto(player_1, player_2):
    game_state = GameState()
    game_status = GameStatus.PLAYING
    toggle_player_turns = -1
    turn_player = player_1
    display_game_state(game_state)
    while game_status == GameStatus.PLAYING:
        toggle_player_turns = -toggle_player_turns
        if toggle_player_turns == 1:
            turn_player = player_1
        else:
            turn_player = player_2
        while True:
            [move, game_status] = turn_player.get_move(game_state)
            if game_status == GameStatus.QUITTING: 
                break
            [move_check, game_status] = check_move(game_state,move)
            if move_check == MoveStatus.LEGAL_MOVE:
                make_move_and_display(game_state, move)
                break
            else:
                display_game_state(game_state)
                signal_bad_move(move, move_check, turn_player) 
    final_move = turn_player
    return [game_state, game_status, final_move, player_1, player_2]

while True: # main game loop
  o  MAIN_SURF.fill(WHITE)
    for event in pygame.event.get():
        if(event.type == QUIT):
            pygame.quit()
            sys.exit()
        elif (event.type == KEYDOWN):
            print "YEPPP"
            #Programmer laziness at its finest
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
