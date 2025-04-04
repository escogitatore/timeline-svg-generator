import svg

date="2000 aEV - 1900 aEV"
colore="orange"
titolo="Evento di prova"
descrizione="Utilizziamo i cookie per personalizzare contenuti ed annunci, per fornire funzionalità dei social media e per analizzare il nostro traffico. Condividiamo inoltre informazioni sul modo in cui utilizza il nostro sito con i nostri partner che si occupano di analisi dei dati web, pubblicità e social media, i quali potrebbero combinarle con altre informazioni che ha fornito loro o che hanno raccolto dal suo utilizzo dei loro servizi."


# Definizione delle funzioni per le unità di misura
def EV(a: int) -> str:
    if a < 0:
        return str(a) + " aEV"
    else:
        return str(a) + " EV"

def mm(a: int) -> str:
    return str(a) + "mm"

def pt(a: int) -> str:
    return str(a) + "pt"


def split_text(text: str, max_length: int) -> list[str]:
    """
    Divide il testo in righe di lunghezza massima specificata.
    """
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        if len(" ".join(current_line + [word])) <= max_length:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))

    return lines

# Definizione della funzione principale per disegnare l'immagine SVG
def draw() -> svg.SVG:
    descrizione_lines = split_text(descrizione, max_length=40)  # Lunghezza massima per riga
    descrizione_elements = [
        svg.Text(
            x=mm(0), y=mm(75 + i * 10),  # Incrementa la posizione verticale per ogni riga
            text=line,
            font_size=pt(30),
            fill="black",
            font_family="Arial",
        )
        for i, line in enumerate(descrizione_lines)
    ]

    return svg.SVG(
        width=mm(220),
        height=mm(165),
        elements=[
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
            # descrizione dell'evento (testo a capo)
            *descrizione_elements,
        ],
    )

if __name__ == '__main__':
    print(draw())