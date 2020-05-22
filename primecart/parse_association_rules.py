import pickle
from itertools import combinations
import ast


def read_rules():
    # with open('rules.pickle', 'rb') as handle:
    #     rules = pickle.load(handle)
    # return rules
    with open('association_rules.txt', 'r') as f:
        temp = f.read()
        rules = ast.literal_eval(temp)
    return rules


def format_rules(rules):
    # returns [ tuple_of_cart_items, tuple_of_suggestions, float]
    new_rules = []
    for i in rules.keys():
        new_rules.append([tuple(set(tuple(map(int, i)))), tuple(tuple(set(tuple(map(int, rules[i][0]))))), rules[i][1]])
    return new_rules


def suggestions(product_list, rules):
    combination_list = []
    n = len(product_list)
    for i in range(1, n + 1):
        temp_list = list(combinations(product_list, i))
        for i in temp_list:
            combination_list.append(tuple(set(i)))
    combination_list = list(set(combination_list))
    suggestions = {}
    for combination in combination_list:
        temp_dict = search_rules(combination, new_rules)
        for i in temp_dict.keys():
            if i in suggestions.keys():
                if temp_dict[i] > suggestions[i]:
                    suggestions.update({i: temp_dict[i]})
            else:
                suggestions.update({i: temp_dict[i]})
    return suggestions


def search_rules(combination, rules):
    for rule in rules:
        if combination == rule[0]:
            temp_dict = {}
            for p in rule[1]:
                temp_dict.update({p: rule[2]})
            return temp_dict
    return {}


rules = read_rules()
new_rules = format_rules(rules)
