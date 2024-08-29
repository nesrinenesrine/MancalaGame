class Game():
    def __init__(self,state,humanplayer,computerplayer) :
        self.state=state
        self.playerSide={-1:humanplayer, 1:computerplayer}
        
    def gameOver(self):
        cpt1=0
        cpt2=0
        add=0
        for move in self.state.board_player1 :
            if self.state.board[move]==0:
                cpt1=cpt1+1
        
        for move in self.state.board_player2 :
            if self.state.board[move]==0:
                cpt2=cpt2+1
                
        if cpt1==6:
            for move in self.state.board_player2:
                add=add+self.state.board[move]
                self.state.board[move]=0
            self.state.board[2]=self.state.board[2]+add
            
        elif cpt2==6:
            for move in self.state.board_player1:
                add=add+self.state.board[move]
                self.state.board[move]=0
            self.state.board[1]=self.state.board[1]+add
            
        if cpt1==6 or cpt2==6:
            return True
        else: 
            return False

    def findWinner(self):
        if self.state.board[1] > self.state.board[2]:
            return 1
        else:
            return 2
    
    def evaluate(self):
        heur=[]
        h1=self.state.board[self.playerSide[1]]-self.state.board[self.playerSide[-1]]
        heur.append(h1)
        if self.playerSide[1]==1:
            moves=self.state.board_player1
        else:
            moves=self.state.board_player2
            moves.reverse()
        for x in moves:
            pos=6-moves.index(x)
            if self.state[x]==pos:
                h2=3*h1
                heur.append(h2)
        return max(heur)
    
    def evaluate2(self):
        print("evaluete")
            
            
        
        
