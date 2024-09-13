#Basis-URL kann hier geändert werden
base_url = ""

#Token kann hier gespeichert werden
saved_token = ""

#Ausgabedatei kann hier gespeichert werden
saved_out = ""

#siteID von Matomo
saved_site_id = ""

#Für welchen Zeitraum sollen Daten geholt werden
#mode = 1 --> Monatsweise
#mode = 2 --> Tagesweise
mode = 0    

#Abgerufene Daten
sites_to_fetch = []

table_data = []

import os
import json
import re
from datetime import datetime
import requests
import time
import urllib.parse
import sys
import calendar

def main():
    print("Hinweis!\nDie Ausgabedatei darf nicht verwendet werden! Bitte alle Anwendungen, die diese direkt benutzen schließen!\n")
    
    if os.path.isfile(os.getcwd() + "/data.json"):
        print("data.json wird verwendet!")
        with open(os.getcwd() + "/data.json", 'r', encoding='utf-8') as data_file:
            try:
                fetch_data = json.load(data_file)
            except ValueError as e:
                raise ValueError(f"JSON-Fehler: {e}")
        if isinstance(fetch_data, dict):
            stf = fetch_data.get("sites_to_fetch")
            if stf == None:
                print("Keine URL-Daten in Datei gefunden!")
            else:
                global sites_to_fetch
                sites_to_fetch = stf
            
            td = fetch_data.get("table_data")
            if stf == None:
                print("Keine Tabellen-Daten in Datei gefunden!")
            else:
                global table_data
                table_data = td
            
            tok = fetch_data.get("token")
            if tok != None:
                global saved_token
                saved_token = tok
            
            tok = fetch_data.get("id_site")
            if tok != None:
                global saved_site_id
                saved_site_id = tok
                
            tok = fetch_data.get("out")
            if tok != None:
                global saved_out
                saved_out = tok
                
            tok = fetch_data.get("mode")
            if tok != None:
                global mode
                mode = tok
                
            tok = fetch_data.get("base_url")
            if tok != None:
                global base_url
                base_url = tok

    if saved_token == "":
        token = input("Bitte Token eingeben > ")
    else:
        token = saved_token
        
    if saved_site_id == "":
        site_id = input("Bitte Seiten-ID eingeben > ")
    else:
        site_id = saved_site_id
    
    day = ""
    ex = ""
    one = "Monat"
    if mode == 2:
        day = "Tag."
        ex = "20."
        one = "Tag"
    time_start = input(f"Bitte Start-{day}Monat.Jahr eingeben (z.B. {ex}09.2023) > ")
    
    time_end = input(f"Bitte End-{day}Monat.Jahr eingeben ([ENTER] wenn nur ein {one}) > ")
 
    day, month, year = parse_month_year(time_start)
    if time_end == "":
        month_end = month
        year_end = year
        day_end = day
    else:
        day_end, month_end, year_end = parse_month_year(time_end)
    
    if f"{year}-{month:02d}-{day:02d}" > f"{year_end}-{month_end:02d}-{day:02d}":
        raise ValueError("Startmonat muss kleiner als Endmonat sein!")
        
    
    if saved_out == "":
        out_path = input("Ausgabedatei > ") 
    else:
        out_path = saved_out
        
    
    if mode < 0 or mode > 2:
        raise ValueError(f"\"mode\" hat einen ungültigen Wert: {mode}")
    
    req_and_write(year, month, day, year_end, month_end, day_end, site_id, token, out_path)
    
    
def req_and_write(s_year, s_month, s_day, e_year, e_month, e_day, site_id, token, out_path):
    if e_day == -1:
        e_day = calendar.monthrange(e_year, e_month)[1]
    if s_day == -1:
        s_day = 1
    dates = f"{s_year}-{s_month:02d}-{s_day}%2C{e_year}-{e_month:02d}-{e_day}"
    built_url = build_url(dates, site_id, token)
    print("Daten holen...")
    contents = requests.get(built_url)
    parsed = contents.json()
    parse_and_write_data(parsed, out_path, s_month, s_year)

def parse_month_year(to_parse):
    try:
        splitted = to_parse.split('.')
        if len(splitted) == 2:
            month_str, year_str = to_parse.split('.')
            day = -1
            month = int(month_str)
            year = int(year_str)
        elif len(splitted) == 3:
            day_str, month_str, year_str = to_parse.split('.')
            day = int(day_str)
            month = int(month_str)
            year = int(year_str)
        else:
            raise ValueError("Datum hat falsches Format")
        if len(year_str) != 4:
            raise ValueError("Jahr hat falsches Format!")
        if not (1 <= month <= 12):
            raise ValueError("Monat ist ungültig!")
        return day, month, year
    except ValueError as e:
        raise ValueError(f"{e}")
        
def build_url(dates, site_id, token):
    url = base_url + "?module=API&format=JSON&method=API.getBulkRequest"
    period = "range"
    if mode == 1:
        period = "month"
    if mode == 2:
        period = "day"
    for i in range(len(sites_to_fetch)):
        url += f"&urls[{i}]={urllib.parse.quote_plus(urllib.parse.urlencode(sites_to_fetch[i]), safe='%2C')}%26idSite%3D{site_id}%26format_metrics%3D0"
    url = f"{url}&period={period}&date={dates}&token_auth={token}"
    return url

def parse_and_write_data(data, out_path, month, year):
    if isinstance(data, dict):
        if data.get("result","") == "error":
            raise ValueError(data.get('message', str(data)))
            
    
    #Check for errors
    if isinstance(data, list):
        for entry in data:
            if isinstance(entry, dict):
                if entry.get("result", "") == "error":
                    raise ValueError(entry.get("message", str(data)))
    
    print("Daten verarbeiten...")
    
    #Mode 0 --> range
    #Mode 1 --> month
    #Mode 2 --> day
    lines = read_existing(os.path.abspath(out_path))
    if mode == 0:
        write_line_to_list(create_data(data, m), lines, month, year)
    elif mode == 1:
        for m in data[0].keys():
            year, month = m.split("-")
            month = int(month)
            year = int(year)
            write_line_to_list(create_data(data, m), lines, month, year)
    elif mode == 2:
        for m in data[0].keys():
            year, month, day = m.split("-")
            month = int(month)
            year = int(year)
            day = int(day)
            write_line_to_list(create_data(data, m), lines, month, year, day)
    
    print("Daten speichern...")
    lines.sort()
    save(os.path.abspath(out_path), lines)
    print("Speichern abgeschlossen!")
    

def create_data(data, date=""):
    month_data = []
    for i in range(len(table_data)):
        idx = table_data[i].get("idx", -1)
        name = table_data[i].get("name", "")
        field = table_data[i].get("field", "")
        label = table_data[i].get("label", "")
        factor = table_data[i].get("factor", 1)
        if label == "":
            if date != "":
                month_data.append(data[idx].get(date).get(field, -1))
            else:
                month_data.append(data[idx].get(field, -1))
        else:
            if date != "":
                month_data.append(next((entry.get(field, 0) for entry in data[idx].get(date) if entry.get("label", "") == label), 0))
            else:
                month_data.append(next((entry.get(field, 0) for entry in data[idx] if entry.get("label", "") == label), 0))
        month_data[i] = month_data[i] * factor
    
    return month_data
    
def read_existing(path):
    
    lines = []
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                file_lines = file.read().splitlines()
                lines.extend(file_lines[1:])
        except PermissionError as err:
            raise ValueError(f"{err}\nBitte versuchen alle Anwendungen, die diese Datei verwenden zu schließen!")
    return lines
    
def write_line_to_list(m_data, llist, month, year, day=0):
    line = f"{year}-{month:02d}"
    if day > 0:
        line = line + f"-{day:02d}"
        
    for i in range(len(m_data)):
        val = f"{m_data[i]}".replace(".", ",")
        line += f";{val}"
        
    llist.append(line)
    
def save(path, lines):
    header = "Zeitraum"
    for i in range(len(table_data)):
        header += ";" + table_data[i].get("name", "Undefined")
    
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(f"{header}\n")
            for line in lines:
                file.write(f"{line}\n")
    except PermissionError as err:
        raise ValueError(f"{err}\nBitte versuchen alle Anwendungen, die diese Datei verwenden zu schließen!")

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Fehler: {e}")
    input("Zum Beenden bitte [ENTER] drücken...");
