import re
import sys
import json
import random
import string
import math



WORD_LENGTH = 5

def load_words() -> list[str]:
    file = open("words.txt")
    word = [word.rstrip(word[-1]) for word in file.readlines()]
    file.close()
    return word

def evaluate_word(word : str,wordList : list[str]):
    return evaluate_word_helper(0,[],word,wordList)


def evaluate_word_helper(idx : int,color : list[int],word : str,wordList : list[str]) -> float:
    sum = 0
    if(idx == WORD_LENGTH):
        matches = len(matcher(word,wordList,color))
        if(matches == 0):
            return 0
        return (matches * math.log2(len(wordList)/matches)) / len(wordList)
    
    for c in range(0,3):
        color.append(c)
        sum += evaluate_word_helper(idx+1,color,word,wordList)
        color.pop()
    
    return sum


def matcher(word : str,wordList : list[str], color : list[int]) -> list[str]:
 
    all_letters_regexp = "[abcdefghijklmnopqrstuvwxyz]"


    regexps : list[str] = []

    yellow_freq = {}
    green_freq = {}
    grays = []

    for letter_idx,c in enumerate(color):
        if (c == 2): # green
            regexps.append(word[letter_idx])
            if(green_freq.get(word[letter_idx])):
                green_freq[word[letter_idx]] += 1
            else:
                green_freq[word[letter_idx]] = 1

        elif (c == 1): # yellow
            if(yellow_freq.get(word[letter_idx])):
                yellow_freq[word[letter_idx]] += 1
            else:
                yellow_freq[word[letter_idx]] = 1

            regexps.append(all_letters_regexp)
            regexps[letter_idx] = all_letters_regexp.replace(word[letter_idx],'')
        else: # gray
            #print("gray",word[letter_idx])
            grays.append(word[letter_idx])
            regexps.append(all_letters_regexp.replace(word[letter_idx],''))


    for gray in grays:
        if(not yellow_freq.get(gray) and not green_freq.get(gray)):
            for i in range(len(regexps)):
                regexps[i] = regexps[i].replace(gray,'')

    regexp = ''.join(regexps)

    
    match_list = [word for word in wordList if re.match(regexp,word)]

    final_match = []
    for word in match_list:
        bad = False
        for c in string.ascii_lowercase:

            cnt = 0
            if(green_freq.get(c)):
                cnt+=green_freq[c]
            if(yellow_freq.get(c)):
                cnt+=yellow_freq[c] 
            if(c in grays and (green_freq.get(c) or yellow_freq.get(c))):
                # means there is green + yellow no. of c
                if(word.count(c) != cnt):
                    bad = True

            if(not c in grays and (yellow_freq.get(c) or green_freq.get(c)) and word.count(c) < cnt):
                bad = True
                

        if(not bad):
            final_match.append(word)

    #print(color,match_list)
    #print(final_match)
        #print(math.log2(len(match_list)/matches))
        #print("matches is",matches / len(wordList))

    return final_match



main_words = load_words()


def give_color(word,given):
    color = [0 for _ in range(WORD_LENGTH)]
    #print(word,given)
    for i in range(WORD_LENGTH):
        if(word[i] == given[i]):
            color[i] = 2
            given = given.replace(word[i],'?',1)

    #print(color)

    for i in range(WORD_LENGTH):
        if(given.count(word[i]) > 0 and color[i] != 2):
            color[i] = 1
            given = given.replace(word[i],'?',1)

    return color


def precompute(word : str, wordList : list[str]):
    return precompute_helper(0,[],word,wordList)

precomputed_p = {}

def precompute_helper(idx : int,color : list[int],word : str,wordList : list[str]) :
    if(idx == WORD_LENGTH):
        matched_word = matcher(word,wordList,color)
        mx = 0
        best=word
        for curr_word in matched_word:
            p = evaluate_word(curr_word,matched_word)
            #print(p)
            if(p > mx):
                mx = p
                best = curr_word

        precomputed_p[''.join([str(x) for x in color])] = best
        return
    
    for c in range(0,3):
        color.append(c)
        precompute_helper(idx+1,color,word,wordList)
        color.pop()


precomp_file = open("precompute.txt","r") 
precomputed_p =  json.load(precomp_file)
 
def run():
    words = main_words.copy()
    curr = "tares"
    turns = 1
    solved = False

    for i in range(0,6):

        print("Enter {}".format(curr))
        color = [int(x) for x in input().split()]

        #color = give_color(curr,given)
        #print(curr)
        #print(color)
        
        words = matcher(curr,words,color)

        if(i == 0):
            curr = precomputed_p[''.join([str(x) for x in color])]
            if curr not in words:
                print("cant find",curr)
                break
            words.remove(curr)
        else:
            def sort_by_p(word):
                return evaluate_word(word,words)

            words = sorted(words,key=sort_by_p)
            if(len(words) == 0):
                solved = False
                break
            curr = words.pop()                             

        print("Best guess is {}".format(curr))
        turns += 1

run()
    
#freq = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0}

#for i in range(0,1):
#    idx = random.randint(0,len(main_words) - 1)
    #print(main_words[idx])
#    freq[run(main_words[idx])] += 1


#print(freq)
#precompute("tares",main_words)

#file = open("precompute.txt","w")
#file.write(json.dumps(precomputed_p))
#file.close()
#print(evaluate_word("tears",main_words))

