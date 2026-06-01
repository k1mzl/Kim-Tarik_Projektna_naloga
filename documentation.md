# Documentation: Knjižnica treningov
 
## Pregled
Spletna aplikacija, kjer uporabnik shranjuje svoje treninge.
 
## Tech stack
- Backend: Flask
- Baza: TinyDB
- Frontend: HTML, CSS, JavaScript
 
## Funkcionalnosti
 
### F1: Registracija uporabnika
**Status:** DONE
**Opis:** Uporabnik se registrira z uporabniškim imenom in geslom.
**Zahteve:**
- uporabniško ime mora biti unikatno
- geslo min. 6 znakov
- po registraciji preusmeritev na glavno stran
**Opombe iz razvoja:**
Registracija deluje z osnovnim preverjanjem in shranjevanjem gesla kot hash.
 
### F2: Dodajanje treninga
**Status:** DONE
**Opis:** Uporabnik vidi seznam vseh treningov / vaj.
**Zahteve:**
- prikaz imena vaje
- prikaz športa
- prikaz težavnosti
- podatki se berejo iz TinyDB
**Opombe iz razvoja:**
	Seznam treningov je mogoče filtrirati.
 
### F3: Pregled mojih treningov
**Status:** DONE
**Opis:** Uporabnik lahko filtrira treninge po športu in težavnosti.
**Zahteve:**
- filter po športu
- filter po težavnosti
- prikaz samo ustreznih vaj
 
### F4: Podrobnosti vaje
**Status:** DONE

**Opis:**  
Uporabnik lahko odpre posamezni trening in vidi podrobnosti.

**Zahteve:**
- ime vaje
- opis vaje
- trajanje
- potrebna oprema

---

### F5: Dodajanje vaj
**Status:** DONE

**Opis:**  
Uporabnik lahko doda nov trening / vajo.

**Zahteve:**
- obrazec za dodajanje
- shranjevanje v TinyDB
- preverjanje praznih polj

---

 
## Podatkovni model
 
| Tabela | Polja |
|---|---|
| users | id, username, password_hash |
| trenings | id, user_id, name, sport, difficulty, description, duration, equipment |
 
## Znane omejitve
- ni možnosti urejanja že dodanih treningov
- ni iskanja po treningih
