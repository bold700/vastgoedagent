"""Groeimodel naar een doelinkomen uit een woningportefeuille.

Rekent twee dingen uit:
  1. hoeveel vastgoed en eigen vermogen een doelcashflow vereist, in box 3 en in een BV;
  2. een jaar-op-jaar groeipad vanaf een startbedrag, met herinvestering.

Draai met:  python3 -m tools.portfolio
"""
from __future__ import annotations
from dataclasses import dataclass

# fiscaal 2026
BOX3_BEZIT, BOX3_SCHULD, BOX3_TARIEF = 0.06, 0.0262, 0.36
BOX3_VRIJ_PARTNERS = 118_714.0
VPB_LAAG, VPB_GRENS, VPB_HOOG = 0.19, 200_000.0, 0.258
BOX2_LAAG, BOX2_GRENS, BOX2_HOOG = 0.245, 68_843.0, 0.31
OVB = 0.08

# exploitatie
BAR = 0.085              # bruto aanvangsrendement bij taxatie
OPEX_VAST = 2_370.0      # per eenheid per jaar: onderhoud, verzekering, gem. lasten
LEEGSTAND = 0.05
RENTE = 0.055
HUURGROEI = 0.041        # gereguleerd sociaal 2026


def box3_heffing(waarde, schuld, vrijstelling=BOX3_VRIJ_PARTNERS):
    grondslag = waarde - schuld
    if grondslag <= vrijstelling:
        return 0.0
    rendement = waarde * BOX3_BEZIT - schuld * BOX3_SCHULD
    return max(0.0, rendement) * ((grondslag - vrijstelling) / grondslag) * BOX3_TARIEF


def vpb(winst):
    if winst <= 0:
        return 0.0
    return (min(winst, VPB_GRENS) * VPB_LAAG
            + max(0.0, winst - VPB_GRENS) * VPB_HOOG)


def box2(uitkering):
    if uitkering <= 0:
        return 0.0
    return (min(uitkering, BOX2_GRENS) * BOX2_LAAG
            + max(0.0, uitkering - BOX2_GRENS) * BOX2_HOOG)


def netto_cashflow(waarde, ltv, eenheden, structuur="box3", beheer=0.0):
    """Netto besteedbare cashflow per jaar bij een gegeven portefeuillewaarde."""
    schuld = waarde * ltv
    huur = waarde * BAR
    eff = huur * (1 - LEEGSTAND)
    noi = eff - eenheden * OPEX_VAST - eff * beheer
    rente = schuld * RENTE
    if structuur == "box3":
        return noi - rente - box3_heffing(waarde, schuld)
    # BV: vpb over de winst, daarna box 2 om het geld prive te krijgen
    winst = noi - rente                      # afschrijving beperkt door bodemwaarde
    na_vpb = winst - vpb(winst)
    return na_vpb - box2(na_vpb)


def benodigde_omvang(doel_pj, ltv, structuur="box3", m2_per_eenheid=60,
                     prijs_per_m2=2_400):
    """Zoek de portefeuillewaarde die het doelinkomen oplevert."""
    laag, hoog = 100_000.0, 30_000_000.0
    for _ in range(80):
        mid = (laag + hoog) / 2
        eenheden = max(1, round(mid / (m2_per_eenheid * prijs_per_m2)))
        if netto_cashflow(mid, ltv, eenheden, structuur) < doel_pj:
            laag = mid
        else:
            hoog = mid
    waarde = hoog
    return waarde, waarde * (1 - ltv), max(1, round(waarde / (m2_per_eenheid * prijs_per_m2)))


DOEL = 6_000 * 12

if __name__ == "__main__":
    print(f"Doel: EUR {DOEL:,.0f} netto per jaar, oftewel EUR 6.000 per maand\n")
    kop = (f"{'structuur':<10}{'financiering':>14}{'portefeuille':>14}"
           f"{'eigen vermogen':>17}{'eenheden':>10}{'huur/mnd':>11}")
    print(kop); print("-" * len(kop))
    for structuur in ("box3", "bv"):
        for ltv in (0.0, 0.30, 0.45, 0.60, 0.70):
            w, ev, n = benodigde_omvang(DOEL, ltv, structuur)
            print(f"{structuur:<10}{ltv:>13.0%}{w:>14,.0f}{ev:>17,.0f}"
                  f"{n:>10}{w*BAR/12:>11,.0f}")


# ---------------------------------------------------------------- groeipad ----
@dataclass
class Aannames:
    start_eigen_geld: float = 200_000
    jaarlijkse_inleg: float = 0.0        # wat je er zelf nog bij stort
    ltv: float = 0.60
    prijs_per_eenheid: float = 145_000   # koopsom inclusief kosten koper
    huur_start_pm: float = 700           # bij aankoop, matig energielabel
    huur_na_label_pm: float = 950        # na verduurzaming naar label A
    upgrade_bruto: float = 30_000        # kosten labelsprong per eenheid
    svoh_deel: float = 0.30              # subsidie, max EUR 15.000 per woning
    svoh_max: float = 15_000
    mutatiegraad: float = 0.15           # deel van de huurders dat per jaar wisselt
    beheer: float = 0.0                  # zelfbeheer
    structuur: str = "box3"
    bv_vanaf_jaar: int | None = None     # None = altijd dezelfde structuur
    korting_inkoop: float = 0.0          # deel onder marktwaarde ingekocht
    direct_upgraden: bool = False        # leegstaand kopen, meteen verduurzamen


def groeipad(a: Aannames, jaren=25, doel_pm=6_000):
    kas = a.start_eigen_geld
    eenheden_oud = 0        # nog niet verduurzaamd
    eenheden_nieuw = 0      # verduurzaamd, hogere huur
    schuld = 0.0
    huur_index = 1.0
    rijen = []
    for jaar in range(1, jaren + 1):
        structuur = a.structuur
        if a.bv_vanaf_jaar and jaar >= a.bv_vanaf_jaar:
            structuur = "bv"
        huur_index *= (1 + HUURGROEI) if jaar > 1 else 1.0

        # 1. verduurzamen wat vrijkomt bij mutatie
        graad = 1.0 if a.direct_upgraden else a.mutatiegraad
        te_upgraden = min(eenheden_oud, max(0, round(eenheden_oud * graad)))
        netto_kosten = a.upgrade_bruto - min(a.upgrade_bruto * a.svoh_deel, a.svoh_max)
        if te_upgraden and kas >= te_upgraden * netto_kosten:
            kas -= te_upgraden * netto_kosten
            eenheden_oud -= te_upgraden
            eenheden_nieuw += te_upgraden

        # 2. waarde en herfinanciering op de nieuwe huur
        huur_pj = (eenheden_oud * a.huur_start_pm
                   + eenheden_nieuw * a.huur_na_label_pm) * 12 * huur_index
        waarde = huur_pj / BAR if huur_pj else 0.0
        ruimte = max(0.0, waarde * a.ltv - schuld)
        kas += ruimte
        schuld += ruimte

        # 3. bijkopen zolang er eigen geld is
        koopsom = a.prijs_per_eenheid * (1 - a.korting_inkoop)
        eigen_per_eenheid = koopsom * (1 - a.ltv) + koopsom * OVB
        gekocht = 0
        while kas >= eigen_per_eenheid:
            kas -= eigen_per_eenheid
            schuld += koopsom * a.ltv
            eenheden_oud += 1
            gekocht += 1

        # 4. resultaat van het jaar
        n = eenheden_oud + eenheden_nieuw
        huur_pj = (eenheden_oud * a.huur_start_pm
                   + eenheden_nieuw * a.huur_na_label_pm) * 12 * huur_index
        waarde = huur_pj / BAR if huur_pj else 0.0
        eff = huur_pj * (1 - LEEGSTAND)
        noi = eff - n * OPEX_VAST - eff * a.beheer
        rente = schuld * RENTE
        if structuur == "box3":
            cf = noi - rente - box3_heffing(waarde, schuld)
        else:
            winst = noi - rente
            na = winst - vpb(winst)
            cf = na - box2(na)
        kas += cf + a.jaarlijkse_inleg
        rijen.append(dict(jaar=jaar, eenheden=n, nieuw=eenheden_nieuw, gekocht=gekocht,
                          waarde=waarde, schuld=schuld, ev=waarde - schuld,
                          cf_pm=cf / 12, kas=kas, structuur=structuur))
        if cf / 12 >= doel_pm:
            break
    return rijen


def toon(titel, rijen, doel_pm=6_000):
    print(f"\n{titel}")
    kop = (f"{'jaar':>5}{'eenheden':>10}{'waarvan A':>11}{'gekocht':>9}"
           f"{'portefeuille':>14}{'schuld':>12}{'eigen verm.':>13}{'CF/mnd':>9}")
    print(kop); print("-" * len(kop))
    for r in rijen:
        if r["jaar"] % 2 == 1 or r is rijen[-1]:
            print(f"{r['jaar']:>5}{r['eenheden']:>10}{r['nieuw']:>11}{r['gekocht']:>9}"
                  f"{r['waarde']:>14,.0f}{r['schuld']:>12,.0f}{r['ev']:>13,.0f}"
                  f"{r['cf_pm']:>9,.0f}")
    laatste = rijen[-1]
    if laatste["cf_pm"] >= doel_pm:
        print(f"  -> doel van EUR {doel_pm:,.0f} per maand bereikt in jaar {laatste['jaar']}")
    else:
        print(f"  -> na {laatste['jaar']} jaar: EUR {laatste['cf_pm']:,.0f} per maand")
