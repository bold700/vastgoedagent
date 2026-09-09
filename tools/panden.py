"""Werkelijke, op 9 september 2026 aangeboden panden, doorgerekend met het model.

Alle panden zijn afkomstig van een daadwerkelijk geraadpleegde aanbieding; de
bron staat per pand vermeld. Prijzen zijn vraagprijzen kosten koper.
Dit is geen advies en geen taxatie: het is een eerste zeef.
"""
from dataclasses import dataclass
from .wws import Woning
from .rendement import Plan


@dataclass
class Pand:
    naam: str
    koopsom: float
    m2_te_ontwikkelen: float     # vloeroppervlak dat je omzet naar wonen
    eenheden: int                # aantal zelfstandige eenheden na verbouwing
    woz_per_eenheid: float
    bron: str
    ovb: float = 0.104           # winkel/bedrijfsruimte; 8% als het een woning is
    compensatie: float = 0.0     # Zuid-Limburgse transformatiecompensatie
    huur_bestaand_pj: float = 0.0   # lopende huur die je overneemt
    opmerking: str = ""

    def netto_m2_per_eenheid(self) -> float:
        return self.m2_te_ontwikkelen * 0.82 / self.eenheden   # 18% verkeersruimte

    def plan(self, bouwkosten_per_m2: float) -> Plan:
        m2 = self.netto_m2_per_eenheid()
        units = [Woning(f"eenheid {i+1}", opp_vertrekken=m2,
                        woz=self.woz_per_eenheid, transformatie=True)
                 for i in range(self.eenheden)]
        return Plan(self.naam, self.koopsom, units,
                    bouwkosten=self.m2_te_ontwikkelen * bouwkosten_per_m2,
                    ovb_tarief=self.ovb, exit_bar=0.085, ltv=0.60, bron=self.bron,
                    compensatie_per_eenheid=self.compensatie)

    def max_bouwkosten_per_m2(self, ondergrens=100, bovengrens=3000) -> float:
        """Hoogste bouwkosten per m2 waarbij de waarde de investering nog dekt."""
        laag, hoog = ondergrens, bovengrens
        for _ in range(50):
            mid = (laag + hoog) / 2
            if self.plan(mid).waardecreatie() >= 0:
                laag = mid
            else:
                hoog = mid
        return laag


PANDEN = [
    Pand("Heerlen, Wilhelminaplein 6", 295_000, 420, 7, 105_000,
         "bedrijfspand.com/.../wilhelminaplein-6-heerlen/107658", compensatie=6_251,
         opmerking="494 m2 totaal, 209 m2 lege bovenverdiepingen, bouwjaar 1909, "
                   "aangeboden als transformatieobject"),
    Pand("Heerlen, Geleenstraat 64", 330_000, 700, 11, 100_000,
         "bedrijfspand.com/.../geleenstraat-64-heerlen/114407", compensatie=6_251,
         opmerking="944 m2 bvo in de hoofdwinkelstraat, appartementsrecht in "
                   "actieve VvE, nu verhuurd"),
    Pand("Geleen, Marktpad 10-14", 450_000, 260, 5, 115_000,
         "bedrijfspand.com/.../marktpad-10-geleen/122851", compensatie=7_175,
         opmerking="4 huisnummers, 2 lege bovenwoningen, bestemming Centrum-1 "
                   "laat wonen toe"),
    Pand("Hulst, Frans van Waesberghestraat 5", 245_000, 209, 3, 120_000,
         "bedrijfspand.com/.../frans-van-waesberghestraat-5-hulst/123053",
         opmerking="voormalige slagerij 125 m2 plus bovenwoning 84 m2, leeg"),
    Pand("Terneuzen, Noordstraat 82", 290_000, 199, 3, 115_000,
         "bedrijfspand.com/.../noordstraat-82-terneuzen/103242",
         huur_bestaand_pj=14_100,
         opmerking="winkel verhuurd, bovenwoning 84 m2 nooit verhuurd geweest"),
    Pand("Coevorden, Weeshuisstraat 27", 347_500, 314, 5, 110_000,
         "bedrijfspand.com/.../weeshuisstraat-27-coevorden/114566",
         opmerking="220 m2 bedrijfsruimte plus turnkey appartement 94 m2"),
    Pand("Sittard, Tunnelstraat 93-95", 425_000, 148, 3, 125_000,
         "bedrijfspand.com/.../tunnelstraat-95-sittard/116054", compensatie=7_175,
         huur_bestaand_pj=36_207,
         opmerking="winkel verhuurd tot 2031, bovenwoning 148 m2 met 5 slaapkamers"),
    Pand("Meerssen, Beekstraat 58", 575_000, 0, 4, 130_000,
         "bedrijfspand.com/.../beekstraat-58-meerssen/105925",
         huur_bestaand_pj=32_500,
         opmerking="4 eenheden, alleen bouwkundig gesplitst, notariele splitsing "
                   "is de value-add; gemeentelijk monument"),
]


def zeef(bouwkosten_per_m2=1_100):
    kop = (f"{'pand':<38}{'vraagprijs':>11}{'m2':>6}{'eenh':>5}"
           f"{'invest.':>10}{'waarde':>10}{'creatie':>10}{'eigen geld':>12}"
           f"{'CF/mnd':>8}{'max bouw/m2':>13}")
    print(kop); print("-" * len(kop))
    for p in PANDEN:
        if p.m2_te_ontwikkelen == 0:
            print(f"{p.naam:<38}{p.koopsom:>11,.0f}{'-':>6}{p.eenheden:>5}"
                  f"{'geen verbouwing, zie toelichting':>45}")
            continue
        r = p.plan(bouwkosten_per_m2).rapport()
        print(f"{p.naam:<38}{p.koopsom:>11,.0f}{p.m2_te_ontwikkelen:>6.0f}"
              f"{p.eenheden:>5}{r['investering']:>10,.0f}{r['waarde']:>10,.0f}"
              f"{r['waardecreatie']:>10,.0f}{r['eigen_geld']:>12,.0f}"
              f"{r['cashflow_pm']:>8,.0f}{p.max_bouwkosten_per_m2():>13,.0f}")


if __name__ == "__main__":
    print("Zeef bij bouwkosten van EUR 1.100 per m2\n")
    zeef(1_100)
