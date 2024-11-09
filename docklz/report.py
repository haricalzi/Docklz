from fpdf import FPDF
import matplotlib.pyplot as plt
import sys

# Function to create the PDF report
def create_pdf(title, path_res):

    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_title(title)
        pdf.set_font("helvetica", '', 18)
        pdf.multi_cell(0, 10, title, align='C')
        #pdf.cell(0, 10, title, 0, 1, 'C')
        pdf.ln(10)
        text = f"The raw results of each scan are saved in the directory {path_res}"
        add_data_report(pdf, text)
        return pdf
    except Exception as e:
        print(f"An error occurred during PDF creation: {str(e)}")
        sys.exit(-1)


# Function to add data to the report
def add_data_report(pdf, data):

    try:
        pdf.set_font("helvetica", '', 10)
        pdf.multi_cell(0, 5, data, align='L')
        pdf.ln(1)
    except Exception as e:
        print(f"An error occurred while adding data to the report: {str(e)}")
        #print(f"Problematic text: {data}")
        sys.exit(-1)


# Function to add a heading to a paragraph in the report
def add_little_title_report(pdf, title):
    
    try:
        pdf.set_font("helvetica", 'B', 14)
        pdf.cell(0, 10, title, 0, 1, 'L')
    except Exception as e:
        print(f"An error occurred while adding the heading to the report: {str(e)}")
        sys.exit(-1)

# Function to add a link to a paragraph in the report
def add_link_report(pdf, text, url):

    try:
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("helvetica", 'U', 10)
        pdf.cell(0, 5, text, 0, 1, 'L', link=url)
        pdf.set_text_color(0, 0, 0)
    except Exception as e:
        print(f"An error occurred while adding the link to the report: {str(e)}")
        sys.exit(-1)

# Function to save the report PDF
def save_pdf(pdf, path_to_save, type):

    try:
        print("----------------------------------------------------------------")
        pdf.output(path_to_save)
        match type:
            case "report":
                print(f"\nScan report generated successfully: {path_to_save}\n")
            case "attachment":
                print(f"\nCVE attachment generated successfully: {path_to_save}\n")
    except Exception as e:
        print(f"An error occurred while saving the file: {str(e)}")
        sys.exit(-1)


# Function to create a bar chart
def make_graph(weight3, weight2, weight1, weight0):

    try:
        labels = ['Weight 3', 'Weight 2', 'Weight 1', 'Weight 0']
        values = [weight3, weight2, weight1, weight0]
        colors = ['lightcoral', 'gold', 'lightskyblue', 'yellowgreen']
        bars = plt.bar(labels, values, color=colors)
        plt.xlabel('Weight Categories')
        plt.ylabel('Number of CVEs')
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height}', ha='center', va='bottom')
        chart_name = 'CVE_weight_chart.png'
        plt.savefig(chart_name)
        plt.close()

        return chart_name
    except Exception as e:
        print(f"An error occurred while creating the chart: {str(e)}")
        sys.exit(-1)


# Function to insert an image into the report
def add_image_report(pdf, image_file):

    try:
        y = pdf.get_y()
        page_width = pdf.w - 2 * pdf.l_margin
        image_width = 150
        x = (page_width - image_width) / 2 + pdf.l_margin
        pdf.image(image_file, x=x, y=y, w=image_width)
        pdf.set_y(y + image_width + 5)
    except Exception as e:
        print(f"An error occurred while adding the image to the report: {str(e)}")
        sys.exit(-1)
