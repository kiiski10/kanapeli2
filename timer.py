import time

class TimedAction:
	def __init__(self, interval, action):
		self.action = action
		self.interval = interval
		self.lastTick = time.time() * 1000

	def activate(self):
		if time.time() * 1000 - self.lastTick >= self.interval:
			self.lastTick = time.time() * 1000
			self.action()
