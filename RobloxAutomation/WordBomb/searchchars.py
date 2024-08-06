import random

textdocument = open("wordlist.txt", "r", encoding="utf8")
funny_words = open("words.txt", "r", encoding="utf8")
array_list = []
funny_list = []
for line in textdocument:
    array_list.append(line)
for line in funny_words:
    funny_list.append(line)

while(True):
    chars = input("What chars are in the word: ")
    i = 0
    word_pool = []
    for words in array_list:
        if chars in words and len(words) >= 3:
            word_pool.append(words)
            i += 1
        #if i >= 200:
        #    break
    for i in range(10):
        try:
            print(word_pool[random.randint(0, len(word_pool) - 1)])
        except ValueError:
            print("No words")
    
    word_pool = []
    for words in funny_list:
        if chars in words and len(words) >= 3:
            word_pool.append(words)
        
    for i in range(2):
        try: 
            print(word_pool[random.randint(0, len(word_pool) - 1)])

        except ValueError:
            print("No funny")