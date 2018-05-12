from functools import reduce
import hashlib
from collections import OrderedDict
import json
import pickle

from hash_util import hash_string_256, hash_block
from block import Block

# The reward we give to miners
MINING_REWARD = 10

# Initializing our (empty) blockchain list
blockchain = []
# Unhandled transactions
open_transactions = []
# We are the owner of this blockchain node, hence this is our identifier (e.g. for sending coins)
owner = 'Ayush'
# Registered participants: Ourself + other people sending/ receiving coins
participants = {'Ayush'}


def load_data():
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode='r') as f:
            # file_content = pickle.loads(f.read())
            file_content = f.readlines()

            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']

            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [OrderedDict(
                    [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]
                updated_block = Block(
                    block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain

            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = OrderedDict(
                    [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except (IOError, IndexError):
        # Our starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing our (empty) blockchain list
        blockchain = [genesis_block]
        # Unhandled transactions
        open_transactions = []
    finally:
        print('Cleanup')


load_data()


def save_data():
    try:
        with open('blockchain.txt', mode='w') as f:
            saveable_chain = [block.__dict__ for block in blockchain]
            f.write(json.dumps(saveable_chain))
            f.write('\n')
            f.write(json.dumps(open_transactions))
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving failed!')


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    """Calculate and return the balance for a participant.

    Arguments:
        :participant: The person for whom to calculate the balance.
    """
    tx_sender = [[tx['amount'] for tx in block.transactions
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx['amount'] for tx in block.transactions
                     if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    return amount_recieved - amount_sent


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def verify_transaction(transaction):
    """Verify a transaction by checking whether the sender has sufficient coins.

    Arguments:
        :transaction: The transaction that should be verified.
    """
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Appends a new value as well as last value to the current blockchain

    Arguments:
        :recipient: The recipient of the coins.
        :sender: The sender of the coins.
        :amount: The amount of coins sent with the transaction (default = 1.0)
    """
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False


def mine_block():
    """Create a new block and add open transactions to it."""
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()

    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    reward_transaction = OrderedDict(
        [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True


def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float. """
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amout please: '))
    return tx_recipient, tx_amount


def get_user_choice():
    """Prompts the user for its choice and return it."""
    return input('Your choice: ')


def print_blockchain_elements():
    """ Output all blocks of the blockchain """
    for block in blockchain:
        print('Outputting block')
        print(block)
    else:
        print('_' * 20)


def verify_chain():
    """ Verify the current blockchain and return True if it's valid, False if not """
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue

        if block.previous_hash != hash_block(blockchain[index-1]):
            return False

        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print('Proof of work is invalid')
            return False

    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

# A while loop for the user input interface
# It's a loop that exits once waiting_for_input becomes False or when break is called
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check transaction validity')
    print('q: Quit')
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print(open_transactions)

    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()

    elif user_choice == '3':
        print_blockchain_elements()

    elif user_choice == '4':
        print(participants)

    elif user_choice == '5':
        if verify_transactions():
            print('All transaction are valid')
        else:
            print('There are invalid transactions')

    elif user_choice == 'q':
        waiting_for_input = False

    else:
        print('Input was invalid, please pick a value from the list!')

    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
    print('Balance of {}: {:6.2f}'.format(owner, get_balance(owner)))
else:
    print('User left!')

print('Done!')
