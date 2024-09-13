# Matomo: Export zu CSV

## Beschreibung
Mit diesem Python-Skript können Daten, wie Besuche, Seitenansichten und weitere ausgewählte Daten automatisch aus Matomo extrahiert und in eine CSV-Datei abgespeichert werden.

## Vorbereitung
- [Python](https://python.org/) installieren
- requests installieren:
  - in einer Konsole folgenden Befehl eingeben:
  ```
   pip install requests
  ```
- Matomo-Token generieren, Basis-URL und eigene ```idSite``` herausfinden:
    - Matomo-Token kann generiert werden unter Matomo > Enstellungen > Sicherheit > Neuen Token generieren > Nur sicher Anfragen zulassen **abhaken** > Neuen Token generieren
    - ```idSite``` kann in der URL gefunden werden
      - z.B. ```https://MATOMOSITE/index.php?module=CoreHome&action=index&idSite=1&period=month&date=today```: ```idSite``` ist ```1```
    - Die Basis-URL ist die URL bis zum 1. Fragezeichen
      - z.B. ```https://matomo.com/index.php?module=CoreHome&action=index&idSite=1&period=month&date=today```: Basis-URL ist ```https://matomo.com/index.php```
- Diese Daten müssen nun entweder direkt im Skript oder in der Datei ```data.json```, die im gleichen Verzeichnis, wie das Skript liegen muss, eingespeichert werden.

### data.json
In dieser Datei kann konfiguriert werden, welche Daten exportiert werden sollen und wohin.
Diese muss im gleichen Verzeichnis, wie das Skript liegen.
Ein Bespiel für eine data.json kann [hier](examples/data.json) gefunden werden.
#### Werte in der data.json:
- ```token```: Der Token zu Matomo
- ```out```: Der Pfad zur CSV-Datei, in die exportiert werden soll
- ```id_site```: Die ```idSite``` von Matomo
- ```base_url```: Die Basis-URL
- ```mode```: Ob Tagesweise oder Monatsweise extrahiert werden soll (1 = Monatsweise, 2 = Tagesweise)
- ```sites_to_fetch```: Die Seiten, die geholt werden sollen (mehr Infos zur Matomo-API [hier](https://developer.matomo.org/api-reference/reporting-api))
- ```table_data```: Welche Daten aus den Seiten exportiert werden sollen

### table_data
- ```name```: Der Anzeigename in der CSV
- ```idx```: Der Index aus ```sites_to_fetch```, aus welcher Seite der Wert geholt werden soll
- ```field```: Der Schlüssel, wie der Wert als JSON-Export heißt.
- ```factor```: (optional) Ein Produkt mit dem der Wert multipliziert wird.
- ```label```: (optional) Wenn Wert anhand eines labels identifiziert werden muss.

### Hinzufügen von Werten
1. Den Wert in Matomo finden
2. In der Nähe des Wertes (meist unten auf der Tafel auf der der Wert steht), auf das Export-Symbol drücken
3. Exportformat: Json auswählen > EXPORT
4. Im Browser können durch ein Häkchen oben die Werte schöner angezeigt werden
5. Nun mit z.B. Strg.-F den gewünschten Wert suchen
6. Der Schlüssel steht vor dem Wert in Anführungszeichen
7. Wenn es im gleichen Objekt (in den gleichen {}) einen Wert ```label``` gibt, ist dieser in die [table_data](#table_data) einzutragen
8. In der URL muss der Parameter ```method``` in ```sites_to_fetch``` eingetragen werden, wenn nicht schon vorhanden
9. Index abzählen und Werte in data.json hinzufügen

## Verwendung
Nach Starten des Skripts durch Doppelklick, wird dazu aufgefordert, den Start- und Beginnmonat/-tag einzugeben, sowie andere Daten, wenn diese nicht in der data.yml oder im Skript hinterlegt sind.
Danach wird das Programm die Daten exportieren und in der angegebenen CSV-Datei abspeichern. Diese kann nun auch immer wiederverwendet werden, da neue Daten einfach hinzugefügt werden.

## Verbindung mit Excel
Die CSV-Datei kann nun in Excel eingebunden werden unter Daten > aus Text/CSV und werden von Excel automatisch aktualisiert, sobald sich die CSV-Datei ändert.
Alternativ kann mit Rechtsklick auf die Tabelle > Aktualisieren auch manuell aktualisiert werden.
