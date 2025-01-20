import numpy as np 


def calculate_tilings(input_size, tiling_size):
    '''
    calculates the tiling locations for a multiplier given the input size and tiling size
    '''
    # calculate the number of tilings
    num_tilings = input_size // tiling_size

    # calculate the tiling offsets 
    tiling_offsets = np.arange(0, input_size, tiling_size)
    

    # compute the partial products

    diagonal_products = dict()
    for i in range(num_tilings):
        diagonal_products[f'A{i}B{i}'] = (tiling_offsets[i], tiling_offsets[i])
    
    upper_produdcts = dict()
    for i in range(num_tilings-1):
        for j in range(i+1, num_tilings):
            upper_produdcts[f'A{i}B{j}'] = (tiling_offsets[i], tiling_offsets[j])
    
    lower_products = dict()
    for i in range(1, num_tilings):
        for j in range(i):
            lower_products[f'A{i}B{j}'] = (tiling_offsets[i], tiling_offsets[j])

    partial_products = diagonal_products | upper_produdcts | lower_products
    # compute the sums for the final multiplication 

    additions = dict() 
    substractions = dict()
    for id in range(2*num_tilings-1):
        addends = []
        substrahends = []
        if id >= num_tilings: 
            i = id - num_tilings + 1 
            j = num_tilings - 1
        else: 
            i = 0
            j = id
        while  i <= j:
            if i == j:
                addends.append(f'D{i}{j}')
            else:
                addends.append(f'M{i}{j}')
                substrahends.append(f'D{i}{i}')
                substrahends.append(f'D{j}{j}')
            i += 1
            j -= 1
        additions[id] = addends
        substractions[id] = substrahends


    return additions, substractions

# test the function

input_size = 32
tiling_size = 8
additions, substractions = calculate_tilings(input_size, tiling_size)
print(additions)
print(substractions)
#print(sums)