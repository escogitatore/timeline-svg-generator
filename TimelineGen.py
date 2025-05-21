import svg
import csv

interlinea = 1  # Interlinea desiderata in pt
annozero = 4500  # annozero dell'immagine SVG in mm

def EV(a: int) -> str:
    if a < 0:
        return str(a) + " aEV"
    else:
        return str(a) + " EV"

def mm(a: int) -> str:
    return str(a) + "mm"

def pt(a: int) -> str:
    return str(a) + "pt"

def card(evento: dict) -> list:
    inizio = evento["inizio"]
    fine = evento["fine"]
    colore = evento["colore"]
    titolo = evento["titolo"]
    descrizione = evento["descrizione"]
    nlinee = evento["nlinee"]
    scartoy = evento["scartoy"]
    indice = evento["indice"]
    
    partenza = annozero + inizio

    # Calcola intervallo
    if inizio < 0 and fine > 0:
        intervallo = fine + inizio - 1  # Non esiste l'anno 0
    else:
        intervallo = fine - inizio
    intervallo = abs(intervallo)

    # Formatta le date
    if inizio < 0:
        inizio = abs(inizio)
    if fine < 0:
        fine = abs(fine)
    date = EV(inizio) + " - " + EV(fine)

    # Pulisci la descrizione da caratteri problematici
    descrizione = evento["descrizione"].replace('"', '&quot;').replace("'", '&apos;')
    
    elements = [
        # Date
        svg.Text(
            x=mm(partenza), y=mm(11+scartoy),
            text=date,
            font_size=pt(30),
            fill="black",
            font_family="Arial",
        ),
        # Titolo
        svg.Text(
            x=mm(partenza), y=mm(39+scartoy),
            text=titolo,
            font_size=pt(80),
            fill=colore,
            font_family="Arial",
        ),
        # Linea temporale
        svg.Line(
            x1=mm(partenza), y1=mm(55+scartoy),
            x2=mm(partenza+intervallo), y2=mm(55+scartoy),
            stroke=colore,
            stroke_width=mm(15),
        ),
        # Rettangolo contenitore
        svg.Rect(
            x=mm(partenza), y=mm(69+scartoy),
            width=mm(240), height=mm((15 + interlinea) * nlinee),
            fill="none",
            stroke="red",
            id=f"text-container-{indice}",
        ),
        # Testo con wrapping migliorato
        svg.Text(
            text=descrizione,
            font_size=pt(30),
            fill="black",
            font_family="Arial",
            style=f"text-align: justify; white-space: pre-wrap; word-wrap: break-word; shape-inside: url(#text-container-{indice}); display: inline;",
        ),
    ]
    return elements

def generate_elements(file_path: str) -> list:
    elements = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Salta l'intestazione

        for i, riga in enumerate(reader):
            if len(riga) < 9 or not riga[0] or not riga[3]:
                continue

            nlinee = len(riga[8]) // 50 if riga[8] else 1
            dizionario = {
                "inizio": int(riga[0]) if riga[0] else None,
                "fine": int(riga[3]) if riga[3] else None,
                "colore": "#ee0045",
                "titolo": riga[6],
                "descrizione": riga[8] if len(riga) > 8 else "",
                "nlinee": nlinee,
                "scartoy": i*89+nlinee*(11+interlinea),
                "indice": str(i),
            }
            elements.extend(card(dizionario))

    return elements

def draw() -> svg.SVG:
    return svg.SVG(
        width=mm(7000),
        height=mm(3000),
        elements=generate_elements("Linea Temporale - Filosofia.csv"),
    )

if __name__ == '__main__':
    svg_content = draw()
    with open("output.svg", "w", encoding="utf-8") as file:
        file.write(str(svg_content))
    print("File SVG generato: output.svg")