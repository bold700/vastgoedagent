"""Vergelijking van vier value-add strategieen bij EUR 200.000 eigen inbreng.

Draai met:  python3 -m tools.scenarios
"""
from .wws import Woning
from .rendement import Plan

EIGEN_GELD = 200_000


def unit(naam, m2, woz, label="A", **kw):
    return Woning(naam, opp_vertrekken=m2, woz=woz, label=label, **kw)


def plannen():
    return [
        Plan(
            "A. Groot pand splitsen in 3 eenheden, aankoop tegen marktprijs",
            koopsom=225_000,
            units=[unit(f"unit {i+1}", 55, 140_000, transformatie=True) for i in range(3)],
            bouwkosten=200_000, exit_bar=0.085,
        ),
        Plan(
            "B. Zelfde pand, maar 30% onder marktwaarde ingekocht + sobere verbouwing",
            koopsom=160_000,
            units=[unit(f"unit {i+1}", 55, 140_000, transformatie=True) for i in range(3)],
            bouwkosten=120_000, exit_bar=0.085,
        ),
        Plan(
            "C. Bestaand 4-unit rendementspand, label F -> A, geen splitsing",
            koopsom=340_000,
            units=[unit(f"unit {i+1}", 50, 125_000) for i in range(4)],
            bouwkosten=140_000, splitsen=False, exit_bar=0.085,
        ),
        Plan(
            "D. Winkel-woonhuis transformeren naar 3 eenheden",
            koopsom=185_000,
            units=[unit(f"unit {i+1}", 48, 125_000, transformatie=True) for i in range(3)],
            bouwkosten=210_000, exit_bar=0.088,
        ),
        Plan(
            "E. Los turnkey appartement kopen en verhuren (nulmeting)",
            koopsom=165_000,
            units=[unit("appartement", 70, 165_000, label="C")],
            bouwkosten=0, splitsen=False, exit_bar=0.075,
        ),
    ]


def tabel():
    kop = (f"{'strategie':<62}{'inv.':>10}{'huur/mnd':>10}{'waarde':>10}"
           f"{'creatie':>10}{'eigen geld':>12}{'CF/mnd':>9}{'RvEV':>7}{'ICR':>6}")
    print(kop)
    print("-" * len(kop))
    for p in plannen():
        r = p.rapport()
        print(f"{r['naam']:<62}{r['investering']:>10,.0f}{r['huur_pm']:>10,.0f}"
              f"{r['waarde']:>10,.0f}{r['waardecreatie']:>10,.0f}"
              f"{r['eigen_geld']:>12,.0f}{r['cashflow_pm']:>9,.0f}"
              f"{r['rendement_eigen_geld']*100:>6.1f}%{r['rentedekking']:>6.2f}")
    print()
    print(f"Toets: past de eigen inbreng binnen EUR {EIGEN_GELD:,.0f}?")
    for p in plannen():
        r = p.rapport()
        ok = "JA " if r["eigen_geld"] <= EIGEN_GELD else "NEE"
        tekort = max(0, r["eigen_geld"] - EIGEN_GELD)
        extra = f"  tekort {tekort:,.0f}" if tekort else ""
        print(f"  {ok}  {r['naam'][:58]:<58}{r['eigen_geld']:>11,.0f}{extra}")


if __name__ == "__main__":
    tabel()
