import svg
import csv

interlinea= 1  # Interlinea desiderata in pt

def csv_dict(file_path: str) -> dict:

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Salta l'intestazione
        riga = next(reader)
        nlinee = len(riga[8]) // 50
        dizionario = {
            "inizio": int(riga[0]) if riga[0] else None,
            "fine": int(riga[3]) if riga[3] else None,
            "colore": "#ee0045",
            "titolo": riga[6],
            "descrizione": riga[8],
            "nlinee": nlinee,
            "scartoy": 0,
        }
    return dizionario

annozero= 4500  # annozero dell'immagine SVG in mm assolutamente da cambiare
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
        width=mm(7000),
        height=mm(3000),
        elements=card(csv_dict("Linea Temporale - Cronologia.csv")),
    )

def card(evento: dict) -> list:
    inizio = evento["inizio"]
    fine = evento["fine"]
    
    colore = evento["colore"]
    titolo = evento["titolo"]
    descrizione = evento["descrizione"]
    nlinee = evento["nlinee"]
    scartoy = evento["scartoy"]
    partenza = annozero+inizio
    #conclusione = annozero+fine
    # Toglie il segno negativo se presente
    

    # Grandezza intervallo da usare per larghezza di svg.Line
    if inizio < 0 and fine > 0:
        intervallo = fine + inizio -1 # Non esiste l'anno 0
    else:
        intervallo = fine - inizio
    if intervallo < 0: # Con date negative abbiamo intervallo negativo, lo giriamo
        intervallo = abs(intervallo)
    
    if inizio<0:
        inizio = abs(inizio)
    if fine<0:
        fine = abs(fine)
    
    date = EV(inizio) + " - " + EV(fine) #scrive in stringa le date
    
    elements = [
        # date ex. 2000 aEV - 1900 aEV
        svg.Text(
            x=mm(partenza), y=mm(11+scartoy),
            text=date,
            font_size=pt(30),
            fill="black",
            font_family="Arial",
        ),
        # titolo ex. Distruzione di Gerusalemme
        svg.Text(
            x=mm(partenza), y=mm(39+scartoy),
            text=titolo,
            font_size=pt(80),
            fill=colore,
            font_family="Arial",
        ),
        # linea del tempo
        svg.Line(
            x1=mm(partenza), y1=mm(55+scartoy),
            x2=mm(partenza+intervallo), y2=mm(55+scartoy),
            stroke=colore,
            stroke_width=mm(15),
        ),
        # rettangolo invisibile con id
        svg.Rect(
            x=mm(partenza), y=mm(69+scartoy),
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