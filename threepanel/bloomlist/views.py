from django.shortcuts import render
from .bloom import bloom

def bloom_view(name, list_of_strings, request):
    b = bloom(list_of_strings)
    context = {}
    context['set_name'] = name 
    context['number_of_hash_functions'] = b.n_hash_functions
    context['number_of_bits'] = b.n_bits_in_the_filter
    context['bitstring'] = b.bits.to01()
    return render(request, "bloomlist/bloom.js", context, content_type="application/javascript")
