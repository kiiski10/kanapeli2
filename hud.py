import pygame, os

class Field:
	def __init__(self, label, parent):
		self.parent = parent
		self.label = label
		self.value = ""
		self.textSurface = self.parent.font.render('Loading', False, (0, 0, 0))
		self.rowHeight = parent.fontSize

class HUD():
	def __init__(self, game, fontSize):
		self.game = game
		self.fontSize = fontSize
		self.font = pygame.font.SysFont('monotype', self.fontSize)
		self.fields = {
			"TIME": Field("Time", self),
			"FPS": Field("Fps", self),
			"CPU_PERCENT": Field("Cpu usage", self),
			"FPS_LOCK": Field("Fps lock", self),
			"PATH_LEN": Field("Path length", self),
			"FOOD": Field("Food", self),
			"EGGS": Field("Eggs", self),
		}

	def render(self):
		y = 5
		for f in self.fields:
			self.textSurface = self.font.render("{}: {}".format(self.fields[f].label, self.fields[f].value), False, (0, 0, 0))
			self.game.displaySurf.blit(self.textSurface, (10, y))
			y += self.fields[f].rowHeight

