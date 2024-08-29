import random
fosses_position=[(370, 400),(480, 400),(590, 400),(710, 400),(820, 400),(930, 400),(370, 250),(480, 250),(590, 250),(710, 250),(820, 250),(930, 250)]
magazins=[(1000, 200, 100,250),(200, 200, 100,250)]
initial_board={"A":4,"B":4,"C":4,"D":4,"E":4,"F":4, 
       1:0,
       "G":4,"H":4,"I":4,"J":4,"K":4,"L":4,
       2:0}

class Mancalaboard():
    def __init__(self,board) :
        self.board=board
        self.board_player1=["A", "B", "C", "D", "E", "F"]
        self.board_player2=["G", "H", "I", "J", "K", "L"]
        
        self.frant={"A":"G","B":"H","C":"I","D":"J","E":"K","F":"L",
                    "G":"A","H":"B","I":"C","J":"D","K":"E","L":"F"}
        
        self.next_case={"A":"B","B":"C","C":"D","D":"E","E":"F","F":1,1:"L","L":"K","K":"J","J":"I",
                        "I":"H","H":"G","G":2,2:"A"}
        self.fosse_positions={"A":fosses_position[0],"B":fosses_position[1],"C":fosses_position[2],"D":fosses_position[3],"E":fosses_position[4],"F":fosses_position[5],1:magazins[0],
                    "G":fosses_position[6],"H":fosses_position[7],"I":fosses_position[8],"J":fosses_position[9],"K":fosses_position[10],"L":fosses_position[11],2:magazins[1]}
    
    def possibleMoves(self,player):
        posible_moves=[]
        if player ==1:
            for f in self.board_player1:
                if self.board[f]!=0:
                    posible_moves.append(f)
            return posible_moves
        else:
            for f in self.board_player2:
                if self.board[f]!=0:
                    posible_moves.append(f)
            return posible_moves


    def doMove(self,move,player):
        
        if player==1:
            other=2
            playerboard=self.board_player1
        else:
            other=1
            playerboard=self.board_player2
            
        next=move
        while self.board[move]!=0 :
            next=self.next_case[next]
            if next == other:
                next=self.next_case[next]
                
            self.board[next]=self.board[next]+1
            self.board[move]=self.board[move]-1
             
        last_move=next
        plusgain=0
        if self.board[last_move]==1 and last_move in playerboard:
            self.board[player]=self.board[player]+self.board[self.frant[last_move]]+1
            self.board[last_move]=0
            self.board[self.frant[last_move]]=0
            plusgain=1
            
        if last_move==player :
            return player,plusgain
        else:
            return other,plusgain
        

    def bestmove(self,game) :
        if game.playerSide[1]==1:
            playerboard=self.board_player1
            bestmove="C"
        else:
            playerboard=self.board_player2
            bestmove="J"
        initial=True
        for move in playerboard :
            if (game.state.board[move]!=4):
                initial=False
        if(initial) :
            self.doMove(bestmove, game.playerSide[1])
            return 1,bestmove
        
        return 0,bestmove
    
    def randomove(self,player):
        posible_moves=self.possibleMoves(player)
        i=random.randint(0,len(posible_moves)-1)
        return posible_moves[i]