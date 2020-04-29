from pymongo import MongoClient
import pyfpgrowth

def get_transactions():
    DATABASE = MongoClient()['primecart']
    purchase_data = DATABASE.PurchaseData.find()
    transaction_dict = {}
    for i in purchase_data:
        if i['InvoiceId'] in transaction_dict:
            single_transaction = transaction_dict[i['InvoiceId']]
            single_transaction.append(i['ProductId'])
            transaction_dict[i['InvoiceId']] = single_transaction
        else:
            single_transaction = []
            single_transaction.append(i['ProductId'])
            transaction_dict[i['InvoiceId']] = single_transaction
    transaction = list(transaction_dict.values())
    return transaction

def get_rules(transactions):
    print('transactions retrived')
    print('generating patterns...')
    patterns = pyfpgrowth.find_frequent_patterns(transactions, 400)
    print('patterns generated')
    print('generating rules...')
    return pyfpgrowth.generate_association_rules(patterns, 0.7)
    print('rules generated...')

with open('rules.txt', 'w') as f:
    f.write(str(get_rules(get_transactions())))
