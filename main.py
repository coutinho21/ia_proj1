import pygame
import random
from utils import *
from math import *
from hexagon import Hexagon
from piece import Piece
from state import GameState
from button import Button
from tree import Tree
from tree import Node

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
pi2 = 2 * 3.14

blue_color = (37,29,169)
red_color = (230,0,0)

#   GOAL CELL - The marked cell on the opposite side of the board.
# 	BLOCKED STONE - A stone adjacent to an enemy stone.
# 	TURN - At each turn, each player must move one of his non-blocked stones:
# 	A stone may move to an adjacent empty cell or jump over a line of friendly stones landing on the immediate next cell. It that cell is occupied by an enemy stone, that stone is captured.
# 	A stone cannot move into the opponent's goal cell.
# 	GOAL - Wins the player that moves a stone into his own goal cell or stalemates the opponent. 


radius = 45
width = sqrt(3) * (radius)
height = 2 * radius
hexagons = []
blue_pieces = []
red_pieces = []
blue_score = 0
red_score = 0
state = GameState.MENU
gamegoing = False


def initBoard():
    temp = 0
    counter = 0
    for j in range(5,9):
        for i in range(j):
            hexagons.append(Hexagon(screen, 'black', radius, pygame.Vector2(screen.get_width() / 2 + width*i - width * (j/2 - 0.5), screen.get_height() / 2 + ((height/4)*3)*temp - 3 * height),counter))
            counter += 1
        temp += 1
    for j in range(9, 4, -1):
        for i in range(j):
            hexagons.append(Hexagon(screen, 'black', radius, pygame.Vector2(screen.get_width() / 2 + width*i - width * (j/2 - 0.5), screen.get_height() / 2 + ((height/4)*3)*temp - 3 * height),counter))
            counter += 1
        temp += 1
    

def drawBoard():
        for i in range(len(hexagons)):
            if(i == 26) : 
                hexagons[i].base = red_color
            if(i == 34) :
                hexagons[i].base = blue_color
            hexagons[i].draw(hexagons[i].Surface ,hexagons[i].color, hexagons[i].radius, hexagons[i].position)
            font = pygame.font.Font(None, 15)
            text = font.render(str(i+1), 1, (10, 10, 10))
            hexagons[i].Surface.blit(text, (hexagons[i].position.x - 27, hexagons[i].position.y - 27))



def piecesInit():
    i1 = 0
    j1 = 4
    k1 = 5
    i2 = 35
    j2 = 42
    k2 = 8
    while i1 < 19 and j1 < 26:
        blue_pieces.append(Piece(hexagons[i1].position, blue_color, i1))
        red_pieces.append(Piece(hexagons[j1].position, red_color, j1))
        i1 += k1
        j1 += k1 + 1
        k1 += 1

    blue_pieces.append(Piece(hexagons[27].position, blue_color,27))
    red_pieces.append(Piece(hexagons[33].position, red_color,33))

    while i2 < 57 and j2 < 61:
        blue_pieces.append(Piece(hexagons[i2].position, blue_color, i2))
        red_pieces.append(Piece(hexagons[j2].position, red_color, j2))
        i2 += k2
        j2 += k2 - 1
        k2 -= 1


def drawPieces():
    for j in range(len(blue_pieces)):
        Piece.draw(blue_pieces[j],screen)
    for i in range(len(red_pieces)):
        Piece.draw(red_pieces[i],screen)


def getNearbyHexagons(piece):
    if piece == None:
        return None
    nearby_hexagons = []
    for hexagon in hexagons:
        if (hexagon.distance_to(piece) <= 2 * radius) and (hexagon.pos_n != piece.pos_n):
            nearby_hexagons.append(hexagon)
    return nearby_hexagons


def checkIfCanJumpOver(piece, hexagon, same_color_p, other_color_p):
    if hexagon == None:
        return False
    
    if piece == None:
        if hexagon == None or piece == None:
            return False
        elif hexagon.position.x == piece.position.x and hexagon.position.y == piece.position.y:
            return True
        return False
    
    if piece in other_color_p:
        if hexagon.position.x == piece.position.x and hexagon.position.y == piece.position.y:
            return True
        return False
    
    goalPiece = getPieceByPos(hexagon.pos_n)
    if goalPiece in same_color_p:
        return False

    best_hex = None
    vector = pygame.Vector2(hexagon.position.x - piece.position.x, hexagon.position.y - piece.position.y)
    if vector.length() == 0:
        return False
    vectorDirection = vector.normalize()


    for hex in getNearbyHexagons(piece):
        if hex == None:
            continue

        vector2 = pygame.Vector2(hex.position.x - piece.position.x, hex.position.y - piece.position.y)
        vectorDirection2 = vector2.normalize()


        if vectorDirection2 == vectorDirection:
            best_hex = hex
            break
    
    if best_hex == None:
        return False

    new_near_piece = getPieceByPos(best_hex.pos_n)
    nearby_goal = getNearbyHexagons(hexagon)
    

    if best_hex in nearby_goal:
        if new_near_piece in same_color_p:
            return True
        else:
            return False

    return checkIfCanJumpOver(new_near_piece, hexagon, same_color_p, other_color_p)


def checkBlockChange(piece):
    hexagons = getNearbyHexagons(piece)
    for hex in hexagons:
        piece = getPieceByPos(hex.pos_n)
        if piece != None:
            if piece.color == red_color:
                checkBlock(piece, blue_pieces)
            else:
                checkBlock(piece, red_pieces)



def movePiece(piece, nearby_hexagons, same_color_p, other_color_p):
    global state
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                for hexagon in hexagons:
                    if hexagon.is_clicked() and not piece.isBlocked:
                        if hexagon not in nearby_hexagons:
                            if checkIfCanJumpOver(piece, hexagon, same_color_p, other_color_p):
                                print(f'Jumping piece from {piece.pos_n + 1} to {hexagon.pos_n + 1}')
                                if getPieceByPos(hexagon.pos_n) != None:
                                    other_color_p.remove(getPieceByPos(hexagon.pos_n))
                                Piece.move(piece, hexagon.pos_n, hexagon.position)
                                checkBlockChange(piece)
                                if hexagon.base == other_color_p[0].color :
                                    print('That is not your base')
                                    return False
                                elif hexagon.base == piece.color:
                                    if piece.color == red_color:
                                        print('You win')
                                        state = GameState.RED_WON
                                    elif piece.color == blue_color:
                                        print('You win')
                                        state = GameState.BLUE_WON
                                    
                                    Piece.move(piece, hexagon.pos_n, hexagon.position)
                                    return True
                                
                                return True
                            else:
                                print('Cannot make that move')
                                return False
                check = False
                for hexagon in nearby_hexagons:
                    if hexagon.is_clicked():
                        if piece.isBlocked:
                            print(f'Piece {piece.pos_n + 1} is blocked')
                            return False
                        check = True
                        for p in same_color_p:
                            if p.pos_n == hexagon.pos_n:
                                print('There is already a piece in that position')
                                return False
                            elif hexagon.base == other_color_p[0].color :
                                print('That is not your base')
                                return False
                            elif hexagon.base == piece.color:
                                if piece.color == red_color:
                                    print('You win')
                                    state = GameState.RED_WON
                                elif piece.color == blue_color:
                                    print('You win')
                                    state = GameState.BLUE_WON
                                
                                Piece.move(piece, hexagon.pos_n, hexagon.position)
                                return True
                            
                        for p in other_color_p:
                            if p.pos_n == hexagon.pos_n:
                                print('There is an enemy piece in that position')
                                return False
                        print(f'Moving piece from {piece.pos_n + 1} to {hexagon.pos_n + 1}')
                        Piece.move(piece, hexagon.pos_n, hexagon.position)
                        return True
                if check == False:
                    print('Else was clicked')
                    return False
                break







def getHexagonByPos(pos):
        for hexagon in hexagons:
            if hexagon.pos_n == pos:
                return hexagon
        return None

def getPieceByPos(pos):
    for piece in blue_pieces:
        if piece.pos_n == pos:
            return piece
    for piece in red_pieces:
        if piece.pos_n == pos:
            return piece
    return None


def checkBlock(piece, other_color_p):
    flag = False
    for p in other_color_p:
        hexagon = getHexagonByPos(piece.pos_n)
        if hexagon in getNearbyHexagons(p):
            piece.isBlocked = True
            p.isBlocked = True
            flag = True

    if not flag:
        piece.isBlocked = False
    

def checkIfWon(pieces):
    for piece in pieces:
        if not piece.isBlocked:
            return False
    return True


def play(ai):
    global turn
    global running
    global state
    global blue_pieces
    global red_pieces
    

    menuButton = Button((screen.get_width() - 160, screen.get_height()-50), (192,157,89), 'Go back to Menu', (160, 50), GameState.MENU)
    

    screen.fill((220,190,131))
    drawBoard()
    drawPieces()
    menuButton.draw(screen)


    if turn == blue_color:
        drawText(screen, "Blue's turn", blue_color, 40, 150, 100)
    else:
        drawText(screen, "Red's turn", red_color, 40, 150, 100)
        
    if checkIfWon(blue_pieces):
            state = GameState.RED_WON
            return

    if checkIfWon(red_pieces):
            state = GameState.BLUE_WON
            return

    # linha a meio do ecra
    # pygame.draw.line(screen, 'green', (0,screen.get_height() / 2), (screen.get_width(), screen.get_height() / 2))
    if turn != ai:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menuButton.is_clicked():
                    state = menuButton.action
                    break
                if turn == blue_color:
                    for piece in blue_pieces:
                        if piece.is_clicked() and not piece.isBlocked:
                            pygame.draw.circle(screen, blue_color, piece.position, 30)
                            pygame.display.flip()
                            nearby_hexagons = getNearbyHexagons(piece)
                            change_turn = movePiece(piece, nearby_hexagons, blue_pieces, red_pieces)
                            if change_turn and state == GameState.PvsAI:
                                checkBlock(piece, red_pieces)
                                turn = red_color
                                print('Changed turn to red')
                            elif state == GameState.BLUE_WON:
                                print('Blue won')
                            
                            break

                elif turn == red_color:
                    if checkIfWon(red_pieces):
                        state = GameState.BLUE_WON
                        return
                    for piece in red_pieces:
                        if piece.is_clicked() and not piece.isBlocked:
                            pygame.draw.circle(screen, red_color, piece.position, 30)
                            pygame.display.flip()
                            nearby_hexagons = getNearbyHexagons(piece)
                            change_turn = movePiece(piece, nearby_hexagons, red_pieces, blue_pieces)
                            if change_turn and state == GameState.PvsAI:
                                checkBlock(piece, blue_pieces)
                                turn = blue_color
                                print('Changed turn to blue')
                            elif state == GameState.RED_WON:
                                print('Red won')
                            
                            break

    elif turn == ai: 
        
        pieces_state = copyState()
        blue_pieces_copy = pieces_state[0]
        red_pieces_copy = pieces_state[1]

        if ai == blue_color:
            minimax_result = minimax(blue_color, blue_pieces_copy, red_pieces_copy, 0)
            piece_to_move = minimax_result[0]
            hexagon_to_move = minimax_result[1]
            
            print(f'Moving piece from {piece_to_move.pos_n + 1} to {hexagon_to_move.pos_n + 1}')
            Piece.move(piece_to_move, hexagon_to_move.pos_n, hexagon_to_move.position)
            checkBlockChange(piece_to_move)
            if hexagon_to_move.base == blue_color:
                state = GameState.BLUE_WON
            turn = red_color
            print('Changed turn to red - ended AI turn')
            

        else:
            # minimax_result = minimax(red_color, blue_pieces_copy, red_pieces_copy, 0)
            # piece_to_move = minimax_result[0]
            # hexagon_to_move = minimax_result[1]
            
            # print(f'Moving piece from {piece_to_move.pos_n + 1} to {hexagon_to_move.pos_n + 1}')
            # Piece.move(piece_to_move, hexagon_to_move.pos_n, hexagon_to_move.position)
            # checkBlockChange(piece_to_move)
            # if hexagon_to_move.base == red_color:
            #     state = GameState.RED_WON
            tree = buildTreeMiniMax(red_color, blue_pieces_copy, red_pieces_copy, 3)
            print(tree)
            turn = blue_color
            print('Changed turn to blue - ended AI turn')
             




def minimax(color, blue_pieces_copy, red_pieces_copy, depth):
    global blue_pieces
    global red_pieces
    best_score = -1000
    piece_to_move = None
    hexagon_to_move = None
    
    if(color == blue_color):
        same_color_p = blue_pieces
        other_color_p = red_pieces
    else:
        same_color_p = red_pieces
        other_color_p = blue_pieces
   
    moves = getAllPossibleMoves(color)
    
    for move in moves:
        piece = move[1]
        new_piece = Piece(piece.position, piece.color, piece.pos_n, piece.selected, piece.isBlocked)
        hexagon = move[0]
        Piece.move(piece, hexagon.pos_n, hexagon.position)
        checkBlockChange(piece)
        evaluateGame()
        score = getTeamScore(same_color_p)
        if score > best_score:
            best_score = score
            piece_to_move = new_piece
            hexagon_to_move = hexagon

        
        blue_pieces = blue_pieces_copy
        red_pieces = red_pieces_copy
        

    for p in red_pieces_copy:
        if p.pos_n == piece_to_move.pos_n:
            piece_to_move = p
    
    return piece_to_move, hexagon_to_move


def buildTreeMiniMax(color, blue_pieces_copy, red_pieces_copy, depth):
    nodes = []
    global blue_pieces
    global red_pieces
    tree = Tree(nodes)
    if(color == blue_color):
        same_color_p = blue_pieces
        other_color_p = red_pieces
    else:
        same_color_p = red_pieces
        other_color_p = blue_pieces

    moves = getAllPossibleMoves(color)
    for move in moves:
        nodes.append(evolveMove(depth, move, same_color_p, other_color_p, True))


    blue_pieces = blue_pieces_copy
    red_pieces = red_pieces_copy
    
    print_tree(tree.nodes[0])
    return tree



def print_tree(node, depth=0):
    if node is None:
        return
    print("  " * depth + f"Depth: {depth}, Value: {node.value}, Type: {node.type}, Data: {node.data[0].pos_n + 1} -> {node.data[1].pos_n + 1}")
    if node.children:
        for child in node.children:
            print_tree(child, depth + 1)


def evolveMove(depth, move, same_color_p, other_color_p, Maximizing):
        node = Node(None, None, None, None)
        print(f'Depth: {depth}')
       
        if Maximizing:
            type = 'Max'
        else:
            type = 'Min'

        if depth == 0:
            return None
        
        piece = move[1]
        new_piece = Piece(piece.position, piece.color, piece.pos_n, piece.selected, piece.isBlocked)
        hexagon = move[0]
        data = (new_piece, hexagon)

        Piece.move(piece, hexagon.pos_n, hexagon.position)
        checkBlockChange(piece)
        evaluateGame()
        score = getTeamScore(same_color_p)
        print(score)

        node_children = []

        for move in getAllPossibleMoves(other_color_p[0].color):
            child_node = evolveMove(depth - 1, move, other_color_p, same_color_p, not Maximizing)
            node_children.append(child_node)

        node = Node(score, data, node_children, type)

        return node
        

    




def winStates():
    global state
    global gamegoing
    


    pygame.draw.rect(screen, (220,190,131), (0,0,300,200))
    if state == GameState.RED_WON:
        color = red_color
        drawText(screen, "Red won", (184,20,20), 80, screen.get_width() / 2, screen.get_height() / 2 - 200)
    elif state == GameState.BLUE_WON:
        color = blue_color
        drawText(screen, "Blue won", (11,11,100), 80, screen.get_width() / 2, screen.get_height() / 2 - 200)

    initGame()
    gamegoing = False

    menuButton = Button((screen.get_width() / 2 , screen.get_height() / 2 - 30), color, 'Menu', (60, 60),GameState.MENU, 32,'hexagon')
    quitButton = Button((screen.get_width() / 2 - 54, screen.get_height() / 2 + 60), color, 'Quit', (60, 60), GameState.QUIT, 32, 'hexagon')
    playAgainButton = Button((screen.get_width() / 2 + 52, screen.get_height() / 2 + 62), color, 'Replay', (60, 60), GameState.PvsAI, 32, 'hexagon')
    menuButton.draw(screen)
    quitButton.draw(screen)
    playAgainButton.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is within the menu area
            if menuButton.is_clicked():
                state = menuButton.action   
            # Check if the mouse click is within the quit area
            if quitButton.is_clicked():
                state = quitButton.action
            if playAgainButton.is_clicked():
                state = playAgainButton.action
                initGame()
                gamegoing = True
                break

def menu():
    global state
    global gamegoing
    screen.fill((220,190,131))
    drawText(screen, "ABOYNE", 'black', 80, screen.get_width() / 2, 150)
    playButton = Button((screen.get_width() / 2 , screen.get_height() / 2 - 30), (192,157,89), 'Play', (60, 60),GameState.PvsAI, 32,'hexagon')
    quitButton = Button((screen.get_width() / 2 - 54, screen.get_height() / 2 + 60), (192,157,89), 'Quit', (60, 60), GameState.QUIT, 32, 'hexagon')
    rulesButton = Button((screen.get_width() / 2 + 52, screen.get_height() / 2 + 62), (192,157,89), 'Rules', (60, 60), GameState.RULES, 32, 'hexagon')
    if gamegoing:
        resumeButton = Button((screen.get_width() / 2, screen.get_height() / 2 + 151), (192,157,89), 'Resume', (60, 60), GameState.PvsAI, 32, 'hexagon')
        resumeButton.draw(screen)

    playButton.draw(screen)
    quitButton.draw(screen)
    rulesButton.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if playButton.is_clicked():
                state = playButton.action
                initGame()
                gamegoing = True

            elif quitButton.is_clicked():
                state = quitButton.action

            elif rulesButton.is_clicked():
                state = rulesButton.action

            elif gamegoing and resumeButton.is_clicked():
                state = resumeButton.action

def rules():
    global state
    screen.fill((220,190,131))
    drawText(screen, "ABOYNE", 'black', 80, screen.get_width() / 2, 150)
    drawText(screen, "Rules", 'black', 40, screen.get_width() / 2, 250)
    drawText(screen, "GOAL CELL - The marked cell on the opposite side of the board.", 'black', 30, screen.get_width() / 2, 300)
    drawText(screen, "BLOCKED STONE - A stone adjacent to an enemy stone.", 'black', 30, screen.get_width() / 2, 330)
    drawText(screen, "TURN - At each turn, each player must move one of his non-blocked stones:", 'black', 30, screen.get_width() / 2, 360)
    drawText(screen, "A stone may move to an adjacent empty cell or jump over a line of friendly stones landing on the immediate next cell.", 'black', 30, screen.get_width() / 2, 390)
    drawText(screen, "If that cell is occupied by an enemy stone, that stone is captured.", 'black', 30, screen.get_width() / 2, 415)
    drawText(screen, "A stone cannot move into the opponent's goal cell.", 'black', 30, screen.get_width() / 2, 440)
    drawText(screen, "GOAL - Wins the player that moves a stone into his own goal cell or stalemates the opponent.", 'black', 30, screen.get_width() / 2, 470)
    menuButton = Button((screen.get_width() / 2 , screen.get_height() / 2 + 220), (192,157,89), 'Menu', (60, 60),GameState.MENU, 32,'hexagon')
    menuButton.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menuButton.is_clicked():
                state = menuButton.action
                break



def evaluateGame():
    all_pieces = blue_pieces + red_pieces
    for piece in all_pieces:
        if not piece.isBlocked:
            piece.score = 3
        else:
            piece.score = 1

def getTeamScore(pieces):
    score = 0
    for piece in pieces:
        score += piece.score
    return score

def copyState():
    blue_pieces_copy = []
    red_pieces_copy = []
    for piece in blue_pieces:
        blue_pieces_copy.append(Piece(piece.position, piece.color, piece.pos_n, piece.selected, piece.isBlocked))
    for piece in red_pieces:
        red_pieces_copy.append(Piece(piece.position, piece.color, piece.pos_n, piece.selected, piece.isBlocked))
    return blue_pieces_copy, red_pieces_copy

def getAllPossibleMoves(color):
    possible_moves = []

    if color == blue_color:
        same_color_p = blue_pieces
        other_color_p = red_pieces
    else:
        same_color_p = red_pieces
        other_color_p = blue_pieces

    for piece in same_color_p:

        nearby_hexagons = getNearbyHexagons(piece)
        for hexagon in nearby_hexagons:
            if not piece.isBlocked:
                occupied = False
                for p in same_color_p:
                    if p.pos_n == hexagon.pos_n:
                        occupied = True
                        break
                for p in other_color_p:
                    if p.pos_n == hexagon.pos_n:
                        occupied = True
                        break
                if not occupied:
                    if hexagon.base == other_color_p[0].color:
                        break
                    possible_moves.append((hexagon, piece))
        for hexagon in hexagons:
            if checkIfCanJumpOver(piece, hexagon, same_color_p, other_color_p):
                if hexagon.base == other_color_p[0].color:
                    break
                possible_moves.append((hexagon,piece))

    return possible_moves

             

        
def cleanGame():
    hexagons.clear()
    blue_pieces.clear()
    red_pieces.clear()


def initGame():
    cleanGame()
    initBoard()
    piecesInit()

    random.seed()
    global turn
    if random.randint(0, 1) == 0:
        turn = red_color
    else:
        turn = blue_color




def randomizeAI():
    # if random.randint(0, 1) == 0:
    #     return red_color
    # return blue_color
    return red_color
    




##
##    MAIN LOOP
##   
        
initGame()
ai = randomizeAI()

while running:
    if state == GameState.MENU:
        menu()

    elif state == GameState.PvsP:
        play(None)
    elif state == GameState.PvsAI:
        #escolher cor e dificuldade
        #PvsAI_play(player_color, difficulty)
        play(ai)
    elif state == GameState.RED_WON or state == GameState.BLUE_WON:
        winStates()
    elif state == GameState.RULES:
        rules()
    elif state == GameState.QUIT:
        running = False
        pygame.quit()
        

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    pygame.display.set_caption(f'ABOYNE - {int(clock.get_fps())} FPS')