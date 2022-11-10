# Given a set of numbers, return the additive inverse of each. Each positive becomes negatives, and the negatives become positives.

def invert(lst):
    
    return [n * -1 for n in lst] if len(lst) > 0 else []