import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel 
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
# some more things to add buttons and th like 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout # to arrange the btns
# for the controller class
from functools import partial # to connect signals
ERROR_MSG = 'Something went wrong!'

# be warmed that all the functions are not in the correct order.
# so it wont work sometimes. as it should.

# the model to handle the calculator's operations
def evaluateExpress(expression):
	# evaluate an expression
	try: # shitty try block as it does not catch any specific exception. not good practice in python.
		result = str(eval(expression, {}, {}))
	except Exception:
		result = ERROR_MSG

	return result

# the controller class 
class PyCalcCtrl:

	def __init__(self, model, view):
		# controller initializer
		self._evaluate = model # where is the model func
		self._view = view 
		# connect signals and sloths
		self._connectSignals()

	def _calculateResult(self):
		# evaluate the expression
		result = self._evaluate(expression=self._view.displayText())
		self._view.setDisplayText(result)

	def _buildExpression(self, sub_exp):
		# building the expression
		if self._view.displayText() == ERROR_MSG:
			self._view.clearDisplay()

		# build expression
		expression = self._view.displayText() + sub_exp
		self._view.setDisplayText(expression)
	

	def _connectSignals(self):
		# connect signals and sloths 
		for btnText, btn in self._view.buttons.items():
			if btnText not in {'=', 'C'}:
				btn.clicked.connect(partial(self._buildExpression, btnText))

		#self._view.buttons['C'].clicked.connect(self._view.clearDisplay)
		self._view.buttons['='].clicked.connect(self._calculateResult)
		self._view.display.returnPressed.connect(self._calculateResult)
		self._view.buttons['C'].clicked.connect(self._view.clearDisplay)


class PyCalcUi(QMainWindow):
	def _createDisplay(self):
		# the display 
		self.display = QLineEdit()
		# set some display properties 
		self.display.setFixedHeight(35)
		self.display.setAlignment(Qt.AlignRight)
		self.display.setReadOnly(True)
		# adds the display to the general layout
		self.generalLayout.addWidget(self.display)

	def _createButtons(self):
		# creates the buttons 
		self.buttons = {} # a dictionary to hold each btns text and num
		buttonsLayout = QGridLayout()
		#btn text | position on the GridLayout 
		buttons = {'7': (0,0),
				'8': (0, 1),
				'9': (0, 2),
				'/': (0, 3),
				'C': (0, 4),
				'4': (1, 0),
				'5': (1, 1),
				'6': (1, 2),
				'*': (1, 3),
				'(': (1, 4),
				'1': (2, 0),
				'2': (2, 1),
				'3': (2, 2),
				'-': (2, 3),
				')': (2, 4),
				'0': (3, 0),
				'00': (3, 1),
				'.': (3, 2),
				'+': (3, 3),
				'=': (3, 4),
		}
		# create the btns and add them to the grid layout
		for btnText, pos, in buttons.items():
			self.buttons[btnText] = QPushButton(btnText)
			self.buttons[btnText].setFixedSize(40, 40)
			buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
		# add buttonsLayout to the general layout 
		self.generalLayout.addLayout(buttonsLayout)

	def setDisplayText(self, text):
		# set and update display text 
		self.display.setText(text)
		self.display.setFocus()

	def displayText(self):
		# to get the current display's text
		return self.display.text()

	def clearDisplay(self):
		# clears the display 
		self.setDisplayText('')
	'''pycalc's view gui '''
	def __init__(self):
		''' view initializer '''
		super().__init__()
		# set some main window properties 
		self.setWindowTitle("PyCalc")
		self.setFixedSize(235, 235)
		# sets the cnetral widget and the general layout 
		self.generalLayout = QVBoxLayout()
		# set the central widget
		self._centralWidget = QWidget(self)
		self.setCentralWidget(self._centralWidget)
		self._centralWidget.setLayout(self.generalLayout)
		# create the display and the btns 
		self._createDisplay()
		self._createButtons()

# client code 
def main():
	# main function
	# create an instance of QApplicarion 
	pycalc = QApplication(sys.argv)
	# shows the gui 
	view = PyCalcUi()
	view.show()

	# an instance of the model and the controller
	model = evaluateExpress
	PyCalcCtrl(model=model, view=view)
	# execute the calculators main loop
	sys.exit(pycalc.exec_())

# layout.addWidget(btn)
# msg = QLabel('')
# layout.addWidget(msg)
# window.setLayout(layout)
# window.show()
# sys.exit(app.exec_())

if __name__ == '__main__':
	main()