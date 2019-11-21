
from Ui_Game import *
import Ui_M
import Ui_tie
import Ui_Input
import Ui_Red
import Ui_Blue
from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog,QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush
from PyQt5.QtCore import Qt, QPoint
import othello_solver
import sys

class parentWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)

class tie(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.child=Ui_tie.Ui_Dialog()
        self.child.setupUi(self)

class Input(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.child=Ui_Input.Ui_Dialog()
        self.child.setupUi(self)

class Red(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.child=Ui_Red.Ui_Dialog()
        self.child.setupUi(self)

class Blue(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.child=Ui_Blue.Ui_Dialog()
        self.child.setupUi(self)

class childWindow_H(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.child = Ui_M.Ui_Widget()
        self.child.setupUi(self)
        self.pos = []
        self.EMPTY, self.BLACK, self.WHITE, self.OUTER = '.', '@', 'o', '?'
        self.PIECES = (self.EMPTY, self.BLACK, self.WHITE, self.OUTER)
        self.PLAYERS = {self.BLACK: 'Black', self.WHITE: 'White'}
        self.USER = self.BLACK
        self.AI = self.WHITE
        self.UP, self.DOWN, self.LEFT, self.RIGHT = -10, 10, -1, 1
        self.UP_RIGHT, self.DOWN_RIGHT, self.DOWN_LEFT, self.UP_LEFT = -9, 11, 9, -11
        self.DIRECTIONS = (self.UP, self.UP_RIGHT, self.RIGHT, self.DOWN_RIGHT, self.DOWN, self.DOWN_LEFT, self.LEFT, self.UP_LEFT)
        self.board = othello_solver.initial_board()
        self.player = self.USER
        self.red = Red()
        self.blue = Blue()
        self.tie = tie()
        self.input = Input()
        
    def paintEvent(self,update):
        qp = QPainter()
        qp.begin(self)
        for i in range(len(self.board)):
            if self.board[i] == self.BLACK:
                qp.setPen(Qt.red)
                qp.setBrush(QBrush(Qt.red,Qt.SolidPattern))
                qp.drawEllipse(85+65*(i%10-1),80+50*(i//10-1),20,20)
            elif self.board[i] == self.WHITE:
                qp.setPen(Qt.blue)
                qp.setBrush(QBrush(Qt.blue,Qt.SolidPattern))
                qp.drawEllipse(85+65*(i%10-1),80+50*(i//10-1),20,20)
        qp.end()
    def mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            move = int((int(event.x()) - 53)/65) + 1 + (int((int(event.y()) - 55)/50) + 1)*10
            print(move)
            if othello_solver.is_valid(move,self.board,self.player):
                othello_solver.reversion(move,self.board,self.player)
                self.player = othello_solver.next_player(self.player)
                result = othello_solver.game_status(self.player,self.board)
                if result != True:
                    if len(result) == 3:
                        self.tie.show()
                    else:
                        if self.PLAYERS[result[0]] == self.USER:
                            self.red.show()
                        else:
                            self.blue.show()
                else:
                    move = othello_solver.hard(self.board,self.player)
                    othello_solver.reversion(move,self.board,self.player)
                    self.player = othello_solver.next_player(self.player)
                    result = othello_solver.game_status(self.player,self.board)
                    if result != True:
                        if len(result) == 3:
                            self.tie.show()
                        else:
                            if self.PLAYERS[result[0]] == self.USER:
                                self.red.show()
                            else:
                                self.blue.show()
            else:
                self.input.show()
            self.repaint()

class childWindow_E(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.child = Ui_M.Ui_Widget()
        self.child.setupUi(self)
        self.pos = []
        self.EMPTY, self.BLACK, self.WHITE, self.OUTER = '.', '@', 'o', '?'
        self.PIECES = (self.EMPTY, self.BLACK, self.WHITE, self.OUTER)
        self.PLAYERS = {self.BLACK: 'Black', self.WHITE: 'White'}
        self.USER = self.BLACK
        self.AI = self.WHITE
        self.UP, self.DOWN, self.LEFT, self.RIGHT = -10, 10, -1, 1
        self.UP_RIGHT, self.DOWN_RIGHT, self.DOWN_LEFT, self.UP_LEFT = -9, 11, 9, -11
        self.DIRECTIONS = (self.UP, self.UP_RIGHT, self.RIGHT, self.DOWN_RIGHT, self.DOWN, self.DOWN_LEFT, self.LEFT, self.UP_LEFT)
        self.board = othello_solver.initial_board()
        self.player = self.USER
        self.red = Red()
        self.blue = Blue()
        self.tie = tie()
        self.input = Input()
        
    def paintEvent(self,update):
        qp = QPainter()
        qp.begin(self)
        for i in range(len(self.board)):
            if self.board[i] == self.BLACK:
                qp.setPen(Qt.red)
                qp.setBrush(QBrush(Qt.red,Qt.SolidPattern))
                qp.drawEllipse(85+65*(i%10-1),80+50*(i//10-1),20,20)
            elif self.board[i] == self.WHITE:
                qp.setPen(Qt.blue)
                qp.setBrush(QBrush(Qt.blue,Qt.SolidPattern))
                qp.drawEllipse(85+65*(i%10-1),80+50*(i//10-1),20,20)
        qp.end()

    def mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            move = int((int(event.x()) - 53)/65) + 1 + (int((int(event.y()) - 55)/50) + 1)*10
            print(move)
            if othello_solver.is_valid(move,self.board,self.player):
                othello_solver.reversion(move,self.board,self.player)
                self.player = othello_solver.next_player(self.player)
                result = othello_solver.game_status(self.player,self.board)
                if result != True:
                    if len(result) == 3:
                        self.tie.show()
                    else:
                        if self.PLAYERS[result[0]] == self.USER:
                            self.red.show()
                        else:
                            self.blue.show()
                else:
                    move = othello_solver.easy(self.board,self.player)
                    othello_solver.reversion(move,self.board,self.player)
                    self.player = othello_solver.next_player(self.player)
                    result = othello_solver.game_status(self.player,self.board)
                    if result != True:
                        if len(result) == 3:
                            self.tie.show()
                        else:
                            if self.PLAYERS[result[0]] == self.USER:
                                self.red.show()
                            else:
                                self.blue.show()
            else:
                self.input.show()
            self.repaint()

class childWindow_M(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.child = Ui_M.Ui_Widget()
        self.child.setupUi(self)
        self.pos = []
        self.EMPTY, self.BLACK, self.WHITE, self.OUTER = '.', '@', 'o', '?'
        self.PIECES = (self.EMPTY, self.BLACK, self.WHITE, self.OUTER)
        self.PLAYERS = {self.BLACK: 'Black', self.WHITE: 'White'}
        self.USER = self.BLACK
        self.AI = self.WHITE
        self.UP, self.DOWN, self.LEFT, self.RIGHT = -10, 10, -1, 1
        self.UP_RIGHT, self.DOWN_RIGHT, self.DOWN_LEFT, self.UP_LEFT = -9, 11, 9, -11
        self.DIRECTIONS = (self.UP, self.UP_RIGHT, self.RIGHT, self.DOWN_RIGHT, self.DOWN, self.DOWN_LEFT, self.LEFT, self.UP_LEFT)
        self.board = othello_solver.initial_board()
        self.player = self.USER
        self.red = Red()
        self.blue = Blue()
        self.tie = tie()
        self.input = Input()
        
    def paintEvent(self,update):
        qp = QPainter()
        qp.begin(self)
        for i in range(len(self.board)):
            if self.board[i] == self.BLACK:
                qp.setPen(Qt.red)
                qp.setBrush(QBrush(Qt.red,Qt.SolidPattern))
                qp.drawEllipse(85+65*(i%10-1),80+50*(i//10-1),20,20)
            elif self.board[i] == self.WHITE:
                qp.setPen(Qt.blue)
                qp.setBrush(QBrush(Qt.blue,Qt.SolidPattern))
                qp.drawEllipse(85+65*(i%10-1),80+50*(i//10-1),20,20)
        qp.end()
    def mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            move = int((int(event.x()) - 53)/65) + 1 + (int((int(event.y()) - 55)/50) + 1)*10
            print(move)
            if othello_solver.is_valid(move,self.board,self.player):
                othello_solver.reversion(move,self.board,self.player)
                self.player = othello_solver.next_player(self.player)
                result = othello_solver.game_status(self.player,self.board)
                if result != True:
                    if len(result) == 3:
                        self.tie.show()
                    else:
                        if self.PLAYERS[result[0]] == self.USER:
                            self.red.show()
                        else:
                            self.blue.show()
                else:
                    move = othello_solver.medium(self.board,self.player)
                    othello_solver.reversion(move,self.board,self.player)
                    self.player = othello_solver.next_player(self.player)
                    result = othello_solver.game_status(self.player,self.board)
                    if result != True:
                        if len(result) == 3:
                            self.tie.show()
                        else:
                            if self.PLAYERS[result[0]] == self.USER:
                                self.red.show()
                            else:
                                self.blue.show()
            else:
                self.input.show()
            self.repaint()





if __name__=='__main__':

    app=QApplication(sys.argv)
    window=parentWindow()
    child_e=childWindow_E()
    child_m=childWindow_M()
    child_h=childWindow_H()
    btn=window.main_ui.pushButton 
    btn.clicked.connect(child_e.show)
    btn=window.main_ui.pushButton_2 
    btn.clicked.connect(child_m.show)
    btn=window.main_ui.pushButton_3
    btn.clicked.connect(child_h.show)
    window.show()
    sys.exit(app.exec_())
