from pymongo import MongoClient
import pyfpgrowth
import time

def get_transactions():
    print('retriving transactions from database')
    start_time = time.time()
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
    transaction2 = []
    for i in transaction:
        single_transaction = []
        for j in i:
            try:
                temp = int(j)
                single_transaction.append(temp)
            except ValueError:
                pass
            except TypeError:
                pass
        if len(single_transaction) != 0:
            transaction2.append(single_transaction)
    print(transaction2[0])
    print(type(transaction2[0][0]))
    print(f'transactions retrived. (time taken : {round(time.time()-start_time, 4)} seconds)')
    return transaction

def get_rules(transactions):
    print('generating patterns...')
    patterns = pyfpgrowth.find_frequent_patterns(transactions, 40)
    print('patterns generated')
    print('generating rules...')
    return pyfpgrowth.generate_association_rules(patterns, 0.7)
    print('rules generated...')

with open('rules.txt', 'w') as f:
    f.write(str(get_rules(get_transactions())))
