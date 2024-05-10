import os

def homework1_anagram(word):

    anagram=[]

    # ランダムな文字列をソートする
    sorted_word = sorted(word)

    #辞書ファイルを読み込む 
    with open('./words.txt', 'r') as f:
        dictionary = f.read().splitlines()
    new_dictionary = [] 
    new_sorted_dictionary = []

    if './new_dictionary' in os.listdir():
        with open('./new_dictionary.txt', 'r') as f:
            new_dictionary = f.read().splitlines()
            for new_word in new_dictionary:
                new_sorted_dictionary.append([new_word.split('\t')[0],new_word.split('\t')[1]])
    
    else:
        with open('./new_dictionary.txt', 'w') as f:
            for new_word in dictionary:
                new_dictionary.append([sorted(new_word),new_word])
        
            new_sorted_dictionary =sorted(new_dictionary)
            for new_word in new_sorted_dictionary:
                f.write(''.join(new_word[0]) +'\t' + new_word[1] + '\n')



    # 二分探索法でアナグラムを探す
    def binary_search(sorted_word, new_sorted_dictionary):
        left = 0
        right = len(new_sorted_dictionary) - 1
        while left <= right:
            mid = (left + right) // 2
            if new_sorted_dictionary[mid][0] == sorted_word:
                anagram.append(new_sorted_dictionary[mid][1])
                new_sorted_dictionary.pop(mid)
                return binary_search(sorted_word, new_sorted_dictionary)
                
            elif new_sorted_dictionary[mid][0] < sorted_word:
                left = mid + 1

            else:
                right = mid - 1

        return ""
    
    binary_search(sorted_word, new_sorted_dictionary)

    if len(anagram) == 0:
        return "No anagram"
    else:  
        return anagram

# テストケース
print(homework1_anagram('cat'))
print(homework1_anagram('dog'))
print(homework1_anagram('fkahjsdkfjhkash'))
print(homework1_anagram('a'))
print(homework1_anagram(''))
print(homework1_anagram('dehydtrogenaed'))


