import pygame
from game import Game
import mancalaBoard
from time import sleep
import sys
from button import Button
from copy import deepcopy


class Play():
    def humanTurn(self,game):
        move=game.state.randomove(game.playerSide[-1])
        n=game.state.board[move]
        player,plusgain=game.state.doMove(move, game.playerSide[-1])
        update(game,move,n,game.playerSide[-1],plusgain)
        return player
    
    def computerTurn(self,game):
        didbestmove,move=game.state.bestmove(game)
        if didbestmove == 0:
            bestValue, bestPit = self.NegaMaxAlphaBetaPruning(game, 1, 5, -99999, 99999)
            n=game.state.board[bestPit]
            player,plusgain=game.state.doMove(bestPit, game.playerSide[1])
            update(game,bestPit,n,game.playerSide[1],plusgain)
            return player
        else : # we did best move so now computer will play for another round
            update(game,move,4,game.playerSide[1],0)
            self.computerTurn(game)
        
        
    def NegaMaxAlphaBetaPruning(self,game, player, depth, alpha, beta):
        if game.gameOver() or depth == 1:
            bestValue = game.evaluate()
            bestPit = None
            if player == -1:
                bestValue = - bestValue
            return bestValue, bestPit
        bestValue = -99999
        bestPit = None
        for pit in game.state.possibleMoves(game.playerSide[player]):
            child_game = deepcopy(game)
            nextplayer=child_game.state.doMove(pit,game.playerSide[player])
            if(nextplayer==game.playerSide[player]):
                value, _ = self.NegaMaxAlphaBetaPruning (child_game, player, depth-1, -beta, -alpha)
            else :
                value, _ = self.NegaMaxAlphaBetaPruning (child_game, -player, depth-1, -beta, -alpha) 
            value = - value
            if value > bestValue:
                bestValue = value
                bestPit =pit
            if bestValue > alpha:
                alpha = bestValue
            if  beta <= alpha:
                break
        return bestValue, bestPit  

fosses_position=[(370, 400),(480, 400),(590, 400),(710, 400),(820, 400),(930, 400),(370, 250),(480, 250),(590, 250),(710, 250),(820, 250),(930, 250)]
magazins=[(1000, 200, 100,250),(200, 200, 100,250)]

grey = (150, 150, 150)  
white = (255, 255, 255) 
yellow = (200, 200, 0)  
red = (200,0,0) 
black = (0, 0, 0) 
blue = (50,50,160)
brown = (121, 96, 76)
brownlight = (171, 149, 132)

display_width = 1300
display_height = 650
radius = 20 # node size

pygame.init()
screen = pygame.display.set_mode((display_width, display_height))

def get_font(size): 
    return pygame.font.SysFont('segoeuisymbol',size,italic=False,bold=True)

def printdata(data,position,size=20,color=black) :
    font = get_font(size)
    text= font.render(data,True, (color))
    textrect = text.get_rect(center=position)
    screen.blit(text, textrect)

def menu():
    screen.fill(white) 
    while True:

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        printdata("select a player :",(640, 150),50,yellow)
        

        Player1_BUTTON = Button(image=pygame.image.load("Method Rect.png"), pos=(640, 300), 
                            text_input="Player1", font=get_font(50), base_color="White", hovering_color="Red")
        Player2_BUTTON = Button(image=pygame.image.load("Method Rect.png"), pos=(640, 450), 
                            text_input="Player2", font=get_font(50), base_color="White", hovering_color="Red")
        


        for button in [Player1_BUTTON, Player2_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Player1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return(1)
                if Player2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return(2)

        pygame.display.update()

def result (humanscore, computerscore, winner) :
    screen.fill(white) 
    printdata("human score ",(325, 150),50,yellow)
    pygame.draw.circle(screen, grey, (325, 250), 50)
    printdata(str(humanscore),(325, 250),50,red)
    
    printdata("computer score ",(975, 150),50,yellow)
    pygame.draw.circle(screen, grey, (975, 250), 50)
    printdata(str(computerscore),(975, 250),50,red)

    pygame.draw.rect(screen, grey ,(300, 400, 700,100) )
    printdata(winner+" is the winner",(650, 450),50,red)

    while True:
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def get_graine_pos(nb,fosse_pos) : 
    if nb<3 : graine_pos=(fosse_pos[0]-25+nb*22,fosse_pos[1]-25)
    if 3<=nb<7 : graine_pos=(fosse_pos[0]-30+(nb-3)*22,fosse_pos[1]-3)
    if 7<=nb<10 : graine_pos=(fosse_pos[0]-25+(nb-7)*22,fosse_pos[1]+19)
    if 10<=nb<13 : graine_pos=(fosse_pos[0]-20+(nb-10)*22,fosse_pos[1]-20)
    if 13<=nb<17 : graine_pos=(fosse_pos[0]-25+(nb-13)*224,fosse_pos[1]+2)
    if 17<=nb<20 : graine_pos=(fosse_pos[0]-20+(nb-17)*22,fosse_pos[1]+24)
    return graine_pos

def mancala_board():
    screen.fill(white) 
    printdata("Mancala",(640, 50),100,brown)
    pygame.draw.rect(screen, brownlight,(150, 150, 1000,350) )

    for magasin in magazins :
        pygame.draw.rect(screen, brown,magasin )

    for position in fosses_position :
        pygame.draw.circle(screen, brown, position, (50))

    printdata("player1",(1050, 475), 30,brown)
    printdata("player2",(250, 475),30,brown)

def display (game) :
    mancala_board()    
    for fosse in game.state.board_player1 :
        for nb in range(game.state.board[fosse]) :
            pos=game.state.fosse_positions[fosse]
            pygame.draw.circle(screen, red, get_graine_pos(nb,pos), (10))
    for fosse in game.state.board_player2 :
        for nb in range(game.state.board[fosse]) :
            pos=game.state.fosse_positions[fosse]
            pygame.draw.circle(screen, red, get_graine_pos(nb,pos), (10))
    printdata(str(game.state.board[1]),(1050, 325),50,red)
    printdata(str(game.state.board[2]),(250, 325),50,red)
    pygame.display.update()
    sleep(4)

def update (game,move,n,player,plusgain) :
    if player==1:
            other=2
            playermagazin=(1000, 200, 100,250)
            playerscorepos=(1050, 325)
    else:
            other=1
            playermagazin=(200, 200, 100,250)
            playerscorepos=(250, 325)
    pos=game.state.fosse_positions[move]
    next=move  
    pygame.draw.circle(screen, blue, pos, 55, width=5)
    pygame.display.update()
    sleep(1)
    for nb in range(n) :
        next=game.state.next_case[next]
        pygame.draw.circle(screen, brown, get_graine_pos(nb,pos), (10))
        if(nb+10<n):
            pygame.draw.circle(screen, blue, get_graine_pos(nb+10,pos), (10))
            if(nb!=0 and nb!=3 and nb!=7) :
                pygame.draw.circle(screen, blue, get_graine_pos(nb+9,pos), (10))
        pygame.display.update()
        sleep(1)
        if(next==player) :
            pygame.draw.rect(screen, brown,playermagazin)
            printdata(str(game.state.board[player]),playerscorepos,50,red)
        else :
            if(next==other or next==move) :
                next=game.state.next_case[next]
            posnext=game.state.fosse_positions[next]
            nbnext=game.state.board[next]-1
            if(nbnext==-1):
                nbnext=nbnext+1
            if(nbnext<10):
                pygame.draw.circle(screen, red, get_graine_pos(nbnext,posnext), (10))
            else :
                pygame.draw.circle(screen, blue, get_graine_pos(nbnext,posnext), (10))
        
        pygame.display.update()
        sleep(1)
    if plusgain==1 : #the last move was empty
        posfrant=game.state.fosse_positions[game.state.frant[next]]
        pygame.draw.circle(screen, yellow, posnext, 55, width=5)
        pygame.draw.circle(screen, yellow, posfrant, 55, width=5)
        pygame.display.update()
        sleep(2)
        pygame.draw.circle(screen, brown, posnext, 50)
        pygame.draw.circle(screen, brown, posfrant, 50)
        #update score
        pygame.draw.rect(screen, brown,playermagazin)
        printdata(str(game.state.board[player]),playerscorepos,50,red)
        pygame.draw.circle(screen, brownlight, posnext, 55, width=5)
        pygame.draw.circle(screen, brownlight, posfrant, 55, width=5)
    pygame.draw.circle(screen, brownlight, pos, 55, width=5)
    pygame.display.update()
    sleep(2)

def startplay():
        humanplayer=menu()
        if(humanplayer==1):
            computerplayer=2
        else :
            computerplayer=1

        mancalaboard=mancalaBoard.Mancalaboard(mancalaBoard.initial_board)
        game=Game(mancalaboard, humanplayer, computerplayer)
        play=Play()
        player=1
        display (game)
        while(not game.gameOver()):
            if(player==game.playerSide[1]):
                player=play.computerTurn(game)     
            else :
                player=play.humanTurn(game)  
                
        display (game)

        if(game.findWinner() == game.playerSide[-1]):
            winner="Human"
        else :
            winner="Computer"
        humanscore=game.state.board[game.playerSide[-1]]
        computerscore=game.state.board[game.playerSide[1]]
        result(humanscore, computerscore, winner)