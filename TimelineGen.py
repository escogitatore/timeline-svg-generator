# Importa le librerie necessarie
import svg  # Libreria per generare elementi SVG
import csv  # Libreria per leggere file CSV

# Variabili globali
interlinea = 1      # Spazio tra le righe di testo in punti
annozero = 4500     # Punto di riferimento per la timeline in millimetri
nome_tabella="Civiltà", "Cronologia", "Filosofia", "Linguaggio", "Scienza"  # Nome della tabella per il CSV

# Funzione per formattare le date con "aEV" (avanti Era Volgare) o "EV" (Era Volgare)
def EV(a: int) -> str:
    if a < 0:
        return str(a) + " aEV"  # Per date negative (avanti era volgare)
    else:
        return str(a) + " EV"   # Per date positive (era volgare)
# Funzioni helper per le unità di misura
def mm(a: int) -> str:
    return str(a) + "mm"  # Converte numeri in millimetri per SVG
def pt(a: int) -> str:
    return str(a) + "pt"  # Converte numeri in punti per SVG

# Funzione principale per creare una "carta" evento
def card(evento: dict) -> list:
    # Estrae i dati dal dizionario
    inizio = evento["inizio"]        # Anno di inizio evento
    fine = evento["fine"]            # Anno di fine evento
    accent_color = evento["colore1"]        # Colore della carta
    text_color = evento["colore2"]          # Colore del testo
    titolo = evento["titolo"]        # Titolo dell'evento
    descrizione = evento["descrizione"]  # Descrizione dell'evento
    nlinee = evento["nlinee"]        # Numero di linee del testo
    scartoy = evento["scartoy"]      # Spaziatura verticale
    indice = evento["indice"]        # Indice univoco della carta
    
    # Calcola la posizione orizzontale dell'evento
    partenza = annozero + inizio     # Posizione rispetto all'anno zero

    # Calcola la lunghezza della linea temporale
    if inizio < 0 and fine > 0:
        # Gestisce eventi che attraversano l'anno zero
        intervallo = fine + inizio - 1  # -1 perché non esiste l'anno 0
    else:
        intervallo = fine - inizio
    intervallo = abs(intervallo)      # Converte in valore positivo

    # Formatta le date per la visualizzazione
    if inizio < 0:
        inizio = abs(inizio)
    if fine < 0:
        fine = abs(fine)
    date = EV(inizio) + " - " + EV(fine)  # Stringa formato "XXXX aEV - YYYY EV"

    # Pulisce la descrizione da caratteri che potrebbero causare problemi in SVG
    descrizione = evento["descrizione"].replace('"', '&quot;').replace("'", '&apos;')
    
    # Crea la lista di elementi SVG per la carta
    elements = [
        # Data dell'evento
        svg.Text(
            x=mm(partenza), y=mm(11+scartoy),
            text=date,
            font_size=pt(30),
            fill=text_color,
            font_family="Arial",
        ),
        # Titolo dell'evento
        svg.Text(
            x=mm(partenza), y=mm(39+scartoy),
            text=titolo,
            font_size=pt(80),
            fill=accent_color,
            font_family="Arial",
        ),
        # Linea temporale che rappresenta la durata dell'evento
        svg.Line(
            x1=mm(partenza), y1=mm(55+scartoy),
            x2=mm(partenza+intervallo), y2=mm(55+scartoy),
            stroke=accent_color,
            stroke_width=mm(15),
        ),
        # Rettangolo contenitore per il testo della descrizione
        svg.Rect(
            x=mm(partenza), y=mm(69+scartoy),
            width=mm(240), height=mm((15 + interlinea) * nlinee),
            fill="none",
            stroke=accent_color,
            id=f"text-container-{indice}",
        ),
        # Testo della descrizione con wrapping automatico
        svg.Text(
            text=descrizione,
            font_size=pt(30),
            fill=text_color,
            font_family="Arial",
            style=f"text-align: justify; white-space: pre-wrap; word-wrap: break-word; shape-inside: url(#text-container-{indice}); display: inline;",
        ),
    ]
    return elements

# Funzione per generare tutti gli elementi SVG dal file CSV
def generate_elements(file_path: str, nome_tab: str) -> list:
    elements = []  # Lista per tutti gli elementi SVG
    accent_color = scegli_colore(nome_tab)[0]
    text_color = scegli_colore(nome_tab)[1]  # Colore del testo
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Salta la riga di intestazione

        # Itera su tutte le righe del CSV
        for i, riga in enumerate(reader):
            # Salta righe che non hanno date di inizio o fine
            if not riga[0] or not riga[3]:
                continue

            try:
                # Calcola il numero di linee per la descrizione
                nlinee = len(riga[8]) // 40 if riga[8] else 1
                
                # Crea il dizionario con i dati dell'evento
                dizionario = {
                    "inizio": int(riga[0].strip()),  # Rimuove spazi e converte in intero
                    "fine": int(riga[3].strip()),    # Rimuove spazi e converte in intero
                    "colore1": accent_color,
                    "colore2": text_color,
                    "titolo": riga[6],
                    "descrizione": riga[8] if len(riga) > 0 else "",
                    "nlinee": nlinee,
                    "scartoy": i*89+nlinee*(11+interlinea),
                    "indice": nome_tab + str(i),
                }
                # Aggiunge gli elementi della carta alla lista principale
                elements.extend(card(dizionario))
            except ValueError as e:
                print(f"Errore nella riga {i+2}: {e}")  # i+2 perché contiamo l'intestazione e l'indice base 0
                continue

    return elements

# Funzione principale per creare l'SVG
def draw(file_path: str, nome_tab: str) -> svg.SVG:
    return svg.SVG(
        width=mm(7000),    # Larghezza totale dell'SVG
        height=mm(3000),   # Altezza totale dell'SVG
        elements=generate_elements(file_path, nome_tab),  # Genera tutti gli elementi
    )

def scegli_colore(nome_tabella: str) -> list:
    """
    Restituisce una lista di due colori [accent_color, text_color] per la tabella specificata
    """
    # Dizionari dei colori per accent e text
    colori = {
        0: {  # Colori accent
            "Civiltà": "#FF5733",      # Rosso	
            "Cronologia": "#33FF57",   # Verde
            "Filosofia": "#3357FF",    # Blu
            "Linguaggio": "#FF33A1",   # Rosa
            "Scienza": "#FF8C33",      # Arancione
        },
        1: {  # Colori text
            "Civiltà": "#180000",      # Rosso scuro
            "Cronologia": "#001800",   # Verde scuro
            "Filosofia": "#000018",    # Blu scuro
            "Linguaggio": "#180018",   # Rosa scuro
            "Scienza": "#180A00",      # Arancione scuro
        }
    }
    
    # Restituisce una lista con i due colori [accent_color, text_color]
    return [
        colori[0].get(nome_tabella, "#000000"),  # Colore accent (nero se non trovato)
        colori[1].get(nome_tabella, "#000000")   # Colore text (nero se non trovato)
    ]

# Punto di ingresso del programma
if __name__ == '__main__':
    
    for each in nome_tabella:
        file_path = f"Linea Temporale - {each}.csv"
        svg_content = draw(file_path,each)  # Genera il contenuto SVG
        # Salva il contenuto in un file
        with open(f"output_{each}.svg", "w", encoding="utf-8") as file:
            file.write(str(svg_content))
    print(f"File SVG generato: output_{each}.svg")