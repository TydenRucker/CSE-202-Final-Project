# Intialize card
import random
import copy
class Card:
    def __init__(self, color, type):
        self.color = color
        self.type = type

def initilize_deck():
    cards = []

    colors = ["Green", "Red", "Yellow", "Blue"]

    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    special = ["skip", "reverse"]

    # Loop through each color
    for color in colors:
        # Add 0 card once
        cards.append(Card(color, "0"))

        # Loop twice for each number and sepcial
        for type in (numbers[1:] + special):
            cards.append(Card(color, type))
            cards.append(Card(color, type))
        
    # Add four wild cards
    for i in range(4):
        cards.append(Card("Wild", "Wild"))
    
    # Returns cards
    return cards


class CardState:
    def __init__(self, n):
        self.n = n
        self.all_cards = []
        self.discard_card = None
        self.cards_played = []
        self.number_of_turns = 0
        self.turn = 0
        self.game_end = False
        self.winner = None
        self.reverse = False

    def shuffle(self):
        self.all_cards = []
        self.discard_card = None
        self.cards_played = []
        self.number_of_turns = 0
        self.turn = 0
        self.game_end = False
        self.winner = None
        self.reverse = False

        deck = initilize_deck()
        cards = random.sample(deck, (self.n * 7) + 1)

        index = 0
        for i in range(self.n):
            player = []
            for j in range(7):
                player.append(cards[index])
                index = index + 1
            self.all_cards.append(player)
        self.discard_card = cards[-1]

    def play_card(self, index, new_card, next_turn, change_reverse):
        # Increase number of turns by 1
        self.number_of_turns = self.number_of_turns + 1

        # Add cards_played
        self.cards_played.append((self.turn, new_card))

        # If change_reverse is true
        if change_reverse:
            self.reverse = not self.reverse
        
        # Set discard_card to card
        self.discard_card = new_card

        # Remove card from player
        del self.all_cards[self.turn][index]
        #self.all_cards[player].pop(index)

        # If all_Cards[player] is 0
        if len(self.all_cards[self.turn]) == 0:
            # End the game
            self.game_end = True
            self.winner = self.turn
        
        # Set next turn to be self.turn
        self.turn = next_turn

#  Intiailize the current state based on the discard pile
def intialize_state(state: CardState):
    # If the discard card is reverse
    state = copy.deepcopy(state)
    if(state.discard_card.type == 'skip'):
        # Set the state's next turn to be next_turn +1
        state.turn = state.turn + 1
        
        # If state.turn is n
        if(state.turn == state.n):
            # Set turn to be 1
            state.turn = 0
        
        # Return state
        return [state]
    elif(state.discard_card.type == 'reverse'):
        # Set reverse to be true
        state.reverse = True
        state.turn = state.n - 1
        return [state]
    elif(state.discard_card.type == 'Wild'):
        # Make 4 copies of current state 
        red_state = copy.deepcopy(state)
        yellow_state = copy.deepcopy(state)
        blue_state = copy.deepcopy(state)
        green_state = copy.deepcopy(state)

        # Create 4 possible cards
        red_card = Card("Red", "any")
        blue_card = Card("Green", "any")
        green_card = Card("Blue", "any")
        yellow_card = Card("Yellow", "any")

        green_state.discard_card = green_card
        red_state.discard_card = red_card
        yellow_state.discard_card = yellow_card
        blue_state.discard_card = blue_card
     

        return [red_state, yellow_state, blue_state, green_state]
    else:
        return [state]

# Return a list of states
def update(state: CardState):
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # Get the player
    player = state.all_cards[state.turn]

    # Create list of states  
    future_states = []
    
    # Go through each card in player
    for j in range(len(player)):
        card = player[j]

        # Store the values for the new state
        next_turn = state.turn
        change_reverse = False

        # Check if the card can be played
        # If the card matches if color or type 
        if (state.discard_card.type == card.type or state.discard_card.color == card.color):
            # Make copy of current state 
            new_state = copy.deepcopy(state)
            # If card.type is a number type 

            if card.type in numbers:
                # If reverse
                if (state.reverse == False):
                    next_turn = next_turn + 1
                else:
                    next_turn = next_turn - 1
            # Otherwise if skard is a skip type
            elif card.type == "skip":
                # If reverse
                if (state.reverse == False):
                    next_turn = next_turn + 2
                else:
                    next_turn = next_turn - 2
            # Otherwise if card type is reverse
            elif card.type == "reverse":
                # Update reverse 
                reverse = not state.reverse
                change_reverse = True

                # If reverse if alse
                if (reverse == False):
                    next_turn = next_turn + 1
                else:
                    next_turn = next_turn - 1
            
            if next_turn == state.n:
                next_turn = 0
            elif next_turn == state.n + 1:
                next_turn = 0
            elif next_turn == - 1:
                next_turn = state.n - 1
            elif next_turn == -2:
                next_turn = state.n - 2

            # Update new_state 
            new_state.play_card(j, card,  next_turn, change_reverse)

            # Add the state to future states
            future_states.append(new_state)

        # If the card type is wild
        elif(card.type == 'Wild'):
            # Make 4 copies of current state 
            red_state = copy.deepcopy(state)
            yellow_state = copy.deepcopy(state)
            blue_state = copy.deepcopy(state)
            green_state = copy.deepcopy(state)

            # Create 4 possible cards
            red_card = Card("Red", "any")
            blue_card = Card("Green", "any")
            green_card = Card("Blue", "any")
            yellow_card = Card("Yellow", "any")

            # Update turn
            if (state.reverse == False):
                next_turn = next_turn + 1
                if next_turn == state.n:
                    next_turn = 0
            else:
                next_turn = next_turn - 1
                if next_turn == -1:
                    next_turn = state.n - 1
            
            # Update each state
            red_state.play_card(j, red_card, next_turn, False)
            blue_state.play_card(j, blue_card, next_turn, False)
            yellow_state.play_card(j, yellow_card, next_turn,  False)
            green_state.play_card(j, green_card, next_turn, False)

            # Add all cards to future_states
            future_states.append(red_state)
            future_states.append(blue_state)
            future_states.append(yellow_state)
            future_states.append(green_state)
    
    # If the number of states created is greater than 0
    return future_states

def run(og_state, n):
    plays_left = n
    # Keep track of a queue
    queue = intialize_state(og_state)

    # Keep track of all winners
    winners = [None for i in range(n)]

    # Run until queue isn't empty
    while len(queue) > 0 and plays_left != 0:
        # Pop the first element of queue
        print(len(queue))
        state = queue.pop(0)

        # If the state is winner
        if(state.game_end == True):
            # Add state to winners
            if(winners[state.winner] == None):
                winners[state.winner] = state
                plays_left = plays_left - 1
        else:
            # Get new states
            new_states = update(state)

            # Add new state to state
            for state in new_states:
                queue.append(state)
    return winners

"""
winners = run(10, 10)
for winner in winners:
    if winner != None:
        print(f"{winner.number_of_turns} {len(winner.cards_played)} {winner.winner}")
        for turn in winner.cards_played:
            print(f"Player {turn[0]} Card {turn[1].color} {turn[1].type}")
"""


def main():
    # Create state
    n = 3
    seed = 100


    # Run
    for n in range(3,4):
        for seed in range(190, 191):
            print(f"Seed {seed}")
            random.seed(seed)
            og_state = CardState(n)
            og_state.shuffle()
            with open(f"{seed}_{n}_results.txt", "w") as f:
                for i in range(n):
                    f.write(f"Player {i}\n")

                    for card in og_state.all_cards[i]:
                        f.write(f"Card {card.color} {card.type}\n")
                    f.write("\n")
                f.write(f"Discard Card {og_state.discard_card.color} {og_state.discard_card.type}\n\n")
                winners = run(og_state, n)
                for i in range(n):
                    if(winners[i] != None):
                        f.write(f"Winner for Player {i}\n")
                        f.write(f"Number of turns {winners[i].number_of_turns}\n")
                        for turn in winners[i].cards_played:
                            f.write(f"Player {turn[0]} Card {turn[1].color} {turn[1].type}\n")

main()




    




            
            






        

