import svg
import csv

percorso = "Linea Temporale - cronologia.csv"

interlinea= 1  # Interlinea desiderata in pt

def generate_elements(file_path: str) -> list:
    elements = []  # Lista per contenere tutti gli elementi SVG
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Salta l'intestazione
        """ for i, riga in enumerate(reader):
            if i >= 10:  # Limita il ciclo a 10 passaggi
                break """

        for i, riga in enumerate(reader):  # Ciclo su tutte le righe del CSV
            # Controlla che la riga abbia abbastanza colonne e dati validi
            if len(riga) < 9 or not riga[0] or not riga[3]:
                continue

            # Crea il dizionario per la funzione card
            nlinee = len(riga[8]) // 50 if riga[8] else 1
            dizionario = {
                "inizio": int(riga[0]) if riga[0] else None,
                "fine": int(riga[3]) if riga[3] else None,
                "colore": "#ee0045",  # Puoi personalizzare il colore
                "titolo": riga[6],
                "descrizione": riga[8] if len(riga) > 8 else "",
                "nlinee": nlinee,
                "scartoy": i*89+nlinee*(11+interlinea),  # Calcola lo scarto in base all'indice della riga
                "indice": "#text-container-" + str(i),
            }

            # Chiama la funzione card e unisce i risultati
            elements.extend(card(dizionario))

    return elements

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
        elements=generate_elements(percorso),
    )

def card(evento: dict) -> list:
    inizio = evento["inizio"]
    fine = evento["fine"]
    
    colore = evento["colore"]
    titolo = evento["titolo"]
    descrizione = evento["descrizione"]
    nlinee = evento["nlinee"]
    scartoy = evento["scartoy"]
    indice= evento["indice"]
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
            id=indice,  # Assegna un id al rettangolo
        ),
        # testo giustificato all'interno del rettangolo
        svg.Text(
            text=descrizione,
            font_size=pt(30),
            fill="black",
            font_family="Arial",
            style="text-align: justify; white-space: pre; shape-inside: url("+indice+"); display: inline;",
        ),
    ]
    return elements

if __name__ == '__main__':
    # Genera il contenuto SVG
    svg_content = draw()
    
    # Scrive il contenuto SVG in un file
    with open("output-civilta.svg", "w", encoding="utf-8") as file:
        file.write(str(svg_content))
    
    print("File SVG generato: output-civilta.svg")