
.. raw:: latex

   \clearpage

MikroTik-Router
===============

.. index:: ! RouterOS, SDN
   see: MikroTik; RouterOS

MikroTik-Router eignen sich,
um mal eben ein VPN aufzubauen
neben all den anderen Funktionen,
die sie im Netz übernehmen können.
Es gibt diese Router in den verschiedensten Größen,
als SOHO-Router, als Core-Router für größere Netzwerke und als virtuelle
Maschine in SDN-Umgebungen. Alle laufen mit RouterOS, einem auf Linux
aufsetzenden proprietären Betriebssystem.
Wenn damit jedoch mehr als ein oder zwei VPN
zu Peers anderer Hersteller aufgebaut werden sollen,
werden die Logs schnell unübersichtlich,
was die Fehlersuche erschwert.

MikroTik-Router können auf drei Arten konfiguriert werden:

* via CLI,
* via Web-Interface,
* via WinBox, einem MS-Windows-Programm.

Mit WinBox ist es möglich,
einen MikroTik-Router über die MAC-Adresse zu kontaktieren,
wenn er mit dem selben Netzsegment verbunden ist.
Dann brauch man die IP-Adressen nicht erst auf der Konsole einstellen
oder den Umweg über die Default-Adresse gehen.
Mit dem Windows-Emulator Wine konnte ich das leider nicht,
ansonsten funktioniert WinBox mit Wine auf einem Linux-Rechner.

.. index::
   pair: CLI; RouterOS

Die Konfiguration läuft auf allen drei Wegen ähnlich ab.
Hier konzentriere ich mich auf das CLI,
dass ich über die Konsole oder SSH erreichen kann.

Grundsätzlich gibt man bei der Konfiguration im CLI
eine Kategorie, eine Aktion und nötigenfalls zusätzliche Parameter an.
Lässt man die Kategorie weg, so kommt automatisch die aktuelle zum Zuge.
Gibt man nur die Kategorie an und keine Aktion,
dann wird diese Kategorie zur aktuellen.
Nach dem Anmelden ist die aktuelle Kategorie '/'.

Durch Eingabe von einem oder zwei <TAB> werden mögliche Fortsetzungen
der aktuellen Kommandozeile angezeigt beziehungsweise teilweise
eingegebene Kategorien, Aktionen oder Parameter soweit ergänzt, wie sie
eindeutig sind.

Starten, Stoppen und Kontrollieren von VPN-Tunneln
--------------------------------------------------

Die aktuell aufgebauten Tunnel kann ich mit folgenden Befehlen ansehen::

  /ip ipsec remote-peers print
  /ip ipsec installed-sa print

Alternativ kann ich auch die verkürzte Schreibweise nehmen::

  /ip ipsec
  remote-peers print
  installed-sa print

.. index::
   single: Child-SA; Traffic-Selektoren

Leider zeigt ``installed-sa print`` die Traffic-Selektoren der Child-SA
nicht an.
In der aktuellen Version kenne ich auch keinen Weg,
an diese Information zu kommen.
Als Workaround kann ich auf die Systemprotokolle zugreifen.
Doch auch diese zeigen nur die Traffic-Selektoren für Child-SA,
die vom Peer initiiert wurden.
Um die Traffic-Selektoren für Child-SA, die das Gerät selbst initiiert hat,
zu bekommen, muss ich das Debug-Log für IPsec einschalten.

Um einen VPN-Tunnel zu beenden verwende ich die Befehle::

  /ip ipsec
  remote-peers kill-connections
  installed-sa flush

.. index::
   pair: RouterOS; Systemlogs
   pair: RouterOS; Debug-Informationen

Systemlogs und Debug-Informationen
----------------------------------

Was auf der MikroTik protokolliert wird und wohin, bestimme ich mit
den Befehlen der Kategorie ``/system logging``.

Von diesen sind vor allem zwei wichtig:

``/system logging topics ...``:
  legt fest was protokolliert wird, mit welchem Level und in welchen
  Kanal.

``/system logging action ...``:
  definiert die Log-Kanäle, die ich nutzen kann (Hauptspeicher, Datei,
  Logserver, ...).

Die Logs, die sich im lokalen Speicher der MikroTik befinden, lese ich
mit dem Befehl::

  /log print

Ich kann hier filtern, bevorzuge aber meist die Arbeit mit
Textwerkzeugen auf dem eigenen Rechner.
Dafür habe ich mehrere Möglichkeiten.

Wenn ich den Verbindungsaufbau kontrollieren kann
oder exakte Timing-Informationen bekomme,
geht am schnellsten,
die Lognachrichten in einem Terminalfenster durchlaufen lassen.
Dazu verwende ich im CLI der MikroTik den Befehl::

  /log print follow

Sobald der Verbindungsaufbau durch ist,
beende ich mit ``CTRL-C`` die Ausgabe der Logzeilen
und kann die Log- und Debug-Meldungen
relativ einfach in der Ausgabe des Terminalfensters finden.
Das funktioniert allerdings nur,
wenn auf dem MikroTik-Router nur wenige VPN laufen,
weil ansonsten unweigerlich INFORMATIONAL-Meldungen
von anderen IKE-Sitzungen in der Ausgabe auftauchen
und diese unübersichtlich machen.

.. index:: SSH

Alternativ kann ich
die Ausgabe von ``/log print`` in eine Textdatei umleiten.
Zum Beispiel, indem ich via SSH nur diesen Befehl aufrufe
und die SSH-Sitzung mit ``script`` protokolliere::

  script mikrotik.log
  ssh user@mikrotik /log print
  exit
 
Sind die interessanten Lognachrichten nicht im Hauptspeicher zu finden,
muss ich auf andere Art und Weise auf die Logs zugreifen.

Eine Möglichkeit ist, die Logs zu einem Syslog-Server zu senden
und dann bei diesem abzuholen.
Um zum Syslog-Server mit Adresse a.b.c.d zu protokollieren, verwende
ich die folgenden Befehle::

  /system logging action
  add name=remote remote=a.b.c.d

  /system logging
  add action=remote topics=...

Bei den Topics interessiert mich vor allem ``ipsec``.
Leider wird die Priorität, das heißt der Loglevel, ebenfalls über das
Attribut *topic* eingestellt.
Darum kombiniere ich ``ipsec`` immer mit den gewünschten Levels.

``topics=ipsec,!packet``
  lässt den Packet-Dump der Datagramme aus.
  Diesen will ich auf dem Syslog-Server nicht haben.

``topics=ipsec,debug,!packet``
  schalte ich ein, wenn ich Probleme mit einem VPN untersuche.

``topics=ipsec,!debug,!packet``
  habe ich im Normalbetrieb eingestellt.

Weiterhin kann ich die Logs in eine Datei schreiben lassen
und diese Datei via SCP für die Untersuchung abholen.
Die Befehle dazu sind::

  /system logging action
  add action=file name=vpn.log
  /system logging topic
  add action=file topics=ipsec,debug

Welche Dateien es gibt sehe ich mit dem Befehl::

  /file print

.. index:: SCP

Von meinem Rechner aus hole ich sie mittels SCP wie folgt zur Analyse ab::

  scp user@mikrotik:vpn.log .

.. index::
   pair: RouterOS; Paketmitschnitt

Paketmitschnitte
----------------

Auch Paketmitschnitte sind mit RouterOS möglich.
Diese konfiguriere, starte und beende ich unter ``/tool sniffer``.

Die aktuellen Einstellungen bekomme ich mit ``/tool sniffer print``.

Ich kann den Paketmitschnitt im Speicher halten oder in eine Datei
schreiben lassen, indem ich einen Dateiname vorgebe (``file-name``) und
gegebenenfalls die Größenbeschränkung (``file-limit``) modifiziere. Die
Datei finde ich mit ``/file print`` und kann sie mit SCP auf meinen
Rechner kopieren.
Bevor ich Limits ändere, schaue ich mit ``/system resource print`` nach,
wie viel Ressourcen (Hauptspeicher, Plattenplatz) ich zur Verfügung habe.

Es gibt etliche Filterattribute,
für die ich jeweils bis zu 16 Werte vorgeben kann.
Diese werden, je nach Einstellung von ``filter-operator-between-entries``,
mit UND oder ODER verknüpft.

Mit dem Befehl ``/tool sniffer packet`` kann ich
den Paketmitschnitt auch direkt auf dem Gerät anschauen.
Das ist bei einfachen Fragen oft ausreichend.

Mit dem Attribut ``memory-scroll`` kann ich einen dauerhaften Mitschnitt
bei beschränktem Speicherplatz einstellen.

Es ist sinnvoll,
sich mit den Paketmitschnitten bei RouterOS vertraut zu machen,
bevor man diese benötigt.
Je nach Modell und Konfiguration der Schnittstellen kann es sonst sein,
dass man gar nichts
oder nur direkt an ein Interface gesandte Datagramme erhält.
Auch verhalten sich die Switch-Modelle teilweise anders
als die Router-Modelle,
obwohl beide mit RouterOS betrieben werden können.

.. index::
   pair: RouterOS; Konfiguration analysieren

Konfiguration analysieren
-------------------------

Die Konfiguration bekomme ich mit dem Befehl ``export`` als Text.
Direkt in der Wurzel eingegeben (``/export``) bekomme ich die gesamte
Konfiguration, ich kann mich aber auch auf Teile beschränken, zum
Beispiel auf die IPsec-Konfiguration::

  /ip ipsec export

.. index:: grep

Für den Export der Konfiguration sind zwei Attribute wichtig:

``export terse``:
  zeigt die Kategorien in jeder Zeile. Damit ist diese Ausgabe besser
  für die Suche mit ``grep`` geeignet und ich kann die ganze Zeile
  einfacher in die Konfiguration einer anderen Maschine übernehmen.

``export detail``:
  zeigt auch Defaultwerte.
  Damit kann ich Missverständnisse ausräumen,
  die durch falsche Annahmen über die Defaults entstanden sind.

Besonderheiten
--------------

Verwendet man mehrere IPsec-SA mit unterschiedlichen Traffic-Selektoren,
sollte in der Policy ``level=unique`` konfiguriert werden,
damit der Traffic an die richtige IPsec-SA gesendet wird.
Wird das vergessen
und die Gegenstelle akzeptiert keinen Traffic für die falsche SA,
dann funktioniert zwar ein Teil des VPN
- der, bei dem der Traffic-Selektor der SA passt -
aber nicht alles.

Default-Port für IKE ist 4500
.............................

.. index:: ESP, NAT

Eine Eigenart der MikroTik-Router ist,
dass sie mit den Default-Einstellungen
für die erste Anfrage beim Peer immer UDP-Port 4500 verwenden.
Normalerweise geht die erste Anfrage immer an UDP-Port 500
und erst,
wenn die Peers NAT zwischen den beiden externen Adressen erkennen,
schalten sie um auf Port 4500
und verwenden diesen auch für ESP.

.. index:: SHA

Außerdem stimmt in diesem Fall (zumindest bis Version 6.45)
die SHA1-Hash für die NAT-Detection nicht,
so dass der Peer hier NAT erkennt,
auch wenn gar keines zur Anwendung kommt.
Dadurch wird der ESP-Traffic ohne Not in UDP gekapselt,
was mehr Overhead durch IPsec für jedes einzelne Datagramm bedeutet.

Damit der MikroTik-Router bei der ersten Anfrage Port 500 verwendet,
muss ich diesen explizit bei der Konfiguration des Peers angeben:

.. code-block:: none

   ip ipsec peer ... port=500

Gebe ich damit den Standard-Port vor,
funktioniert auch die NAT-Detection
und der IPsec-Tunnel wird mit nativem ESP aufgebaut,
wodurch der Overhead durch den Tunnel etwas geringer wird.

.. index:: CHR

Netzwerk-Performance des CHR ist lizenzabhängig
...............................................

Ein CHR (Cloud Hosted Router) ist eine virtuelle Maschine,
welche in verschiedenen Umgebungen laufen kann,
die die benötigte Hardware (X86) zur Verfügung stellen,
zum Beispiel unter VMware, Xen oder im GNS3-Netzwerksimulator.

Das benötigte Image ist für alle Plattformen das gleiche
und kann frei von der Website heruntergeladen werden.
Dieses Image hat die volle Funktionalität,
ist jedoch beim Datendurchsatz auf ungefähr 1 MBit/s beschränkt.

Für Simulationen in GNS3 ist das in den meisten Fällen ausreichend.
Im Produktivbetrieb ist es in den meisten Fällen ratsam,
mit einem einmaligen Erwerb eine höheren Lizenz
einen höheren Datendurchsatz freizuschalten.

Das Verfahren ist in meinen Augen nur fair,
da man genügend Zeit hat,
den CHR in der speziellen Umgebung zu evaluieren,
und sich anschließend mit dem Erwerb der benötigten Lizenz
an den Kosten für die Entwicklung zu beteiligen.

Man muss allerdings daran denken,
die höhere Lizenz freizuschalten.
Uns ist es hin und wieder passiert,
dass wir nicht rechtzeitig daran gedacht hatten
und uns anschließend über die schlechte Performance
des VPN mit dem CHR wunderten.

