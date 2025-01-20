import numpy as np

from tiling_karatsuba_entity import TilingKaratsubaEntity
from tiling_karatsuba_architecture import TilingKaratsubaArchitecture
from tiling_karatsuba_signals import TilingKaratsubaSignals
from tiling_karatsuba_statements import TilingKaratsubaStatements

class TilingKaratsubaGenerator:
    def __init__(self, mbits, tiling_size, output_file=''):
        self._output_file = output_file
        self._content = []


        # just for the other classes not acually needed inside this class 
        self._mbits = mbits
        self._tiling_size = tiling_size


    def generate_vhdl(self):
        entity_generator = TilingKaratsubaEntity(self._mbits)

        entity_generator.generate_header(self._content)
        entity_generator.generate_entity(self._content)

        self.generate_architecture(self._content)

        self.write_to_file()


    def generate_architecture(self, content):
        signal_generator = TilingKaratsubaSignals(self._mbits, self._tiling_size)
        statement_generator = TilingKaratsubaStatements(self._mbits, self._tiling_size)


        architecture_header = f"""
-- Architecture
architecture karatsuba_arch of karatsuba is"""
        content.append(architecture_header)

        signal_generator.generate_signals(content)

        content.append("\nbegin")

        statement_generator.generate_statements(content)

        content.append("\nend karatsuba_arch;")


    def write_to_file(self):
        if self._output_file == '':
            raise ValueError("Output file not defined.")
        with open(self._output_file, 'w') as f:
            f.write("\n".join(self._content))
        self._content = []


        

    
# test the function 

input_size = 32
tiling_size = 8
output_file = 'tiling_karatsuba.vhd'
tiling_karatsuba = TilingKaratsubaGenerator(input_size, tiling_size, output_file)
tiling_karatsuba.generate_vhdl()
