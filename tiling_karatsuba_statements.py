import numpy as np

from tiling_karatsuba_architecture import TilingKaratsubaArchitecture

class TilingKaratsubaStatements(TilingKaratsubaArchitecture):
    def __init__(self, mbits, tiling_size):
        super().__init__(mbits, tiling_size)


    def generate_statements(self, content):
        input_assignment_comment = f"""
-- Split the input signals"""     
        content.append(input_assignment_comment)

        self.generate_input_split_statements(content)

        partial_products_comment = f"""
-- Generate the partial products"""
        content.append(partial_products_comment)

        self.generate_partial_products_statements(content)

        sum_statements_comment = f"""
-- Generate the sums"""
        content.append(sum_statements_comment)

        self.generate_sum_statements(content)

        final_sum_comment = f"""
-- Generate the result"""
        content.append(final_sum_comment)

        self.generate_final_sum(content)

    def generate_input_split_statements(self, content):
        for key, value in self._a_splits.items():
            content.append(f"{key} <= a({value+self._tiling_size-1} downto {value});")

        for key, value in self._b_splits.items():
            content.append(f"{key} <= b({value+self._tiling_size-1} downto {value});")

    def generate_partial_products_statements(self, content):
        for key, values in self._diagonal_products.items():
            content.append(f"{key} <= {values[0]} * {values[1]};")

        for key, values in self._mixed_products.items():
            content.append(f"{key} <= ({values[0]} + {values[1]}) * ({values[2]} + {values[3]});")

    def generate_sum_statements(self, content):
        for id, addends in self._sums.items():
            addend_str = " + ".join(addends)
            if self._substractions[id]:
                substrahend_str = " - ".join(self._substractions[id])
                content.append(f"S{id} <= {addend_str} - {substrahend_str};")
            else:
                content.append(f"S{id} <= {addend_str};")

    def generate_final_sum(self, content):
        shifted_sums = [f'S{0}']
        for i in range(1, 2*self._num_tilings-1):
            shifted_sums.append(f'shift_left(S{i}, {i*self._tiling_size});')
        final_result = " + ".join(shifted_sums)
        content.append(f"result <= {final_result};")