
function bloom_checker(number_of_bits, number_of_hash_functions, bitstring){
    var n_bits = number_of_bits
    var n_hashes = number_of_hash_functions
    var bitstring = bitstring
    function check(str){
        for (var i = 0; i < n_hashes; i++){
            var hash = CryptoJS.MD5(i+str);
            var loc = parseInt(hash.toString().substring(0,5), 16) % n_bits
            if(bitstring[loc] === "0"){
                return false;
            }
        }
        return true;
    }
    return check
}
