import numpy as np 


class TilingKaratsubaArchitecture: 
    '''Parent class for the signal and statement generators'''

    def __init__(self, mbits, tiling_size):
        self._mbits = mbits
        self._tiling_size = tiling_size
        self._num_tilings = mbits // tiling_size
        self._tiling_offsets = np.arange(0, mbits, tiling_size)
        self._a_splits, self._b_splits = self.input_splits()
        self._diagonal_products, self._mixed_products = self.partial_produts()
        self._sums, self._substractions = self.sums()


    def input_splits(self):
        a_splits = dict() 
        b_splits = dict()
        for i in range(self._num_tilings):
            a_splits[f'A{i}'] = self._tiling_offsets[i]
            b_splits[f'B{i}'] = self._tiling_offsets[i]
        return a_splits, b_splits

    def partial_produts(self):
        diagonal_products = dict()
        for i in range(self._num_tilings):
            diagonal_products[f'D{i}{i}'] = (f'A{i}', f'B{i}')
        
        mixed_products = dict()
        for i in range(self._num_tilings-1):
            for j in range(i+1, self._num_tilings):
                mixed_products[f'M{i}{j}'] = (f'A{i}', f'A{j}', f'B{i}', f'B{j}')

        return diagonal_products, mixed_products
    
    def sums(self):
        additions = dict() 
        substractions = dict()
        for id in range(2*self._num_tilings-1):
            addends = []
            substrahends = []
            if id >= self._num_tilings: 
                i = id - self._num_tilings + 1 
                j = self._num_tilings - 1
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
