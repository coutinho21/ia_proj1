import pygame
import random
import math
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
ai_vs_ai_color = (5, 5, 5)
ai_turn = 0

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
currentModeState = None
gamegoing = False
difficulty = 1
difficulty2 = 1
currentModeDifficulty = None
d1done = False


# Creates the board
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
    

# Draws the board
def drawBoard():
        for i in range(len(hexagons)):
            if(i == 26) : 
                hexagons[i].base = red_color
            if(i == 34) :
                hexagons[i].base = blue_color
            hexagons[i].draw(hexagons[i].Surface ,hexagons[i].color, hexagons[i].radius, hexagons[i].position)
            font = pygame.font.Font(None, 15)
            text = font.render(str(i + 1), 1, (10, 10, 10))
            hexagons[i].Surface.blit(text, (hexagons[i].position.x - 27, hexagons[i].position.y - 27))


# Initializes the pieces
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


# Draws the pieces according to their current position
def drawPieces():
    for j in range(len(blue_pieces)):
        Piece.draw(blue_pieces[j],screen)
    for i in range(len(red_pieces)):
        Piece.draw(red_pieces[i],screen)

# Gets all the hexagons that are within a distance of 1 Hexagon from the piece
def getNearbyHexagons(piece):
    if piece == None:
        return None
    nearby_hexagons = []
    for hexagon in hexagons:
        if (hexagon.distance_to(piece) <= 2 * radius) and (hexagon.pos_n != piece.pos_n):
            nearby_hexagons.append(hexagon)
    return nearby_hexagons


# Uses recursion to check if a piece can jump over another piece

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
    
    if same_color_p[0].color == blue_color:
        goalPiece = getPieceByPos(hexagon.pos_n, same_color_p, other_color_p)
    else:
        goalPiece = getPieceByPos(hexagon.pos_n, other_color_p, same_color_p)


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


    if same_color_p[0].color == blue_color:
        new_near_piece = getPieceByPos(best_hex.pos_n, same_color_p, other_color_p)
    else:
        new_near_piece = getPieceByPos(best_hex.pos_n, other_color_p, same_color_p)

    nearby_goal = getNearbyHexagons(hexagon)
    

    if best_hex in nearby_goal:
        if new_near_piece in same_color_p:
            return True
        else:
            return False

    return checkIfCanJumpOver(new_near_piece, hexagon, same_color_p, other_color_p)


# Checks if the last made move has blocked/unblocked any pieces
def checkBlockChange(piece, new_blue_pieces, new_red_pieces):
    hexagons = getNearbyHexagons(piece)
    for hex in hexagons:
        piece = getPieceByPos(hex.pos_n, new_blue_pieces, new_red_pieces)
        if piece != None:
            if piece.color == red_color:
                checkBlock(piece, new_blue_pieces)
            else:
                checkBlock(piece, new_red_pieces)


# Moce the piece to the new position after doing some checks
                
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
                                if getPieceByPos(hexagon.pos_n, blue_pieces, red_pieces) != None:
                                    other_color_p.remove(getPieceByPos(hexagon.pos_n, blue_pieces, red_pieces))
                                Piece.move(piece, hexagon.pos_n, hexagon.position)
                                checkBlockChange(piece, blue_pieces, red_pieces)
                                if hexagon.base == other_color_p[0].color:
                                    print('That is not your base')
                                    return False
                                elif hexagon.base == piece.color:
                                    if piece.color == red_color:
                                        screen.fill((220,190,131))
                                        drawBoard()
                                        drawPieces()
                                        state = GameState.RED_WON
                                    elif piece.color == blue_color:
                                        screen.fill((220,190,131))
                                        drawBoard()
                                        drawPieces()
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
                                    screen.fill((220,190,131))
                                    drawBoard()
                                    drawPieces()
                                    state = GameState.RED_WON
                                elif piece.color == blue_color:
                                    screen.fill((220,190,131))
                                    drawBoard()
                                    drawPieces()
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


# Gets the Hexagon by its position
def getHexagonByPos(pos):
        for hexagon in hexagons:
            if hexagon.pos_n == pos:
                return hexagon
        return None

# Gets the piece by its position
def getPieceByPos(pos, new_blue_pieces, new_red_pieces):
    for piece in new_blue_pieces:
        if piece.pos_n == pos:
            return piece
    for piece in new_red_pieces:
        if piece.pos_n == pos:
            return piece
    return None

# Checks if a piece is blocked by another piece
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

# Checks if a player has won by the other player having no moves left
def checkIfWon(pieces):
    for piece in pieces:
        if not piece.isBlocked:
            return False
    return True

# Main play function
# Depending on the game mode, the player can play against another player, against the AI or watch the AI play against itself
# The AI uses the minimax algorithm to make its moves and the depth of the tree its based on the difficulty of the AI
# The Player can also ask for a hint, which will show the best move the AI would make.

def play(ai, depth = 1, depth2 = 1):
    global ai_turn
    global turn
    global running
    global state
    global blue_pieces
    global red_pieces
    

    if turn == blue_color:
        hint_pos = (70, 130)
    else:
        hint_pos = (screen.get_width()-278, 130)
    menuButton = Button((screen.get_width() - 160, screen.get_height()-50), (192,157,89), 'Go back to Menu', (160, 50), GameState.MENU)
    giveMeaHintButton = Button(hint_pos, (192,157,89), 'Give me a hint!', (160, 50), None)
    

    screen.fill((220,190,131))
    drawBoard()
    drawPieces()
    menuButton.draw(screen)


    if turn != ai and ai != ai_vs_ai_color:
        giveMeaHintButton.draw(screen)
        if turn == blue_color:
            drawText(screen, "Blue's turn", blue_color, 40, 150, 100)
        else:
            drawText(screen, "Red's turn", red_color, 40, screen.get_width()-200, 100)
    elif turn == ai:
        if ai == blue_color:
            drawText(screen, "Blue AI's turn...", ai, 40, 180, 100)
        if ai == red_color:
            drawText(screen, "Red AI's turn...", ai, 40, screen.get_width()-200, 100)
    elif ai == ai_vs_ai_color:
        if turn == blue_color:
            drawText(screen, "Blue AI's turn...", blue_color, 40, 180, 100)
        if turn == red_color:
            drawText(screen, "Red AI's turn...", red_color, 40, screen.get_width()-200, 100)
    
    pygame.display.flip()


    if checkIfWon(blue_pieces):
        state = GameState.RED_WON
        return

    if checkIfWon(red_pieces):
        state = GameState.BLUE_WON
        return



    if turn != ai and ai != ai_vs_ai_color:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menuButton.is_clicked():
                    state = menuButton.action
                    break
                if giveMeaHintButton.is_clicked():
                    copy = copyState()
                    blue_pieces_copy = copy[0]
                    red_pieces_copy = copy[1]
                    tree = buildTreeMiniMax(turn, blue_pieces_copy, red_pieces_copy, 1  )
                    piece_to_move, hexagon_to_move = minimax(tree)
                    print(f'Piece to move: {piece_to_move.pos_n + 1} to {hexagon_to_move.pos_n + 1}')
                    showHint(piece_to_move, hexagon_to_move, turn)

                    break
                if turn == blue_color:
                    if checkIfWon(blue_pieces):
                        state = GameState.RED_WON
                        return
                    for piece in blue_pieces:
                        if piece.is_clicked() and not piece.isBlocked:
                            pygame.draw.circle(screen, blue_color, piece.position, 30)
                            pygame.display.flip()
                            nearby_hexagons = getNearbyHexagons(piece)
                            change_turn = movePiece(piece, nearby_hexagons, blue_pieces, red_pieces)
                            if change_turn and (state == GameState.PvsP or state == GameState.PvsAI):
                                checkBlock(piece, red_pieces)
                                turn = red_color
                                print('Changed turn to red')
                            elif state == GameState.BLUE_WON:
                                screen.fill((220,190,131))
                                drawBoard()
                                drawPieces()
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
                            if change_turn and (state == GameState.PvsP or state == GameState.PvsAI):
                                checkBlock(piece, blue_pieces)
                                turn = blue_color
                                print('Changed turn to blue')
                            elif state == GameState.RED_WON:
                                screen.fill((220,190,131))
                                drawBoard()
                                drawPieces()
                                print('Red won')
                            
                            break

    elif turn == ai:
        copy = copyState()

        blue_pieces_copy = copy[0]
        red_pieces_copy = copy[1]

        tree = buildTreeMiniMax(ai, blue_pieces_copy, red_pieces_copy, depth)
        piece_to_move, hexagon_to_move = minimax(tree)
        moveAIPiece(piece_to_move, hexagon_to_move)


    elif ai == ai_vs_ai_color:

        copy = copyState()
        blue_pieces_copy = copy[0]
        red_pieces_copy = copy[1]

        if ai_turn == 0:
            tree = buildTreeMiniMax(turn, blue_pieces_copy, red_pieces_copy, depth)
            piece_to_move, hexagon_to_move = minimax(tree)
            moveAIPiece(piece_to_move, hexagon_to_move)
            ai_turn = 1

        else:
            tree = buildTreeMiniMax(turn, blue_pieces_copy, red_pieces_copy, depth2)
            piece_to_move, hexagon_to_move = minimax(tree)
            moveAIPiece(piece_to_move, hexagon_to_move)
            ai_turn = 0
 

# Draws the hint
def showHint(piece, hexagon, turn):
    
    if turn == red_color:
        new_color = (128, 0, 0)
        arrow_color = (255, 20, 147)
    else:
        new_color = (19, 15, 87)
        arrow_color = (132, 223, 239)
    pygame.draw.circle(screen, new_color , hexagon.position, 25)
    
    # Draw an arrow from piece to hexagon
    dx = hexagon.position[0] - piece.position[0]
    dy = hexagon.position[1] - piece.position[1]
    angle = math.atan2(dy, dx)
    length = math.sqrt(dx*dx + dy*dy)
    arrow_length = 30  # or whatever you want
    arrow_angle = math.pi / 6  # or whatever you want
    end_point = (piece.position[0] + length * math.cos(angle), piece.position[1] + length * math.sin(angle))
    pygame.draw.line(screen, arrow_color, piece.position, end_point, 2)
    
    # Draw a filled triangle for the arrowhead
    arrowhead_points = [
        end_point,
        (end_point[0] - arrow_length * math.cos(angle + arrow_angle), end_point[1] - arrow_length * math.sin(angle + arrow_angle)),
        (end_point[0] - arrow_length * math.cos(angle - arrow_angle), end_point[1] - arrow_length * math.sin(angle - arrow_angle))
    ]
    pygame.draw.polygon(screen, arrow_color, arrowhead_points)
    
    pygame.display.flip()
    pygame.time.delay(1000)
    pygame.draw.circle(screen, (220,190,131), hexagon.position, 25)
    pygame.display.flip()


# Minimax algorithm that returns the best move for the AI
def minimax(tree):
    global blue_pieces
    global red_pieces
    global state
    global turn


    best_score = float('-inf')
    best_set = []
    piece_to_move = None
    hexagon_to_move = None
    for node in tree.nodes:
        if node.value == best_score:
            best_set.append(node)
        elif node.value > best_score:
            best_score = node.value
            piece_to_move = node.data[0]
            hexagon_to_move = node.data[1]
            best_set = [node]

    random_data = random.choice(best_set)
    piece_to_move = random_data.data[0]
    hexagon_to_move = random_data.data[1]

    for p in red_pieces + blue_pieces:
        if p.pos_n == piece_to_move.pos_n:
            piece_to_move = p

    return piece_to_move, hexagon_to_move


# Makes the move for the AI
def moveAIPiece(piece_to_move, hexagon_to_move):
    global blue_pieces
    global red_pieces
    global state
    global turn

    Piece.move(piece_to_move, hexagon_to_move.pos_n, hexagon_to_move.position)
    checkBlockChange(piece_to_move, blue_pieces, red_pieces)


    if piece_to_move.color == red_color:
        other_color = blue_pieces
    else:
        other_color = red_pieces
    for pc in other_color:
        if pc.pos_n == hexagon_to_move.pos_n:
            other_color.remove(pc)
            checkBlockChange(piece_to_move, blue_pieces, red_pieces)
            break

    if hexagon_to_move.base == blue_color:
        screen.fill((220,190,131))
        drawBoard()
        drawPieces()
        state = GameState.BLUE_WON
        print('Blue won')
        return

    if hexagon_to_move.base == red_color:
        screen.fill((220,190,131))
        drawBoard()
        drawPieces()
        state = GameState.RED_WON
        print('Red won')
        return

    if turn == blue_color:
        turn = red_color
        print('Changed turn to red - ended AI turn')
    else:
        turn = blue_color
        print('Changed turn to blue - ended AI turn')



# Builds the tree for the minimax algorithm, using the evolveMove function
def buildTreeMiniMax(color, blue_pieces_copy, red_pieces_copy, depth):
    global blue_pieces
    global red_pieces
    nodes = []
    tree = Tree(nodes)

    if color == blue_color:
        same_color_p = blue_pieces
        other_color_p = red_pieces
    else:
        same_color_p = red_pieces
        other_color_p = blue_pieces

    moves = getAllPossibleMoves(same_color_p, other_color_p)

    for move in moves:
        nodes.append(evolveMove(color, depth, move, same_color_p, other_color_p, False, float('-inf'), float('inf')))

    blue_pieces = blue_pieces_copy
    red_pieces = red_pieces_copy

    with open('output.txt', 'w') as f:
        for node in nodes:
            f.write(print_tree(node))

    return tree


# Prints the tree
def print_tree(node, depth=0):
    output = ' ' * depth + 'Depth: ' + str(depth) + ' Value: ' + str(node.value) + ' Type: ' + str(node.type) + ' Data: ' + str(node.data[0].pos_n + 1 ) + ' to '  + str(node.data[1].pos_n + 1 ) + '\n'
    for child in node.children:
        output += print_tree(child, depth + 1)
    return output


# Recursively builds the tree for the minimax algorithm, evaluating the state of the deepest nodes
def evolveMove(ai_color, depth, move, same_color_p, other_color_p, Maximizing, alpha, beta):
    node = Node(None, None, None, None)

    if Maximizing:
        type = 'Max'
    else:
        type = 'Min'

    piece = move[1]
    new_piece = Piece(piece.position, piece.color, piece.pos_n, piece.selected, piece.isBlocked)
    hexagon = move[0]
    data = (new_piece, hexagon)


    new_same_color_p = []
    new_other_color_p = []

    for mock_piece in same_color_p:
        new_same_color_p.append(Piece(mock_piece.position, mock_piece.color, mock_piece.pos_n, mock_piece.selected, mock_piece.isBlocked))
    for mock_piece in other_color_p:
        new_other_color_p.append(Piece(mock_piece.position, mock_piece.color, mock_piece.pos_n, mock_piece.selected, mock_piece.isBlocked))



    # Find the piece in the new game state and move it
    for p in new_same_color_p:
        if p.pos_n == piece.pos_n:
            Piece.move(p, hexagon.pos_n, hexagon.position)
            
            for p2 in new_other_color_p:
                if p2.pos_n == hexagon.pos_n:
                    new_other_color_p.remove(p2)
                    break

            if same_color_p[0].color == blue_color:
                checkBlockChange(p, new_same_color_p, new_other_color_p)
            else:
                checkBlockChange(p, new_other_color_p, new_same_color_p)
            break


    if depth == 0:
        if same_color_p[0].color == blue_color:
            evaluateGame(new_same_color_p, new_other_color_p)
        else:
            evaluateGame(new_other_color_p, new_same_color_p)


        if ai_color == blue_color: # ends in MAX
            score = blue_score - red_score
        else: # ends in MIN
            score = red_score - blue_score

        node = Node(score, data, [], None)
        return node


    node_children = []
    best_score = -1000


    if Maximizing:
        best_score = float('-inf')
        value = float('-inf')
        for new_move in getAllPossibleMoves(new_other_color_p, new_same_color_p):
            child_node = evolveMove(ai_color, depth - 1, new_move, new_other_color_p, new_same_color_p, not Maximizing, alpha, beta)
            value = max(value, child_node.value)
            alpha = max(alpha, value)
            node_children.append(child_node)
            if alpha >= beta:
                break

        for child in node_children:
            if child.value > best_score:
                best_score = child.value

    else:
        best_score = float('inf')
        value = float('inf')
        for new_move in getAllPossibleMoves(new_other_color_p, new_same_color_p):
            child_node = evolveMove(ai_color, depth - 1, new_move, new_other_color_p, new_same_color_p, not Maximizing, alpha, beta)
            value = min(value, child_node.value)
            beta = min(beta, value)
            node_children.append(child_node)
            if beta <= alpha:
                break

        for child in node_children:
            if child.value < best_score:
                best_score = child.value
    


    node = Node(best_score, data, node_children, type)

    return node


# Evaluates the game state, updating the point of each piece, and the score of each player
# The score is based on the distance of each piece to the goal cell, and the number of blocked pieces
def evaluateGame(eval_blue_pieces, eval_red_pieces):
    global blue_score
    global red_score
    blue_score = 0
    red_score = 0

    for piece in eval_blue_pieces:
        distance_factor = (60 - int(distance_to_goal(piece)) / 10) / 3

        if not piece.isBlocked:
            piece.score = 100
            piece.score += int(distance_factor)
        else:
            piece.score = 20
            piece.score += int(distance_factor / 3)
        
        if piece.pos_n == 26:
            piece.score += float('inf')

        blue_score += piece.score

    for piece in eval_red_pieces:
        distance_factor = (60 - int(distance_to_goal(piece)) / 10) / 3
        if not piece.isBlocked:
            piece.score = 100
            piece.score += int(distance_factor)
        else:
            piece.score = 20
            piece.score += int(distance_factor / 3)

        if piece.pos_n == 34:
            piece.score += float('inf')
        
        red_score += piece.score
        

# Calculates the distance of a piece to the goal cell
def distance_to_goal(piece):
    if piece.color == blue_color:
        goal = hexagons[34]
    else:
        goal = hexagons[26]
    return goal.distance_to(piece)

# Calculates the score of a team
def getTeamScore(pieces):
    score = 0
    for piece in pieces:
        score += piece.score
    return score


# Gets all possible moves for a player
def getAllPossibleMoves(same_color_p, other_color_p):
    possible_moves = []

    for piece in same_color_p:
        if not piece.isBlocked:
            nearby_hexagons = getNearbyHexagons(piece)
            for hexagon in nearby_hexagons:
                occupied = False
                for p in same_color_p + other_color_p:
                    if p.pos_n == hexagon.pos_n:
                        occupied = True
                        break

                if not occupied:
                    if hexagon.base == other_color_p[0].color:
                        continue
                    possible_moves.append((hexagon, piece))


            for hexagon in hexagons:
                if checkIfCanJumpOver(piece, hexagon, same_color_p, other_color_p):
                    if hexagon.base == other_color_p[0].color:
                        continue
                    possible_moves.append((hexagon,piece))


    return possible_moves


# Draws the win state 
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
    playAgainButton = Button((screen.get_width() / 2 + 52, screen.get_height() / 2 + 62), color, 'Replay', (60, 60), currentModeState, 32, 'hexagon')
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

# Draws the menu State
def menu():
    global state
    global gamegoing
    screen.fill((220,190,131))
    drawText(screen, "ABOYNE", 'black', 80, screen.get_width() / 2, 150)
    playButton = Button((screen.get_width() / 2 , screen.get_height() / 2 - 30), (192,157,89), 'Play', (60, 60), GameState.GAME_MODE_MENU, 32,'hexagon')
    quitButton = Button((screen.get_width() / 2 - 54, screen.get_height() / 2 + 60), (192,157,89), 'Quit', (60, 60), GameState.QUIT, 32, 'hexagon')
    rulesButton = Button((screen.get_width() / 2 + 52, screen.get_height() / 2 + 62), (192,157,89), 'Rules', (60, 60), GameState.RULES, 32, 'hexagon')
    if gamegoing:
        resumeButton = Button((screen.get_width() / 2, screen.get_height() / 2 + 151), (192,157,89), 'Resume', (60, 60), currentModeState, 32, 'hexagon')
        resumeButton.draw(screen)

    playButton.draw(screen)
    quitButton.draw(screen)
    rulesButton.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if playButton.is_clicked():
                state = playButton.action

            elif quitButton.is_clicked():
                state = quitButton.action

            elif rulesButton.is_clicked():
                state = rulesButton.action

            elif gamegoing and resumeButton.is_clicked():
                state = resumeButton.action

# Draws the Game mode menu
def gameModeMenu():
    global state
    global gamegoing


    screen.fill((220,190,131))
    drawText(screen, "ABOYNE", 'black', 80, screen.get_width() / 2, 100)
    drawText(screen, "Choose game mode", 'black', 40, screen.get_width() / 2, 180)
    PvsPButton = Button((screen.get_width() / 2 , screen.get_height() / 2 - 80), (192,157,89), 'P vs P', (60, 60), GameState.PvsP, 32,'hexagon')
    PvsAIButton = Button((screen.get_width() / 2 - 54, screen.get_height() / 2 + 10), (192,157,89), 'P vs AI', (60, 60), GameState.PvsAI, 32, 'hexagon')
    AIvsAIButton = Button((screen.get_width() / 2 + 52, screen.get_height() / 2 + 12), (192,157,89), 'AI vs AI', (60, 60), GameState.AIvsAI, 32, 'hexagon')
    menuButton = Button((screen.get_width() / 2 , screen.get_height() / 2 + 101), (192,157,89), 'Menu', (60, 60), GameState.MENU, 32, 'hexagon')
  
    PvsPButton.draw(screen)

    PvsAIButton.draw(screen)
    

    AIvsAIButton.draw(screen)
    menuButton.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PvsPButton.is_clicked():
                state = PvsPButton.action
                initGame()
                gamegoing = True
                break
            elif PvsAIButton.is_clicked():
                state = GameState.DIFFICULTY_MENU
                break
            elif AIvsAIButton.is_clicked():
                state = GameState.DIFFICULTY_MENU2
                break

            elif menuButton.is_clicked():
                state = menuButton.action
                break


# Draws the difficulty menu
def gameDifficultyMenu():
    global state
    global difficulty
    global gamegoing
    screen.fill((220,190,131))
    drawText(screen, "ABOYNE", 'black', 80, screen.get_width() / 2, 100)
    drawText(screen, "Choose AI difficulty", 'black', 40, screen.get_width() / 2, 180)
    difficultyEasyButton = Button((screen.get_width() / 2 , screen.get_height() / 2 - 80), (192,157,89), 'Easy', (60, 60), None, 32, 'hexagon')
    difficultyMediumButton = Button((screen.get_width() / 2 - 54, screen.get_height() / 2 + 10), (192,157,89), 'Medium', (60, 60), None, 32, 'hexagon')
    difficultyHardButton = Button((screen.get_width() / 2 + 52, screen.get_height() / 2 + 12), (192,157,89), 'Hard', (60, 60), None, 32, 'hexagon')
    menuButton = Button((screen.get_width() / 2 , screen.get_height() / 2 + 101), (192,157,89), 'Menu', (60, 60), GameState.MENU, 32, 'hexagon')

    difficultyEasyButton.draw(screen)
    difficultyMediumButton.draw(screen)
    difficultyHardButton.draw(screen)
    menuButton.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if difficultyEasyButton.is_clicked():
                difficulty = 1
                state = GameState.PvsAI
                initGame()
                gamegoing = True
                return 
                
            elif difficultyMediumButton.is_clicked():
                difficulty = 2
                state = GameState.PvsAI
                initGame()
                gamegoing = True
                return 
                
            elif difficultyHardButton.is_clicked():
                difficulty = 3
                
                state = GameState.PvsAI
                initGame()
                gamegoing = True

                return
            
            elif menuButton.is_clicked():
                state = menuButton.action
                return
                
# Draws the difficulty menu for the second AI
def gameDifficultyMenu2():
    global state
    global d1done
    global difficulty
    global difficulty2
    global gamegoing
    if not d1done:
        screen.fill((220,190,131))
        drawText(screen, "ABOYNE", 'black', 80, screen.get_width() / 2, 100)
        drawText(screen, "Choose AI 1 difficulty", 'black', 40, screen.get_width() / 2, 180)
    else:
        screen.fill((220,190,131))
        drawText(screen, "ABOYNE", 'black', 80, screen.get_width() / 2, 100)
        drawText(screen, "Choose AI 2 difficulty", 'black', 40, screen.get_width() / 2, 180)
    difficultyEasyButton = Button((screen.get_width() / 2 , screen.get_height() / 2 - 80), (192,157,89), 'Easy', (60, 60), None, 32, 'hexagon')
    difficultyMediumButton = Button((screen.get_width() / 2 - 54, screen.get_height() / 2 + 10), (192,157,89), 'Medium', (60, 60), None, 32, 'hexagon')
    difficultyHardButton = Button((screen.get_width() / 2 + 52, screen.get_height() / 2 + 12), (192,157,89), 'Hard', (60, 60), None, 32, 'hexagon')
    menuButton = Button((screen.get_width() / 2 , screen.get_height() / 2 + 101), (192,157,89), 'Menu', (60, 60), GameState.MENU, 32, 'hexagon')

    difficultyEasyButton.draw(screen)
    difficultyMediumButton.draw(screen)
    difficultyHardButton.draw(screen)
    menuButton.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if difficultyEasyButton.is_clicked() and not d1done:
                difficulty = 1
                d1done = True
                
            elif difficultyMediumButton.is_clicked() and not d1done:
                difficulty = 2
                d1done = True
                
            elif difficultyHardButton.is_clicked() and not d1done:
                difficulty = 3
                d1done = True

            elif menuButton.is_clicked():
                state = menuButton.action
                return
                        
            elif d1done:
                
                if difficultyEasyButton.is_clicked():
                    difficulty2 = 1
                    state = GameState.AIvsAI
                    initGame()
                    gamegoing = True
                    return 
                    
                elif difficultyMediumButton.is_clicked():
                    difficulty2 = 2
                    state = GameState.AIvsAI
                    initGame()
                    gamegoing = True
                    return 
                    
                elif difficultyHardButton.is_clicked():
                    difficulty2 = 3
                    state = GameState.AIvsAI
                    initGame()
                    gamegoing = True
                    return
                
                elif menuButton.is_clicked():
                        state = menuButton.action
                        return
                
# Draws the rules
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



# Makes a copy of the game state
def copyState():
    blue_pieces_copy = []
    red_pieces_copy = []
    for piece in blue_pieces:
        blue_pieces_copy.append(Piece(piece.position, piece.color, piece.pos_n, piece.selected, piece.isBlocked))
    for piece in red_pieces:
        red_pieces_copy.append(Piece(piece.position, piece.color, piece.pos_n, piece.selected, piece.isBlocked))
    return blue_pieces_copy, red_pieces_copy



# Cleans up data structures before the game
def cleanGame():
    hexagons.clear()
    blue_pieces.clear()
    red_pieces.clear()

# Initializes the game, creating the board and the pieces, and setting the turn, randomly
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


# Randomizes the AI color
        
def randomizeAI():
    random.seed()
    if random.randint(0, 1) == 0:
        return red_color
    return blue_color



##
##    MAIN LOOP
##   
        
initGame()
ai_color = randomizeAI()

while running:
    if state == GameState.MENU:
        menu()
    elif state == GameState.GAME_MODE_MENU:
        gameModeMenu()
    elif state == GameState.DIFFICULTY_MENU:
        gameDifficultyMenu()
    elif state == GameState.DIFFICULTY_MENU2:
        gameDifficultyMenu2()

    elif state == GameState.PvsP:

        currentModeState = GameState.PvsP
        play(None)
    elif state == GameState.PvsAI:
        currentModeState = GameState.PvsAI
        play(ai_color, difficulty)
    elif state == GameState.AIvsAI:
        currentModeState = GameState.AIvsAI
        play(ai_vs_ai_color, difficulty, difficulty2)
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


