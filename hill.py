import numpy as np
import sympy as smp
import sys


class HillCipher:
    def __init__(self, key, keysize, alphabet=None):
        self._inv_alphabet = {}
        self.alphabet = alphabet
        self.keysize = keysize
        self._valid_key_length = (4, 9, 16, 25)
        self.key = key
    
    @property
    def alphabet(self):
        return self._alphabet
    
    @alphabet.setter
    def alphabet(self, value):
        self._alphabet = {}
        
        if value is None or type(value) != str:
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ'.-"
        else:
            alphabet = value
            
        for idx, letter in enumerate(alphabet):
            self._alphabet[letter] = idx
            self._inv_alphabet[idx] = letter
            
    @property
    def keysize(self):
        return self._keysize
    
    @keysize.setter
    def keysize(self, value):
        if value != (2, 2) and value != (3, 3):
            print('[-] Key matrix can either be a 2x2 or 3x3.')
            sys.exit(1)
        self._keysize = value
        
    @property
    def key(self):
        return self._key
    
    @key.setter
    def key(self, value):
        if type(value) != str:
            
            if type(value) == list:
                
                if len(value) != self.keysize[0]:
                    print("Invalid list lenght provided, use (2x2) or (3x3) in conjuction with provided keysize.")
                    sys.exit(1)
                    
                for v in value:
                    if type(v) != list:
                        print("[-] 2D list or string input required for key.")
                        sys.exit(1)
                        
                    if len(v) != self.keysize[0]:
                        print("Invalid list length provided, use (2x2) or (3x3) instead.")
                        sys.exit(1) 
                    
                    for vi in v:
                        if type(vi) != int:
                            print("[-] Key matrix can only accept integer values.")
                            sys.exit(1)
                            
                self._key = np.array(value)
            else:
                print("[-] 2D list or string input required for key.")
                sys.exit(1)
        else:
            if len(value) not in self._valid_key_length:
                print("[-] Key length should be square of integer in the following range 4, 9, 16, 25")
                sys.exit(1)
                
            self._key = self.get_matrix_from_key(value)
        
    def get_matrix_from_key(self, key_str):
        key_matrix = []
        step = self.keysize[0]
        
        key_str = key_str.upper()
        for i in range(0, len(key_str), step):
            elements = []
            for j in range(i, i + step, 1):
                elements.append(self.alphabet.get(key_str[j], len(self.alphabet) - 1))
            key_matrix.append(elements)
        
        return np.array(key_matrix)
        
    def _pad(self, message):
        product = self.keysize[0] * self.keysize[1]
        
        while len(message) % product != 0:
            message += "-"
            
        return message.upper()
    
    def _convert_to_numeric(self, message):
        message_numeric = []
        
        for letter in message:
            message_numeric.append(self.alphabet.get(letter, len(self.alphabet) - 1))
                
        return message_numeric     
    
    def _convert_to_text(self, message):
        result_str = ""
        
        for i in range(len(message)):
            for j in range(len(message[0])):
                result_str += self._inv_alphabet[message[j][i]]
        
        return result_str
            
    def apply(self, operation, message):
        message = self._pad(message)
        
        message_numeric = self._convert_to_numeric(message)
        
        if operation == "decrypt":
            key = smp.Matrix(self.key).inv_mod(len(self.alphabet))
            print("[+] Decrypting: {}".format(message))
        elif operation == "encrypt":
            key = self.key
            print("[+] Encrypring: {}".format(message))
        else:
            print("[-] Operations permitted are encrypt/decrypt")
            sys.exit(1)
        
        result = ""
        step = self.keysize[0] * self.keysize[1]
        for x in range(0, len(message_numeric), step):
            message_part = message_numeric[x : x + step]
            message_matrix = []

            for i in range(0, len(message_part), self.keysize[0]):
                message_matrix.append(message_part[i : i + self.keysize[0]])
        
            message_matrix = np.array(message_matrix).T
            processed = np.matmul(message_matrix, key) % len(self.alphabet)
            result += self._convert_to_text(processed)
            
        return result
    
    
if __name__ == "__main__":
    hill = HillCipher(key=[[2, 9, 2], [3, 8, 6], [1, 0, 5]], keysize=(3, 3))
    
    encrypted_message = hill.apply(operation="encrypt", message="hello world")
    print("[+] Encryption result: {}".format(encrypted_message))
    
    print("\n")
    
    decrypted_message = hill.apply(operation="decrypt", message=encrypted_message)
    print("[+] Decryption result: {}".format(decrypted_message))