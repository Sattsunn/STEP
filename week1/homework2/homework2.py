import os
from itertools import combinations, chain
import score_checker


def count_word(count_word):
    count = {}
    for char in count_word:
        if char in count:
            count[char] += 1        
        else:
            count[char]=1
    return count

def get_all_combinations(word):
   all_combinations = []
   for r in range(1, len(word) + 1):
       for combo in combinations(word, r):
            # print('コンボ')
            # print(combo)
            combo_dict = count_word(''.join(combo))
            # for char in combo:
            #    combo_dict[char] = word[char]
            all_combinations.append([''.join(combo),combo_dict])
    
   all_combinations = sorted(all_combinations)
#    print('全ての組み合わせ')
#    print(all_combinations)
   return all_combinations

        
def check_score(count):
    point = {
    'a': 1, 'e': 1, 'h': 1, 'i': 1, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1,
    'c': 2, 'd': 2, 'l': 2, 'm': 2, 'u': 2,
    'b': 3, 'f': 3, 'g': 3, 'p': 3, 'v': 3, 'w': 3, 'y': 3,
    'j': 4, 'k': 4, 'q': 4, 'x': 4, 'z': 4
    }
    score=0

    for key in count:
        score += point[key] * count[key]
    
    return score
         

def binary_search(word, dictionary):
    # print('二分探索')
    # print(word)
    left = 0
    right = len(dictionary) - 1
    while left <= right:
        mid = (left + right) // 2
        # print(''.join(dictionary[mid][0]))
        if ''.join(dictionary[mid][0]) == word:
            # print('探索結果')
            # print(dictionary[mid])
            return dictionary[mid]
            
        elif str(''.join(dictionary[mid][0])) < str(word):
            left = mid + 1
        else:
            right = mid - 1
    pass

def choice_anagram(anagrams):
    max_score = 0
    max_score_word = ''
    for anagram in anagrams:
        if check_score(anagram[2]) > max_score:
            max_score = check_score(anagram[2])
            max_score_word = anagram[1]
    # print(max_score_word)
    return max_score_word


def homework2_anagram(file):

    #入力されたファイルを読み込む
    search_words = []
    new_search_words = []

    file_path = f'./input_file/{file}.txt'
    with open(file_path, 'r') as f:
        search_words = f.read().splitlines()
        for search_word in search_words:
            search_word_count = count_word(sorted(search_word))
            new_search_words.append([''.join(sorted(search_word)),search_word_count])
        new_search_words = sorted(new_search_words)
    
    # print(new_search_words)
    

    # 辞書ファイルを読み込む 
    dictionary = []
    with open('./words.txt', 'r') as f:
        dictionary = f.read().splitlines()

    new_dictionary = [] 
    new_sorted_dictionary = []

    if './new_count_dictionary' in os.listdir():
        with open('./new_count_dictionary.txt', 'r') as f:
            new_dictionary = f.read().splitlines()
            for new_word in new_dictionary:
                new_sorted_dictionary.append([new_word.split('\t')[0],new_word.split('\t')[1],new_word.split('\t')[2],new_word.split('\t')[3]])
    
    else:
        with open('./new_count_dictionary.txt', 'w') as f:
            for word in dictionary:
                sorted_word = sorted(word)
                word_count = count_word(sorted_word)
                new_dictionary.append([sorted_word,word,word_count])

            new_sorted_dictionary = sorted(new_dictionary)
            for new_word in new_sorted_dictionary:
                f.write(''.join(new_word[0]) + '\t' + new_word[1] + '\t' + str(new_word[2])  + '\n')

    def search_anagram(search_words, dictionary):
        answer=[]
        for search_word in search_words:
            conbination=get_all_combinations(search_word[0])
            test_anagrams = []
            for con in conbination:
                if binary_search(con[0],dictionary) != None:
                    test_anagrams.append(binary_search(con[0],dictionary))
            answer.append(choice_anagram(test_anagrams))
            # print(answer)
        return answer
                
    search_anagram(new_search_words, new_sorted_dictionary)
    

     # fileの出力
    with open(f'./answer_file/{file}_answer.txt', 'w') as f:
        count=0
        for ans in search_anagram(new_search_words, new_sorted_dictionary):
            count += check_score(count_word(ans))
            f.write(ans + '\n')
        print(count)


    return None  

# テストケース
if __name__ == "__main__":
    # print(homework2_anagram('small'))
    # print(homework2_anagram('medium'))
    print(homework2_anagram('large'))