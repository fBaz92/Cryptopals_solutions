# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 12:11:55 2020

@author: fbazzani
"""

def repeating_key_XOR(key, plaintext):
    '''
    Ex. key = 'ICE'
    
    In repeating-key XOR, you'll sequentially apply each byte of the key; the 
    first byte of plaintext will be XOR'd against I, the next C, the next E, 
    then I again for the 4th byte, and so on. 
    '''
    result = b''
    i = 0
    for byte in plaintext:
        result += bytes([byte^key[i]])
        i = i + 1 if i < len(key) - 1 else 0
    return result 

def main():
    from binascii import hexlify
    
    target = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    
    byte_plaintext = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    byte_key = b"ICE"
    result = str(hexlify(repeating_key_XOR(byte_key,byte_plaintext)))[2:-1]
    
    if result == target:
        print(result)
    else: 
        print(result)
        print(target)
    
    return

if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print('The execution time is {0}'.format(time.time()-start_time))