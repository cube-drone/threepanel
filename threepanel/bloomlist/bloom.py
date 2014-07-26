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
    """
        Given
            i = a salt
            item = an item
            mod = the size of the bit array
        Calculate the index of the bit-array to look for or set a '1'
        
        This function must be exactly parallel to
            var loc = parseInt(hash.toString().substring(0,5), 16) % n_bits
        in templates/bloomlist/bloom.js 

        Why the substring?  Javascript has trouble dealing with very large
        integers - like the sort produced by MD5 - so if we parse the whole
        MD5 output into an integer (before we mod it) - we will destroy 
        the universe. As a quick-and-lazy fix (what do you think I am, a 
        professional?) we just lop off all but the first six characters - 
        which still gives us 8^6 (262144) possible outputs - a number
        that Javascript can handle easy when parsed to an integer. 

        We may need to re-evaluate/improve this, should the blooms grow.
    """
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
        if len(string_list) <= 0:
            # seriously, that's not how this bloom filter was designed to work.
            # you give it a list, it makes a bloom filter from that list. 
            raise ValueError("You can't start this bloom with an empty list.")
        self.n_items = len(string_list)
        self.probability_of_false_positive = p
        self.n_bits_in_the_filter, self.n_hash_functions = calculator(self.n_items, 
                self.probability_of_false_positive)
        self.bits = bitarray([0]*self.n_bits_in_the_filter) 

        for item in string_list:
            self.insert(item)

        for item in string_list:
            if not self.check(item):
                raise AssertionError("""
                    Somehow this Bloom Filter doesn't contain the items that
                    have been placed within it. """)
        
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
    
