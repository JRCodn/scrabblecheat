from tkinter import *
import textwrap
"""
This is a scrabble cheat I made for fun, as my girlfriend plays scrabble online every night and I thought it would be a good little project.
The dictionary I originally used had words that weren't valid in scrabble so I found this one which hopefully is more accurate.
Originally all the words were uppercase which stuffed with my code, I could of easily just had a line in my code to deal with this but this would take the computer a lot of extra steps,
so I found a neat piece of code on stack overflow that takes the whole file and rewrites it to lowercase.
 
    file = open('words.txt', 'r')
    lines = [line.lower() for line in file]

    with open('words.txt', 'w') as out:
        out.writelines(sorted(lines))

Blank tiles are represented with a "."
7 letter words give a bonus 50 points
Prints out highest scoring words
"""

#Game logic

def load_words():
    #loads all the words and puts it in a list without any \n
    with open('words.txt', 'r') as words_file:
       return [line.rstrip('\n') for line in words_file]


def check_word(word, rack):
    #make a list of all blank tiles
    blank_tile = [b for b in rack if b == "."]
    rack = rack.copy()

    #check every letter in word to see if it's in the rack, if not then is there a blank tile to use else return false.
    for letter in word:
        if letter in rack:
            rack.remove(letter)
        elif letter not in rack and "." in blank_tile:
            blank_tile.remove(".")
        else:
            return False
    return True




def word_score(word, rack):
    get_score = 0
    rack = rack.copy()
    scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
              "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
              "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
              "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
              "x": 8, "z": 10}
    for a in word:
        #checks if there's a blank tile and adds no points.
        if a not in rack:
            continue
        else:
            get_score += scores.get(a)
            rack.remove(a)
    if len(word) == 7:
        get_score += 50
    return get_score


def valid_words(rack):
    # load dictionary of words and create empty list for use in function
    word_copy = load_words()
    list_valid_words = []
    # for every word in dictionary
    for word in word_copy:
        #check we can make the word if we can then put it in our list of valid words
        if check_word(word, rack):
            list_valid_words.append(word)
    return list_valid_words



def best_words(rack):
    rack = [a for a in rack]
    word_scores = {}

    # find all the possible words then gathers the scores of all the valid words in a dictionary
    for words in valid_words(rack):
        word_scores[words] = word_score(words, rack)

    max_value = max(word_scores.values())
    max_words = ", ".join(a for a, v in word_scores.items() if v == max_value)
    other_words = ", ".join("{}: {}".format(l, k) for l, k in word_scores.items() if  k == max_value - 6)

    return ("Highest score is {} with the words: {}\n".format(max_value, max_words) +
           "\nOther high scoring words: " +
           textwrap.fill(other_words))


def replay(word_scores):
    see_all_answers = input("\nPress N for a new rack or A for all the words available: ")
    if see_all_answers.upper() == 'N':
        words_by_points()
    elif see_all_answers.upper() == 'A':
        print(textwrap.fill(", ".join("{}: {}".format(k, v) for k, v in word_scores.items())))
        words_by_points()
    else:
        replay(word_scores)


def words_by_points():
        new_rack = input("\nPlease put in new rack: ")
        best_words(new_rack)




#Tkinter logic

root = Tk()

aword = Entry(root, width=50)
aword.pack()


def checkWords():
    myLabel = Label(root, text=best_words(aword.get()))
    myLabel.pack()

myButton = Button(root, text="Enter your scrabble rack", command=checkWords)
myButton.pack()

root.mainloop()
