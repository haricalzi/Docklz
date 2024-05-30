from fpdf import FPDF

# Funzione che permette di creare il report PDF
def create_pdf(title):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_title(title)
    pdf.set_font("Arial", size=12)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, title, 0, 1, 'C')
    pdf.ln(10)
    return pdf


# Funzione che permette di aggiungere dei dati al report
def add_data_report(pdf, data):
    pdf.multi_cell(0, 10, data)
    pdf.ln()


# Funzione che permette di salvare il PDF del report
def save_report(pdf, path_to_save):
    pdf.output(path_to_save)