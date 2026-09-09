# Due diligence: wat je uitzoekt voordat je biedt

Werk deze lijst af **voordat** je een bod uitbrengt, en neem ontbindende
voorwaarden op voor de punten die je niet vooraf hard krijgt.

## A. Mag het uberhaupt

1. **Omgevingsplan.** Staat wonen toe op dit adres? Zo nee, dan is een BOPA nodig:
   maximaal 26 weken wettelijke termijn, verplichte participatie, in de praktijk
   vier tot twaalf maanden. Vraag altijd eerst vooroverleg aan bij de gemeente.
2. **Woningvormings- of splitsingsvergunning.** Heeft de gemeente die in de
   huisvestingsverordening? Wat zijn de weigeringsgronden?
3. **Minimale oppervlakte per nieuwe woning.** Dit is de meest bepalende
   gemeentelijke regel voor een studioplan. Vraag het getal expliciet op.
4. **Quota, moratoria of wijkverboden** op splitsen of kamerverhuur.
5. **Opkoopbescherming.** Geldt die op dit adres, en onder welke WOZ-grens? Een
   pand dat op de leveringsdatum geen woning is, valt er buiten.
6. **Verhuurvergunning** onder de Wet goed verhuurderschap.
7. **Zuid-Limburg:** geldt regionaal beleid dat het toevoegen van woningen
   koppelt aan compensatie elders? Laat de gemeente dit schriftelijk bevestigen.
8. **Monumentenstatus,** rijks- of gemeentelijk. Beperkt de ingrepen, maar geeft
   ook vrijstelling van de energielabelstrafpunten en straks een zwaardere weging
   in het WWS.
9. **VvE.** Bij een appartementsrecht in een actieve VvE heb je medewerking nodig
   voor splitsing en vaak voor gevelingrepen. Lees de splitsingsakte en het
   huishoudelijk reglement.

## B. Wat het gaat opbrengen

10. Bereken de WWS-punten per beoogde eenheid met `tools/wws.py`. Reken met het
    label **na** verduurzaming en met de WOZ **na** splitsing.
11. Toets of het resultaat onder 143 punten blijft. Zo ja, dan is de huur
    gemaximeerd op EUR 932,93 en is de vrije sector geen optie.
12. Controleer of de eenheden in aanmerking komen voor de opslag van 10% voor
    door transformatie toegevoegde woningen. Laat dit door de gemeente en een
    huurrechtjurist bevestigen; het scheelt ongeveer EUR 80 per eenheid per maand.
13. Toets de berekende huur aan de werkelijke markthuur ter plaatse. In een
    krimpregio kan de markt onder het wettelijk maximum liggen; dan is de markt de
    bovengrens, niet het WWS.

## C. Wat het gaat kosten

14. Vraag een aannemersbegroting op **voordat** je biedt en leg die naast de
    maximale bouwkosten per m2 uit `tools/panden.py`.
15. Laat geluidsisolatie en brandcompartimentering apart begroten. Dat zijn bij
    splitsing de duurste en meest onderschatte posten.
16. Reken op EUR 5.500 per extra eenheid aan nutsaansluitingen en losse meters.
17. Houd minimaal 10% onvoorzien aan bij panden ouder dan vijftig jaar. Bij
    Wilhelminaplein 6, bouwjaar 1909, eerder 15%.
18. Reken zes tot twaalf maanden huurderving mee terwijl de rente doorloopt.

## D. Fiscaal, vooraf met een adviseur

19. **Overdrachtsbelasting.** 8% voor woningen, 10,4% voor bedrijfsmatig vastgoed.
    Bij een winkel-woonhuis bepaalt de kwalificatie op de leveringsdatum het
    tarief, en wordt gesplitst naar gebruik. Op EUR 300.000 scheelt dat EUR 7.200.
20. **Btw.** Dit is de grootste fiscale valkuil bij transformatie. Levert de
    verbouwing "in wezen nieuwbouw" op, dan ontstaat voor de btw een nieuw
    vervaardigd goed. Verhuur van woonruimte is btw-vrijgesteld, dus de 21% btw op
    de bouwkosten is dan **niet terugvorderbaar** en de herzieningstermijn loopt
    tien jaar. Verkoop binnen twee jaar na eerste ingebruikname is juist belast
    met 21% btw. Leg deze twee vragen voor aan een btw-specialist voordat je
    tekent:
    - is hier sprake van vervaardiging;
    - wat is per scenario, verhuren dan wel verkopen, het netto btw-resultaat.
21. **Box 3.** Neem mee dat de leegwaarderatio per 1 januari 2027 vervalt, wat de
    grondslag van verhuurd vastgoed verhoogt.
22. **Renteaftrek.** De rente op de opgenomen overwaarde is niet aftrekbaar en
    verlaagt bovendien je eigenwoningschuld met renteaftrek. Laat het effect op je
    huidige hypotheek doorrekenen.
23. Weeg prive-bezit in box 3 af tegen een BV. Bij meerdere eenheden en actieve
    ontwikkeling kan een BV gunstiger uitpakken.

## E. Het pand zelf

24. Bouwkundige keuring, gericht op fundering, dak, houtrot en asbest. Bij
    bouwjaren voor 1994 is asbest een reeel risico.
25. Bestaande huurcontracten opvragen en lezen. Sinds 1 juli 2024 is het contract
    voor onbepaalde tijd de norm; een zittende huurder krijg je niet zonder rechter
    weg. Toets ook of de lopende huur boven de maximale WWS-huur ligt, want dan
    koop je een huurverlagingsclaim mee.
26. Bij een executieveiling: dataroom volledig doorlezen, bijkomende kosten
    optellen, en er rekening mee houden dat ontruiming voor rekening en risico van
    de koper is. De aanname dat veilingen forse korting geven klopt in 2026 niet
    meer: in het vierde kwartaal van 2025 lag de gerealiseerde veilingwaarde
    gemiddeld op 100% van de WOZ-waarde.
27. Energielabel opvragen. Geen label betekent in het WWS de punten van het
    bouwjaar, wat bij oude panden zwaar negatief uitpakt.

## F. Financiering

28. Vraag vooraf aan je geldverstrekker of de verbouwing meegefinancierd kan
    worden en tegen welke waardegrondslag.
29. Toets de rentedekking. Verstrekkers eisen minimaal 1,25, bij hogere
    financiering 1,35. Reken de dekking ook door op 7% rente.
30. Controleer welk deel aflossingsvrij mag blijven; dat bepaalt je werkelijke
    vrij besteedbare cashflow.
