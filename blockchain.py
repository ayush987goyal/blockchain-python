blockchain = []


def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amout, last_transaction=[1]):
    blockchain.append([last_transaction, transaction_amout])


def get_user_input():
    return float(input('Your transaction amout please: '))


tx_amt = get_user_input()
add_value(tx_amt)

tx_amt = get_user_input()
add_value(last_transaction=get_last_blockchain_value(),
          transaction_amout=tx_amt)

tx_amt = get_user_input()
add_value(tx_amt, get_last_blockchain_value())

print(blockchain)
