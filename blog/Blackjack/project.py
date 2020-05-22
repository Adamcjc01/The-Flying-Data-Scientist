import random
from time import sleep

def makeDeck():
	#Create a new list of 52 cards
	#First just make numbered cards 1- 10 and face cards Ace, Jack, Queen, King
	new_deck = []
	faces = ['A','J','Q','K']
	new_deck.extend(list(range(1,11)))
	new_deck.extend(faces)
	#set the number of required decks
	no_of_decks = 1
	#Multiply the number of decks by 4 to represent the 52 cards in a deck
	new_deck = new_deck*(no_of_decks*4)

	return new_deck

def dealCard(Deck):
	card = Deck.pop()
	return card

def calculateScore(hand):
	#intialise total and aces
	total = 0
	aces = 0

	#check each card, if a face then add 10, else add card number
	#if an ace, add to the ace count
	for card in hand:
		if card in ['K','Q','J']:
			total += 10
		elif card in ['A']:
			aces += 1
		else:
			total += card
	#first add aces at their lowest value (1)
	total = total + aces

	#then check to see if we should 'upgrade aces' to 11

	while total + 10 < 22 and aces != 0:
		total += 10
		aces - 1

	return total

def writeScore(number_of_games, running_total):
	file_name = "./score.txt"
	with open(file_name, 'w') as fn:
		fn.write("{}:{}".format(number_of_games,running_total))

def loadScore():
	file_name = "./score.txt"
	total_and_wins = []
	try:
		with open(file_name, 'r') as fn:
			total_and_wins = fn.read().split(":")
	except FileNotFoundError:
		pass
	return total_and_wins

def game(Deck, running_total,number_of_games):
		#initialise first cards
		player_card_list = []
		player_card_list.append(dealCard(Deck))

		dealer_score = 0
		dealer_card_list = []
		dealer_card_list.append(dealCard(Deck))
		dealer_card_list.append(dealCard(Deck))
		dealer_score = calculateScore(dealer_card_list)

		print("""You have drawn {}
			The dealer has drawn {}
			The dealer's current score is {}"""\
		.format(player_card_list[-1], dealer_card_list, dealer_score))

		if dealer_score == 21:
			print("The dealer has a blackjack! You lose\nCurrent wins = {}\nCurrent losses = {}\nWin/Lose ratio = {:.3%}"\
			.format(running_total, number_of_games - running_total, running_total/number_of_games))
			return False

		#run the player's hand
		player_score = 0
		tmp = None
		while tmp != ('n' or 'N'):
			tmp = input("Hit y/n?")
			sleep(0.5)
			if tmp == ('y' or 'Y'):
				player_card_list.append(dealCard(currentDeck))
				player_score = calculateScore(player_card_list)
				print("""You have drawn a {}
					Cards in your hand are: {}
					Your current score is {}"""\
				.format(player_card_list[-1], player_card_list,player_score))
				
			if player_score > 21:
				print("You have gone bust!\nCurrent wins = {}\nCurrent losses = {}\nWin/Lose ratio = {:.3%}"\
				.format(running_total, number_of_games - running_total, running_total/number_of_games))
				return False

			if player_score == 21:
				print("BLACKJACK! You win\nCurrent wins = {}\nCurrent losses = {}\nWin/Lose ratio = {:.3%}"\
				.format(running_total, number_of_games - running_total, running_total/number_of_games))
				return True

		sleep(0.5)
		#Run the dealer's turn
		while dealer_score < 18:
			dealer_card_list.append(dealCard(Deck))
			dealer_score = calculateScore(dealer_card_list)
			print("""The dealer has drawn {}
					Cards in the dealer's hand are: {}
					The dealer's current score is {}"""\
				.format(dealer_card_list[-1], dealer_card_list,dealer_score))
			sleep(0.5)
		

		if dealer_score > 21:
			running_total += 1
			print("You win!\nCurrent wins = {}\nCurrent losses = {}\nWin/Lose ratio = {:.3%}"\
				.format(running_total, number_of_games - running_total, running_total/number_of_games))
			return True
		elif player_score > dealer_score:
			running_total += 1
			print("You win!\nCurrent wins = {}\nCurrent losses = {}\nWin/Lose ratio = {:.3%}"\
				.format(running_total, number_of_games - running_total, running_total/number_of_games))
			return True
		else:
			print("You Lose!\nCurrent wins = {}\nCurrent losses = {}\nWin/Lose ratio = {:.3%}"\
				.format(running_total, number_of_games - running_total, running_total/number_of_games))
			return False
		
def autoGame(Deck, running_total,number_of_games):
	#initialise first cards
	player_card_list = []
	player_card_list.append(dealCard(Deck))

	dealer_score = 0
	dealer_card_list = []
	dealer_card_list.append(dealCard(Deck))
	dealer_card_list.append(dealCard(Deck))
	dealer_score = calculateScore(dealer_card_list)

	if dealer_score == 21:
		print("The dealer has a blackjack! You lose\nCurrent wins = {}\nCurrent losses = {}\nWin/Lose ratio = {:.3%}"\
		.format(running_total, number_of_games - running_total, running_total/number_of_games))
		return False

	#run the player's hand
	player_score = 0

	while player_score < 16:
		player_card_list.append(dealCard(currentDeck))
		player_score = calculateScore(player_card_list)	
		if player_score > 21:
			print("You have gone bust!\nCurrent wins = {}\nCurrent losses = {}\nWin/Lose ratio = {:.3%}"\
			.format(running_total, number_of_games - running_total, running_total/number_of_games))
			return False
		if player_score == 21:
			print("BLACKJACK! You win\nCurrent wins = {}\nCurrent losses = {}\nWin/Lose ratio = {:.3%}"\
			.format(running_total, number_of_games - running_total, running_total/number_of_games))
			return True

	#Run the dealer's turn
	while dealer_score < 18:
		dealer_card_list.append(dealCard(Deck))
		dealer_score = calculateScore(dealer_card_list)
	

	if dealer_score > 21:
		running_total += 1
		print("You win!\nCurrent wins = {}\nCurrent losses = {}\nWin/Lose ratio = {:.3%}"\
			.format(running_total, number_of_games - running_total, running_total/number_of_games))
		return True
	elif player_score > dealer_score:
		running_total += 1
		print("You win!\nCurrent wins = {}\nCurrent losses = {}\nWin/Lose ratio = {:.3%}"\
			.format(running_total, number_of_games - running_total, running_total/number_of_games))
		return True
	else:
		print("You Lose!\nCurrent wins = {}\nCurrent losses = {}\nWin/Lose ratio = {:.3%}"\
			.format(running_total, number_of_games - running_total, running_total/number_of_games))
		return False
#set up a new deck and shuffle it
print("""               ~*   Welcome to *~ 
.------..------..------..------..------..------..------..------..------.
|B.--. ||L.--. ||A.--. ||C.--. ||K.--. ||J.--. ||A.--. ||C.--. ||K.--. |
| :(): || :/\\: || (\\/) || :/\\: || :/\\: || :(): || (\\/) || :/\\: || :/\\: |
| ()() || (__) || :\\/: || :\\/: || :\\/: || ()() || :\\/: || :\\/: || :\\/: |
| '--'B|| '--'L|| '--'A|| '--'C|| '--'K|| '--'J|| '--'A|| '--'C|| '--'K|
`------'`------'`------'`------'`------'`------'`------'`------'`------' 
""")

sleep(1)

currentDeck = makeDeck()
random.shuffle(currentDeck)
length_of_deck = len(currentDeck)

continue_playing = None

number_of_games , running_total = loadScore()
number_of_games = int(number_of_games)
running_total = int(running_total) 

number_of_games +=1

auto_game = input("Run a simulation? y/n")

if auto_game == 'y':
	iteration_of_games = int(input("number of simulations?"))
	for i in range(0,iteration_of_games):
		if len(currentDeck) / length_of_deck < 0.25:
			currentDeck = makeDeck()
			random.shuffle(currentDeck)
			print("Deck is 75\% empty, shuffling in new deck")
		player_won = autoGame(currentDeck,running_total,number_of_games)
		if player_won == True: running_total += 1
		number_of_games +=1
else:
	while continue_playing != ('n' or 'N'):
		if len(currentDeck) / length_of_deck < 0.25:
			currentDeck = makeDeck()
			random.shuffle(currentDeck)
			print("Deck is 75\% empty, shuffling in new deck")
		player_won = game(currentDeck,running_total,number_of_games)
		if player_won == True: running_total += 1
		continue_playing = input("Would you like to play another game y/n?:")
		number_of_games +=1
	writeScore(number_of_games, running_total)






