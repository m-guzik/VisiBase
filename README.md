# VisiBase
Visualize your Wikibase

VisiBase to aplikacja służąca do wizualizacji modelu danych baz powstałych przy wykorzystaniu oprogramowania Wikibase. Program został stworzony w ramach pracy magisterskiej na kierunku Informatyka Stosowana na Uniwersytecie Jagiellońskim. 

## Wymagania

Program został napisany przy użyciu języka Python w wersji 3.12.8. 

Przed pierwszym użyciem aplikacji należy w katalogu 'backend' otworzyć wiersz poleceń i wpisać komendę: 

pip install -r requirements.txt 

która poskutkuje zainstalowaniem bibliotek potrzebnych do działania programu.



## Uruchamianie

W celu skorzystania z aplikacji konieczne jest osobne uruchomienie serwera oraz klienta w dwóch osobnych wierszach poleceń.

### backend

Serwer projektu jest uruchamiany za pomocą wpisanej w wierszu poleceń otworzonym z poziomu katalogu 'backend' komendy: 

uvicorn app:app --host 0.0.0.0 --port 8000

### frontend



