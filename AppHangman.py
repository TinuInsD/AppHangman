import csv
from typing import List
from collections import Counter
import random

class CuvantGhicit:
    def __init__(self, index: int, indiciu: str, cuvant: str):
        self.index = index
        self.cuvant = cuvant
        self.indiciu = indiciu

def incarca_cuvinte_din_fisier(nume_fisier: str) -> List[CuvantGhicit]:
    cuvinte = []
    with open(nume_fisier, "r", encoding="utf-8") as fisier:
        reader = csv.reader(fisier, delimiter=';')
        for linie in reader:
            if len(linie) == 3:
                index = int(linie[0])
                indiciu = linie[1]
                cuvant = linie[2]
                cuvinte.append(CuvantGhicit(index, indiciu, cuvant))
    return cuvinte

def obtine_indici_litere_cunoscute(indiciu: str) -> List[int]:
    return [i for i, caracter in enumerate(indiciu) if caracter != '*']

def obtine_pozitii_litera(cuvant: str, litera: str) -> List[int]:
    return [i for i, caracter in enumerate(cuvant) if caracter == litera]

def filtreaza_cuvinte_posibile(cuvinte_posibile: List[str], indiciu: str, indici_cunoscute: List[int]) -> List[str]:
    return [cuvant for cuvant in cuvinte_posibile
            if len(cuvant) == len(indiciu) and all(cuvant[i] == indiciu[i] for i in indici_cunoscute)]

def obtine_litera_aleatorie(cuvinte_posibile: List[str], litere_incercate: set) -> str:
    toate_literele = [caracter for cuvant in cuvinte_posibile for caracter in cuvant if
                      caracter not in litere_incercate]
    if toate_literele:
        return random.choice(toate_literele)

def rezolva_spanzuratoarea(indiciu: str, lista_cuvinte: List[CuvantGhicit]) -> int:
    cuvinte_posibile = [cuvant.cuvant for cuvant in lista_cuvinte]
    indici_cunoscute = obtine_indici_litere_cunoscute(indiciu)
    cuvinte_filtrate = filtreaza_cuvinte_posibile(cuvinte_posibile, indiciu, indici_cunoscute)
    numar_incercari = 0
    litere_incercate = set()
    indiciu_curent = list(indiciu)

    while '*' in indiciu_curent and len(cuvinte_filtrate) > 0:
        litera_curenta = obtine_litera_aleatorie(cuvinte_filtrate, litere_incercate)
        litere_incercate.add(litera_curenta)
        numar_incercari += 1
        pozitii_litera = obtine_pozitii_litera(cuvinte_filtrate[0], litera_curenta)
        if pozitii_litera:
            for pozitie in pozitii_litera:
                indiciu_curent[pozitie] = litera_curenta
    return numar_incercari

def main():
    print("Bine ai venit la rezolvatorul automat de spânzurătoare!")
    lista_cuvinte = incarca_cuvinte_din_fisier("cuvinte_de_verificat.txt")
    numar_total_incercari = 0
    for cuvant in lista_cuvinte:
        incercari = rezolva_spanzuratoarea(cuvant.indiciu, lista_cuvinte)
        print(f"Cuvânt: {cuvant.cuvant}, Găsit în {incercari} încercări")
        numar_total_incercari += incercari
    print(f"Numărul total de încercări: {numar_total_incercari}")
    if numar_total_incercari > 1200:
        print("Soluția a depășit 1200 de încercări.")
    else:
        print("Soluția nu a depășit 1200 de încercări.")

if __name__ == "__main__":
    main()