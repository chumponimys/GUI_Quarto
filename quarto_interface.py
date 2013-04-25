import pygame, sys
from pygame.locals import *

pygame.init()
MAIN_SURF = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Quarto')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 100, 0)
BLUE = (0, 0, 128)
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (100, 100, 0)
RED = (255, 0, 0)
LIGHT_RED = (100, 0, 0)
GRAY = (150, 150, 150)

class Board():

    def __init__(self, position, board_width, square_width):
        self.position = position
        self.total_squares = board_width * board_width
        self.board_width = board_width
        self.square_width = square_width
        self.squares = []
        for square_num in range(self.total_squares):
            new_square = Square(square_num, self)
            self.squares.append(new_square)
        width = (board_width * square_width) + (5 * (board_width - 1))
        self.surface = pygame.Surface((width, width))
        self.board_rect = pygame.Rect(position[0], position[1], width, width)

    def set_square(self, square_number, piece):
        pass

    def get_square(self, square_number):
        pass

    def update_board_surface(self):
        self.surface.fill(BLACK)
        for square in self.squares:
            square_surf = square.get_square_surface()
            self.surface.blit(square_surf, square.position)
        return self.surface

    def draw_board(self):
        board_surf = self.update_board_surface()
        MAIN_SURF.blit(board_surf, self.position)

    def check_for_mouse(self, dragging_piece):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.board_rect.collidepoint([mouse_x, mouse_y]):
            mouse_x -= self.position[0]
            mouse_y -= self.position[1]
            col = mouse_x / (self.square_width + 5)
            row = mouse_y / (self.square_width + 5)
            bad_drag = self.squares[(self.board_width * row) + col].click_action(dragging_piece)
            if(bad_drag):
                return False
            else:
                return True
        else:
            return False
    
class Square():

    EMPTY = 0

    def __init__(self, square_number, board):
        self.square_num = square_number
        self.board = board
        self.width = self.board.square_width
        row = self.square_num / self.board.board_width
        col = self.square_num % self.board.board_width
        self.position = ((self.width + 5) * col, (self.width + 5) * row)
        self.surface = pygame.Surface((self.width, self.width))
        self.surface.fill(GREEN)
        self.piece = Square.EMPTY

    def get_val(self):
        pass

    def set_val(self):
        pass

    def get_location(self):
        return self.position

    def get_square_surface(self):
        return self.surface

    def click_action(self, piece_num):
        if(self.piece == Square.EMPTY):
            raw_piece = pygame.image.load("Quarto_Pieces/Shadowed/Piece_"+str(piece_num)+".png") #for 3d use jpg
            self.piece = pygame.transform.scale(raw_piece, (self.width, self.width))
            self.surface.blit(self.piece, (0, 0))
            return False
        else:
            return True

class Piece_Holder():

    NO_CLICK = 7
    DONE_MOVING = -2
    RETURN_STEPS = 30
    PIECE_WIDTH = 69

    def __init__(self, position, board):
        self.board = board
        self.position = position
        self.surface = pygame.Surface(((Piece_Holder.PIECE_WIDTH + 5) * 2, ((Piece_Holder.PIECE_WIDTH + 5) * (board.total_squares / 2)) + 5))
        self.squares = []
        for square in range(board.total_squares):
            self.squares.append(Holder_Square(square, self))
        self.holder_rect = pygame.Rect(position[0], position[1], (Piece_Holder.PIECE_WIDTH + 5) * 2, ((Piece_Holder.PIECE_WIDTH + 5) * (board.total_squares / 2)) + 5)
        self.moving_piece = Piece_Holder.DONE_MOVING
        self.moving_piece_loc = (0, 0)


    def update_holder_surface(self):
        self.surface.fill(WHITE)
        #pygame.draw.rect(self.surface, BLACK, (0, 0, (Piece_Holder.PIECE_WIDTH + 5) * 2, ((Piece_Holder.PIECE_WIDTH + 5) * (self.board.total_squares / 2)) + 5), 5)
        for square in self.squares:
            square_surf = square.get_square_surface()
            self.surface.blit(square_surf, square.position)
        return self.surface
        

    def draw_holder(self):
        self.surface = self.update_holder_surface()
        MAIN_SURF.blit(self.surface, self.position)


    def check_for_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.holder_rect.collidepoint([mouse_x, mouse_y]):
            mouse_x -= self.position[0]
            mouse_y -= self.position[1]
            col = mouse_x / ((Piece_Holder.PIECE_WIDTH + 5))
            row = mouse_y / ((Piece_Holder.PIECE_WIDTH + 5))
            clicked_piece = self.squares[(row * 2) + col].click_action()
            if(clicked_piece == Holder_Square.EMPTY):
                return (Piece_Holder.NO_CLICK, 0)
            else:
                return (clicked_piece, (row * 2) + col)
        else:
            return (Piece_Holder.NO_CLICK, 0)

    def put_piece_back(self, piece, location):
        self.moving_piece = piece
        self.moving_piece_loc = location
        destination_x, destination_y = self.squares[piece].position
        final_destination = (destination_x + self.position[0], destination_y + self.position[1])
        delta_x = location[0] - final_destination[0]
        delta_y = location[1] - final_destination[1]
        x_vals = []
        y_vals = []
        for step in range(Piece_Holder.RETURN_STEPS):
            x_vals.append(delta_x / Piece_Holder.RETURN_STEPS)
            y_vals.append(delta_y / Piece_Holder.RETURN_STEPS)
        for x in range(delta_x % Piece_Holder.RETURN_STEPS):
            x_vals[x] += 1
        for y in range(delta_y % Piece_Holder.RETURN_STEPS):
            y_vals[y] += 1
        return (x_vals, y_vals)

    def piece_returned(self):
        self.squares[self.moving_piece].returned()
        self.moving_piece = Piece_Holder.DONE_MOVING

class Holder_Square():

    EMPTY = -1

    def __init__(self, square_number, piece_holder):
        self.square_num = square_number
        self.holder = piece_holder
        self.position = ((self.square_num % 2) * (Piece_Holder.PIECE_WIDTH + 5),
                         ((self.square_num / 2) * (Piece_Holder.PIECE_WIDTH + 5)) + 5)
        self.surface = pygame.Surface(((Piece_Holder.PIECE_WIDTH + 2), (Piece_Holder.PIECE_WIDTH + 2)))
        if(self.square_num != 15):
            raw_piece = pygame.image.load("Quarto_Pieces/Shadowless/Piece_"+str(self.square_num)+".png")
            self.primary_piece = pygame.transform.scale(raw_piece, (Piece_Holder.PIECE_WIDTH, Piece_Holder.PIECE_WIDTH))
            self.piece = self.primary_piece
        else:
            self.primary_piece = Holder_Square.EMPTY
            self.piece = self.primary_piece
        
    def get_piece(self):
        return self.piece

    def set_piece(self, piece):
        self.piece = piece

    def get_square_surface(self):
        self.surface.fill(WHITE)
        pygame.draw.rect(self.surface, BLACK, (0, 0, (Piece_Holder.PIECE_WIDTH + 2),
                                               (Piece_Holder.PIECE_WIDTH + 2)), 5)
        if (self.piece != Holder_Square.EMPTY):
            self.surface.blit(self.piece, (1, 1))
        return self.surface

    def click_action(self):
        place_holder = self.piece
        self.piece = Holder_Square.EMPTY
        return place_holder

    def returned(self):
        self.piece = self.primary_piece

class Next_Piece_Box():

    def __init__(self, position):
        self.position = position
        self.surface = pygame.Surface((Piece_Holder.PIECE_WIDTH + 2, Piece_Holder.PIECE_WIDTH + 2))
        raw_piece = pygame.image.load("Quarto_Pieces/Shadowless/Piece_15.png")
        self.piece = pygame.transform.scale(raw_piece, (Piece_Holder.PIECE_WIDTH, Piece_Holder.PIECE_WIDTH))
        self.square_rect = pygame.Rect(position[0], position[1], Piece_Holder.PIECE_WIDTH + 2, Piece_Holder.PIECE_WIDTH + 2)
        self.piece_num = 15

    def get_current_piece(self):
        return self.piece

    def update_box_surface(self):
        self.surface.fill(WHITE)
        pygame.draw.rect(self.surface, BLACK, (0, 0, (Piece_Holder.PIECE_WIDTH + 2),
                                               (Piece_Holder.PIECE_WIDTH + 2)), 5)
        if(self.piece != Holder_Square.EMPTY):
            self.surface.blit(self.piece, (1, 1))
        return self.surface

    def draw_box(self):
        self.surface = self.update_box_surface()
        MAIN_SURF.blit(self.surface, self.position)

    def check_for_click(self, piece_num):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.square_rect.collidepoint([mouse_x, mouse_y]):
            if(self.piece != Holder_Square.EMPTY):
                place_holder = (self.piece, self.piece_num)
                self.piece = Holder_Square.EMPTY
                self.piece_num = Holder_Square.EMPTY
                return place_holder
            else:
                self.on_mouse_drop(piece_num)
        else:
            return (Piece_Holder.NO_CLICK, 0)

    def on_mouse_drop(self, piece_num):
        self.piece_num = piece_num
        raw_piece = pygame.image.load("Quarto_Pieces/Shadowless/Piece_"+str(piece_num)+".png")
        self.piece = pygame.transform.scale(raw_piece, (Piece_Holder.PIECE_WIDTH, Piece_Holder.PIECE_WIDTH))
        self.surface.blit(self.piece, (1, 1))
            

my_board = Board((350, 88), 4, 100)
my_piece_holder = Piece_Holder((10, 0), my_board)
my_next_piece_box = Next_Piece_Box((200, 250))
dragging_piece = False
piece_moving = False
piece_num = -1

def mouse_button_down():
    global piece_moving, dragging_piece, piece_clicked, piece_num
    
    if(not piece_moving):
        if(my_next_piece_box.get_current_piece() == Holder_Square.EMPTY):
            piece_clicked, piece_num = my_piece_holder.check_for_click()
            if(piece_clicked != Piece_Holder.NO_CLICK):
                dragging_piece = True
        else:
            piece_clicked, piece_num = my_next_piece_box.check_for_click(piece_num)
            if(piece_clicked != Piece_Holder.NO_CLICK):
                dragging_piece = True

def do_event_fetch():
    while True: # main game loop
        MAIN_SURF.fill(WHITE)
        my_board.draw_board()
        my_piece_holder.draw_holder()
        my_next_piece_box.draw_box()
        
        for event in pygame.event.get():
            if(event.type == QUIT):
                return "Quit"
                #pygame.quit()
                #sys.exit()
            elif(event.type == KEYDOWN):
                #key_map = pygame.key.get_pressed()
                return key_map
            elif(event.type == MOUSEBUTTONDOWN):
                #mouse_button_down()
                return MOUSEBUTTONDOWN
            elif(event.type == MOUSEBUTTONUP):
                return MOUSEBUTTONUP

while True: # main game loop
    MAIN_SURF.fill(WHITE)
    my_board.draw_board()
    my_piece_holder.draw_holder()
    my_next_piece_box.draw_box()
    
    for event in pygame.event.get():
        if(event.type == QUIT):
            pygame.quit()
            sys.exit()
        elif(event.type == KEYDOWN):
            key_map = pygame.key.get_pressed()
        elif(event.type == MOUSEBUTTONDOWN):
            mouse_button_down()
        elif(event.type == MOUSEBUTTONUP):
            if(dragging_piece):
                dragging_piece = False
                piece_dropped_on_board = my_board.check_for_mouse(piece_num)
                if(not piece_dropped_on_board):
                    piece_moving = True
                    piece_path = my_piece_holder.put_piece_back(piece_num, pygame.mouse.get_pos())
                    piece_location = pygame.mouse.get_pos()

    if(dragging_piece):
        MAIN_SURF.blit(piece_clicked, pygame.mouse.get_pos())
    elif(piece_moving):
        if(len(piece_path[0]) == 0):
            piece_moving = False
            my_piece_holder.piece_returned()
        else:
            current_change = (piece_path[0].pop(0), piece_path[1].pop(0))
            new_location = (piece_location[0] - current_change[0], piece_location[1] - current_change[1])
            piece_location = new_location
            MAIN_SURF.blit(piece_clicked, piece_location)
    pygame.display.update()
