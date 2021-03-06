
Cisco ASA
=========

.. index:: !Cisco ASA, Adaptive Security Appliance
   see: ASA; Adaptive Security Appliance

Von den mir bekannten VPN-Gateways ist die Cisco ASA
gerade für den Betrieb sehr vieler VPN besonders gut geeignet.
Leider hat das Vertrauen in diesen Hersteller
durch einige gravierende Sicherheitsprobleme gelitten.
Ob die Geräte für die eigene Situation angemessen sind,
muss jeder für sich selbst entscheiden.

Die Cisco ASA (Adaptive Security Appliance) bietet verschiedene Interfaces
zur Konfiguration:

* die Kommandozeile, die derjenigen in Cisco-Routern und Switches
  ähnelt,

.. index:: ASDM

* den ASDM (Adaptive Security Device Manager), eine Java-Anwendung die
  direkt auf dem Gerät abgelegt ist und via Webbrowser gestartet werden
  kann,

.. index:: CSM

* den CSM (Cisco Security Manager), mit dem mehrere ASA verwaltet werden
  können.

Jede dieser Schnittstellen hat ihre Vor- und Nachteile.
Ich bevorzuge
für die Extraktion der Konfiguration und für Zustandsabfragen
die Kommandozeile.
Für den Zugriff auf die aktuellen Systemlogs
bietet der ASDM gute Möglichkeiten zur Filterung.
Wenn es gilt,
Konfigurationen auf verschiedenen Geräten konsistent zu halten,
kann der CSM seine Vorteile ausspielen.

.. index::
   pair: CLI; Cisco ASA

Bei den nachfolgenden Betrachtungen gehe ich auf die
Befehle der Kommandozeile ein, für die ich meist höhere Rechte benötige.
Das heißt, nach dem Anmelden gebe ich ``enable`` ein, falls mein Zugang
nicht von sich aus höhere Rechte besitzt.
Generell kann ich alle Befehle und Optionen so weit kürzen,
wie sie eindeutig bleiben.
Mit dem Fragezeichen oder dem
Tabulator kann ich jederzeit eine kurze Hilfe bekommen, welche Eingaben
als nächstes möglich sind.

Muss ich die Konfiguration ändern, kann ich das mit dem folgenden Befehl::

  configure terminal

oder abgekürzt::

  conf t

Ich beende die Konfiguration mit ``end`` und sichere sie mit dem Befehl
``write memory`` (kurz ``wr``).

Starten, Stoppen und Kontrollieren von VPN-Tunneln
--------------------------------------------------

Policy-based VPN werden bei der ASA meist On-Demand gestartet,
das heißt, wenn Traffic dafür da ist.

Um einen solchen VPN-Tunnel zu öffnen,
kann ich diesen Traffic direkt in der Konsole
mit dem Befehl ``packet-tracer`` simulieren::

  packet-tracer input $if $proto $src $dst [detail]

Dabei muss ich bei der Spezifikation des Protokolls
``$proto $src $dst``
sehr genau sein und Werte für die spezifischen Parameter angeben::

  icmp $saddr 8 0 $daddr
  tcp $saddr $sport $daddr $dport
  udp $saddr $sport $daddr $dport

Die Ausgabe von ``packet-tracer`` kann
mir bei manchen Problemen schon erste Hinweise geben,
insbesondere, wenn ich die Option ``detail`` hinzugefügt habe.

Um einen VPN-Tunnel zu schließen, hat sich für mich der folgende Befehl
als am zuverlässigsten erwiesen::

  vpn-db log-off index $i

Den Index ``$i`` bekomme ich
aus der zweiten Zeile der Ausgabe des Befehls::

  show vpn-db detail l2l filter name $peeraddress

.. index:: Child-SA

Um erste Informationen über ein VPN zu bekommen,
wie zum Beispiel offene Child-SA oder ob Traffic hindurch geht,
verwende ich ebenfalls diesen Befehl - hier in der Kurzform::

  sh vpn- d l f n $peeraddress

oder einen zweiten::

  show crypto ipsec sa peer $peeraddress

Der erste Befehl ist etwas übersichtlicher,
der zweite Befehl enthält dafür Informationen,
die ich bei tiefergehender Analyse benötige.

.. index::
   pair: Cisco ASA; Systemlogs
   pair: Cisco ASA; Debug-Informationen

Systemlogs und Debug-Informationen
----------------------------------

Im Internet sind Informationen zur Konfiguration von Cisco-Geräten sehr
leicht zu finden.
Die ultimative Referenz befindet sich auf den Webseiten von Cisco selbst.

Möchte ich die Systemlogs in der Konsole oder SSH-Sitzung sehen,
gebe ich den folgenden Befehl ein::

   terminal monitor

Um die Systemlogs und Debug-Informationen zu einem Logserver zu
schicken, muss ich die Konfiguration ändern::

   conf t
   logging enable
   logging trap $level
   logging host $if $address [ ... ]

Hierbei steht $level für eine der folgenden Prioritäten:

===== =============
Level Schlüsselwort
===== =============
  0   emergency
  1   alert
  2   critical
  3   error
  4   warning
  5   notification
  6   informational
  7   debugging
===== =============

Mit ``$if`` gebe ich die Schnittstelle an, zu der die Logs rausgehen,
mit ``$address`` die Adresse des Logservers.
Wenn nötig kann ich weitere Informationen zum Logserver bereitstellen,
näheres findet sich in der Dokumentation zum Logging.

.. index:: ASDM

Um auf den ASDM oder die (SSH-)Konsole zu loggen,
konfiguriere ich zusätzlich die folgenden Befehle::

  logging asdm $level
  logging console $level

Dann kann ich in der jeweiligen Sitzung auf die Logs zugreifen.
Auf der Konsole steuere ich die Ausgabe mit den folgenden Befehlen::

  term monitor
  no term monitor

Der Befehl ``show logging`` zeigt die aktuellen Einstellungen.

Für das Debugging sieht es ähnlich aus.
Um Debug-Ausgaben zum Syslog-Server zu senden, konfiguriere ich
zusätzlich zur Konfiguration für die normalen Logs::

  logging debug-trace
  logging trap debugging

Interaktiv steuere ich das Debugging von IPsec mit den folgenden
Befehlen::

  debug crypto condition peer $address
  debug crypto ikev2 protocol $dlevel
  debug crypto ikev2 platform $dlevel

  undebug all

Der erste Befehl schränkt das Debugging auf einen Peer ein und ist
dringend geboten, wenn mehr als ein Peer aktiv ist.
Mit ``$address`` gebe ich die Adresse des Peers an, an dem ich interessiert
bin.
Der Parameter ``$dlevel`` bestimmt die Granularität der Debugmeldungen und
liegt zwischen 1 und 255.
Mit ``undebug all`` schalte ich das Debugging ab, wenn ich alle
benötigten Informationen habe.

In den Logs kann ich Debug-Informationen an der Markierung
``%ASA-7-711001`` erkennen und damit ausfiltern.
Ich suche darin nach Zeilen mit dem folgenden Mustern:

* ``SENT PKT``
* ``RECV PKT``
* ``Sent Packet``
* ``Received Packet``

.. index:: MID

Dabei achte ich auf die Message-ID (MID).
*IKE_SA_INIT* hat immer die MID 0, *IKE_AUTH* beginnt bei 1.

Bei der Interpretation der Debugausgaben ziehe ich
meine Kenntnisse über das IKE-Protokoll zu Rate,
die im Kapitel :ref:`ikev2/nachrichten:IKEv2 Nachrichten`
und im Anhang :ref:`anhang/datagram-header:Datagramm-Header` dargelegt sind.
Da sich die Debugmeldungen von Version zu Version unterscheiden,
werde ich hier nicht detaillierter darauf eingehen.
Am schnellsten wird man damit vertraut,
wenn man ein paar funktionierende VPN beobachtet,
um zu sehen,
wie die Meldungen aussehen wenn alles in Ordnung ist.

.. index::
   pair: Cisco ASA; Paketmitschnitt

Paketmitschnitte
----------------

Ich kann Paketmitschnitte direkt auf der ASA entweder mit dem ASDM oder
in der Kommandozeile anfertigen.
Zum Auswerten kann ich die Datagramme direkt in der Konsole betrachten
oder den Mitschnitt als PCAP-Datei für Wireshark herunterladen.

In der Kommandozeile fertige ich den Paketmitschnitt mit dem ``capture``
Befehl an::

  capture $name interface $if [ $options ] match $filter

Mit *$name* lege ich den Namen der Datei fest.
Ich kann mehrere ``capture`` Befehle mit demselben Namen absetzen und so
komplexe Mitschnitte zusammensetzen oder Optionen ändern.

Ich verweise mit dem Namen meist auf den Zweck des Mitschnitts,
zum Beispiel auf eine Ticketnummer,
so dass ich bei einem älteren Paketmitschnitt leichter entscheiden kann,
ob er noch nötig ist oder entfernt werden sollte.

Das Interface $if gibt an, auf welcher Seite ich die Pakete mitschneiden
will.
Um zu sehen, ob Datagramme tatsächlich das VPN-Gateway passieren, kann
ich sowohl auf der Inside als auch auf der Outside mitschneiden.
Verwende ich dazu zwei ``capture`` Befehle mit dem gleichen Namen,
kann ich bei der Auswertung die Datagramme im selben Mitschnitt
verschlüsselt und unverschlüsselt sehen.

Die Möglichkeiten zur Filterung sind nicht so detailliert
wie bei tcpdump oder Wireshark,
aber für die meisten Zwecke ausreichend.
Der grundlegende Aufbau ist wie folgt::

  match $proto $spec1 $spec2

Dabei gibt *$proto* das Protokoll an, (ip, tcp, udp, icmp, ...).
Die Spezifikationen *$spec1* und *$spec2* geben Quell- und Zieladressen
der Datagramme an, die Reihenfolge ist dabei unwichtig.
Ich habe grundsätzlich die beiden Möglichkeiten:

* ``$network $mask``
* ``host $address``

Zusätzlich kann ich bei TCP und UDP
mit der Ergänzung ``lt``, ``eq`` oder ``gt`` und der Portnummer
noch Angaben zum Quell- oder Zielport machen.

Komplexere Kommunikationsbeziehungen erfasse ich
durch mehrmaligen Aufruf des ``capture`` Befehls
mit verschiedenen eng gefassten Filtern.
Dabei verwende ich immer den gleichen Namen für den Mitschnitt.

Ein Weg, IKE- von ESP-Traffic bei NAT-T zu unterscheiden
ist mir zurzeit nicht bekannt.
Diese geringere Flexibilität bei der Filterung gegenüber tcpdump oder Wireshark
kompensiert die ASA zumindest teilweise
mit einigen nützlichen Features beim Mitschnitt.

Da wäre zunächst der Typ des Mitschnitts.
Gebe ich keinen an, ist der Typ automatisch ``raw-data`` es werden normale
Datagramme geschrieben.
Beim Typ ``isakmp`` hingegen erzeugt die ASA zusätzlich
Pseudo-Datagramme, die den Inhalt der entschlüsselten IKE-Nachrichten
enthalten.
Damit ist es möglich, auch andere Nachrichten als IKE_SA_INIT zu
untersuchen.
So kann ich zum Beispiel Probleme beim Erzeugen der Child-SA
oder beim Rekeying genauer unter die Lupe nehmen
ohne auf Debug-Informationen zurückgreifen zu müssen.
Mit dem Typ ``asp-drop`` gibt die ASA an, welche Datagramme sie mit
welcher Begründung verworfen hat.
Diesen Typ brauche ich eher selten,
aber wenn ich Datagramme auf einer Seite ankommen sehe
und nicht auf der anderen abgehen,
kann ich hier manchmal einen Hinweis bekommen.

Bei den Optionen zum Paketmitschnitt sind die folgenden interessant:

``real-time``:
  zeigt die Datagramme sofort als Text in der Konsole.

  Ich verwende diese Option, wenn überhaupt nichts funktioniert und ich
  auf das erste Datagramm warte.
  Mit ``<CTRL>-C`` kann ich die Echtzeitausgabe abbrechen, der
  Mitschnitt geht weiter.
  Will ich später wieder Echtzeitausgabe, starte ich sie erneut mit dem
  Befehl ``capture $name real-time``.

``circular-buffer``:
  überschreibt die ersten Datagramme, wenn der Puffer voll ist, so dass
  sich stets die letzten mitgeschnittenen Datagramme im Puffer befinden.
  Ich verwende diese Option, wenn ich längere Zeit auf ein Ereignis
  warten muss und der Mitschnitt sonst aufgrund des vollen Puffers
  abgebrochen wird.

  Zur Auswertung muss ich die Option mit dem Befehl ``no capture $name
  circular-buffer`` ausschalten.
  Dabei darf ich die Option ``circular-buffer`` nicht vergessen,
  weil sonst der gesamte Mitschnitt gelöscht wird
  und der Aufwand umsonst gewesen wäre.

``buffer``, ``packet-length``:
  Mit diesen beiden Optionen kann ich im Rahmen der auf dem Gerät
  verfügbaren Ressourcen und der gewünschten Details experimentieren,
  wenn ich sehr viele Datagramme mitschneiden muss.

Auswertung der Paketmitschnitte
...............................

Generell bekomme ich mit::

  show capture

eine Übersicht über alle Paketmitschnitte und wieviel Daten bereits
mitgeschnitten sind.

Zur Auswertung kann ich den Befehl ``show capture $name`` verwenden.
Auch hier habe ich etliche Optionen, die mir die Analyse erleichtern.

``dump``:
  zeigt das komplette Datagramm als Hexdump an.

.. index:: TTL

``detail``:
  zeigt etwas mehr Details an, benötigt dafür mindestens zwei Zeilen pro
  Datagramm.

  Ich verwende diese Option vor allem, wenn ich an der TTL interessiert
  bin, um traceroute zu erkennen.

``decode``:
  zeigt mir die Details von IKE-Nachrichten an.

  Bei normalen Mitschnitten funktioniert das nur für IKE_SA_INIT, bei
  Typ ``isakmp`` auch für IKE_AUTH, CREATE_CHILD_SA und INFORMATIONAL,
  so dass ich den kompletten Nachrichtenaustausch analysieren kann und
  nicht nur den Anfang.

``packet-number $number``, ``count $count``:
  mit diesen beiden Optionen kann ich gezielt die Datagramme
  untersuchen, die mich interessieren.

.. index:: TFTP

Prinzipiell kann ich den Paketmitschnitt auch mit Wireshark analysieren.
Beim ASDM kann ich die PCAP-Datei direkt herunterladen.
Auf der Console schicke ich die Datei mit folgendem Befehl
zu einem TFTP-Server::

  copy /pcap capture:$name tftp

.. index:: Perl

Da ich einmal bei einer ASA weder Zugang zum ASDM hatte,
noch ein TFTP-Server in Reichweite war,
habe ich ein Skript geschrieben,
dass die Ausgabe von ``show capture $name dump``
in eine PCAP-Datei für die weitere Analyse umwandeln kann.
Dieses Skript ist im Perl-Modul File::PCAP enthalten und kann bei
meta::cpan [#]_ gefunden werden.
Das Programm ``text2pcap``, ein Teil von Wireshark,
leistet in etwa das gleiche.
Als ich das Perl-Skript schrieb kannte ich ``text2pcap`` noch nicht.

.. [#] https://metacpan.org/release/File-PCAP

.. index::
   pair: Cisco ASA; Konfiguration analysieren

Konfiguration analysieren
-------------------------

Die Konfiguration kann ich mir mit den folgenden Befehlen als Text
ausgeben lassen::

  show running-config
  show running-config all

Meist reicht der erste Befehl.
In hartnäckigen Fällen füge ich ``all`` an,
um auch die Defaultwerte angezeigt zu bekommen.

.. index:: NAT

Adressumsetzungen sind zwar in der Konfiguration zu sehen,
aber bei der Verwendung von Objekten mit Namen,
die die Adressen nicht enthalten,
untersuche ich NAT lieber mit den folgenden Befehlen::

  show nat $addr [ detail ]
  show nat translated $addr [ detail ]

Mit der Option ``detail`` bekomme ich die Adressen hier auch,
wenn bei der Konfiguration die Objektnamen ungeschickt gewählt wurden.

Um die Analyse der Konfiguration in der Konsole zu beschleunigen, kann
ich die Ausgaben der ``show`` Befehle mit Filtern begrenzen.
Dazu füge ich an das Ende der Zeile ein Leerzeichen,
ein Pipe-Symbol (``|``),
ein weiteres Leerzeichen und den Filter an.
Auch hier habe ich mehrere Möglichkeiten:

.. index:: grep

``| include $muster``:
  zeigt nur die Zeilen an, die $muster enthalten.

``| grep -v $muster``:
  zeigt die Zeilen an, die $muster nicht enthalten.

``| begin $muster``:
  zeigt die Konfiguration ab der Zeile, die $muster enthält, an.

  Mit ``term pager $lines`` kann ich angeben, wieviel Zeilen ich auf
  einmal angezeigt haben will.
  Der Wert 0 schaltet den Pager ab.

Um aus der Konfiguration alle relevanten Informationen zu einem VPN
zu bekommen, benötige ich die folgenden Befehle::

  sh run [all] | i $cryptomap
  sh run [all] tunnel-group $peeraddress
  sh run | i $acl
  sh run [all] | b ikev2 ipsec-proposal $proposal
  sh run [all] | b ikev2 policy
  sh nat $address detail

Der erste Befehl zeigt Informationen an,
die direkt die Child-SA betreffen,
und verweist auf weitere Informationen.

Der zweite Befehl zeigt Informationen zum KeepAlive an.
Die Peer-Adresse erhalte ich aus dem ersten Befehl.
Pre-Shared-Keys sind hier unkenntlich gemacht.
Will ich diese sehen, muss ich den Befehl
``more system:running-config | b tunnel-group $peeraddress`` verwenden.

.. index:: Access Control List
   see: ACL; Access Control List

Beim dritten Befehl filtere ich nach der Access Control List (ACL) für dieses VPN.
Den Namen der ACL erhalte ich aus dem ersten Befehl.
Diese ACL bestimmt die zulässigen Traffic-Selektoren.

Mit dem vierten Befehl kontrolliere ich die Crypto-Parameter für die Child-SA. 
Den Namen des Proposals finde ich aus der Ausgabe des ersten Befehls.

Der fünfte Befehl zeigt die globalen Policies für IKEv2 und damit die
für IKE-SA verhandelbaren Parameter.

Schließlich kontrolliere ich mit dem letzten Befehl die
Adressumsetzungen auf Korrektheit, falls für das VPN Adressen umgesetzt
werden.

Habe ich am Anfang nur die Adresse des Peers zur Identifizierung des VPN,
beginne ich mit dem Befehl ``show run | i $peeraddress`` und finde damit
die benötigte Crypto-Map.

