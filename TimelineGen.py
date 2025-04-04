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


# Definizione della funzione principale per disegnare l'immagine SVG
def draw() -> svg.SVG:
    return svg.SVG(
        width=mm(220),
        height=mm(165),
        elements=[
            #date ex. 2000 aEV - 1900 aEV
            svg.Text(
                x=mm(0), y=mm(11),
                text=date,
                font_size=pt(30),
                fill="black",
                font_family="Arial",
            ),
            #titolo ex. Distruzione di Gerusalemme
            svg.Text(
                x=mm(0), y=mm(39),
                text=titolo,
                font_size=pt(80),
                fill=colore,
                font_family="Arial",
                #font_style="bold",
                #font_weight="bold",
            ),
            #linea del tempo
            svg.Line(
                x1=mm(0), y1=mm(55),
                x2=mm(100), y2=mm(55),
                stroke=colore,
                stroke_width=mm(15),
            ),
            #descrizione dell'evento
            svg.Text(
                x=mm(0), y=mm(75),
                text=descrizione,
                font_size=pt(30),
                fill="black",
                font_family="Arial",
            ),
        ],
    )



if __name__ == '__main__':
    print(draw())