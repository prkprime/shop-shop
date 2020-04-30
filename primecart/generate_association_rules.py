from pymongo import MongoClient
import pyfpgrowth
import time
import pickle

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
    print(f'transactions retrived. (time taken : {round(time.time()-start_time, 4)} seconds)')
    return transaction

def get_rules(transactions):
    print('generating patterns...')
    start_time = time.time()
    patterns = pyfpgrowth.find_frequent_patterns(transactions, 400)
    print(f'patterns generated (time taken : {round(time.time()-start_time, 4)} seconds)')
    print('generating rules...')
    start_time = time.time()
    rules = pyfpgrowth.generate_association_rules(patterns, 0.7)
    print(f'rules generated (time taken : {round(time.time()-start_time, 4)} seconds)')
    return rules

rules = get_rules(get_transactions())
print('dumping rules to rules.pickle...')
start_time = time.time()
with open('rules.pickle', 'wb') as handle:
    pickle.dump(rules, handle, protocol=pickle.HIGHEST_PROTOCOL)
print(f'rules saved in rules.pickle (time taken : {round(time.time()-start_time, 4)} seconds)')
