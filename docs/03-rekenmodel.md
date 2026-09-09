# Rekenmodel en uitkomsten

Alle cijfers komen uit `tools/`. Draaien met `python3 -m tools.scenarios`.

## Aannames

| Post | Waarde | Toelichting |
|---|---|---|
| Overdrachtsbelasting | 8% | woningtarief 2026 |
| Aankoopkosten | ca. EUR 8.100 | notaris, kadaster, taxatie, advies, keuring |
| Leges omgevingsvergunning | 3% van de bouwsom | |
| Ontwerp en constructeur | 8% van de bouwsom | 2% bij verbouwing zonder splitsing |
| Onvoorzien | 10% van de bouwsom | ondergrens bij oude panden |
| Nutsaansluitingen | EUR 5.500 per extra eenheid | eigen meter per woning |
| Leegstand en oninbaar | 5% van de huur | |
| Beheer | 6% van de effectieve huur | nul bij zelfbeheer |
| Onderhoudsreservering | EUR 1.400 per eenheid per jaar | |
| Verzekering | EUR 420 per eenheid per jaar | |
| Gemeentelijke lasten | EUR 550 per eenheid per jaar | OZB, riool, waterschap |
| Rente | 5,5% | |
| Financieringsgraad | 60% van waarde in verhuurde staat | |
| Bruto aanvangsrendement bij taxatie | 8,5% | secundaire regio, gereguleerde huur |

De huur per eenheid wordt niet geschat maar **berekend** uit het
woningwaarderingsstelsel, zodat de opbrengst per definitie binnen de wet blijft.

## Uitkomst 1: bij marktprijs inkopen werkt niet

Vier value-add strategieen, telkens met huur volgens het WWS:

| Strategie | Investering | Huur per maand | Waarde | Waardecreatie | Eigen geld |
|---|---|---|---|---|---|
| Groot pand splitsen in 3, ingekocht tegen marktprijs | 508.000 | 2.836 | 400.350 | **-107.650** | 267.790 |
| Zelfde pand, 30% onder marktwaarde, sobere verbouwing | 341.000 | 2.836 | 400.350 | **+59.350** | 100.790 |
| Bestaand 4-unit pand, label F naar A, niet splitsen | 537.300 | 3.278 | 462.810 | **-74.490** | 259.614 |
| Winkel-woonhuis transformeren naar 3 eenheden | 476.900 | 2.670 | 364.111 | **-112.789** | 258.433 |
| Los turnkey appartement kopen (nulmeting) | 186.300 | 818 | 130.922 | **-55.378** | 107.747 |

Alleen de tweede regel levert waarde op, en het verschil met de eerste regel zit
volledig in de **inkoopprijs**, niet in de verbouwing. De huur is in beide regels
identiek.

Dit is de belangrijkste uitkomst van de hele analyse. Bouwkosten zijn landelijk,
huren en waarden zijn lokaal. In een goedkope regio verdien je een verbouwing van
EUR 1.000 per vierkante meter niet terug uit een huur van EUR 900 per maand. De
marge zit in wat je betaalt voor het casco.

## Uitkomst 2: de drempelprijs

De hoogste koopsom waarbij het project na verbouwing niet minder waard is dan het
heeft gekost. Uitgangspunt: een pand van 200 m2 dat drie eenheden van 55 m2
oplevert, huur EUR 907 per eenheid inclusief transformatieopslag.

| Verbouwbudget | Maximale koopsom | Koopsom per m2 |
|---|---|---|
| 80.000 | 259.768 | 1.299 |
| 120.000 | 214.953 | 1.075 |
| 160.000 | 170.139 | 851 |
| 200.000 | 125.324 | 627 |
| 240.000 | 80.509 | 403 |

Zet dit af tegen de goedkoopste gemeenten van Nederland, waar de gemiddelde
vraagprijs EUR 1.995 tot EUR 2.500 per m2 is. Je moet dus ver onder de gemiddelde
marktprijs inkopen. Dat lukt niet met een normale woning in normale staat. Het lukt
alleen bij panden die voor een eigenaar-bewoner onbruikbaar of onfinancierbaar zijn.

## Uitkomst 3: hoeveel cashflow koopt EUR 200.000

Inkoop op de drempelprijs, 60% financiering:

| Omvang | Koopsom | Verbouwing | Investering | Waarde | Waardecreatie | Eigen geld | Cashflow per maand |
|---|---|---|---|---|---|---|---|
| 3 eenheden | 160.000 | 120.000 | 341.000 | 400.350 | 59.350 | 100.790 | 701 |
| 4 eenheden | 215.000 | 160.000 | 455.000 | 533.800 | 78.800 | 134.720 | 804 |
| 5 eenheden | 270.000 | 200.000 | 569.000 | 667.249 | 98.249 | 168.650 | 906 |
| **6 eenheden** | **320.000** | **240.000** | **677.600** | **800.699** | **123.099** | **197.180** | **1.008** |
| 8 eenheden | 430.000 | 320.000 | 905.600 | 1.067.599 | 161.999 | 265.041 | 1.213 |

Zes eenheden gebruikt de EUR 200.000 vrijwel exact op, met een rentedekking van
1,76. Dat is het antwoord op de vraag: ongeveer **EUR 1.000 per maand netto** en
ongeveer **EUR 123.000 aan waardecreatie**, bij een project van rond de
EUR 675.000 totaal.

## Wat het model niet meeneemt

- Aflossing. De cashflow is voor aflossing. Is maar de helft aflossingsvrij, dan
  gaat er bij 60% financiering ongeveer EUR 400 per maand af.
- Rente- en huurderving tijdens de verbouwing. Reken op zes tot twaalf maanden
  zonder inkomsten terwijl de rente doorloopt.
- Het vervallen van de leegwaarderatio per 1 januari 2027, dat de box 3-grondslag
  verhoogt.
- Waardegroei of waardedaling van het vastgoed zelf.
- Vennootschapsbelasting; het model gaat uit van bezit in prive, in box 3.

## Gevoeligheid die er echt toe doet

| Variabele | Effect |
|---|---|
| Rente van 5,5% naar 7% | cashflow van 1.008 naar 408 per maand, ICR naar 1,38 |
| Bruto aanvangsrendement bij aankoop onder 7% | cashflow wordt negatief |
| Energielabel G in plaats van A | ongeveer EUR 339 per maand per eenheid minder huur |
| Bouwkosten 20% hoger dan begroot | waardecreatie verdampt vrijwel volledig |

De laatste regel is de reden voor de post onvoorzien van 10% en voor een
ontbindende voorwaarde op de vergunning.
