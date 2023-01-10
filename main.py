from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtMultimedia, QtCore
import sys
import pygame

pygame.mixer.init()
bell = pygame.mixer.Sound("bell-sound.mp3")
new_cycle = pygame.mixer.Sound("new_cycle.mp3")


class Window(QMainWindow):

	def __init__(self):
		super().__init__()
		self.setWindowTitle("Timer ")

		self.setGeometry(1000, 500, 600, 1000)

		self.UiComponents()

		self.show()

	def UiComponents(self):
		self.state = "Таймер не запущен."

		self.cycle_counter = 0
		self.container_seconds = [0, 0, 0]

		self.count_vdox = 0
		self.count_derzanie = 0
		self.count_vidox = 0

		self.first = True
		self.second = True
		self.third = True
		self.start = False

		button = QPushButton("Set time(s)", self)
		button.setGeometry(200, 40, 250, 100)
		button.clicked.connect(self.get_seconds)

		self.label = QLabel("//TIMER//", self)
		self.label.setGeometry(125, 200, 400, 200)
		self.label.setStyleSheet("border : 3px solid black")
		self.label.setFont(QFont('Times', 15))
		self.label.setAlignment(Qt.AlignCenter)

		start_button = QPushButton("Start", self)
		start_button.setGeometry(200, 500, 250, 80)
		start_button.clicked.connect(self.start_action)

		pause_button = QPushButton("Pause", self)
		pause_button.setGeometry(200, 600, 250, 80)
		pause_button.clicked.connect(self.pause_action)

		reset_button = QPushButton("Reset", self)
		reset_button.setGeometry(200, 700, 250, 80)
		reset_button.clicked.connect(self.reset_action)

		timer = QTimer(self)
		timer.timeout.connect(self.show_time)

		timer.start(100)

		self.state_text = QLabel(self.state, self)
		self.state_text.setGeometry(125, 100, 400, 150)

		self.label_text = QLabel("количество повторений: " + str(self.cycle_counter), self)
		self.label_text.setGeometry(20, 350, 600, 150)

		self.font = QFont()
		self.font.setFamily("Rubik")
		self.font.setPointSize(15)

		self.label_text.setFont(self.font)
		self.state_text.setFont(self.font)

	def show_time(self):

		if self.start:
			self.count_vdox -= 1
			if self.count_vdox <= 0:
				self.first = play_sound(self.first, bell)
				self.count_derzanie -= 1

				if self.count_derzanie <= 0:
					self.second = play_sound(self.second, bell)
					self.count_vidox -= 1

					if self.count_vidox <= 0:
						self.third = play_sound(self.third, new_cycle)
						self.cycle_counter += 1
						self.set_text()
						self.set_seconds()
						self.zero_sounds()
					else:
						if self.start:
							self.new_state("Выдох")
							text = str(self.count_vidox / 10) + " s"

							self.label.setText(text)
				else:
					if self.start:
						self.new_state("Удержание")
						text = str(self.count_derzanie / 10) + " s"

						self.label.setText(text)
			else:
				if self.start:
					self.new_state("Вдох")
					text = str(self.count_vdox / 10) + " s"

					self.label.setText(text)

	def zero_sounds(self):
		self.first, self.second, self.third = True, True, True

	def new_state(self, state):
		self.state = state
		self.state_text.setText(self.state)

	def set_text(self):
		self.label_text.setText("количество повторений: " + str(self.cycle_counter))

	def set_seconds(self):
		self.count_vdox = self.container_seconds[0]

		self.count_derzanie = self.container_seconds[1]

		self.count_vidox = self.container_seconds[2]

	def get_seconds(self):

		self.start = False

		second_vdox, done1 = QInputDialog.getInt(self, 'Seconds', 'Время вдоха:')

		if done1:

			second_detzanie, done2 = QInputDialog.getInt(self, 'Seconds', "Время задержки дыхания")

			if done2:

				second_vidox, done3 = QInputDialog.getInt(self, 'Seconds', 'Время выдоха')
				if done3:
					self.count_vdox = second_vdox * 10
					self.count_vidox = second_vidox * 10
					self.count_derzanie = second_detzanie * 10

					self.container_seconds[0] = self.count_vdox
					self.container_seconds[1] = self.count_derzanie
					self.container_seconds[2] = self.count_vidox

					# setting text to the label
					self.label.setText(str(self.count_vdox))

	def start_action(self):
		self.start = True

		if self.count_vdox == 0 and self.count_derzanie == 0 and self.count_vidox == 0:
			self.start = False

	def pause_action(self):
		self.start = False

	def reset_action(self):

		self.start = False

		self.count_vdox = 0
		self.count_vidox = 0
		self.count_derzanie = 0
		self.cycle_counter = 0

		self.label.setText("//TIMER//")
		self.set_text()
		self.new_state("Таймер не запущен")
		self.zero_sounds()


def play_sound(why, sound):
	if why is True:
		sound.play()
		return False


App = QApplication(sys.argv)
window = Window()

sys.exit(App.exec())
