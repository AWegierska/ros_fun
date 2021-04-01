# Laboratorium robotów usługowych

## Oprogramownie:
ROS noetic
Processing 3.5.4
Dodatkowe biblioteki do Processingu w utworzonym katalogu sketchbook:
- ROSProcessing (https://github.com/pronobis/ROSProcessing)
- controlP5 (https://github.com/sojamo/controlp5)

## Pobranie materiałow do zajęć
Do obrazu należy pobrać również dodatkowe materiały do laboratorium.
Po sklonowaniu tego repozytorium w katalogu ros_fun należy sklonować repozytoria:

***git clone https://github.com/AWegierska/pkg_rob_usl.git***

***git clone https://github.com/AWegierska/lab_rob_usl.git***

## Dostęp
Dostęp do ekranu kontenera z poziomu przeglądarki:

[http://localhost:6080](http://localhost:6080)


Dostęp do notatnika jupyter notebook z poziomu przeglądarki możliwy jest po uruchomieniu w kontenerze skrótu z pulpitu z notatnikiem. Jeśli nie działa to należy uruchomić tam terminal i wpisać:

*jupyter notebook*

Następnie w oknie przeglądarki z poziomu dockera lub przeglądarki głównego systemu dostęp do *jupyter notebook* możliwy jest po wpisaniu:

[http://localhost:8888](http://localhost:8888) 

## Uruchomienie środowiska
Z poziomu terminala w katalogu ros_fun należy wpisać polecenie:

***docker-compose up***
