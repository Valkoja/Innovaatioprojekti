## Innovaatioprojekti
Kevään 2019 Innovaatioprojekti -kurssi


### Trello  
https://trello.com/b/2GZE3upU/

### Log=>CSV-kääntäjä

Tekee python-skriptin (log_to_csv.py) kanssa samassa kansiossa olevasta logfile.log-tiedostosta logfile.csv-version, missä järkevät taulukoinnit
Jos samassa hakemistossa on jo logfile.csv, kirjoittaa tiedoston perään, elikkäs ei näin

### Unity-konsolin käyttö

**Tyyppi 0: Data; näyttää tiedon koko ajan näytön alareunassa (esim. FPS)**

1. Luo ListItem luokan juuressa

`ListItem item = new ListItem(0);`

2. Lisää ListItem konsoliin joko juuressa tai Start() sisällä

`ConsoleHandler.Instance.AddItemToConsole(item);`

3. Päivitä tietoa koodissa

`item.SetData("asd");`

**Tyyppi 1: Viesti; näyttää tiedon ruudulla, kunnes Data tai uudempi tieto syrjäyttää sen**

1. Luo ListItem dynaamisesti ja siirrä se konsoliin

`ConsoleHandler.Instance.AddItemToConsole(new ListItem("asd",1));`

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

### Conda ympäristö palvelimen ajamiseen windows alustalla

`conda create -n [NIMI] python=3.7`

`conda activate [NIMI]`

`pip install https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/Twisted-18.9.0-cp37-cp37m-win_amd64.whl`

`pip install autobahn qt5reactor python-can`

`conda install pyqt pywin32`
