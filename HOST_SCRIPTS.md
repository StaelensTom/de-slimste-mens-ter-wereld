# Host Scripts & Presentator Teksten - De Slimste Mens Ter Wereld

Dit document bevat alle host scripts en presentator teksten die doorheen het spel verschijnen, georganiseerd per ronde en scherm.

---

## 📋 Overzicht Spelverloop

1. **Start Scherm** - Introductie en spelstart
2. **3-6-9 Ronde** - Eerste speelronde (15 vragen)
3. **Interlude: Einde 3-6-9** - Tussenstand na 3-6-9
4. **Open Deur Ronde** - Foto's met trefwoorden (3 vragen)
5. **Interlude: Einde Open Deur** - Tussenstand na Open Deur
6. **Puzzel Ronde** - Verbanden zoeken (3 puzzels)
7. **Galerij Ronde** - Foto's herkennen (3x10 foto's)
8. **Collectief Geheugen Ronde** - Video fragmenten (3 video's)
9. **Finale** - Hoofd-aan-hoofd tussen 2 finalisten

---

## 🎬 START SCHERM

### Locatie
- **Bestand:** `app/templates/game.html`
- **Sectie:** `<div id="round_start">`
- **Wanneer:** Bij het opstarten van het spel, voor de eerste ronde

### Knoppen
- 🎬 Intro "De Slimste Mens Ter Wereld"
- 🎬 Intro "3-6-9"
- ▶️ Start het spel (zonder intro)
- 📖 Toon Host Scripts (opent modal met 3 scripts)

### Host Script 1: Openingswoorden
**Element ID:** `host_script_1`

```
Wie is de slimste mens ter wereld. Wie heeft geen nood aan een souffleur, maar weet dat hard werk ook komt met hard labeur. 
Wie kent alle gassen in onze atmosfeer, en weet dat Pyrus communis latijn is voor de gewone peer. 
En dat ik mijn cola zonder ijsblokken bestel, want dan krijg je meer.

Is het misschien [Speler 1] - (kort rijmpje)
Of is het misschien [Speler 2] - (kort rijmpje)
Zij worden uitgedaagd door [Speler 3] - (kort rijmpje)

Welkom bij de finale van de slimste mens ter wereld.
```

**Dynamische elementen:**
- `player_name_1_1` - Naam speler 1
- `player_name_2_1` - Naam speler 2
- `player_name_3_1` - Naam speler 3

### Host Script 2: Kandidaten Voorstelling
**Element ID:** `host_script_2`

```
Dag [Speler 1], [Speler 2] en [Speler 3].

Jullie kennen de eerste vraag "Zouden jullie de slimste mens ter wereld kunnen worden"?
Van wie ben je het meeste bang, [Speler 2] of [Speler 3]?

Het wordt tijd om de jury officieel voor te stellen: jurylid 1 en jurylid 2.
De kandidaten, prachtig. Wat verwachten jullie van de kandidaten?
```

**Dynamische elementen:**
- `player_name_1_2` - Naam speler 1
- `player_name_2_2` - Naam speler 2
- `player_name_2_3` - Naam speler 2
- `player_name_3_3` - Naam speler 3

### Host Script 3: Start 3-6-9 Ronde
**Element ID:** `host_script_3`

```
Ik ga 60 seconden uitdelen aan ieder van jullie. Dat is jullie startkapitaal, en je verdient bijkomende seconden per goed antwoord, mogelijk ook in de finale. 
En we beginnen bij 3-6-9
(klik op tune 3-6-9)

De slimste mens kent alle deelgebergten van de karpaten. En babbelt vlotjes over nitraten en fosfaten. 
Maar steekt het ook wijselijk op de hond wanneer je een wind hebt gelaten. Dat is waar, he. 
12 vragen, wie juist antwoord blijft aan de beurt. En elke 3de vraag levert 10 seconden op.

[Speler 1], ik begin bij jou.
```

**Dynamische elementen:**
- `player_name_1_3` - Naam speler 1

**Technische info:**
- Functie: `showStartHostScripts()` - Opent modal met alle 3 scripts
- Functie: `populateHostScriptPlayerNames(players)` - Vult spelernamen in

---

## 🔢 3-6-9 RONDE

### Locatie
- **Bestand:** `app/templates/rounds/369.html`
- **Sectie:** `<div id="round_3-6-9">`
- **Wanneer:** Eerste speelronde

### Beschrijving
- 15 vragen (configureerbaar via `settings["369_round_no"]`)
- Wie juist antwoordt blijft aan de beurt
- Elke 3de vraag (3, 6, 9, 12, 15) levert 10 seconden op
- Andere vragen leveren geen seconden op

### Scripts
Geen aparte host scripts tijdens deze ronde (zie Start Scherm Script 3 voor introductie).

---

## 📊 INTERLUDE: EINDE 3-6-9

### Locatie
- **Bestand:** `app/templates/rounds/InterludeOpenDeur.html`
- **Sectie:** `<div id="round_Interlude_Open_deur">`
- **Wanneer:** Na afloop van de 3-6-9 ronde, voor Open Deur

### Knoppen
- 🎬 Start Intro "Open Deur"

### Host Script: 3-6-9 Resultaten
**Element ID:** `interlude_369_results`

```
En dat brengt ons bij het einde van deze legendarische ronde, waar 
[Speler 1] [0] seconden heeft gescoord, 
[Speler 2] [0] en 
[Speler 3] [0].

Dat geeft deze stand:
[0] voor [Speler],
[0] voor [Speler]
en aan de leiding [Speler] met [0].

Tot zo meteen.
```

**Dynamische elementen:**
- `interlude_player1_name` - Naam speler 1
- `interlude_player1_score` - Score speler 1
- `interlude_player2_name` - Naam speler 2
- `interlude_player2_score` - Score speler 2
- `interlude_player3_name` - Naam speler 3
- `interlude_player3_score` - Score speler 3
- `interlude_lowest_name` - Naam laagste speler
- `interlude_lowest_score` - Score laagste speler
- `interlude_middle_name` - Naam middelste speler
- `interlude_middle_score` - Score middelste speler
- `interlude_highest_name` - Naam hoogste speler
- `interlude_highest_score` - Score hoogste speler

**Technische info:**
- Functie: `populateInterludeScores(players)` - Vult scores in

### Host Script: Open Deur Introductie
**Element ID:** `interlude_opendeur_intro`
**Wanneer:** Verschijnt NA het klikken op "Start Intro Open Deur"

```
(Start tune Open Deur)

We zijn terug in de ronde waar iedereen 1 vraag krijgt waarbij 4 kernwoorden horen, die elk 20 seconden kunnen opleveren. 
Maar dit is onze eerste De Slimste Mens ter Wereld, dus we moeten al even recupereren. 
Dus laten we ons vervangen door deze knappe koppen.

Mieke, huispoes in Poezielaan. Overdag ligt ze lui en in de avond zoekt ze aaitjes voor het plezier.
Tom, zonder twijfel, de knapste man van de avond, die sinds recent werkt voor Uber, maar niet als courier.
Yang, ook zonder twijfel, de knapste vrouw van de avond, en een echte HR-database beheerder avonturier.

[Speler], jullie mogen als eerste kiezen.

… mooie keuze. Hier is zijn/haar vraag.
```

**Dynamische elementen:**
- `interlude_lowest_name_2` - Naam laagste speler (mag eerst kiezen)

**Technische info:**
- Functie: `showOpenDeurIntro()` - Toont dit script na intro
- Functie: `dsmtw.playOpenDeurInterlude()` - Triggert intro en advance

---

## 🚪 OPEN DEUR RONDE

### Locatie
- **Bestand:** `app/templates/rounds/OpenDeur.html`
- **Sectie:** `<div id="round_Open deur">`
- **Wanneer:** Na Interlude Open Deur

### Knoppen
- 📖 Toon Script (alleen zichtbaar bij de 3 foto's, niet bij trefwoorden)

### Host Script: Open Deur Introductie (Herhaling)
**Element ID:** `opendeur_host_script`
**Wanneer:** Alleen zichtbaar bij het tonen van de 3 foto's (questioneers)

```
(Start tune Open Deur)

We zijn terug in de ronde waar iedereen 1 vraag krijgt waarbij 4 kernwoorden horen, die elk 20 seconden kunnen opleveren. 
Maar dit is onze eerste De Slimste Mens ter Wereld, dus we moeten al even recupereren. 
Dus laten we ons vervangen door deze knappe koppen.

Mieke, huispoes in Poezielaan. Overdag ligt ze lui en in de avond zoekt ze aaitjes voor het plezier.
Tom, zonder twijfel, de knapste man van de avond, die sinds recent werkt voor Uber, maar niet als courier.
Yang, ook zonder twijfel, de knapste vrouw van de avond, en een echte HR-database beheerder avonturier.

[Speler], jullie mogen als eerste kiezen.

… mooie keuze. Hier is zijn/haar vraag.
```

**Dynamische elementen:**
- `opendeur_lowest_name` - Naam laagste speler (mag eerst kiezen)

**Technische info:**
- Functie: `populateOpenDeurHostScript(players)` - Vult spelernamen in
- Functie: `showOpenDeurHostScript()` - Opent modal met script
- Script button wordt alleen getoond bij `state.answer_time === false` (foto's zichtbaar)
- Script button wordt verborgen bij `state.answer_time === true` (trefwoorden zichtbaar)

### Beschrijving
- 3 vragen (1 per speler)
- Elke vraag heeft 1 foto en 4 trefwoorden
- Elk correct trefwoord levert 20 seconden op
- Speler met minste seconden mag eerst een foto kiezen

---

## 📊 INTERLUDE: EINDE OPEN DEUR

### Locatie
- **Bestand:** `app/templates/rounds/InterludeOpenDeurResults.html`
- **Sectie:** `<div id="round_Interlude_Open_deur_Results">`
- **Wanneer:** Na afloop van Open Deur ronde, voor Puzzel

### Knoppen
- 🎬 Start Intro "Puzzel"

### Host Script: Open Deur Resultaten
**Element ID:** `interlude_opendeur_results`

```
We gaan kijken naar de stand op het einde van deze ronde.
[Speler] [0] seconden,
[Speler] [0] seconden
en aan de leiding staat [Speler] op [0] seconden.
```

**Dynamische elementen:**
- `interlude_opendeur_lowest_name` - Naam laagste speler
- `interlude_opendeur_lowest_score` - Score laagste speler
- `interlude_opendeur_middle_name` - Naam middelste speler
- `interlude_opendeur_middle_score` - Score middelste speler
- `interlude_opendeur_highest_name` - Naam hoogste speler
- `interlude_opendeur_highest_score` - Score hoogste speler

**Technische info:**
- Functie: `populateInterludeOpenDeurResultsScores(players)` - Vult scores in

### Host Script: Puzzel Introductie (Verborgen)
**Element ID:** `interlude_opendeur_puzzel_intro`
**Wanneer:** Gebruikt voor modal/intro, niet direct zichtbaar

```
(Tune puzzel ronde)

Zet je fobie voor de puzzel ronde maar aan de kant, want hier zijn we er mee. 
Zoek de 3 verbanden, want elk goede oplossing levert je 30 seconden op. 
Hier komt de eerste puzzel.
```

**Technische info:**
- Functie: `dsmtw.playPuzzelInterlude()` - Triggert intro en advance naar Puzzel

---

## 🧩 PUZZEL RONDE

### Locatie
- **Bestand:** `app/templates/rounds/Puzzel.html`
- **Sectie:** `<div id="round_Puzzel">`
- **Wanneer:** Na Interlude Open Deur Results

### Beschrijving
- 3 puzzels (1 per speler)
- Elke puzzel heeft 3 verbanden
- Elk correct verband levert 30 seconden op
- Speler met minste seconden begint

### Scripts
Geen aparte host scripts tijdens deze ronde (zie Interlude Open Deur Results voor introductie).

---

## 🖼️ GALERIJ RONDE

### Locatie
- **Bestand:** `app/templates/rounds/Galerij.html`
- **Sectie:** `<div id="round_Galerij">`
- **Wanneer:** Na Puzzel ronde

### Knoppen
- 📖 Toon Script (alleen bij eerste foto van elke speler)

### Host Script: Galerij Introductie
**Element ID:** `galerij_host_script`
**Wanneer:** Alleen bij eerste foto (subround 0)

```
Gewoon zeggen wie of wat je ziet, op de foto's of tekeningen die zo meteen passeren. 
Per juist antwoord verdien je 15 seconden. 
[Speler], de eerste fotorond is voor jou.
```

**Dynamische elementen:**
- `galerij_lowest_name` - Naam laagste speler (begint)

**Technische info:**
- Functie: `populateGalerijHostScript(players)` - Vult spelernamen in
- Functie: `showGalerijHostScript()` - Opent modal met script
- Script wordt alleen getoond bij `state.current_subround === 0`

### Beschrijving
- 3 fotoreeksen (1 per speler)
- Elke reeks heeft 10 foto's
- Elk correct antwoord levert 15 seconden op
- Speler met minste seconden begint

---

## 🎬 COLLECTIEF GEHEUGEN RONDE

### Locatie
- **Bestand:** `app/templates/rounds/CollectiefGeheugen.html`
- **Sectie:** `<div id="round_Collectief geheugen">`
- **Wanneer:** Na Galerij ronde

### Knoppen
- 📖 Toon Script (alleen bij eerste video)
- ▶️ Start Finale (na laatste video)

### Host Script: Collectief Geheugen Introductie
**Element ID:** `collectief_geheugen_intro`
**Wanneer:** Alleen bij eerste video (subround 0)

```
In deze ronde kijken we wie alles weet in de filmpjesronde. 
Alles is nog mogelijk, slechts 1 ding is zeker, na deze ronde weten we welke 2 teams mogen strijden voor de titel van slimste mens ter wereld. 
Hier komt het eerste fragment, en dat is voor [Speler].
```

**Dynamische elementen:**
- `collectief_geheugen_lowest_name` - Naam laagste speler (begint)

**Technische info:**
- Functie: `populateCollectiefGeheugenIntro(players)` - Vult spelernamen in
- Functie: `showCollectiefGeheugenIntro()` - Opent modal met script
- Intro sectie wordt alleen getoond bij `state.current_subround === 0`

### Host Script: Collectief Geheugen Afsluiting
**Element ID:** `collectief_geheugen_outro`
**Wanneer:** Na laatste video (when `state.to_advance === 'round'`)

```
We hebben een eindstand. [Speler], we moeten afscheid van jou nemen. 
We spelen met [Speler 1] en [Speler 2] het finalspel. 
Zijn jullie er klaar voor.

Jury, wie denken jullie die zal winnen?
```

**Dynamische elementen:**
- `collectief_geheugen_eliminated_name` - Naam geëlimineerde speler
- `collectief_geheugen_finalist1_name` - Naam finalist 1
- `collectief_geheugen_finalist2_name` - Naam finalist 2

**Technische info:**
- Functie: `populateCollectiefGeheugenOutro(players)` - Vult spelernamen in
- Outro sectie wordt alleen getoond bij `state.to_advance === 'round'`

### Beschrijving
- 3 video's (1 per speler)
- Elke video heeft 5 vragen
- Variabele seconden per vraag
- Na deze ronde vallen 1 speler af, 2 gaan naar finale

---

## 🏆 FINALE

### Locatie
- **Bestand:** `app/templates/rounds/Finale.html`
- **Sectie:** `<div id="round_Finale">`
- **Wanneer:** Na Collectief Geheugen (alleen 2 finalisten)

### Knoppen
- 📖 Toon Script (alleen bij eerste vraag)

### Host Script: Finale Introductie
**Element ID:** `finale_intro`
**Wanneer:** Alleen bij eerste vraag (subround 0)

```
Je moet de tijd van de andere op 0 krijgen. 
Dat doe je door goede antwoorden te geven, want per goed antwoord gaan er 20 seconden af bij de tegenstander. 
En de vraag gaat telkens eerst naar diegene met de minste seconden. 
Roep je stop, dan gaat de beurt naar de volgende. 
En we zoeken altijd 5 mogelijke antwoorden.

[Speler 1] [0] seconden, 
[Speler 2] [0] seconden. 
[Speler], we beginnen bij jou.
```

**Dynamische elementen:**
- `finale_player1_name` - Naam finalist 1
- `finale_player1_score` - Score finalist 1
- `finale_player2_name` - Naam finalist 2
- `finale_player2_score` - Score finalist 2
- `finale_starting_player` - Naam speler die begint (laagste score)

**Technische info:**
- Functie: `populateFinaleIntro(players)` - Vult spelernamen en scores in
- Functie: `showFinaleIntro()` - Opent modal met script
- Intro sectie wordt alleen getoond bij `state.current_subround === 0`

### Beschrijving
- Hoofd-aan-hoofd tussen 2 finalisten
- Elke vraag heeft 5 antwoorden
- Elk correct antwoord: -20 seconden voor tegenstander
- Speler met 0 seconden verliest
- Speler met minste seconden krijgt de vraag

---

## 🔧 TECHNISCHE INFORMATIE

### JavaScript Functies (HostScript.js)

#### Start Scherm
- `populateHostScriptPlayerNames(players)` - Vult spelernamen in alle start scripts
- `showStartHostScripts()` - Opent modal met alle 3 start scripts

#### Interlude Open Deur (na 3-6-9)
- `populateInterludeScores(players)` - Vult scores in na 3-6-9
- `showOpenDeurIntro()` - Toont Open Deur intro tekst

#### Open Deur Ronde
- `populateOpenDeurHostScript(players)` - Vult spelernamen in Open Deur script
- `showOpenDeurHostScript()` - Opent modal met Open Deur script

#### Interlude Open Deur Results (na Open Deur)
- `populateInterludeOpenDeurResultsScores(players)` - Vult scores in na Open Deur

#### Galerij Ronde
- `populateGalerijHostScript(players)` - Vult spelernamen in Galerij script
- `showGalerijHostScript()` - Opent modal met Galerij script

#### Collectief Geheugen Ronde
- `populateCollectiefGeheugenIntro(players)` - Vult spelernamen in intro
- `showCollectiefGeheugenIntro()` - Opent modal met intro script
- `populateCollectiefGeheugenOutro(players)` - Vult spelernamen in outro

#### Finale
- `populateFinaleIntro(players)` - Vult spelernamen en scores in finale intro
- `showFinaleIntro()` - Opent modal met finale script

### Modal Systeem
- `openHostScriptModal(content)` - Opent modal met gegeven content
- `closeHostScriptModal()` - Sluit modal

### Spelverloop (dsmtw.js)
- `dsmtw.playMainIntro()` - Speelt hoofdintro af
- `dsmtw.playRoundIntro()` - Speelt 3-6-9 intro af
- `dsmtw.startGame()` - Start spel zonder intro
- `dsmtw.playOpenDeurInterlude()` - Triggert Open Deur intro en advance
- `dsmtw.playPuzzelInterlude()` - Triggert Puzzel intro en advance
- `dsmtw.advanceRound()` - Gaat naar volgende ronde

---

## 📝 NOTITIES

### Belangrijke Patronen
1. **Script Visibility**: Scripts worden alleen getoond op specifieke momenten (eerste foto, eerste video, etc.)
2. **Dynamic Content**: Alle spelernamen en scores worden dynamisch ingevuld via JavaScript
3. **Modal System**: Alle scripts worden getoond in een centrale modal overlay
4. **State Management**: Visibility wordt gecontroleerd via `state.current_subround` en `state.to_advance`

### Customization Points
- **Spelernamen**: Automatisch ingevuld, maar rijmpjes bij start moeten handmatig aangepast worden
- **Jury namen**: Hardcoded in start script 2
- **Open Deur personen**: Mieke, Tom, Yang - kunnen aangepast worden in beide Open Deur scripts
- **Aantal vragen**: 3-6-9 heeft 15 vragen (configureerbaar), andere rondes hebben 3 vragen/videos/puzzels

### Volgorde van Verschijning
1. Start → Host Scripts 1, 2, 3
2. 3-6-9 → (geen scripts tijdens ronde)
3. Interlude → 3-6-9 resultaten + Open Deur intro
4. Open Deur → Script bij foto's (niet bij trefwoorden)
5. Interlude → Open Deur resultaten + Puzzel intro
6. Puzzel → (geen scripts tijdens ronde)
7. Galerij → Script bij eerste foto
8. Collectief Geheugen → Intro bij eerste video + Outro na laatste video
9. Finale → Script bij eerste vraag

---

**Laatste update:** 22 december 2024
**Versie:** 1.0
**Branch:** presentator-teksten
