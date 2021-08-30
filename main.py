import pygame, random, time, os
from pytmx import load_pygame
import psutil
from kana import Kana
from timer import TimedAction
from core import screenPosToTilePos, tilePosToScreenPos, distance
from hud import HUD
from ruoka import Ruoka

"""
pip install pygame
pip install pytmx
"""

VERSION = "0.3"
APP_PATH = os.path.dirname(os.path.realpath(__file__)) + os.sep

class Game:
	def __init__(self):
		# self.renderInterval = 33.34 	# 30fps
		self.renderInterval = 16.67 	# 60fps
		# self.renderInterval = 8.33 	# 120fps
		self.initTime = time.time() * 1000
		self.clock = pygame.time.Clock()
		self.currentFps = 0
		self.fpsLock = 60
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
		self.dt = 0
		self.clock = pygame.time.Clock()
		self.running = True
		self.windowSize = [1280, 720]
		# pygame.event.set_grab(True)
		# pygame.mouse.set_visible(False)
		self.displaySurf = pygame.display.set_mode(self.windowSize, pygame.HWSURFACE | pygame.DOUBLEBUF)# | pygame.FULLSCREEN)
		self.foods = []
		self.hud = HUD(self, 22)
		self.tileMap = load_pygame(os.path.join(APP_PATH, "maps", "chicken2.tmx"))
		self.kana = Kana(
			self.windowSize[0] / 2 + 30,
			self.windowSize[1] / 2,
			self,
		)
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

	def renderLowTiles(self):
		drawSeparately = ["korkeat", "esteet", "ruoka"]
		for layer in self.tileMap.visible_layers:
			if layer.name not in drawSeparately:
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

	def renderHighTiles(self):
			for x, y, gid, in self.tileMap.get_layer_by_name("korkeat"):
				tile = self.tileMap.get_tile_image_by_gid(gid)
				if tile:
					self.displaySurf.blit(
						tile,
						(
							x * self.tileMap.tilewidth - self.kana.location[0],
							y * self.tileMap.tileheight - self.kana.location[1]
						)
					)

	def handleEvents(self):
		events = pygame.event.get()
		for event in events:
			if event.type == 256:				# Window close
				game.running = False

			elif event.type == 768:				# Key down
				if event.unicode == "Q":
					game.running = False
				key = {"unicode": event.unicode, "scancode": event.scancode}
				print("KEY PRESS: unicode: {0:5} scancode: {1}".format(key["unicode"], key["scancode"]))

			elif event.type == 769:				# Key up
				key = event.unicode

			elif event.type == 771:				# Text input event
				pass

			elif event.type == 1024:			# Mouse move
				tilepos = screenPosToTilePos(self.kana, self.tileMap, event.pos)

			elif event.type == 1025:			# Mouse button down
				if event.button == 1:
					targettile = screenPosToTilePos(self.kana, self.tileMap, event.pos)
					self.kana.targetQue.append(targettile)
					self.kana.lastMoveTime = time.time()
					self.foods.append(Ruoka(self.tileMap, targettile))
					self.kana.state = "MOVING"

				elif event.button == 3:
					self.fpsLock = 60
				elif event.button == 4 and self.fpsLock < 345:
					self.fpsLock += 5
				elif event.button == 5 and self.fpsLock > 5:
					self.fpsLock -= 5
				else:
					pass

			elif event.type == 1026:			# Mouse button up
				pass

			elif event.type == 1027:			# Alternative mouse scroll
				pass

			else:
				print("Unhandled event type:", event)

	def renderFood(self):
		for f in self.foods:
			pygame.Surface.blit(self.displaySurf, f.image, tilePosToScreenPos(self.kana, self.tileMap, f.rect.center))

	def renderChicken(self):
		self.kanaSprite.draw(self.displaySurf)

	def renderPath(self):
		if self.kana.targetTile: 	# Draw line from chicken to target
			pygame.draw.line(
				self.displaySurf,
				(130,25,120),
				self.kana.location,
				tilePosToScreenPos(self.kana, self.tileMap, self.kana.targetTile)
			)

		last_p = None
		for p in self.kana.targetQue:
			if last_p:
				pygame.draw.line(
					game.displaySurf,
					(130,25,120),
					tilePosToScreenPos(self.kana, self.tileMap, last_p),
					tilePosToScreenPos(self.kana, self.tileMap, p)
				)
			else:
				pygame.draw.line(
					game.displaySurf,
					(130,25,120),
					tilePosToScreenPos(self.kana, self.tileMap, self.kana.targetTile),
					tilePosToScreenPos(self.kana, self.tileMap, p)
				)
			last_p = p

	def moveChicken(self):
		if self.kana.targetTile:
			if distance(self.kana.lastPos, tilePosToScreenPos(self.kana, self.tileMap, self.kana.targetTile)) < 20:
				self.kana.targetQue = self.kana.targetQue[1:]
				self.foods = self.foods[1:]
				if len(self.kana.targetQue) > 0:
					self.kana.targetTile = self.kana.targetQue[0]

				else:
					self.kana.state = "WAITING"
					self.kana.targetTile = None
			else:
				self.kana.update()
				if  self.kana.image == self.kana.image_up:
					kanaTilePos = screenPosToTilePos(self.kana, self.tileMap, self.kana.location)
				else:
					kanaTilePos = screenPosToTilePos(self.kana, self.tileMap, (self.kana.location[0], self.kana.location[1] - 24))

				if kanaTilePos in self.blockingTiles:
					self.kana.location = self.kana.lastPos
					self.kana.state = "BLOCKED"
				else:
					self.kana.lastPos = self.kana.rect.center
		else:
			if len(self.kana.targetQue) > 0:
				self.kana.targetTile = self.kana.targetQue[0]
			else:
				self.kana.state = "WAITING"


def updateHUD():
	game.hud.fields["FPS"].value = game.currentFps
	game.hud.fields["FPS_LOCK"].value = game.fpsLock
	game.hud.fields["PATH_LEN"].value = len(game.kana.targetQue)
	game.hud.fields["FOOD"].value = 0
	game.hud.fields["EGGS"].value = 0
	game.hud.fields["TIME"].value = round((time.time() * 1000 - game.initTime) / 1000)

def printStatusLog():
	x, y = screenPosToTilePos(game.kana, game.tileMap, game.kana.location)
	print("TME:{0:15} POS:{1}x{2:6} FPS:{3:6} CPU:{4}%{6:4} PATH:{5}".format(
			str(round(time.time() * 1000 - game.initTime)),
			str(round(x)),
			str(round(y)),
			str(game.currentFps),
			psutil.cpu_percent(),
			str(len(game.kana.targetQue)),
			""
		)
	)

def renderInOrder():
	pygame.display.set_caption("Kanapeli II v{} State: {}".format(VERSION, game.kana.state))
	game.moveChicken()
	if game.kana.state == "BLOCKED":
		game.kana.hitReaction()
	game.renderLowTiles()
	game.renderFood()
	game.renderChicken()
	game.renderHighTiles()
	# game.renderPath()
	updateHUD()
	game.hud.render()
	pygame.display.flip()
	renderedMsAgo = time.time() * 1000 - game.lastRenderTime
	game.currentFps = "{:.1f}".format(1000 / renderedMsAgo)
	game.lastRenderTime = time.time() * 1000

game = Game()
pygame.event.get()
pygame.display.set_caption("Kanapeli II v{}".format(VERSION))

timedActions = {
	# "CONSOLE_LOG":
	# 	TimedAction(
	# 		1000,
	# 		printStatusLog,
	# 	)
}

while game.running:
	game.handleEvents()
	renderInOrder()

	for a in timedActions:
		timedActions[a].activate()

	game.clock.tick(game.fpsLock)

pygame.quit()
print("QUIT BYE")