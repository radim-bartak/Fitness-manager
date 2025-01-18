# Fitness Manager

Fitness Manager je webová aplikace určená pro správu fitness centra. Umožňuje efektivní řízení členů, trenérů, lekcí, rezervací, členství a plateb.

## Funkcionality
- Správa členů: Přidávání, úprava a mazání informací o členech.
- Správa trenérů: Správa profilů trenérů a jejich specializací.
- Plánování lekcí: Vytváření a správa lekcí včetně kapacity a času konání.
- Rezervace: Umožňuje členům rezervovat si lekce.
- Členství: Správa typů členství a jejich platnosti.
- Platby: Zpracování plateb za členství a sledování platební historie.

## Technologie
- Backend: Python s využitím Flask frameworku.
- Frontend: HTML, CSS.
- Databáze: MySQL.
- ORM: SQLAlchemy pro mapování objektově-relačních dat.

## Instalace
1. Otevřete XAMPP a nastartujte v něm MySQL modul.
2. Otevřete MySQL Workbench, přihlaste se jako root a spusťtě následující script:
   
  `CREATE DATABASE fitnessdb;
    CREATE USER 'fitnessuser'@'localhost' IDENTIFIED BY 'fitness';
    GRANT ALL PRIVILEGES ON fitnessdb.* TO 'fitnessuser'@'localhost';
    FLUSH PRIVILEGES;`
    
3. V příkazovém řádku přejděte do složky s projektem a pomocí následujících příkazů vytvořte virtuální prostředí:
  
   `python -m venv venv`

   `.\venv\Scripts\activate`

4. Nainstalujte závislosti:

     `pip install -r requirements.txt`

5. Spusťte aplikaci:

     `python run.py`

Aplikaci otevřete ve webovém prohlížeči na adrese: http://127.0.0.1:5000/.

## Struktura projektu
- app/: Obsahuje hlavní kód aplikace.
	- init.py: Inicializace aplikace Flask.  
	- models.py: Definice databázových modelů.
	- config.py: Konfigurační logika.
	- routes/: Definice aplikačních rout.
	- services/: Logika pro objekty.
	- templates/: HTML šablony a stránky.
	- static/: CSS.
- tests/: Test casy aplikace.
- config.json: Konfigurační soubor.
- requirements.txt: Závislosti projektu.
- run.py: Spouštěcí soubor aplikace.

## Použité knihovny
- Flask
- SQLAlchemy, Author: Mike Bayer
- PyMySQL, Author: Inada Naoki
