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
        pass

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
        return (self.get_number(row + 1, col), self.get_number(row - 1, col))

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_number(row, col - 1), self.get_number(row, col + 1))



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
            
        for i in range(0, self.size):
            if (vector[i]==1):
                counter_1 += 1
            elif (vector[i]==0):
                counter_0 += 1

        return (counter_0,counter_1)


    def different_vectors(self, index1: int, index2: int, type:int):
        
        if (type==ROW):
            vector1=self.get_row(index1)
            vector2=self.get_row(index2)

        elif (type==COL):
            vector1=self.get_col(index1)
            vector2=self.get_col(index2)
            
        for i in range(0, self.size):
            if (vector1[i]!=vector2[i]):
                return True

        return False

    def different_cols(self, col1:int, col2:int):
        return self.different_vectors(col1,col2,COL)

    def different_rows(self, row1:int, row2:int):
        return self.different_vectors(row1,row2,ROW)

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
                if self.board.get_number(i,j)==2:
                    return False

        return True 
    





    def get_action(self):

        for i in range(0,self.size) :
            for j in range (0,self.size):
                if (Board.adjacent_vertical_numbers(i,j)==(0,0)):
                    return (i,j,1)
                elif (Board.adjacent_horizontal_numbers(i,j)==(1,1)):
                    return (i,j,0)

        for i in range (0, self.size):
            col=Board.get_col(i)
            row=Board.get_row(i)
            z=0
            s=self.size
            if (s%2==1):
                z=1
            card_row=Board.get_card_row(i)
            card_col=Board.get_card_col(i)
            if (card_row[0]==s//2+z):
                j=Board.first_void_position(i,ROW)
                return(i,j,1)
            if card_row[1]==s//2+z:
                j=Board.first_void_position(i,ROW)
                return(i,j,0)
            if card_col[0]==s//2+z:
                j=Board.first_void_position(i,COL)
                return(j,i,1)
            if card_col[1]==s//2+z:
                j=Board.first_void_position(i,COL)
                return(j,i,0)

            for i in range(0,self.size):
                j=self.first_void_position(i)
                if j!=None:
                    return [(i,j,0),(i,j,1)]


    

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
        return Board(board, size)

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.state=TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        return [self.state.board.get_action()]
        
    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        i=action[0]
        j=action[1]
        value=action[3]
        board_copy = np.ndarray.__deepcopy__(self.state.board)
        new_state=TakuzuState(board_copy)
        new_state.board.change_value(i,j,value)
        return new_state
        
    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        if self.state.board.all_positions_filled()==False:
            return False
        
        for i in range(0,self.state.board.size):
            for j in range(0,self.state.board.size):
                value=self.state.board.get_number(i,j)
                (v1,v2)=self.state.board.adjacent_horizontal_numbers(i,j)
                if v1==value and v2==value:
                    return False
                (v1,v2)=self.state.board.adjacent_vertical_numbers(i,j)
                if v1==value and v2==value:
                    return False

        z=0
        s=self.size
        if (s%2==1):
            z=1 

        for i in range(0,self.state.board.size):
            (n0,n1)=self.state.board.get_card_vector(i,ROW)
            if n0>s//2+z or n1>s//2+z:
                return False
            
        for i in range(0,self.state.board.size):
            for j in range(i,self.state.board.size):
                if self.state.board.different_cols(i,j):
                    return False
                if self.state.board.different_rows(i,j):
                    return False
        
        return True

    

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    board = Board.parse_instance_from_stdin()
    print(board.adjacent_vertical_numbers(3, 3))
    print(board.adjacent_horizontal_numbers(3, 3))
    print(board.adjacent_vertical_numbers(1, 1))
    print(board.adjacent_horizontal_numbers(1, 1))
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
