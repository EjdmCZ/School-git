# -*- coding: utf-8 -*-
import unittest  # importujeme knihovnu pro testování

def to_uppercase(text):
    if not isinstance(text, str):  # kontrola, zda je vstup text (string)
        raise TypeError("Vstup musí být text (str), nikoli číslo nebo jiný typ.")  # vyvolání chyby, pokud není
    return text.upper()  # převedeme text na velká písmena


# ---------------------- TESTY FUNKCE ----------------------

class TestToUppercase(unittest.TestCase):  # definice testovací třídy

    def test_uppercase_word(self):  # test pro jedno slovo
        self.assertEqual(to_uppercase("ahoj"), "AHOJ")  # očekáváme převod na velká písmena

    def test_uppercase_sentence(self):  # test pro větu
        self.assertEqual(to_uppercase("Dnes je hezky"), "DNES JE HEZKY")  # ověření převodu celé věty

    def test_input_is_not_string(self):  # test, že číslo způsobí chybu
        with self.assertRaises(TypeError):  # očekáváme vyvolání výjimky
            to_uppercase(12345)  # číslo není text

    def test_input_is_string_type(self):  # test, že funkce funguje jen s textem
        self.assertIsInstance(to_uppercase("text"), str)  # výsledek by měl být typu str


# Spuštění testů, pokud je soubor spuštěn přímo
if __name__ == "__main__":  # ochrana před automatickým spuštěním při importu
    unittest.main()  # spustí všechny testy
