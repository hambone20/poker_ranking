# ranking cards in Poker
import sys

__test_hands = {"royal flush":  [('h', 'j'), ('h', 'q'), ('h', 'k'), ('h', 'a'), ('h', '10')], 
              "4 of a kind":    [('h', 'j'), ('c', 'j'), ('d', 'j'), ('s', 'j'), ('s', '10')], 
              "3 of a kind":    [('h', 'j'), ('c', 'j'), ('d', 'a'), ('s', 'j'), ('s', '10')], 
              "2 pair":         [('h', 'j'), ('c', 'j'), ('d', '10'), ('s', 'k'), ('s', '10')], 
              "1 pair":         [('h', 'j'), ('c', 'j'), ('d', 'k'), ('s', 'q'), ('s', '10')], 
              "straight":       [('h', '2'), ('c', '3'), ('d', '4'), ('s', '5'), ('s', '6')], 
              "straight flush": [('h', '2'), ('h', '3'), ('h', '4'), ('h', '5'), ('h', '6')], 
              "flush":          [('h', '2'), ('h', '3'), ('h', '4'), ('h', '7'), ('h', '6')], 
              "high card":      [('c', '2'), ('h', '3'), ('h', '4'), ('h', '7'), ('h', '6')],
              "straight la":    [('c', 'a'), ('h', '2'), ('h', '3'), ('h', '5'), ('h', '4')] }

__rankings = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']

#1 royal flush     S
#2 straight flush  S
#3 four of a kind  M-
#4 full house      M-
#5 flush
#6 straight        S
#7 3 of a kind     M-
#8 2 pair          M-
#9 pair            M-
#10 high card

def get_rank(card):
    return __rankings.index(card[1])

def hash_multiples(hand):
    ret = {}
    for (x, y) in hand:
        ret[y] = ret.get(y, 0) + 1
    return ret

def check_straight(hand):
    sorted_hand = sorted(list(map(lambda a: get_rank(a), hand)))
    high_card = get_face(sorted_hand[-1])
    if sorted_hand[-1] == len(__rankings)-1: # check for ace low
        for i in range(4):
            if sorted_hand[i] != i:
                break
        else:
            return (True, get_face(sorted_hand[-2]))
    for i in range(4):
        if not sorted_hand[i] + 1 == sorted_hand[i+1]:
            return (False, high_card)
    return (True, high_card)
    
def check_multiples(hand):
    hm = hash_multiples(hand)

    multis = list(filter(lambda x: x > 1, sorted(list(hm.values()))))

    if len(multis) > 0: # possible multis TODO return highest matching card
        if multis[-1] == 4: # 4 of a kind
            return "4 of a kind"
        elif len(multis) == 2 and multis[-1] == 3 and multis[-2] == 2: # full house
            return "full house"
        elif multis[-1] == 3:
            return "3 of a kind"
        elif len(multis) == 2 and multis[-1] == 2 and multis[-2] == 2: # 2 pair
            return "2 pair"
        else:
            return "a pair"
            
    return ""

def get_face(rank):
    return __rankings[rank]

def check_suited(hand):
    for i in range(4):
        if not hand[i][0] == hand[i+1][0]:
            return False
    return True

def rank_hand(hand):
    res = check_multiples(hand)
    if res:
        return res

    res = check_straight(hand)
    if not res[0]:
        if check_suited(hand):
            return "flush"
        else:
            return "high card " + res[1]
    else:
        if check_suited(hand):
            if res[1] == 'a':
                return "royal flush"
            else:
                return "straight flush, " + res[1] + ", high"
        else:
            return "straight, " + res[1] + ", high"

def print_hand(hand):
    for suit, face in hand:
        print("%s of %s, " % (face, suit), end = '')
    print()    
    
def main():
    for (ranking, hand)  in __test_hands.items():
        print_hand(hand)
        print("should be: %s" % ranking)
        print("Evaled to:")
        print(rank_hand(hand))
        print()
        
if __name__ == '__main__':
        sys.exit(main())
