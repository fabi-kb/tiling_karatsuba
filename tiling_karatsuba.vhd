
-- File: karatsuba.vhd
-- This file defines a VHDL implementation of the Karatsuba multiplication algorithm.
-- Author : Fabian Kubek
-- Date: 2025-01-20

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

-- Entity
entity karatsuba is
    generic (
        MBITS : integer := 32
    );
    port (
        clk : in std_logic;
        reset : in std_logic 
        a : in unsigned(MBITS-1 downto 0) := (others => '0');
        b : in unsigned(MBITS-1 downto 0) := (others => '0');
        result : out unsigned((2*MBITS)-1 downto 0) := (others => '0')
    );
end entity karatsuba;

-- Architecture
architecture karatsuba_arch of karatsuba is

-- Generate Signals for the Tiling splits
signal A0 : unsigned(7 downto 0) => (others => '0');
signal A1 : unsigned(7 downto 0) => (others => '0');
signal A2 : unsigned(7 downto 0) => (others => '0');
signal A3 : unsigned(7 downto 0) => (others => '0');
signal B0 : unsigned(7 downto 0) => (others => '0');
signal B1 : unsigned(7 downto 0) => (others => '0');
signal B2 : unsigned(7 downto 0) => (others => '0');
signal B3 : unsigned(7 downto 0) => (others => '0');

-- Generate Signals for the Partial Products
signal D00 : unsigned(15 downto 0) => (others => '0');
signal D11 : unsigned(15 downto 0) => (others => '0');
signal D22 : unsigned(15 downto 0) => (others => '0');
signal D33 : unsigned(15 downto 0) => (others => '0');
signal M01 : unsigned(15 downto 0) => (others => '0');
signal M02 : unsigned(15 downto 0) => (others => '0');
signal M03 : unsigned(15 downto 0) => (others => '0');
signal M12 : unsigned(15 downto 0) => (others => '0');
signal M13 : unsigned(15 downto 0) => (others => '0');
signal M23 : unsigned(15 downto 0) => (others => '0');

-- Generate Signals for the Sum
signal S0 : unsigned(15 downto 0) => (others => '0');
signal S1 : unsigned(15 downto 0) => (others => '0');
signal S2 : unsigned(15 downto 0) => (others => '0');
signal S3 : unsigned(15 downto 0) => (others => '0');
signal S4 : unsigned(15 downto 0) => (others => '0');
signal S5 : unsigned(15 downto 0) => (others => '0');
signal S6 : unsigned(15 downto 0) => (others => '0');

-- Generate Signals for the Sum Shift
signal S0_shift : unsigned(63 downto 0) => (others => '0');
signal S1_shift : unsigned(63 downto 0) => (others => '0');
signal S2_shift : unsigned(63 downto 0) => (others => '0');
signal S3_shift : unsigned(63 downto 0) => (others => '0');
signal S4_shift : unsigned(63 downto 0) => (others => '0');
signal S5_shift : unsigned(63 downto 0) => (others => '0');
signal S6_shift : unsigned(63 downto 0) => (others => '0');

begin

-- Split the input signals
A0 <= a(7 downto 0);
A1 <= a(15 downto 8);
A2 <= a(23 downto 16);
A3 <= a(31 downto 24);
B0 <= b(7 downto 0);
B1 <= b(15 downto 8);
B2 <= b(23 downto 16);
B3 <= b(31 downto 24);

-- Generate the partial products
D00 <= A0 * B0;
D11 <= A1 * B1;
D22 <= A2 * B2;
D33 <= A3 * B3;
M01 <= (A0 + A1) * (B0 + B1);
M02 <= (A0 + A2) * (B0 + B2);
M03 <= (A0 + A3) * (B0 + B3);
M12 <= (A1 + A2) * (B1 + B2);
M13 <= (A1 + A3) * (B1 + B3);
M23 <= (A2 + A3) * (B2 + B3);

-- Generate the sums
S0 <= D00;
S1 <= M01 - D00 - D11;
S2 <= M02 + D11 - D00 - D22;
S3 <= M03 + M12 - D00 - D33 - D11 - D22;
S4 <= M13 + D22 - D11 - D33;
S5 <= M23 - D22 - D33;
S6 <= D33;

-- Generate the final shifts
S0_shift <= shift_left(to_unsigned(0, 48) & S0, 0);
S1_shift <= shift_left(to_unsigned(0, 48) & S1, 8);
S2_shift <= shift_left(to_unsigned(0, 48) & S2, 16);
S3_shift <= shift_left(to_unsigned(0, 48) & S3, 24);
S4_shift <= shift_left(to_unsigned(0, 48) & S4, 32);
S5_shift <= shift_left(to_unsigned(0, 48) & S5, 40);
S6_shift <= shift_left(to_unsigned(0, 48) & S6, 48);

-- Generate the result
result <= S0_shift + S1_shift + S2_shift + S3_shift + S4_shift + S5_shift + S6_shift;

end karatsuba_arch;