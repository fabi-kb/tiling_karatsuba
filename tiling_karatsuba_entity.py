import datetime

class TilingKaratsubaEntity:
    def __init__(self, mbits):
        self._mbits = mbits
        
    def generate_header(self, content):
        file_header = f"""
-- File: karatsuba.vhd
-- This file defines a VHDL implementation of the Karatsuba multiplication algorithm.
-- Author : Fabian Kubek
-- Date: {datetime.datetime.now().strftime("%Y-%m-%d")}"""
        
        content.append(file_header)

        libraries = """
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;"""

        content.append(libraries)

    def generate_entity(self, content):
        entity = f"""
-- Entity
entity karatsuba is
    generic (
        MBITS : integer := {self._mbits}
    );
    port (
        clk : in std_logic;
        reset : in std_logic 
        a : in unsigned(MBITS-1 downto 0) := (others => '0');
        b : in unsigned(MBITS-1 downto 0) := (others => '0');
        result : out unsigned((2*MBITS)-1 downto 0) := (others => '0')
    );
end entity karatsuba;"""
        content.append(entity)
