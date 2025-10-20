import unittest  # import knihovny pro testování

class Teplomer:
    def __init__(self, max_teplota=100):
        """Inicializuje objekt teploměru s výchozí teplotou 0 a maximální teplotou."""
        self.teplota = 0
        self.max_teplota = max_teplota

    def nastav_teplotu(self, nova_teplota):
        """Nastaví aktuální teplotu na hodnotu nova_teplota.
        Pokud přesáhne maximální teplotu, vyvolá výjimku."""
        if nova_teplota > self.max_teplota:
            raise ValueError("Teplota přesáhla maximální povolenou hodnotu!")
        self.teplota = nova_teplota

    def oteplit(self, stupne):
        """Zvýší teplotu o zadaný počet stupňů.
        Pokud výsledná teplota přesáhne maximální povolenou hodnotu, vyvolá výjimku."""
        if self.teplota + stupne > self.max_teplota:
            raise ValueError("Teplota přesáhla maximální povolenou hodnotu!")
        self.teplota += stupne

    def ochladit(self, stupne):
        """Sníží teplotu o zadaný počet stupňů.
        Teplota nesmí klesnout pod -273.15 °C."""
        nova_teplota = self.teplota - stupne
        self.teplota = max(nova_teplota, -273.15)


# ---------------------- TESTOVACÍ TŘÍDA ----------------------

class TestTeplomer(unittest.TestCase):  # testovací třída pro Teplomer

    def test_inicializace(self):  # 1️ Test inicializace
        t = Teplomer()  # vytvoření objektu
        self.assertEqual(t.teplota, 0)  # teplota má být 0
        self.assertEqual(t.max_teplota, 100)  # max_teplota výchozí = 100
        t2 = Teplomer(200)  # jiný limit
        self.assertEqual(t2.max_teplota, 200)  # kontrola nastavení limitu

    def test_nastaveni_teploty(self):  # 2️ Test nastavení teploty
        t = Teplomer()  # nový teploměr
        t.nastav_teplotu(50)  # nastavíme platnou teplotu
        self.assertEqual(t.teplota, 50)  # kontrola hodnoty
        with self.assertRaises(ValueError):  # očekáváme chybu při překročení limitu
            t.nastav_teplotu(150)

    def test_zvyseni_teploty(self):  # 3️ Test zvýšení teploty
        t = Teplomer()  # nový teploměr
        t.nastav_teplotu(80)  # výchozí hodnota
        t.oteplit(10)  # zvýšíme o 10
        self.assertEqual(t.teplota, 90)  # kontrola nové hodnoty
        with self.assertRaises(ValueError):  # pokus o překročení limitu
            t.oteplit(20)

    def test_snizeni_teploty(self):  # 4Test snížení teploty
        t = Teplomer()  # nový teploměr
        t.nastav_teplotu(0)  # výchozí hodnota
        t.ochladit(10)  # snížíme o 10
        self.assertEqual(t.teplota, -10)  # kontrola hodnoty
        t.ochladit(300)  # pokus o pokles pod -273.15 °C
        self.assertEqual(t.teplota, -273.15)  # teplota nesmí být nižší


# ---------------------- SPUŠTĚNÍ TESTŮ ----------------------

if __name__ == "__main__":  # spuštění testů při přímém běhu
    unittest.main(verbosity=2)  # zvýšená podrobnost výpisu
