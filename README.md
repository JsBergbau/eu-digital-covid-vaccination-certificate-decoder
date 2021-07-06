# Vaccination Pass Decoder
See englisch version below

Mit diesem einfachen Skript kann der EU weite digitale Impfnachweis in ein menschlich lesbares Format (JSON) dekodiert werden und überprüft werden, welche persönlichen Daten gespeichert sind. Die Gültigkeit des Zertifikats kann mit der [offiziellen RKI-App CovPassCheck]( https://play.google.com/store/apps/details?id=de.rki.covpass.checkapp) überprüft werden. 

Um als frisch geimpfter sicherzugehen, dass das Zertifikat auch funktioniert: Das Datum des Smartphones 15 Tage in die Zukunft stellen und Zertifikat scannen. Es wird dann der Name, sowie das Geburtsdatum in der RKI-App angezeigt.

Auch Testzertifikate oder Genesenenzertifikate können damit dekodiert werden.

## Vorbereitungen / Voraussetzungen

Es wird Python3 und einige Module benötigt.

Installation via `pip3 base45 cose` bzw. je nach Installation lautet der Befehl auch nur `pip` statt `pip3`.

## Verwendung
Scannt euren QR-Code mit einer App. Meine Empfehlung hierfür ist der [Cognex Barcode Scanner]( https://play.google.com/store/apps/details?id=com.manateeworks.barcodescanners). Das Programm wird mit diesem String als einziges Argument aufgerufen. Zum Beispiel

```
python impfzertifikatDecoder.py "HC1:6BF+70790T9WJWG.FKY*4GO0.O1CV2 O5 N2FBBRW1*70HS8WY04AC*WIFN0AHCD8KD97TK0F90KECTHGWJC0FDC:5AIA%G7X+AQB9746HS80:54IBQF60R6$A80X6S1BTYACG6M+9XG8KIAWNA91AY%67092L4WJCT3EHS8XJC$+DXJCCWENF6OF63W5NW6WF6%JC QE/IAYJC5LEW34U3ET7DXC9 QE-ED8%E.JCBECB1A-:8$96646AL60A60S6Q$D.UDRYA 96NF6L/5QW6307KQEPD09WEQDD+Q6TW6FA7C466KCN9E%961A6DL6FA7D46JPCT3E5JDLA7$Q6E464W5TG6..DX%DZJC6/DTZ9 QE5$CB$DA/D JC1/D3Z8WED1ECW.CCWE.Y92OAGY8MY9L+9MPCG/D5 C5IA5N9$PC5$CUZCY$5Y$527B+A4KZNQG5TKOWWD9FL%I8U$F7O2IBM85CWOC%LEZU4R/BXHDAHN 11$CA5MRI:AONFN7091K9FKIGIY%VWSSSU9%01FO2*FTPQ3C3F"
```

Oder je nach Installation auch `python3` statt `python`

Das Ergebnis ist

```json
{
      "1": "DE",
      "6": 1622316073,
      "4": 1643356073,
      "-260": {
            "1": {
                  "v": [
                        {
                              "ci": "URN:UVCI:01DE/IZ12345A/5CWLU12RNOB9RXSEOP6FG8#W",
                              "co": "DE",
                              "dn": 2,
                              "dt": "2021-05-29",
                              "is": "Robert Koch-Institut",
                              "ma": "ORG-100031184",
                              "mp": "EU/1/20/1507",
                              "sd": 2,
                              "tg": "840539006",
                              "vp": "1119349007"
                        }
                  ],
                  "dob": "1964-08-12",
                  "nam": {
                        "fn": "Mustermann",
                        "gn": "Erika",
                        "fnt": "MUSTERMANN",
                        "gnt": "ERIKA"
                  },
                  "ver": "1.0.0"
            }
      }
}
```


## Aufbau des QR Codes des digitalen Covid Impfzertifikats 
Die Zeichen im QR-Code sind Base45 kodiert. Warum dieses merkwürdige Base45 Format? 

QR-Codes haben die Besonderheit, dass bei Verwendung 45 vorgegebener Zeichen ein eigener Kompressionsalgorithmus und Fehlerkorrektur verwendet wird. Das heißt der Code wird trotz Fehler einfacher zu dekodieren bzw. kompakter, siehe dazu https://github.com/multiformats/multibase/issues/64

Hier finden sich Beispiel QR-Codes
https://github.com/eu-digital-green-certificates/dgc-testdata/tree/main/DE
und die zugehörigen JSON-Daten
https://github.com/eu-digital-green-certificates/dgc-testdata/blob/main/DE/2DCode/raw/1.json

Es sind an persönlichen Daten also Name und Vorname + Geburtsdatum gespeichert. Des Weiteren wird die Zertifikatsseriennummer gespeichert. Hinter der könnten theoretisch in einer zentralen Datenbank noch weitere Daten hinterlegt sein. Angeblich wird das aber nicht praktiziert. Es wird das Zertifikat erstellt und dann angeblich alle persönlichen Daten von den Servern des RKI wieder gelöscht.

### Dekodierung des Impfzertifikats

Zunächst werden die Base45 Daten in Binärdaten dekodiert. Diese sind zlib komprimiert, daher werden sie dekomprimiert. Die dekomprimierten Daten liegen nun im [CBOR Format]( https://de.wikipedia.org/wiki/Concise_Binary_Object_Representation) vor. Diese werden ins für den Menschen leichter lesbare JSON Format umgewandelt, sodass man überprüfen kann, welche persönlichen Daten gespeichert sind.

### Keine Notwendigkeit eine App für den digitalen Impfausweis zu benutzen

Auf dem digitalen Impfnachweis steht

> "Scannen Sie den nebenstehenden QR-Code mit der CovPass-App oder der Corona-Warn-App, um Ihren digitalen Impfnachweis zu erstellen"

Das ist sehr missverständlich. Der auf Papier vorliegende Code ist bereits der Impfnachweis. Scannt man den Code mit der CornaWarn-App, wird zwar ein QR-Code erzeugt, der etwas anders aussieht, aber der Inhalt ist genau der Gleiche. Ein gutes Foto des Papierzertifikats ist genauso ein digitaler Impfausweis.
Der Code sieht anders aus, weil z.B. das interne Base45 Kodierungsschema nicht verwendet wird oder ein anderes Level an Fehlerkorrektur verwendet wird.

Das Vorzeigen des digitalen Impfnachweises birgt immer das Risiko, dass so Zugriff aufs entsperrte Smartphone erlangt werden kann, daher ist die Papierlösung die einfachste Lösung. Geht es doch nicht anders, so heftet bitte die App an. Damit kann der Übeltäter ohne das Smartphone zu entsperren nur auf diese App zugreifen, [Anleitung zum Anpinnen]( https://www.netzwelt.de/anleitung/184750-android-app-bildschirm-pinnenso-gehts.html).

