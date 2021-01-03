# Pflanzenüberwachung
## Nutzung eines Xiaomi Mi Flora Sensors zur smarten Überwachung einer Zimmerpflanze

In dem Projekt werden von den Pflanzen Umgebungs- temperatur und helligkeit und Fruchtbarkeit und Feuchtigkeit mit dem Mi Flora Sensor erfasst und zu einem hilfreichen Output via Telegram verarbeitet.

Diese Daten und der Batteriezustand des Sensors werden dann in regelmäßigen Zeitabständen von einem Python Skript abgefragt. Dieses Python Skript läuft in meinem Fall auf einem Raspberry Pi Zero W, welcher die Daten mit dem Python Skript via Bluetooth LE ausliest.

Um die Daten dann langfristig untersuchen zu können werden diese vom Raspberry Pi in eine InfluxDB 2.0 Zeitreihendatenbank gespeichert.

In der Zeitreihendatenbank können die erfassten Daten nun mithilfe von Flux weiterverarbeitet und analysiert werden. 

Mithilfe des Flux Telegram package können nun beim Überschreiten verschiedener Schwellwerte Aufforderung verschickt werden.
Zum beispiel kann bei zu geringer Bodenfeuchtigkeit einer Pflanze eine Nachricht verschickt werden, dass die Pflanze gegossen werden muss.


## Setup

### Raspberry Pi

Auf dem Raspberry Pi habe ich ganz normal Raspberry Pi OS Lite installiert und diesen dann headless via ssh genutzt.
Es kann aber eigentlich jeder Bluetooth LE fähige Computer genutzt werden um die Sensordaten auszulesen.

### InfluxDB 2.0

Alle Daten die von den Pflanzen erhoben werden werden in einer InfluxDB 2.0 gespeichert.
Dazu muss nun eine InfluxDB 2.0 zur Verfügung stehen oder aufgesetzt werden.
Bei mir läuft diese in einem Dockercontainer auf dem Hochschulserver. Die Datenbank kann aber auch lokal auf dem Raspberry Pi betrieben werden. 

### Sensor

Nun muss der Pflanzensensor aktiviert werden und dessen Bluetooth Mac Adresse herausgefunden werden.

Die Bluetooth MAC des Mi Flora Sensors kann man unter Linux mit dem Befehl:

    sudo hcitool lescan

herausfinden.

### Python Abfrageskript

Für das Python Skript sensorHandler.py müssen zwei Bibliotheken installiert werden:

    sudo pip3 install miflora
    sudo pip3 install btlewrap

Nun müssen in der sensorHandler die Werte für die InfluxDB sowie die Namen und MAC Adressen eingetragen werden.

Das Pyhthon Skript kann nun mithilfe eines Cronjobs in regelmäßigen Abständen abgefragt werden.

Um das Skript im 15 Minuten Takt auszuführen habe ich folgenden Crontab erstellt:

    */15 * * * * /pathToFile/sensorHandler.py

Bei jedem Abfragen der Sensoren werden diese aus aus dem Tiefschlaf geholt und aktiviert.
Eine sehr häufige Abfrage z.B. im Minutentakt verkürzt die Lebensdauer der Batterie drastisch.

### Telegram Bot

Für die Benachrichtigungen via Telegram muss ein Bot erstellt werden. 

Dieser schickt in meinem Fall täglich in eine Telgram Gruppe ein Lebenszeichen, sodass man weiß, dass noch alles funktioniert. Falls die Pflanze gegossen werden muss oder zum Beispiel mehr Schatten benötigt schickt dieser Bot auch einfach eine Nachricht.

Wenn man eine andere Person zum Pflegen seiner Pflanzen beauftragt kann man diese einfach in die Telegram Gruppe hinzufügen damit sie auch die Nachrichten des Bots bekommt.


https://core.telegram.org/bots

### InfluxDB 2.0 Alerts

https://github.com/influxdata/flux/issues/2442

![](2020-12-29-10-58-17.png)
![](2020-12-29-11-33-13.png)






