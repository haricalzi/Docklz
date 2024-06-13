from fpdf import FPDF
import matplotlib.pyplot as plt
import sys

# Funzione che permette di creare il report PDF
def create_pdf(title, path_ris):

    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_title(title)
        pdf.set_font("helvetica", '', 18)
        pdf.multi_cell(0, 10, title, align='C')
        #pdf.cell(0, 10, title, 0, 1, 'C')
        pdf.ln(10)
        testo = f"I risultati grezzi di ogni scansione sono salvati all'interno della directory {path_ris}"
        add_data_report(pdf, testo)
        return pdf
    except Exception as e:
            print(f"Si è verificato un errore durante la creazione del PDF: {str(e)}")
            sys.exit(-1)


# Funzione che permette di aggiungere dei dati al report
def add_data_report(pdf, data):

    try:
        pdf.set_font("helvetica", '', 10)
        pdf.multi_cell(0, 5, data, align='L')
        pdf.ln(1)
    except Exception as e:
        print(f"Si è verificato un errore durante l'aggiunta dei dati al report: {str(e)}")
        print(f"Testo problematico: {data}")
        sys.exit(-1)


# Funzione che permette di aggiungere un titolo ad un paragrafo nel report
def add_titoletto_report(pdf, titoletto):
    
    try:
        pdf.set_font("helvetica", 'B', 14)
        pdf.cell(0, 10, titoletto, 0, 1, 'L')
    except Exception as e:
        print(f"Si è verificato un errore durante l'aggiunta del titoletto al report: {str(e)}")
        sys.exit(-1)

# Funzione che permette di aggiungere un link ad un paragrafo nel report
def add_link_report(pdf, text, url):

    try:
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("helvetica", 'U', 10)
        pdf.cell(0, 5, text, 0, 1, 'L', link=url)
        pdf.set_text_color(0, 0, 0)
    except Exception as e:
        print(f"Si è verificato un errore durante l'aggiunta del link al report: {str(e)}")
        sys.exit(-1)

# Funzione che permette di salvare il PDF del report
def save_pdf(pdf, path_to_save, type):

    try:
        print("----------------------------------------------------------------")
        pdf.output(path_to_save)
        match type:
            case "report":
                print(f"\nReport delle scansioni generato correttamente: {path_to_save}\n")
            case "allegato":
                print(f"\nAllegato relativo ai CVE generato correttamente: {path_to_save}\n")
    except Exception as e:
        print(f"Si è verificato un errore durante il salvataggio del file: {str(e)}")
        sys.exit(-1)


# Funzione che permette di creare un grafico a colonne
def make_graph(peso3, peso2, peso1, peso0):

    try:
        labels = ['Peso 3', 'Peso 2', 'peso 1', 'Peso 0']
        values = [peso3, peso2, peso1, peso0]
        colors = ['lightcoral', 'gold', 'lightskyblue', 'yellowgreen']
        bars = plt.bar(labels, values, color=colors)
        plt.xlabel('Categorie di peso')
        plt.ylabel('Numero di CVE')
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height}', ha='center', va='bottom')
        nome_grafico = 'CVE_peso_grafico.png'
        plt.savefig(nome_grafico)
        plt.close()

        return nome_grafico
    except Exception as e:
        print(f"Si è verificato un errore durante la creazione del grafo: {str(e)}")
        sys.exit(-1)


# Funzione che permette di inserire un'immagine nel report
def add_image_report(pdf, image_file):

    try:
        y = pdf.get_y()
        page_width = pdf.w - 2 * pdf.l_margin
        image_width = 150
        x = (page_width - image_width) / 2 + pdf.l_margin
        pdf.image(image_file, x=x, y=y, w=image_width)
        pdf.set_y(y + image_width + 5)
    except Exception as e:
        print(f"Si è verificato un errore durante l'aggiunta dell'immagine nel report: {str(e)}")
        sys.exit(-1)
