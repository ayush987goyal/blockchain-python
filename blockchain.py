# Initializing our blockchain list
blockchain = []


def get_last_blockchain_value():
    ''' Returns the last value of the current blockchain.
    '''
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    ''' Appends a new value as well as last value to the current blockchain

    Arguments:
        :transaction_amount: The amount that should be added.
        :last_transaction: The last blockchain transaction (default [1]).
    '''
    blockchain.append([last_transaction, transaction_amount])


def get_user_input():
    return float(input('Your transaction amout please: '))


tx_amt = get_user_input()
add_value(tx_amt)

tx_amt = get_user_input()
add_value(last_transaction=get_last_blockchain_value(),
          transaction_amount=tx_amt)

tx_amt = get_user_input()
add_value(tx_amt, get_last_blockchain_value())

print(blockchain)
