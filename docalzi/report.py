from fpdf import FPDF
import matplotlib.pyplot as plt

# Funzione che permette di creare il report PDF
def create_pdf(title, path_ris):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_title(title)
    pdf.set_font("Arial", '', 18)
    pdf.cell(0, 10, title, 0, 1, 'C')
    pdf.ln(10)
    testo = f"I risultati grezzi di ogni scansione sono salvati all'interno della directory {path_ris}"
    add_data_report(pdf, testo)
    return pdf


# Funzione che permette di aggiungere dei dati al report
def add_data_report(pdf, data):
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 5, data, align='L')


# Funzione che permette di aggiungere un titolo ad un paragrafo nel report
def add_titoletto_report(pdf, titoletto):
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, titoletto, 0, 1, 'L')


# Funzione che permette di aggiungere un link ad un paragrafo nel report
def add_link_report(pdf, text, url):
    pdf.set_text_color(0, 0, 255)
    pdf.set_font("Arial", 'U', 10)
    pdf.cell(0, 5, text, 0, 1, 'L', link=url)
    pdf.set_text_color(0, 0, 0)


# Funzione che permette di salvare il PDF del report
def save_report(pdf, path_to_save):
    pdf.output(path_to_save)
    print(f"\nReport delle scansioni generato correttamente: {path_to_save}")


# Funzione che permette di creare un grafico a colonne
def make_graph(peso3, peso2, peso1, peso0):
    labels = ['Peso 3', 'Peso 2', 'peso 1', 'Peso 0']
    values = [peso3, peso2, peso1, peso0]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
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


# Funzione che permette di inserire un'immagine nel report
def add_image_report(pdf, image_file):
    y = pdf.get_y()
    page_width = pdf.w - 2 * pdf.l_margin
    image_width = 150
    x = (page_width - image_width) / 2 + pdf.l_margin
    pdf.image(image_file, x=x, y=y, w=image_width)
    pdf.set_y(y + image_width + 5)