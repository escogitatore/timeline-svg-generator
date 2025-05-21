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

def split_text(text: str, max_chars: int = 50) -> list:
    """Divide il testo in linee di lunghezza massima specificata."""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word)
        if current_length + word_length + 1 <= max_chars:
            current_line.append(word)
            current_length += word_length + 1
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = word_length + 1

    if current_line:
        lines.append(" ".join(current_line))

    return lines

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
    
    # Divide il testo in linee
    linee = split_text(descrizione, 50)
    
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
            width=mm(240), height=mm((15 + interlinea) * len(linee)),
            fill="none",
            stroke="red",
            id=f"text-container-{indice}",
        ),
    ]
    
    # Aggiungi ogni linea di testo separatamente
    for i, linea in enumerate(linee):
        elements.append(
            svg.Text(
                x=mm(partenza), 
                y=mm(69 + scartoy + (i * (15 + interlinea))),
                text=linea,
                font_size=pt(30),
                fill="black",
                font_family="Arial",
            )
        )
    
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