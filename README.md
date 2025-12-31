# Adaptable – blockbaserad appbyggare

Det här projektet är ett första steg mot ett verktyg där organisationer kan bygga appar utan att skriva kod. Utifrån ett litet blockbibliotek kan man kombinera layouter, dataflöden och interaktioner och spara resultatet som en blåkopia (JSON). En enkel CLI guidar användaren genom att skapa och koppla block.

## Snabbstart

1. **Skapa en tom blåkopia**

   ```bash
   python -m adaptable.cli init --name "Supportverktyg" --output blueprint.json
   ```

2. **Lägg till block** – ange blocktyp, unik nyckel och valfria fält som `--config key=value`.

   ```bash
   python -m adaptable.cli add --blueprint blueprint.json --type page --key start --config title=Start
   python -m adaptable.cli add --blueprint blueprint.json --type form --key kontaktform --config fields=namn,epost
   python -m adaptable.cli add --blueprint blueprint.json --type api-request --key skapa-ärende --config url=https://api.exempel.se/incidents method=POST
   python -m adaptable.cli add --blueprint blueprint.json --type action-button --key skicka --config label=Skicka action=skapa-ärende
   ```

3. **Koppla block** – beskriver hur data eller navigation hänger ihop.

   ```bash
   python -m adaptable.cli connect --blueprint blueprint.json --source skicka --target skapa-ärende --purpose triggers
   python -m adaptable.cli connect --blueprint blueprint.json --source kontaktform --target skicka --purpose submits
   python -m adaptable.cli connect --blueprint blueprint.json --source start --target kontaktform --purpose contains
   ```

4. **Förhandsvisa** – genererar en textuell översikt som kan delas i teamet.

   ```bash
   python -m adaptable.cli preview --blueprint blueprint.json
   ```

5. **Utforska biblioteket** – se vilka blocktyper som finns att tillgå.

   ```bash
   python -m adaptable.cli library
   ```

## Blockbibliotek (nuvarande urval)

- **Layout**: `page`, `card`
- **Data**: `data-list`, `form`
- **Interaktion**: `action-button`, `api-request`

## Vad som ingår i blåkopian

Varje blåkopia sparas som JSON och innehåller:

- `name` – appens namn
- `blocks` – lista med block, deras typ och konfiguration
- `connections` – relationer som beskriver hur block samspelar (t.ex. navigation eller dataflöden)

## Nästa steg

- Lägga till fler blocktyper (t.ex. autentisering, tabeller och dashboards)
- Exportera till färdiga UI-komponenter och generera en körbar app
- Webbaserat gränssnitt som bygger vidare på samma API som CLI:n
