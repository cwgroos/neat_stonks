from __future__ import print_function
import neat
import numpy as np

class stonks_bot:

	def __init__(self, genome, config, initial_money, data):
		self.genome = genome
		self.config = config
		self.money = initial_money
		self.nn = neat.nn.FeedForwardNetwork.create(genome, config)
		self.data = data
		self.stocks = 0

	def take_action(self):

		# Feed Forward and determine whether to amount/sell
		
		# Grab the state of the data for this portion of the action window
		state = self.data.get_next_state()
		print("STATE IS: ",state)
		state = map(float, state)	
		prediction = self.nn.activate(state[2:])
		action = np.argmax(prediction[:-1])

		print(prediction)	
		
		amount = int(prediction[-1])
		price = state[3]	
		if amount > 2:
			amount = 2
		elif amount < 1:
			amount = 1
		cost = amount * price
		print("BOT IS: ACTION: %d, AMOUNT: %d, PRICE: %d\n" % (action, amount, price))
		if action == 0:
			if cost > self.money:
				cost = self.money 
				amount = self.money * price
			self.money = self.money - cost
			self.stocks = self.stocks + amount
		elif action == 1:
			if self.stocks < amount:
				amount = self.stocks
				cost = amount * price
			self.money = self.money + cost
			self.stocks = self.stocks - amount
		return self.money
		
