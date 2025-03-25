def countRankAndSuits(cards, ranks, suits) :
    r_counts = [0] * 13
    s_counts = [0] * 4
    for c in cards :
        r_counts[c.rank] += 1
        s_counts[c.suit] += 1
    return r_counts, s_counts

def countForFlush(cards, ranks, suits) :
    counts = [[0]*len(ranks)]*len(suits)
    for c in cards :
        counts[c.suit][c.rank] = 1
    return counts

def longestSequenceAndIndex(arr) :
    current_length, max_length, last_index = 0, 0, 0
    for i in range(len(arr)):
        if arr[i] != 0:
            current_length += 1
        else:
            if current_length >= max_length :
                max_length = current_length
                last_index = i-1
            current_length = 0

    # Update max_length if there's a non-zero sequence at the end
    if current_length >= max_length :
        max_length = current_length
        last_index = len(arr)-1

    return max_length, last_index

def getRemainingHighestCardsValue(r_counts, s_counts, index_to_exclude, nb_cards) :
    arr = [i for i in range(len(r_counts)) if r_counts[i] > 0 and i not in index_to_exclude]
    arr = arr[len(arr)-nb_cards:]
    v = 0
    for i in range(len(arr)) :
        v += arr[i] << (4*i)
    return v+1

def quinteFlushValue(f_counts) :
    for count in f_counts :
        if sum(count) >= 5 :
            max_length, last_index = longestSequenceAndIndex([count[-1]]+count)
            if max_length >= 5 :
                return last_index #Valeur pour Quinte Flush à shifter
            
def fourOfAKindValue(r_counts, s_counts) :
    index = len(r_counts)-1
    while r_counts[index] < 4 :
        index -= 1
    return index

def fullHouseValue(r_counts, s_counts) :
    three, two = 0, 0
    first, second = True, True
    i = len(r_counts)-1
    while i > -1 and (first or second):
        if r_counts[i] == 3 and first :
            three = i
            first = False
        elif r_counts[i] >= 2 and second :
            two = i
            second = False
        i -= 1
    return (three << 4) + two

def threeOfAKindValue(r_counts, s_counts) :
    i = len(r_counts)-1
    while i > -1 :
        if r_counts[i] == 3 :
            return i
        i -= 1
            
def flushValue(f_counts) :
    for count in f_counts :
        if sum(count) >= 5 :
            s, nb = 0, 0
            index = len(count)-1
            while index >= 0 and nb < 5 :
                if count[index] > 0 :
                    nb += 1
                s += 2**index
                index -= 1
            return s #Valeur pour flush à shifter

def doublePairValue(r_counts, s_counts) :
    two_1, two_2 = 0, 0
    first, second = True, True
    i = len(r_counts)-1
    while i > -1 and (first or second):
        if r_counts[i] == 2 and first :
            two_1 = i
            first = False
        elif r_counts[i] == 2 and second :
            two_2 = i
            second = False
        i -= 1
    return [two_1, two_2]

#Boolean utils
def hasFlush(r_counts, s_counts) :
    return any(s_counts[i] >= 5 for i in range(len(s_counts)))

def hasThreeOfAKindOrMore(r_counts, s_counts) :
    return any(r_counts[i] >= 3 for i in range(len(r_counts)))

def hasFourOfAKind(r_counts, s_counts) :
    return any(r_counts[i] == 4 for i in range(len(r_counts)))

def hasFullHouse(r_counts, s_counts) :
    arr = [r_counts[i] for i in range(len(r_counts)) if r_counts[i] >= 2]
    return (len(arr) >= 2 and max(arr) == 3)
