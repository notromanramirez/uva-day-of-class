# Roman Ramirez
# rr8rk@virginia.edu

# PIP requirements
# pip install num2words

from num2words import num2words
from datetime import date

# the date of the start of class
START = date(2021, 8, 24)
def main():

	# get today's date
	today = date.today()

	# determine the difference in days
	delta = (today - START).days + 1

	# convert what day of class it is into english
	ordinalDelta = num2words(delta, lang='en', to='ordinal')
	
	# print the message
	print("Happy %sdoc!" % ordinalDelta[0])


if __name__ == '__main__':
	main()