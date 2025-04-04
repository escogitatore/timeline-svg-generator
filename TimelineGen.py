import svg

prova = {
    "date": "2000 aEV - 1900 aEV",
    "colore": "orange",
    "titolo": "Evento di prova",
    "descrizione": "Utilizziamo i cookie per personalizzare contenuti ed annunci, per fornire funzionalità dei social media e per analizzare il nostro traffico. Condividiamo inoltre informazioni sul modo in cui utilizza il nostro sito con i nostri partner che si occupano di analisi dei dati web, pubblicità e social media, i quali potrebbero combinarle con altre informazioni che ha fornito loro o che hanno raccolto dal suo utilizzo dei loro servizi."
}

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
        elements=card(prova),
    )

def card(evento: dict) -> list:
    date = evento["date"]
    colore = evento["colore"]
    titolo = evento["titolo"]
    descrizione = evento["descrizione"]
    interlinea= 1  # Interlinea desiderata in pt

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
            x2=mm(100), y2=mm(55),
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