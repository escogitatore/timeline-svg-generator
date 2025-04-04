import svg
import csv

def csv_dict(file_path: str) -> dict:
    """
    Legge il file CSV e genera un dizionario con i dati della prima riga.
    Colonne utilizzate:
    - Prima colonna: inizio
    - Quarta colonna: fine
    - Settima colonna: titolo
    - Nona colonna: descrizione
    """
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Salta l'intestazione
        prima_riga = next(reader)  # Legge la prima riga di dati

        # Crea il dizionario con i dati richiesti
        dizionario = {
            "inizio": int(prima_riga[0]) if prima_riga[0] else None,
            "fine": int(prima_riga[3]) if prima_riga[3] else None,
            "colore": "#ee0045",
            "titolo": prima_riga[6],
            "descrizione": prima_riga[8],
        }
        return dizionario

def EV(a: int) -> str:
    if a < 0:
        return str(a) + " aEV"
    else:
        return str(a) + " EV"
def mm(a: int) -> str:
    return str(a) + "mm"
def pt(a: int) -> str:
    return str(a) + "pt"

# Definizione della funzione principale per disegnare l'immagine SVG
def draw() -> svg.SVG:
    return svg.SVG(
        width=mm(240),
        height=mm(165),
        elements=card(csv_dict("Linea Temporale - Cronologia.csv")),
    )

def card(evento: dict) -> list:
    inizio = evento["inizio"]
    fine = evento["fine"]
    
    colore = evento["colore"]
    titolo = evento["titolo"]
    descrizione = evento["descrizione"]
    interlinea= 1  # Interlinea desiderata in pt

    # Toglie il segno negativo se presente
    if inizio<0:
        inizio = abs(inizio)
    if fine<0:
        fine = abs(fine)
    date = EV(inizio) + " - " + EV(fine) #scrive in stringa le date

    # Grandezza intervallo da usare per larghezza di svg.Line
    if inizio < 0 and fine > 0:
        intervallo = fine + inizio -1 # Non esiste l'anno 0
    else:
        intervallo = fine - inizio
    if intervallo < 0: # Con date negative abbiamo intervallo negativo, lo giriamo
        intervallo = abs(intervallo)

    nlinee = len(descrizione) // 50 + 1  # Calcola il numero di linee in base alla lunghezza del testo
    #nlinee=descrizione.count("\n") + 1  # Conta il numero di linee nel testo
    elements = [
        # date ex. 2000 aEV - 1900 aEV
        svg.Text(
            x=mm(0), y=mm(11),
            text=date,
            font_size=pt(30),
            fill="black",
            font_family="Arial",
        ),
        # titolo ex. Distruzione di Gerusalemme
        svg.Text(
            x=mm(0), y=mm(39),
            text=titolo,
            font_size=pt(80),
            fill=colore,
            font_family="Arial",
        ),
        # linea del tempo
        svg.Line(
            x1=mm(0), y1=mm(55),
            x2=mm(intervallo), y2=mm(55),
            stroke=colore,
            stroke_width=mm(15),
        ),
        # rettangolo invisibile con id
        svg.Rect(
            x=mm(0), y=mm(69),
            width=mm(240), height=mm((15 + interlinea) * nlinee),
            fill="none",
            stroke="none",
            id="text-container",  # Assegna un id al rettangolo
        ),
        # testo giustificato all'interno del rettangolo
        svg.Text(
            text=descrizione,
            font_size=pt(30),
            fill="black",
            font_family="Arial",
            style="text-align: justify; white-space: pre; shape-inside: url(#text-container); display: inline;",
        ),
    ]
    return elements

if __name__ == '__main__':
    # Genera il contenuto SVG
    svg_content = draw()
    
    # Scrive il contenuto SVG in un file
    with open("output.svg", "w", encoding="utf-8") as file:
        file.write(str(svg_content))
    
    print("File SVG generato: output.svg")