from math import ceil, log, pow
from bitarray import bitarray
from hashlib import md5

def calculator(n, p):
    """
        n = number of items in the filter (int, example=4000)
        p = probability of false positives (float, example=0.001)
        
        returns

        m = number of bits in the filter
        k = number of hash functions
    """
    m = ceil((n*log(p) / log(1.0/ (pow(2.0, log(2.0))))));
    k = ceil(log(2.0) * m / n);
    return m, k

def hash_to_location(i, item, mod):
    temp_hash = md5()
    temp_hash.update((str(i) + item).encode("ascii"))
    digest = temp_hash.hexdigest()[0:5]
    bit_location = int(digest,16) % mod 
    return bit_location

class bloom(object):
    def __init__(self, string_list, p=0.001):
        """
            string_list is a list of strings, ["", "", ""]
        """
        self.n_items = len(string_list)
        self.probability_of_false_positive = p
        self.n_bits_in_the_filter, self.n_hash_functions = calculator(self.n_items, 
                self.probability_of_false_positive)
        self.bits = bitarray([0]*self.n_bits_in_the_filter) 

        for item in string_list:
            self.insert(item)

        for item in string_list:
            if not self.check(item):
                print("nooooo")
        
    def insert(self, item):
        for i in range(0, self.n_hash_functions):
            bit_location = hash_to_location(i, item, self.n_bits_in_the_filter)
            self.bits[bit_location] = True

    def check(self, item):
        for i in range(0, self.n_hash_functions):
            bit_location = hash_to_location(i, item, self.n_bits_in_the_filter)
            if not self.bits[bit_location]:
                return False
        return True
    
