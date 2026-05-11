# Documentation: Knjižnica receptov
 
## Pregled
Spletna aplikacija, kjer uporabnik shranjuje svoje recepte.
 
## Tech stack
- Backend: Flask
- Baza: TinyDB
- Frontend: HTML, CSS, JavaScript
 
## Funkcionalnosti
 
### F1: Registracija uporabnika
**Status:** TODO
**Opis:** Uporabnik se registrira z uporabniškim imenom in geslom.
**Zahteve:**
- uporabniško ime mora biti unikatno
- geslo min. 6 znakov
- po registraciji preusmeritev na glavno stran
**Opombe iz razvoja:**
/
 
### F2: Dodajanje recepta
**Status:** TODO
**Opis:** Uporabnik vidi seznam vseh trening vaj.
**Zahteve:**
- prikaz imena vaje
- prikaz športa
- prikaz težavnosti
- podatki se berejo iz TinyDB
**Opombe iz razvoja:**
/
 
### F3: Pregled mojih receptov
**Status:** TODO
**Opis:** Uporabnik lahko filtrira vaje po športu in težavnosti.
**Zahteve:**
- filter po športu
- filter po težavnosti
- prikaz samo ustreznih vaj
- 
### F4: Podrobnosti vaje
**Status:** TODO

**Opis:**  
Uporabnik lahko odpre posamezno vajo in vidi podrobnosti.

**Zahteve:**
- ime vaje
- opis vaje
- trajanje
- potrebna oprema

---

### F5: Dodajanje vaj
**Status:** TODO

**Opis:**  
Trener lahko doda novo vajo.

**Zahteve:**
- obrazec za dodajanje
- shranjevanje v TinyDB
- preverjanje praznih polj

---

 
## Podatkovni model
 
| Tabela | Polja |
|---|---|
| users | id, username, password_hash |
| recipes | id, user_id, name, ingredients, instructions |
 
## Znane omejitve
- ni možnosti urejanja že dodanih receptov
- ni iskanja po receptih
