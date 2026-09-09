"""Rendements- en cashflowmodel voor NL woningbeleggingen, fiscaal regime 2026.

Rekent een value-add plan door: aankoop, verbouwing/splitsing, herfinanciering,
exploitatie en box 3. Zie docs/03-rekenmodel.md voor de aannames.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from .wws import Woning

# --- fiscale en financieringsparameters 2026 ---
OVB_WONING_BELEGGING = 0.08      # per 1-1-2026 (was 10,4%); 2027 voorgenomen 7%
BOX3_FORFAIT_BEZIT = 0.06        # overige bezittingen
BOX3_FORFAIT_SCHULD = 0.0262     # schuldenforfait
BOX3_TARIEF = 0.36
BOX3_HEFFINGSVRIJ = 59_357.0     # per persoon; fiscale partners 2x


@dataclass
class Kosten:
    notaris_akte: float = 1_800
    kadaster: float = 800
    taxatie: float = 1_100
    hypotheekadvies: float = 3_500
    bouwkundige_keuring: float = 900
    makelaar_aankoop: float = 0.0

    def totaal(self) -> float:
        return sum(v for v in self.__dict__.values())


@dataclass
class Plan:
    naam: str
    koopsom: float
    units: List[Woning]
    bouwkosten: float = 0.0
    splitsen: bool = True              # bouwkundig splitsen -> extra posten
    exit_bar: float = 0.085            # bruto aanvangsrendement bij taxatie
    ltv: float = 0.60                  # verhuurhypotheek op waarde in verhuurde staat
    rente: float = 0.055
    leegstand: float = 0.05
    beheer: float = 0.06               # 0 bij zelfbeheer
    onderhoud_pj: float = 1_400        # per eenheid, reservering
    verzekering_pj: float = 420
    gem_lasten_pj: float = 550         # OZB, riool, waterschap
    kosten: Kosten = field(default_factory=Kosten)
    box3_vrijstelling: float = BOX3_HEFFINGSVRIJ * 2
    ovb_tarief: float = OVB_WONING_BELEGGING   # 10,4% bij levering als bedrijfspand
    bron: str = ""                             # URL of vindplaats van de aanbieding

    # ---------- investering ----------
    def overdrachtsbelasting(self) -> float:
        return self.koopsom * self.ovb_tarief

    def ontwikkelkosten(self) -> float:
        n = len(self.units)
        if self.bouwkosten == 0:
            return 0.0
        leges = self.bouwkosten * 0.03                      # omgevingsvergunning
        ontwerp = self.bouwkosten * (0.08 if self.splitsen else 0.02)
        onvoorzien = self.bouwkosten * 0.10
        nuts = (n - 1) * 5_500 if self.splitsen else 0      # aparte aansluitingen
        splitsingsakte = (1_800 + n * 450) if self.splitsen else 0
        labels = n * 250
        return (self.bouwkosten + leges + ontwerp + onvoorzien
                + nuts + splitsingsakte + labels)

    def totale_investering(self) -> float:
        return (self.koopsom + self.overdrachtsbelasting()
                + self.kosten.totaal() + self.ontwikkelkosten())

    # ---------- exploitatie ----------
    def bruto_huur_pj(self) -> float:
        return sum(u.max_huur() for u in self.units) * 12

    def exploitatiekosten_pj(self) -> float:
        n = len(self.units)
        effectief = self.bruto_huur_pj() * (1 - self.leegstand)
        return (n * (self.onderhoud_pj + self.verzekering_pj + self.gem_lasten_pj)
                + effectief * self.beheer)

    def noi_pj(self) -> float:
        return self.bruto_huur_pj() * (1 - self.leegstand) - self.exploitatiekosten_pj()

    # ---------- waarde en financiering ----------
    def waarde_verhuurde_staat(self) -> float:
        return self.bruto_huur_pj() / self.exit_bar

    def hypotheek(self) -> float:
        return self.waarde_verhuurde_staat() * self.ltv

    def eigen_geld(self) -> float:
        return self.totale_investering() - self.hypotheek()

    def waardecreatie(self) -> float:
        return self.waarde_verhuurde_staat() - self.totale_investering()

    # ---------- fiscaal ----------
    def box3_pj(self) -> float:
        grondslag = self.waarde_verhuurde_staat() - self.hypotheek()
        if grondslag <= self.box3_vrijstelling:
            return 0.0
        rendement = (self.waarde_verhuurde_staat() * BOX3_FORFAIT_BEZIT
                     - self.hypotheek() * BOX3_FORFAIT_SCHULD)
        belast_deel = (grondslag - self.box3_vrijstelling) / grondslag
        return max(0.0, rendement * belast_deel) * BOX3_TARIEF

    # ---------- resultaat ----------
    def cashflow_pj(self) -> float:
        return self.noi_pj() - self.hypotheek() * self.rente - self.box3_pj()

    def rapport(self) -> dict:
        eg = self.eigen_geld()
        return {
            "naam": self.naam,
            "eenheden": len(self.units),
            "investering": self.totale_investering(),
            "per_eenheid": self.totale_investering() / len(self.units),
            "bruto_huur_pj": self.bruto_huur_pj(),
            "huur_pm": self.bruto_huur_pj() / 12,
            "noi_pj": self.noi_pj(),
            "waarde": self.waarde_verhuurde_staat(),
            "waardecreatie": self.waardecreatie(),
            "hypotheek": self.hypotheek(),
            "eigen_geld": eg,
            "box3_pj": self.box3_pj(),
            "cashflow_pj": self.cashflow_pj(),
            "cashflow_pm": self.cashflow_pj() / 12,
            "bar_op_kostprijs": self.bruto_huur_pj() / self.totale_investering(),
            "rendement_eigen_geld": self.cashflow_pj() / eg if eg > 0 else float("nan"),
            "rentedekking": (self.noi_pj() / (self.hypotheek() * self.rente)
                             if self.hypotheek() else float("inf")),
        }


def max_koopsom(plan: Plan, eis: str = "cashflow", doel: float = 0.0,
                eigen_geld_max: float = 200_000.0) -> float:
    """Hoogste koopsom waarbij het plan nog aan de gestelde eis voldoet.

    eis = "cashflow"      -> cashflow per jaar >= doel
    eis = "waardecreatie" -> waarde in verhuurde staat >= totale investering
    eis = "eigen_geld"    -> benodigde eigen inbreng <= eigen_geld_max
    """
    from copy import deepcopy
    laag, hoog = 0.0, 2_000_000.0
    for _ in range(60):
        mid = (laag + hoog) / 2
        p = deepcopy(plan)
        p.koopsom = mid
        if eis == "cashflow":
            ok = p.cashflow_pj() >= doel
        elif eis == "waardecreatie":
            ok = p.waardecreatie() >= doel
        else:
            ok = p.eigen_geld() <= eigen_geld_max
        if ok:
            laag = mid
        else:
            hoog = mid
    return laag
