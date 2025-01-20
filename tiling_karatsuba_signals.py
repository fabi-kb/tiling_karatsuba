import numpy as np

from tiling_karatsuba_architecture import TilingKaratsubaArchitecture

class TilingKaratsubaSignals(TilingKaratsubaArchitecture):
    def __init__(self, mbits, tiling_size):
        super().__init__(mbits, tiling_size)

    def generate_signals(self, content):
        tiling_signals_comment = f"""
-- Generate Signals for the Tiling splits"""
        content.append(tiling_signals_comment)

        self.generate_input_split_signals(content)

        partial_products_comment = f"""
-- Generate Signals for the Partial Products"""
        content.append(partial_products_comment)

        self.generate_partial_products_signals(content)

        sum_signals_comment = f"""
-- Generate Signals for the Sum"""
        content.append(sum_signals_comment)

        self.generate_sum_signals(content)


    def generate_input_split_signals(self, content):
        for key, _ in self._a_splits.items():
            content.append(f"signal {key} : unsigned({self._tiling_size-1} downto 0) => (others => '0');")
        for key, _ in self._b_splits.items():
            content.append(f"signal {key} : unsigned({self._tiling_size-1} downto 0) => (others => '0');")


    def generate_partial_products_signals(self, content):
        for key, _ in self._diagonal_products.items():
            content.append(f"signal {key} : unsigned({2*self._tiling_size-1} downto 0) => (others => '0');")
        
        for key, _ in self._mixed_products.items():
            content.append(f"signal {key} : unsigned({2*self._tiling_size-1} downto 0) => (others => '0');")

    def generate_sum_signals(self, content):
        for id, _ in self._sums.items():
            content.append(f"signal S{id} : unsigned({2*self._tiling_size-1} downto 0) => (others => '0');")