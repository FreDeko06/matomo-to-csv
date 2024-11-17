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
    - Matomo-Token kann generiert werden unter Matomo > Enstellungen > Sicherheit > Neuen Token generieren > Neuen Token generieren
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
4. add.py starten
5. Die URL, die durch 3. geöffnet wurde aus dem Browser in das Programm kopieren
6. Den jetzigen Wert in das Programm eintragen
7. Den richtigen Datenpunkt finden und die rote Zahl davor eingeben
8. Einen Namen für die Tabelle festlegen (**Jeder Name darf nur einmal verwendet werden**)
9. Die JSON-Objekte werden ausgegeben oder direkt in die data.json geschrieben
10. Wenn sie manuell eingefügt werden, muss ```idx``` noch geändert werden!

## Verwendung
Nach Starten des Skripts durch Doppelklick, wird dazu aufgefordert, den Start- und Endmonat/-tag einzugeben, sowie andere Daten, wenn diese nicht in der data.json oder im Skript hinterlegt sind.
Danach wird das Programm die Daten exportieren und in der angegebenen CSV-Datei abspeichern. Diese kann nun auch immer wiederverwendet werden, da neue Daten einfach hinzugefügt werden.

## Verbindung mit Excel
Die CSV-Datei kann nun in Excel eingebunden werden unter Daten > aus Text/CSV und werden von Excel automatisch aktualisiert, sobald sich die CSV-Datei ändert.
Alternativ kann mit Rechtsklick auf die Tabelle > Aktualisieren auch manuell aktualisiert werden.
