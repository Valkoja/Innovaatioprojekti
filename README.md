## Innovaatioprojekti
Kevään 2019 Innovaatioprojekti -kurssi


### Trello  
https://trello.com/b/2GZE3upU/

### Log=>CSV-kääntäjä

Tekee python-skriptin (log_to_csv.py) kanssa samassa kansiossa olevasta logfile.log-tiedostosta logfile.csv-version, missä järkevät taulukoinnit
Jos samassa hakemistossa on jo logfile.csv, kirjoittaa tiedoston perään, elikkäs ei näin

### Server/GUI-ajo

avaa python3-ympäristösi

`pip install -r requirements.txt`

`cd Python/Server && python Server.py`

#### Ominaisuuksia
* IP saattaa näyttää väärää
* Tick rate vaihdetaan hardkoodaamalla
* Unityn vastaanotto lapsenkengissään ja defaulttaa localhostiin

### PDO-purkaja

Tekee logitiedostojen riveillä olevasta datasta luettavaa ja laittaa tiedon decoded.out-tiedostoon

`python decodelog.py <logitiedosto>`