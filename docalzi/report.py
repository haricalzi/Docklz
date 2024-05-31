from fpdf import FPDF

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
    pdf.multi_cell(0, 10, data, align='L')
    pdf.ln(1)


# Funzione che permette di aggiungere un titolo ad un paragrafo nel report
def add_titoletto_report(pdf, titoletto):
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, titoletto, 0, 1, 'L')
    pdf.ln(1)


# Funzione che permette di salvare il PDF del report
def save_report(pdf, path_to_save):
    pdf.output(path_to_save)
    print(f"Report delle scansioni generato correttamente: {path_to_save}")


# Funzione che permette di aggiungere un link ad un paragrafo nel report
def add_link_report(pdf, text, url):
    pdf.set_text_color(0, 0, 255)
    pdf.set_font("Arial", 'U', 10)
    pdf.cell(0, 10, text, 0, 1, 'L', link=url)
    pdf.set_text_color(0, 0, 0)