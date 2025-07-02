import EPCI
import os

os.system("python barometre_EPCI_2025_big_percent.py "+"MEL")

for key, value in EPCI.all.items():
    os.system("python barometre_EPCI_2025_big_percent.py "+key)
    os.system("python barometre_EPCI_2021_big_percent.py "+key )
    os.system("python barometre_EPCI_2025_big.py "+key)
    os.system("python barometre_EPCI_2021_big.py "+key)
