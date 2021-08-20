import pygame, random, time, os
from pytmx import load_pygame
from kana import Kana
from timer import TimedAction
import psutil

"""
pip install pygame
pip install pytmx
"""

VERSION = "0.2"
APP_PATH = os.path.dirname(os.path.realpath(__file__)) + os.sep

class Game:
	def __init__(self):
		self.initTime = time.time() * 1000
		self.currentFps = 0
		self.lastRenderTime = time.time() * 1000
		pygame.mixer.pre_init(44100, -16, 1, 1024)		# Shorten the buffer (last parameter) to reduce sound latency
		pygame.mixer.init()
		self.sounds = {}
		# self.sounds["start-game"] = pygame.mixer.Sound(app_path + "snd/chicken.flac")
		# self.sounds["lay"] = pygame.mixer.Sound(app_path + "snd/lay2.flac")
		# self.sounds["shit"] = pygame.mixer.Sound(app_path + "snd/shit.flac")

		for s in self.sounds:	# Adjust the volume for all sounds to 60%
			self.sounds[s].set_volume(0.6)

		# self.sounds["start-game"].play()
		pygame.init()
		pygame.font.init()
		self.font = pygame.font.SysFont('monotype', 16)
		self.dt = 0
		self.clock = pygame.time.Clock()
		self.running = True
		self.windowSize = [1280, 720]
		self.kana = Kana(
			self.windowSize[0] / 2 + 30,
			self.windowSize[1] / 2
		)
		# pygame.event.set_grab(True)
		# pygame.mouse.set_visible(False)
		self.displaySurf = pygame.display.set_mode(self.windowSize, pygame.HWSURFACE | pygame.DOUBLEBUF)# | pygame.FULLSCREEN)
		self.tileMap = load_pygame(os.path.join(APP_PATH, "maps", "testi.tmx"))
		self.sprites = pygame.sprite.Group()
		self.kanaSprite = pygame.sprite.Group()
		self.kanaSprite.add(self.kana)
		self.blockingTiles = self.getBlockingTiles()

	def getBlockingTiles(self):
		blockingTiles = []
		for x, y, gid, in self.tileMap.get_layer_by_name("esteet"):
			if gid:
				blockingTiles.append((x, y))
		return blockingTiles

	def renderTiles(self):
		for layer in self.tileMap.visible_layers:
			for x, y, gid, in layer:
				tile = self.tileMap.get_tile_image_by_gid(gid)
				if tile:
					self.displaySurf.blit(
						tile,
						(
							x * self.tileMap.tilewidth - self.kana.location[0],
							y * self.tileMap.tileheight - self.kana.location[1]
						)
					)

	def screenPosToTileCoords(self, pos):
		return(
			int((pos[0] + self.kana.location[0]) / self.tileMap.tilewidth),
			int((pos[1] + self.kana.location[1]) / self.tileMap.tileheight)
		)

	def handleEvents(self):
		events = pygame.event.get()
		for event in events:
			if event.type == 256:				# Window close
				game.running = False

			elif event.type == 768:				# Key down
				if event.unicode != "":
					key = event.unicode
					if key == "Q":
						game.running = False
					else:
						print("Unhandled key press:", key)

			elif event.type == 769:				# Key up
				key = event.unicode
				# print("KEY UP", key)

			elif event.type == 1024:			# Mouse move
				# print("MOUSE MOVE:", event.pos, event.rel, event.buttons)
				self.kana.targetPos = event.pos

			elif event.type == 1025:			# Mouse button down
				print("CLICK:", self.screenPosToTileCoords(event.pos))

			elif event.type == 1026:			# Mouse button up
				pass

			else:
				print("Unhandled event type:", event)

	def renderChicken(self):
		kanaTilePos = self.screenPosToTileCoords(self.kana.location)
		if kanaTilePos in self.blockingTiles:
			self.kana.rect.center = self.kana.lastPos
			self.kana.location = self.kana.lastPos
		else:
			self.kana.lastPos = self.kana.location
		self.kanaSprite.draw(self.displaySurf)


def printStatusLog():
	loc = game.screenPosToTileCoords(game.kana.location)
	print("TME:{0:15} POS:{1}x{2:6} FPS:{3:6} CPU:{4}%".format(
			str(round(time.time() * 1000 - game.initTime)).ljust(1),
			str(loc[0]),
			str(loc[1]),
			str(game.currentFps),
			psutil.cpu_percent()
		)
	)

def renderInOrder():
	game.renderTiles(),
	game.renderChicken(),
	game.kana.update(),
	pygame.display.flip()
	renderedMsAgo = time.time() * 1000 - game.lastRenderTime
	game.currentFps = round(1000 / renderedMsAgo)
	game.lastRenderTime = time.time() * 1000

game = Game()
pygame.event.get()
pygame.display.set_caption("Kanapeli II v{}".format(VERSION))
RENDER_INTERVAL = 16.67 	# 60fps
# RENDER_INTERVAL = 8.33 	# 120fps

timedActions = [
	(
		TimedAction(
			"handle events",
			RENDER_INTERVAL,
			game.handleEvents,
		)
	),
	(
		TimedAction(
			"render & flip",
			RENDER_INTERVAL,
			renderInOrder,
		)
	),
	(
		TimedAction(
			"console log",
			1000, 			# use only 1000ms for fps counter to work
			printStatusLog,
		)
	)
]

while game.running:
	for a in timedActions:
		a.activate()

pygame.quit()
print("QUIT BYE")