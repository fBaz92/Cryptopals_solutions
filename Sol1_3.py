# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 22:19:27 2020

@author: franc
"""


def english_score_v2(presumable_plaintext):
    '''
    
    Parameters
    ----------
    possible_plaintext : bytes
        DESCRIPTION.
        possible plaintext in byte
    Returns
    -------
    score : float
        DESCRIPTION.
        returns a score wich is proportional to the occurences of english characters in a sentence
        the score are given by a dictionary of the most used letters in english

    '''
    
    CHARACTER_FREQ = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
    }    
    
    score = 0
    
    for letter in presumable_plaintext:
        score += CHARACTER_FREQ.get(chr(letter).lower(), 0)
            
    return score



def english_score_v1(presumable_plaintext):
    database_path = r'C:\Users\franc\Google Drive\git\Script_py\Hex64\1.3\words_alpha.txt'
    def create_dictionary(database_path):
        
        #read the file wich contains all the english words
        words = open(database_path)
        #
        word_list = words.readlines()
        english_word_dictionary = {}
        for count in range(len(word_list)):
            english_word_dictionary[word_list[count].rstrip()] = '1'
        return english_word_dictionary

    english_words_dictionary = create_dictionary(database_path)
    
    def english_percentage(presumable_plaintext, english_words_dictionary): 
        score = 0
        try:
            list_of_words = presumable_plaintext.decode().split()
            for word in list_of_words:
                try:
                    if english_words_dictionary[word] == '1':
                        score += len(word)
                except KeyError:
                    continue
            return score/sum(list(map(len, list_of_words)))
        except: 
            return 0
    
    score = english_percentage(presumable_plaintext, english_words_dictionary)
    
    return score
    
    

def xor_bytes(char_bytes, key):
    '''
    
    Parameters
    ----------
    char_bytes : bytes
        DESCRIPTION
        character of the encoded text.
    key : int
        DESCRIPTION
        integer that represent the character in the ASCII encoding.

    Returns
    -------
    result : bytes
        DESCRIPTION.
        bytes of the decoded string
    '''
    result = b''
    for char in char_bytes:
        result += bytes([char ^ key])
    return result




def single_char_xor_string(bytestring,english_score):
    '''
    Parameters
    ----------
    bytestring : bytes
        DESCRIPTION
        Byte string .
    english_score : function
        DESCRIPTION
        function that returns the "english score".

    Returns
    -------
    Dictionary
        DESCRIPTION
        Return a dictionary which contains the most likely key, text and score.

    '''
    

    result = []
    for key_candidate in range(256):
        plaintext_candidate = xor_bytes(bytestring, key_candidate)
        english_phrase_score = english_score(plaintext_candidate)		
        temp = {    'key': key_candidate,
                    'plaintext': plaintext_candidate,
                    'score' : english_phrase_score}
        result.append(temp)
        
    
    
    #questo metodo restituisce solamente il dizionario contentente i valori che ritengo giusti
    return sorted(result, key=lambda c: c['score'], reverse = True)[0]





def main(hex_string, english_score):
    
    hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    bytestring = bytes.fromhex(hex_string)    
    plaintext = single_char_xor_string(bytestring,english_score)
    print("La stringa esadecimale {0} è stata crittografata con il carattere {1} e il significato è {2}"
          .format(hex_string,chr(plaintext['key']),plaintext['plaintext'].decode()))
    
    return 

if __name__ == '__main__':
    import time
    hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    start_time = time.time()
    main(hex_string,english_score_v1)    
    print('Il tempo di esecuzione con il mio algoritmo è {0}s'.format(time.time()-start_time))
    
    start_time = time.time()
    main(hex_string,english_score_v2)    
    print('Il tempo di esecuzione con il secondo algoritmo è {0}s'.format(time.time()-start_time))




