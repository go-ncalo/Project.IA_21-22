# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 66:
# 99189 Carolina Fonseca Coelho
# 99225 Gonçalo Botelho Mateus

import sys
from sys import stdin
import numpy as np

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

ROW = 0
COL = 1

class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    def __init__(self, board, size):
        """Representação interna de um tabuleiro de Takuzu."""
        self.board = board
        self.size = size
    
    # FUNÇÃO DO GONÇALO
    def copy(self):
        side = board.size
        
        b = Board(np.zeros(shape=(side, side), dtype=int), side)
        
        
        for row in range(board.size):
            for col in range(board.size):
                b.change_value(row, col, int(self.get_number(row, col)))
        
        
        return b

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        try:
            return self.board[row, col]
        except IndexError:
            return None

    def change_value(self, row: int, col: int, value:int):
        self.board[row,col]=value


    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        values = (self.get_number(row + 1, col) if row<self.size else None, self.get_number(row - 1, col) if row > 0 else None)
        #print("values:",row," ",col," ", values," ")
        return values

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_number(row, col - 1) if col>0 else None, self.get_number(row, col + 1) if col<self.size else None)

    def adjacent_above_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os 2 valores imediatamente acima."""
        values = (self.get_number(row - 2, col) if row>1 else None, self.get_number(row - 1, col) if row > 0 else None)
        return values

    def adjacent_below_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os 2 valores imediatamente abaixo."""
        values = (self.get_number(row + 1, col) if row<self.size else None, self.get_number(row + 2, col) if row<self.size-1 else None)
        return values

    def adjacent_left_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os 2 valores imediatamente a esquerda."""
        values = (self.get_number(row, col-2) if col>1 else None, self.get_number(row, col-1) if col>0 else None)
        return values

    def adjacent_right_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os 2 valores imediatamente a direita."""
        values = (self.get_number(row, col+1) if col<self.size else None, self.get_number(row, col+2) if col<self.size-1 else None)
        return values

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_number(row, col - 1) if col>0 else None, self.get_number(row, col + 1) if col<self.size else None)


    def get_row(self, row: int):
        """Devolve os valores da linha pretendida."""
        return self.board[row, :]

    def get_col(self, col: int):
        """Devolve os valores da linha pretendida."""
        return self.board[: ,col]

    def get_card_vector(self, index: int, type:int):
        counter_1=0
        counter_0=0

        if (type==ROW):
            vector=self.get_row(index)
        elif (type==COL):
            vector=self.get_col(index)
            
        #print("Vector: ", vector)
        for i in range(0, self.size):
            if (vector[i]==1):
                counter_1 += 1
            elif (vector[i]==0):
                counter_0 += 1
        #print("COUNTER: ",counter_0," ",counter_1)
        return (counter_0,counter_1)


    def different_vectors(self, index1: int, index2: int, type:int):
        
        if (type==ROW):
            vector1=self.get_row(index1)
            vector2=self.get_row(index2)

        elif (type==COL):
            vector1=self.get_col(index1)
            vector2=self.get_col(index2)
            
        for i in range(0, self.size):
            if (vector1[i]!=vector2[i] or vector1[i]==2 or vector2[i]==2):
                return True

        return False

    def different_cols(self, col1:int, col2:int):
        return self.different_vectors(col1,col2,COL)

    def different_rows(self, row1:int, row2:int):
        return self.different_vectors(row1,row2,ROW)

    def valid_board(self):
        for i in range(0,self.size):
            for j in range(0,self.size):
                value=self.get_number(i,j)
                (v1,v2)=self.adjacent_horizontal_numbers(i,j)
                if v1==value and v2==value and value!=2:
                    return False
                (v1,v2)=self.adjacent_vertical_numbers(i,j)
                if v1==value and v2==value and value!=2:
                    return False
        z=0
        s=self.size
        if (s%2==1):
            z=1 

        for i in range(0,self.size):
            (n0,n1)=self.get_card_vector(i,ROW)
            if n0>s//2+z or n1>s//2+z:
                return False
            (n0,n1)=self.get_card_vector(i,COL)
            if n0>s//2+z or n1>s//2+z:
                return False
            
        for i in range(0,self.size):
            for j in range(i+1,self.size):
                if self.different_cols(i,j)==False:
                    return False
                if self.different_rows(i,j)==False:
                    return False
        return True


    def first_void_position(self, index: int, type:int):
        
        if (type==ROW):
            vector=self.get_row(index)
        elif (type==COL):
            vector=self.get_col(index)

        for i in range(0,self.size):
            if vector[i]==2:
                return i
        
        return None

    def all_positions_filled(self):

        for i in range(0,self.size):
            for j in range(0,self.size):
                if self.get_number(i,j)==2:
                    return False

        return True 
    
    def get_first_void_position(self):
        for i in range(0,self.size):
            for j in range(0,self.size):
                if self.get_number(i,j)==2:
                    #print(i,j)
                    return(i,j)
        return (None,None)
    
    def get_action(self):


        if (self.valid_board()==False):
            return []

        for i in range(0,self.size) :
            for j in range (0,self.size):
                if (self.get_number(i,j)==2):
                    if (self.adjacent_vertical_numbers(i,j)[0]==0 and self.adjacent_vertical_numbers(i,j)[1]==0):
                        return [(i,j,1)]
                    elif (self.adjacent_vertical_numbers(i,j)[0]==1 and self.adjacent_vertical_numbers(i,j)[1]==1):
                        return [(i,j,0)]
                    elif (self.adjacent_horizontal_numbers(i,j)[0]==0 and self.adjacent_horizontal_numbers(i,j)[1]==0):
                        return [(i,j,1)]
                    elif (self.adjacent_horizontal_numbers(i,j)[0]==1 and self.adjacent_horizontal_numbers(i,j)[1]==1):
                        return [(i,j,0)]
                    elif (self.adjacent_above_numbers(i,j)[0]==0 and self.adjacent_above_numbers(i,j)[1]==0):
                        return [(i,j,1)]
                    elif (self.adjacent_above_numbers(i,j)[0]==1 and self.adjacent_above_numbers(i,j)[1]==1):
                        return [(i,j,0)]
                    elif (self.adjacent_below_numbers(i,j)[0]==0 and self.adjacent_below_numbers(i,j)[1]==0):
                        return [(i,j,1)]
                    elif (self.adjacent_below_numbers(i,j)[0]==1 and self.adjacent_below_numbers(i,j)[1]==1):
                        return [(i,j,0)]
                    elif (self.adjacent_left_numbers(i,j)[0]==0 and self.adjacent_left_numbers(i,j)[1]==0):
                        return [(i,j,1)]
                    elif (self.adjacent_left_numbers(i,j)[0]==1 and self.adjacent_left_numbers(i,j)[1]==1):
                        return [(i,j,0)]
                    elif (self.adjacent_right_numbers(i,j)[0]==0 and self.adjacent_right_numbers(i,j)[1]==0):
                        return [(i,j,1)]
                    elif (self.adjacent_right_numbers(i,j)[0]==1 and self.adjacent_right_numbers(i,j)[1]==1):
                        return [(i,j,0)]
                    

        for i in range (0, self.size):
            z=0
            s=self.size
            if (s%2==1):
                z=1
            card_row=self.get_card_vector(i,ROW)
            card_col=self.get_card_vector(i,COL)
            #print("Card row: ",card_row)
            #print("Card col: ",card_col)
            if (card_row[0]==s//2+z):
                #print("here3\n")
                j=self.first_void_position(i,ROW)
                if j!=None and self.get_number(i,j)==2:
                    return [(i,j,1)]
            if card_row[1]==s//2+z:
                #print("here4\n")
                j=self.first_void_position(i,ROW)
                if j!=None and self.get_number(i,j)==2:
                    return [(i,j,0)]
            if card_col[0]==s//2+z:
                #print("here5\n")
                j=self.first_void_position(i,COL)
                if j!=None and self.get_number(i,j)==2:
                    return [(j,i,1)]
            if card_col[1]==s//2+z:
                #print("here6\n")
                j=self.first_void_position(i,COL)
                if j!=None and self.get_number(i,j)==2:
                    return [(j,i,0)]

        for i in range(0,self.size):
            j=self.first_void_position(i,ROW)
            if j!=None and self.get_number(i,j)==2:
                return [(i,j,0),(i,j,1)]

        return []


    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        size = stdin.readline()
        board = np.loadtxt(stdin, dtype=int)
        return Board(board, int(size))

    # FUNÇÃO DO GONÇALO
    def __str__(self):
        out = ""

        for row in range(self.size):
            for col in range(self.size):
                out += str(self.get_number(row, col))
                if col < (self.size - 1):
                    out += '\t'

            if (row != (self.size - 1)):
                out += '\n'
        return out



class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial=TakuzuState(board)
        self.counter=0

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        return state.board.get_action()

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        i=action[0]
        j=action[1]
        value=action[2]
        #print(action)
        board_copy = state.board.copy()
        new_state=TakuzuState(board_copy)
        new_state.board.change_value(i,j,value)
        return new_state
        
    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""

        if state.board.all_positions_filled()==False:
            #print("false1")
            return False

        
        for i in range(0,state.board.size):
            for j in range(0,state.board.size):
                value=state.board.get_number(i,j)
                (v1,v2)=state.board.adjacent_horizontal_numbers(i,j)
                if v1==value and v2==value:
                    #print("false2")
                    return False
                (v1,v2)=state.board.adjacent_vertical_numbers(i,j)
                if v1==value and v2==value:
                    #print("false3")
                    #print(i,j)
                    return False

        z=0
        s=state.board.size
        if (s%2==1):
            z=1 

        for i in range(0,state.board.size):
            (n0,n1)=state.board.get_card_vector(i,ROW)
            if n0>s//2+z or n1>s//2+z:
                #print("false4")
                return False
            (n0,n1)=state.board.get_card_vector(i,COL)
            if n0>s//2+z or n1>s//2+z:
                #print("false4")
                return False
            
        for i in range(0,state.board.size):
            for j in range(i+1,state.board.size):
                if state.board.different_cols(i,j)==False:
                    #print("false5")
                    return False
                if state.board.different_rows(i,j)==False:
                    #print("false6")
                    return False
        
        #print("true")
        return True

    

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board)
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
