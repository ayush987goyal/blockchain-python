# Initializing our blockchain list
blockchain = []


def get_last_blockchain_value():
    ''' Returns the last value of the current blockchain.
    '''
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction=[1]):
    ''' Appends a new value as well as last value to the current blockchain

    Arguments:
        :transaction_amount: The amount that should be added.
        :last_transaction: The last blockchain transaction (default [1]).
    '''
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    return float(input('Your transaction amout please: '))


def get_user_choice():
    return input('Your choice: ')


def print_blockchain_elements():
    # Output the blockchain list to the console
    for block in blockchain:
        print('Outputting block')
        print(block)
    else:
        print('_' * 20)


def verify_chain():
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break

    return is_valid


waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_amt = get_transaction_value()
        add_transaction(tx_amt, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) > 0:
            blockchain[0] = [2]
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')

    if not verify_chain():
        print('Invalid blockchain!')
        break
else:
    print('User left!')

print('Done!')
