# VisiBase

VisiBase to aplikacja służąca do wizualizacji modelu danych baz powstałych przy wykorzystaniu oprogramowania Wikibase. Program został stworzony w ramach pracy magisterskiej przygotowanej na kierunku Informatyka Stosowana na Uniwersytecie Jagiellońskim. 

## Wymagania

Program został napisany przy użyciu języka Python w wersji 3.12.8 oraz środowiska Node.js w wersji 18.19.1; ich instalacja jest konieczna do uruchomienia aplikacji. Poniższa instrukcja zakłada również użycie domyślnych menadżerów pakietów: *pip* (dla języka Python) oraz *npm* (dla środowiska Node.js).

Przed pierwszym uruchomieniem aplikacji należy:

1. (opcjonalne, lecz zalecane) utworzyć wirtualne środowisko z językiem Python we wskazanej wersji i wykonywać kolejne kroki z jego wykorzystaniem

2. w terminalu przejść do katalogu *backend* i wpisać komendę: 

`pip install -r requirements.txt`

3. w terminalu przejść do katalogu *frontend* i wpisać komendę:  

`npm install`

Dzięki tym akcjom zostaną zainstalowane wszystkie dodatkowe biblioteki potrzebne do działania programu.


## Uruchamianie

W celu skorzystania z aplikacji konieczne jest równoległe uruchomienie serwera oraz klienta w dwóch osobnych terminalach.

### backend

Serwer projektu jest uruchamiany w terminalu po przejściu do katalogu *backend* za pomocą komendy: 

`uvicorn app:app --host 0.0.0.0 --port 8000`

W tym terminalu w trakcie działania aplikacji będą pokazywane komunikaty o kolejnych akcjach podejmowanych przez serwer oraz ewentualnych błędach.

### frontend

Klient działający w przeglądarce jest uruchamiany w terminalu po przejściu do katalogu *frontend* za pomocą komendy: 

`npm run dev -- --open`

Takie polecenie automatycznie otworzy aplikację lokalnie w trybie deweloperskim w przeglądarce internetowej używając portu 5173 lub innego wolnego. 


