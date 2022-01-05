# Roman Ramirez, rr8rk@virginia

### IMPORTS ###

import tweepy
from datetime import date
from time import gmtime, strftime, sleep

### CONSTANT TWITTER VARIABLES ###

CONSUMER_KEY = 'ujHGRaBaMknZmgtTEVZZ2IzQL'
CONSUMER_SECRET = 'ZD3EyzNvWsaacYZwQQbd1TR23y2eUomb7ZAc8UPG3eJKniGQIM'

ACCESS_KEY = '1478768806197616642-D7BFHeErEXV5t5NJg2PlxZdj6B4X6A'
ACCESS_SECRET = 'ANieAG7dfN30MMKnunVWbezODhtH7H6m9uu5xroslbpoX'

### SETTING UP TWITTER API ###

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

### SCRIPT ###

# a function that sends a message
def send_tweet(txt_path):
	today = str(date.today())

	message_to_send = ''
	with open(txt_path, 'r') as f:
		for line in f:
			clean_line = line.strip('\n')
			day, message = clean_line.split(' | ')
			if day == today:
				message_to_send = message

	print(message_to_send)
	api.update_status(status=message_to_send)


# run forever
def main():
	while True:

		# the time to tweet an update
		TIME_TO_TWEET = "18:00"
		# TIME_TO_TWEET = '13:00'

		# store the current time
		current_time = strftime('%H:%M', gmtime())

		print(f"It is now {current_time}.")

		# send a tweet if it's time to send one
		if (current_time == TIME_TO_TWEET):
			send_tweet('output.txt')
		# otherwise wait
		else:
			print(f"It isn't time to send a tweet yet. A tweet will be sent at {TIME_TO_TWEET}.")

		sleep(59)


if __name__ == '__main__':
	main()
	# send_tweet('output.txt')
