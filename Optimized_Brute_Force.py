# Intialize card
import random, copy, time
import numpy as np

class Card:
    def __init__(self, color, type):
        self.color = color
        self.type = type

    def __eq__(self, other): 
        if not isinstance(other, Card): 
            return False 
        return self.color == other.color and self.type == other.type

    def __hash__(self):
        return hash((self.color, self.type))

def initilize_deck():
    cards = []
    colors = ["Green", "Red", "Yellow", "Blue"]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    special = ["skip", "reverse"]

    # Loop through each color
    for color in colors:
        # Add 0 card once
        cards.append(Card(color, "0"))
        # Loop twice for each number and special
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
        true_index = self.turn * 7 + index
        self.cards_played.append((self.turn, new_card, true_index))

        # If change_reverse is true
        if change_reverse:
            self.reverse = not self.reverse
        
        # Set discard_card to card
        self.discard_card = new_card

        # Remove card from player
        self.all_cards[self.turn][index] = None

        # Check if player has no cards left
        count = 0
        for card in self.all_cards[self.turn]:
            if card == None:
                count = count + 1
        if count == 7:
            # End the game
            self.game_end = True
            self.winner = self.turn
        
        # Set next turn
        self.turn = next_turn

    def __eq__(self, other):
        if not isinstance(other, CardState): 
            return False
        return (
            self.discard_card == other.discard_card and 
            self.all_cards == other.all_cards and 
            self.reverse == other.reverse and
            self.turn == other.turn
        )
    def __hash__(self):
        new_list = np.array(self.all_cards)
        new_list_flat = new_list.flatten()
        return hash((self.turn, self.discard_card, tuple(list(new_list_flat)), self.reverse))

#  Intiailize the current state based on the discard pile
def intialize_state(state: CardState):
    state = copy.deepcopy(state)
    if(state.discard_card.type == 'skip'):
        # skip next player
        state.turn = state.turn + 1
        if(state.turn == state.n):
            state.turn = 0
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
        if(player[j] == None):
            continue
        card = player[j]

        # Store the values for the new state
        next_turn = state.turn
        change_reverse = False

        # Check if the card can be played
        if (state.discard_card.type == card.type or state.discard_card.color == card.color):
            new_state = copy.deepcopy(state)

            if card.type in numbers:
                if (state.reverse == False):
                    next_turn = next_turn + 1
                else:
                    next_turn = next_turn - 1
            elif card.type == "skip":
                if (state.reverse == False):
                    next_turn = next_turn + 2
                else:
                    next_turn = next_turn - 2
            elif card.type == "reverse":
                reverse = not state.reverse
                change_reverse = True
                if (reverse == False):
                    next_turn = next_turn + 1
                else:
                    next_turn = next_turn - 1
            
            if next_turn == state.n:
                next_turn = 0
            elif next_turn == state.n + 1:
                next_turn = 1
            elif next_turn == - 1:
                next_turn = state.n - 1
            elif next_turn == -2:
                next_turn = state.n - 2

            new_state.play_card(j, card,  next_turn, change_reverse)
            future_states.append(new_state)

        elif(card.type == 'Wild'):
            red_state = copy.deepcopy(state)
            yellow_state = copy.deepcopy(state)
            blue_state = copy.deepcopy(state)
            green_state = copy.deepcopy(state)

            red_card = Card("Red", "any")
            blue_card = Card("Green", "any")
            green_card = Card("Blue", "any")
            yellow_card = Card("Yellow", "any")

            if (state.reverse == False):
                next_turn = next_turn + 1
                if next_turn == state.n:
                    next_turn = 0
            else:
                next_turn = next_turn - 1
                if next_turn == -1:
                    next_turn = state.n - 1
            
            red_state.play_card(j, red_card, next_turn, False)
            blue_state.play_card(j, blue_card, next_turn, False)
            yellow_state.play_card(j, yellow_card, next_turn,  False)
            green_state.play_card(j, green_card, next_turn, False)

            future_states.append(red_state)
            future_states.append(blue_state)
            future_states.append(yellow_state)
            future_states.append(green_state)
    
    return future_states

def check_states(state1, state2):
    if state1.number_of_turns != state2.number_of_turns:
        return False
    elif state1.reverse != state2.reverse:
        return False
    elif state1.discard_card.color != state2.discard_card.color or state1.discard_card.type != state2.discard_card.type:
        return False
    else:
        for i in range(state1.n):
            if(len(state1.all_cards[i]) != len(state2.all_cards[i])):
                return False
            else:
                for j in range(len(state1.all_cards[i])):
                    if(state1.all_cards[i][j].color != state2.all_cards[i][j].color or state1.all_cards[i][j].type != state2.all_cards[i][j].type):
                        return False
        return True

def run(og_state, n):
    dp = [[([False, False] * (7 * n)) ]* (pow(2, 7 * n))]
    plays_left = n
    queue = intialize_state(og_state)
    visited = set()
    winners = [None for i in range(n)]

    while len(queue) > 0 and plays_left != 0:
        state = queue.pop(0)

        ##COMMENT THESE LINES OUT FOR WITHOUT OPTIMIZATION
        if state in visited:
           continue
        ##END COMMENT REGION
        visited.add(state)
        if(state.game_end == True):
            if(winners[state.winner] == None):
                winners[state.winner] = state
                plays_left = plays_left - 1
        else:
            new_states = update(state)
            for s in new_states:
                if s not in visited: 
                    queue.append(s)
    return winners

def main():
    # Create state
    for n in range(3, 4): # n = 4
        for seed in range(190, 191):
            print(f"Seed {seed}")
            random.seed(seed)
            og_state = CardState(n)
            og_state.shuffle()

            # Start timing
            start_time = time.time()
            winners = run(og_state, n)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time for run with seed {seed} and n={n}: {elapsed_time:.4f} seconds")

            with open(f"{seed}_{n}_results.txt", "w") as f:
                for i in range(n):
                    f.write(f"Player {i}\n")
                    for card in og_state.all_cards[i]:
                        f.write(f"Card {card.color} {card.type}\n")
                    f.write("\n")
                f.write(f"Discard Card {og_state.discard_card.color} {og_state.discard_card.type}\n\n")
                
                for i in range(n):
                    if(winners[i] != None):
                        f.write(f"Winner for Player {i}\n")
                        f.write(f"Number of turns {winners[i].number_of_turns}\n")
                        for turn in winners[i].cards_played:
                            f.write(f"Player {turn[0]} Card {turn[1].color} {turn[1].type}\n")

if __name__ == '__main__':
    main()
