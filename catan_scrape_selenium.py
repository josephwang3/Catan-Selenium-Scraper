# this program analyzes a Catan game from colonist.io to keep a continually updated analysis of each player's cards

from selenium import webdriver
"""
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
"""
# for setting an idle timer
import time
# for making deep copies
import copy

# cards dictionary with players as keys and cards as list values
# example cards: {'Joseph4499': ['grain', 'wool', 'lumber', 'brick', 'ore'], 'Lopez': ['grain', 'wool', 'wool', 'brick']}
cards = {}
items = {
    'road': ['brick', 'lumber'], 
    'settlement': ['brick', 'grain', 'lumber', 'wool'], 
    'city': ['grain', 'grain', 'ore', 'ore', 'ore'], 
    'development card': ['grain', 'ore', 'wool']
}

def main():
    # for measuring runtime
    start_time = time.time()
    last_time = time.time()

    passcode = 'SqOv'

    # initialize webdriver, ignore certificate and ssl errors
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    #options.add_argument('--headless')
    #options.add_argument('--no-sandbox')
    #options.add_argument('--disable-gpu')
    #options.headless = True
    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(PATH, options=options)

    # open the Catan game
    driver.get('https://colonist.io/#' + passcode)
    print(driver.title)

    # wait 60 seconds
    time.sleep(45)
    print()
    print("Done sleeping!")

    # print total and incremental runtime
    print()
    print(round(time.time() - start_time, 2))
    print(round(time.time() - last_time, 2))
    last_time = time.time()
    print()


    # get the overall game chat
    game_chat = driver.find_element_by_id('game-log-text')
    messages = game_chat.find_elements_by_class_name('message_post')

    print()
    print(round(time.time() - start_time, 2))
    print(round(time.time() - last_time, 2))
    last_time = time.time()
    print()

    # process the messages once
    process_messages(messages)
    print_cards()

    # save previous messages
    prev_messages = messages

    print()
    print(round(time.time() - start_time, 2))
    print(round(time.time() - last_time, 2))
    last_time = time.time()
    print()

    # loop through and poll the game chat every 3 seconds, maximum 50 minutes
    for i in range(5000):
        time.sleep(3)

        game_chat = driver.find_element_by_id('game-log-text')
        messages = game_chat.find_elements_by_class_name('message_post')

        # only process new messages
        if len(messages[len(prev_messages):]) != 0:
            process_messages(messages[len(prev_messages):])

        prev_messages = messages

        print_cards()

        print()
        print(round(time.time() - start_time, 2))
        print(round(time.time() - last_time, 2))
        last_time = time.time()
        print()

    driver.quit()

# function to return the number of +1's, -1's, other cards, and total cards for each player
def number_cards():
    reduced_cards = copy.deepcopy(cards)
    number_cards = {}

    for player in cards:
        # count +1's and -1's
        positive_mystery_cards = cards[player].count('+1')
        negative_mystery_cards = cards[player].count('-1')

        # count other cards
        while '-1' in reduced_cards[player]:
            reduced_cards[player].remove('-1')
        while '+1' in reduced_cards[player]:
            reduced_cards[player].remove('+1')
        other_cards = len(reduced_cards[player])

        # calculate total apparent number of cards (counting +1's and -1's as cards)
        fake_total_cards = len(cards[player])

        # calculate total actual number of cards
        total_cards = other_cards + positive_mystery_cards - negative_mystery_cards

        # create dictionary with player, number of +1's, -1's, other cards, total apparent cards, and total actual cards, e.g. {'Joseph': [1, 2, 3, 6, 2]}
        number_cards[player] = [positive_mystery_cards, negative_mystery_cards, other_cards, fake_total_cards, total_cards]

    return number_cards

# function to print out each player's number of cards and the cards in their hand
def print_cards():

    # get the numbers of cards from the number_cards function
    number_cards_dict = number_cards()

    for player in number_cards_dict:
        # print player, number of cards, and actual cards of player (with +1's and -1's)
        print(player, number_cards_dict[player][-1], cards[player])

# cleans cards from +1's and -1's when possible
def clean_cards():

    # get the numbers of cards from the number_cards function
    # each value contains number of +1's, -1's, other cards, total apparent cards, and total actual cards
    number_cards_dict = number_cards()

    for player in number_cards_dict:

        # extract data from dictionary from number_cards function
        positive_cards, negative_cards, other_cards, fake_total_cards, total_cards = number_cards_dict[player]

        # if total cards equals 0 and there are apparent cards, delete all cards (cancel out -1's and other cards)
        if total_cards == 0 and fake_total_cards > 0:
            cards[player] = []
            #print_cards()
        
        # if number of +1's greater than total cards and apparent cards greater than total cards, simplify to only +1's
        elif positive_cards >= total_cards and fake_total_cards > total_cards:
            cards[player] = ['+1' for x in range(total_cards)]
            #print_cards()

# function to process messages
def process_messages(messages):

    # initialize the first previous message for trades
    prev_message = messages[0]

    # iterate through each message
    for message in messages:

        print(message.text)

        # initialize players
        if "turn to place" in message.text:
            player = message.text.split()[0]
            cards[player] = []

            #print_cards()

        # add cards to each player's hand as they are gotten
        elif "got" in message.text:
            player = message.text.split()[0]

            resources_msgs = message.find_elements_by_class_name('lobby-chat-text-icon')
            for resource_msg in resources_msgs:
                cards[player].append(resource_msg.get_attribute('alt'))

            cards[player].sort()
            #print_cards()

        # remove cards from player's hand based on what they built
        elif "built" in message.text or "bought" in message.text:
            player = message.text.split()[0]

            item = message.find_element_by_class_name('lobby-chat-text-icon').get_attribute('alt')
            for resource in items[item]:
                if resource in cards[player]:
                    cards[player].remove(resource)
                # if card not in their hand but they have a +1, assume the +1 is the card they need and remove it
                elif resource not in cards[player] and '+1' in cards[player]:
                    cards[player].remove('+1')

            #print_cards()
            clean_cards()
        
        # for robber, add 1 card to robber player and remove 1 card from robbed player
        elif "stole from" in message.text:
            player_robber = message.text.split()[0]
            player_robbed = message.text.split()[-1]

            cards[player_robber].append('+1')
            cards[player_robbed].append('-1')
            
            cards[player_robber].sort()
            cards[player_robbed].sort()

            #print_cards()
            clean_cards()

        # if initiating trade, save trade initiation in case of actual trade
        elif "wants to give" in message.text:
            prev_message = message
        
        # if actual trade, exchange the trade items
        elif "traded" in message.text:
            player_giver = message.text.split()[0]
            player_receiver = message.text.split()[-1]

            # all resources exchanged
            resources_msgs = prev_message.find_elements_by_class_name('lobby-chat-text-icon')
            
            # assumes that the receiver only trades away one resource
            resource_receiver = resources_msgs[-1].get_attribute('alt')
            del resources_msgs[-1]

            # the giver may trade away multiple resources
            resources_giver = []
            for resource_msg in resources_msgs:
                resources_giver.append(resource_msg.get_attribute('alt'))
            
            # adjust the cards for the resource given away by the receiver
            cards[player_giver].append(resource_receiver)
            if resource_receiver in cards[player_receiver]:
                cards[player_receiver].remove(resource_receiver)
            # if card not in their hand but they have a +1, assume the +1 is the card they need and remove it
            elif resource_receiver not in cards[player_receiver] and '+1' in cards[player_receiver]:
                cards[player_receiver].remove('+1')

            # adjust the cards for the resource(s) given away by the giver
            for resource in resources_giver:
                cards[player_receiver].append(resource)
                if resource in cards[player_giver]:
                    cards[player_giver].remove(resource)
                # if card not in their hand but they have a +1, assume the +1 is the card they need and remove it
                elif resource not in cards[player_giver] and '+1' in cards[player_giver]:
                    cards[player_giver].remove('+1')

            cards[player_giver].sort()
            cards[player_receiver].sort()

            #print_cards()
        
        # if changing cards with bank, add changed card and remove other cards
        elif "gave bank" in message.text:
            player = message.text.split()[0]

            resources_msgs = message.find_elements_by_class_name('lobby-chat-text-icon')
            cards[player].append(resources_msgs[-1].get_attribute('alt'))
            del resources_msgs[-1]

            for resource_msg in resources_msgs:
                resource = resource_msg.get_attribute('alt')
                if resource in cards[player]:
                    cards[player].remove(resource)
                # if card not in their hand but they have a +1, assume the +1 is the card they need and remove it
                elif resource not in cards[player] and '+1' in cards[player]:
                    cards[player].remove('+1')

            cards[player].sort()

            #print_cards()
            clean_cards()

        # if discarding cards, remove those discarded cards from that player's hand
        elif "discarded" in message.text:
            player = message.text.split()[0]

            resources_msgs = message.find_elements_by_class_name('lobby-chat-text-icon')
            for resource_msg in resources_msgs:
                resource = resource_msg.get_attribute('alt')
                if resource in cards[player]:
                    cards[player].remove(resource)
                # if card not in their hand but they have a +1, assume the +1 is the card they need and remove it
                elif resource not in cards[player] and '+1' in cards[player]:
                    cards[player].remove('+1')
                
            #print_cards()
            clean_cards()

        # for year of plenty, add corresponding cards to player's hand
        elif "took from bank" in message.text:
            player = message.text.split()[0]

            resources_msgs = message.find_elements_by_class_name('lobby-chat-text-icon')
            for resource_msg in resources_msgs:
                cards[player].append(resource_msg.get_attribute('alt'))

            cards[player].sort()
            
            #print_cards()
        
        # for monopoly, remove cards from everyone else's hands and add to monopoly player
        elif "stole all of" in message.text:
            # get player
            player = message.text.split()[0]

            # get resource that monopoly was played on
            resource = message.find_elements_by_class_name('lobby-chat-text-icon')[-1].get_attribute('alt')
            resource_count = 0

            # remove that resource from other players and count total stolen
            for other_player in cards:
                while resource in cards[other_player]:
                    cards[other_player].remove(resource)
                    resource_count += 1
            
            # add that number of that resource to monopoly player's hand
            for i in range(resource_count):
                cards[player].append(resource)
            
            cards[player].sort()
            #print_cards()
            clean_cards()


if __name__ == '__main__':
    main()

    """
    # test case
    cards = {'Joseph': ['-1', '-1', '+1', '+1', 'ore'], 'Max': ['+1', 'ore']}

    print(number_cards())
    print()
    print_cards()
    print()

    clean_cards()
    print()

    print(number_cards())
    print()
    print_cards()
    print()
    """



"""
try:
    game_chat = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'game-log-text'))
    )
    print(game_chat.text)

    messages = game_chat.find_elements_by_class_name('message_post')
    for message in messages:
        if "turn to place" in message.text:
            cards[message.text.split()[0]] = []
            print(cards)

finally:
    driver.quit()

"""