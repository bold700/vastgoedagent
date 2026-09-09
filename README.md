# Vastgoedagent

Onderbouwing en rekengereedschap voor het inzetten van EUR 200.000 overwaarde in
een te verbeteren huurpand, met als doel extra maandelijkse cashflow.

Peildatum 9 september 2026. Alle regelgeving is geverifieerd bij de bron.

## De korte versie

De EUR 200.000 is eigen inbreng, geen koopsom. Bij 60% financiering draagt dat een
project van ongeveer EUR 675.000, mits de waarde na verbouwing minstens gelijk is
aan wat erin is gestopt. Dat laatste is precies waar de meeste plannen stuklopen.

Drie uitkomsten die de richting bepalen:

1. **De marge zit in de inkoopprijs, niet in de verbouwing.** Hetzelfde pand met
   dezelfde huuropbrengst levert EUR 107.650 verlies op bij inkoop tegen
   marktprijs, en EUR 59.350 winst bij inkoop 30% daaronder.
2. **Studio's leveren per vierkante meter het meeste op**, ook na aftrek van de
   extra keukens en badkamers. De rem is gemeentelijk beleid over minimale
   woningoppervlakte, niet de economie.
3. **Het energielabel is de grootste knop.** Van label G naar A is 52 punten in
   het woningwaarderingsstelsel, ongeveer EUR 339 per maand per eenheid aan
   wettelijke huurruimte.

Realistische uitkomst bij volledige inzet van het budget: ongeveer
**EUR 1.000 per maand netto** en **EUR 123.000 waardecreatie**, op een project van
rond de EUR 675.000. Dat is voor aflossing en bij een rente van 5,5%.

## Documenten

| Bestand | Inhoud |
|---|---|
| `docs/01-regelgeving-2026.md` | Overdrachtsbelasting, Wet betaalbare huur, WWS, splitsingsvergunningen, opkoopbescherming, energielabeleisen, box 3 |
| `docs/02-financiering.md` | Overwaarde opnemen, verhuurhypotheek, effect van de financieringsgraad |
| `docs/03-rekenmodel.md` | Aannames, uitkomsten en gevoeligheden |
| `docs/04-strategie-en-kansen.md` | Drie routes en werkelijk aangeboden panden, doorgerekend |
| `docs/05-due-diligence.md` | Wat je uitzoekt voordat je biedt |
| `docs/06-gemeentelijk-kader.md` | Per gemeente: opkoopbescherming, splitsingsregels, minimale woningmaat, Zuid-Limburgse compensatie |

## Gereedschap

```bash
python3 -m tools.scenarios   # vergelijking van vijf strategieen
python3 -m tools.panden      # werkelijk aangeboden panden door het model
```

Een eigen pand doorrekenen:

```python
from tools.wws import Woning
from tools.rendement import Plan

units = [Woning(f"studio {i+1}", opp_vertrekken=38, woz=105_000,
                label="A", transformatie=True) for i in range(4)]
plan = Plan("mijn pand", koopsom=240_000, units=units,
            bouwkosten=180_000, ovb_tarief=0.08)

print(units[0].punten(), units[0].segment(), units[0].max_huur())
print(plan.rapport())
```

De huur wordt niet geschat maar berekend uit het woningwaarderingsstelsel, zodat
de opbrengst per definitie binnen de wet blijft.

## Belangrijkste waarschuwingen

- Meerdere commerciele partijen beweren dat per 1 januari 2026 label C verplicht is
  voor particuliere verhuur. Dat klopt niet. De echte eis is label D per
  1 januari 2029, en er is geen verhuurverbod. Zie `docs/01`.
- Kamerverhuur valt sinds 1 juli 2024 altijd in het gereguleerde sociale segment.
  Bouw **zelfstandige** eenheden, geen kamers.
- Btw is bij transformatie de grootste fiscale valkuil. Verhuur van woonruimte is
  vrijgesteld, dus de 21% btw op de bouwkosten is dan niet terugvorderbaar.
- Sinds 1 juli 2024 is het huurcontract voor onbepaalde tijd de norm. Wil je
  eenheden los verkopen tegen leegwaarde, verkoop ze dan voordat je verhuurt.

Dit is een analyse en geen beleggingsadvies. Laat de fiscale en juridische punten
toetsen door een adviseur voordat je een verplichting aangaat.
