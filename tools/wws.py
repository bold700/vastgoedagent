"""Woningwaarderingsstelsel (WWS) 2026 - puntentelling zelfstandige woonruimte.

Bronnen en peildatum staan in docs/01-regelgeving-2026.md.
Alle bedragen zijn prijspeil 1 januari 2026.
"""
from __future__ import annotations
from dataclasses import dataclass, field

# Energielabelpunten, label geregistreerd na 1-1-2021 (Beleidsboek Huurcommissie).
LABELPUNTEN_APPARTEMENT = {
    "A++++": 58, "A+++": 53, "A++": 48, "A+": 43, "A": 37,
    "B": 30, "C": 15, "D": 11, "E": -4, "F": -9, "G": -15,
}
LABELPUNTEN_EENGEZINS = {
    "A++++": 62, "A+++": 57, "A++": 52, "A+": 47, "A": 41,
    "B": 34, "C": 22, "D": 14, "E": -4, "F": -9, "G": -15,
}

WOZ_PER_PUNT = 16_954.0        # onderdeel I: 1 punt per EUR WOZ-waarde
WOZ_PER_M2_PER_PUNT = 268.0    # onderdeel II: 1 punt per EUR WOZ per m2
WOZ_CAP_AANDEEL = 0.33         # WOZ telt max 33% van totaal, alleen boven 187 punten

GRENS_SOCIAAL = 143            # t/m 143 punten = gereguleerd sociaal
GRENS_MIDDEN = 186             # 144 t/m 186 = gereguleerd middenhuur
HUUR_GRENS_SOCIAAL = 932.93    # max kale huur bij 143 punten
HUUR_GRENS_MIDDEN = 1_228.07   # max kale huur bij 186 punten (liberalisatiegrens)
EURO_PER_PUNT = 6.52           # 932.93 / 143; de tabel is nagenoeg lineair

NIEUWBOUW_OPSLAG = 0.10        # 10% opslag, 20 jaar, ook bij transformatie


@dataclass
class Woning:
    """Eén zelfstandige wooneenheid."""
    naam: str
    opp_vertrekken: float          # m2 woonkamer/slaapkamers/keuken (1 pt per m2)
    woz: float                     # WOZ-waarde ná splitsing, per eenheid
    label: str = "A"
    appartement: bool = True
    opp_overig: float = 0.0        # berging/zolder zonder daglicht: 0,75 pt per m2
    punten_keuken: float = 9.0     # aanrecht >=2m = 7, plus kwaliteitspunten
    punten_sanitair: float = 9.0   # douche 4 + toilet 3 + wastafel 1, plus kwaliteit
    punten_verwarming: float = 2.0 # 2 pt per verwarmd vertrek
    punten_buitenruimte: float = 2.0  # 0 = geen; aftrek van 5 vervalt per 2027
    punten_overig: float = 0.0     # bijzondere voorzieningen, gemeenschappelijk
    monument: bool = False
    transformatie: bool = False    # nieuw toegevoegde woning -> 10% opslag

    def woz_punten(self) -> float:
        m2 = max(self.opp_vertrekken + self.opp_overig, 1.0)
        return self.woz / WOZ_PER_PUNT + (self.woz / m2) / WOZ_PER_M2_PER_PUNT

    def label_punten(self) -> float:
        tabel = LABELPUNTEN_APPARTEMENT if self.appartement else LABELPUNTEN_EENGEZINS
        pts = tabel[self.label]
        if self.monument and pts < 0:
            return 0.0            # monumenten krijgen geen strafpunten
        return pts

    def punten(self) -> float:
        woz = self.woz_punten()
        overig = (
            self.opp_vertrekken
            + 0.75 * self.opp_overig
            + self.label_punten()
            + self.punten_keuken
            + self.punten_sanitair
            + self.punten_verwarming
            + self.punten_buitenruimte
            + self.punten_overig
        )
        totaal = overig + woz
        if totaal > 187:                       # WOZ-cap bijt alleen boven 187 punten
            max_woz = overig * WOZ_CAP_AANDEEL / (1 - WOZ_CAP_AANDEEL)
            totaal = overig + min(woz, max_woz)
        return round(totaal, 1)

    def segment(self) -> str:
        p = self.punten()
        if p <= GRENS_SOCIAAL:
            return "gereguleerd sociaal"
        if p <= GRENS_MIDDEN:
            return "gereguleerd middenhuur"
        return "vrije sector"

    def max_huur(self) -> float:
        """Maximale kale huur per maand volgens het WWS."""
        p = self.punten()
        if p > GRENS_MIDDEN:
            return float("inf")
        huur = p * EURO_PER_PUNT
        plafond = HUUR_GRENS_SOCIAAL if p <= GRENS_SOCIAAL else HUUR_GRENS_MIDDEN
        huur = min(huur, plafond)
        if self.transformatie:
            huur *= 1 + NIEUWBOUW_OPSLAG
        return round(huur, 2)


def vergelijk_labels(basis: Woning, labels=("G", "F", "E", "D", "C", "B", "A", "A+", "A++")):
    """Wat levert verduurzaming op in punten en euro's per maand?"""
    uit = []
    for lab in labels:
        w = Woning(**{**basis.__dict__, "label": lab})
        uit.append((lab, w.punten(), w.max_huur()))
    return uit
