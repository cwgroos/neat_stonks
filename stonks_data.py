from __future__ import print_function
import os
import csv

class stonks_data:

	def __init__(self, path):
		self.path = path
		self.start = 0
		self.csv = csv.reader(open(path, 'rb'))

	def set_window_start(self, start):
		self.start = self.start + start

	def get_next_state(self):
		return self.csv.next() 