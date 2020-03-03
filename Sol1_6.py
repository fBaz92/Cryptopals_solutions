# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 13:43:35 2020

@author: fbazzani
"""
from Sol1_3 import english_score_v2, single_char_xor_string
from Sol1_5 import repeating_key_XOR

def hamming(word1, word2):
    #assert len(word1) == len(word2), "Hamming distance is defined only for equal length strings"
    res = 0
    for letter1,letter2 in zip(word1,word2):
        #diff = ord(letter1)^ord(letter2)
        diff = letter1^letter2
        a = [1 for i in bin(diff)[2:] if i =='1']
        res += sum(a)
    return res

def decode_base_64(encrypted_file): 
    assert type(encrypted_file) == str, "This script decrypt only strings"
    import base64
    return base64.b64decode(encrypted_file)

def find_the_keys(binary_file):
    """
    binary_file:
        type:           bytes
        description:    binary text decrypted by base 64
    
    return list_of_all_HamDisNormaliz:
        type:           list of dictionaries
        description:    list of the 4 dictionaries which have the shorter hammington
                        normalized distance
    """
    import numpy as np
    
    #starting the search of keysize
    list_of_all_HamDisNormaliz = []
    
    for keysize in range(2,41):
        ham_dist = np.mean([hamming(binary_file[i*keysize:(i+1)*keysize],binary_file[(i+1)*keysize:(i+2)*keysize]) 
        for i in range(4)])/keysize #calculating the ham distance as the medium of the ham dist of 4 blocks
        temp = {'keysize': keysize,
                'ham_dis': ham_dist}
        list_of_all_HamDisNormaliz.append(temp)
    return sorted(list_of_all_HamDisNormaliz, key = lambda x: x['ham_dis'], reverse = False)[:3]

def split_in_chunks(chunk_size, binary_file):
    """
    chunk_size:
        type:           int
        description:    size of the chunks in which I split the binary file
        
    binary_file:
        type:           bytes
        description:    binary text decrypted by base 64

    return list_of_all_HamDisNormaliz:
        type:           list of dictionaries
        description:    list of the 4 dictionaries which have the shorter hammington
                        normalized distance
    """
    #split the cyph text 
    chunks = len(binary_file)
    result = [binary_file[i:chunk_size+i] for i in range(0, chunks, chunk_size)]
    
    #handling the different size of the last chunk; I fill it with '' 
    if len(result[-1]) == len(result[0]):
        return result
    else:
        tmp = result.pop()
        tmp = tmp + bytes(1)*(len(result[0])-len(tmp))
        #tmp = tmp + " "*(len(result[0])-len(tmp))
        result.append(tmp)
        return result


def transpose_the_chunks(chunks):
    """create keysize number of chunks formed by the ith byte, i.e the first is 
    made by all the first byte of the chunks, the second by all the second bytes, ecc...."""
    
    result = []
    for chunk in chunks:
        tmp = []
        for index in range(len(chunk[0])):
            transposed = bytearray(b'')
            for element in chunk:
                transposed.append(element[index])
            tmp.append(transposed)
        result.append(tmp)
    return result

def find_the_key(transposed_keysize_chunks, binary_file):
    #Solve each block as if it was single-character XOR. You already have code to do this. 
    #For each block, the single-byte XOR key that produces the best looking histogram 
    #is the repeating-key XOR key byte for that block. Put them together and you have the key. 
    """
    transposed_chunks:
        type: list
        description: list which contains all the transposed chunks
    """
    result = []
    for transposed_chunks in transposed_keysize_chunks:
        key = bytearray(b'')
        for t_chunk in transposed_chunks:
            key.append(single_char_xor_string(t_chunk,english_score_v2)['key'])
        tmp = {'key': key, 'plaintext': repeating_key_XOR(key,binary_file), 'score': english_score_v2(repeating_key_XOR(key,binary_file))}
        result.append(tmp)
    return sorted(result, key= lambda c: c['score'], reverse = True)[0]



def main():

    import time
    import base64
    start_time = time.time()
    binary_file = base64.b64decode(open("file_1_6.txt").read())
    keys = find_the_keys(binary_file)
    
    chunks = []
    for key in keys:
        chunks.append(split_in_chunks(key['keysize'],binary_file))
    transposed_keysize_chunks = transpose_the_chunks(chunks)
    
    plaintext_object = find_the_key(transposed_keysize_chunks,binary_file)
    
    print("The execution time is {0}s\n".format(time.time()-start_time))
    print("The key is:\n{0}\n".format(plaintext_object['key'].decode()))
    print("The plaintext is:\n{0}\n".format(plaintext_object['plaintext'].decode()))    
    return 

if __name__ == "__main__":
    main()
