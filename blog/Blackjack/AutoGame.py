import random

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

	
def autoGame(Deck, running_total,number_of_games,player_stick,player_stick_dtarget,dealer_target):
	#initialise first cards
	player_score = 0
	player_card_list = []
	player_card_list.append(dealCard(Deck))
	player_card_list.append(dealCard(Deck))
	player_score = calculateScore(player_card_list)

	dealer_score = 0
	dealer_card_list = []
	dealer_card_list.append(dealCard(Deck))
	dealer_score = calculateScore(dealer_card_list)

	if dealer_score < dealer_target:
		player_stick = player_stick_dtarget

	#run the player's hand
	
	while player_score < player_stick:
		player_card_list.append(dealCard(Deck))
		player_score = calculateScore(player_card_list)	
		if player_score > 21:
			return False
		if player_score == 21:
			return True

	#Run the dealer's turn
	while dealer_score < 17:
		dealer_card_list.append(dealCard(Deck))
		dealer_score = calculateScore(dealer_card_list)
	

	if dealer_score > 21:
		return True
	elif player_score > dealer_score:
		return True
	else:
		return False

def runSimulation():
	#set up a new deck and shuffle it
	print("""               ~*   Welcome to *~ 
	.------..------..------..------..------..------..------..------..------.
	|B.--. ||L.--. ||A.--. ||C.--. ||K.--. ||J.--. ||A.--. ||C.--. ||K.--. |
	| :(): || :/\\: || (\\/) || :/\\: || :/\\: || :(): || (\\/) || :/\\: || :/\\: |
	| ()() || (__) || :\\/: || :\\/: || :\\/: || ()() || :\\/: || :\\/: || :\\/: |
	| '--'B|| '--'L|| '--'A|| '--'C|| '--'K|| '--'J|| '--'A|| '--'C|| '--'K|
	`------'`------'`------'`------'`------'`------'`------'`------'`------' 
	""")

	currentDeck = makeDeck()
	random.shuffle(currentDeck)
	length_of_deck = len(currentDeck)

	number_of_games =1
	max_prob = 0

	#iteration_of_games = int(input("number of simulations?"))

	iteration_of_games = 1000
	probability_list = []

	player_stick_list = range(0,21)
	player_stick_dtarget_list = range(0,11)
	dealer_target_list = range(0,21)
	n = 0

	for j in dealer_target_list:
		for i in player_stick_list:
			for k in player_stick_dtarget_list:
				running_total = 0
				number_of_games = 0
				for iterator in range(0,iteration_of_games):
					if len(currentDeck) / length_of_deck < 0.25:
						currentDeck = makeDeck()
						random.shuffle(currentDeck)
					player_won = autoGame(currentDeck,running_total,number_of_games,i,k,j)
					if player_won == True: running_total += 1
					number_of_games +=1
				if running_total/number_of_games > max_prob:
					max_prob = running_total/number_of_games
					best_stick = i
					best_stick_dtarget = k
					best_dealer_target = j
				n += 1
				print('Working: {:.3%}'.format(n/(21*11*21)))
				#print("Player stick [{}] Player d-target [{}] Dealer target [{}] \
				 #probability is: {:.3%}".format(i,k,j,running_total/number_of_games))

	print("0 is always stick. If dealer pulls lower than target dealer value stick at dealer stick target\
	if the dealer pulls higher then stick at player target")
	print("The best always stick value : {}".format(best_stick))
	print("The best target dealer value : {}".format(best_dealer_target))
	print("The best if target dealer stick at X value: {}".format(best_stick_dtarget))
	print("The best probability : {:.3%}".format(max_prob))

if __name__ == "__main__":
	runSimulation()









