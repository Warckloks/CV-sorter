if __name__ == "__main__":
    from bs4 import BeautifulSoup
    from fpdf import FPDF

    pdf = FPDF('P', 'mm', 'Letter')
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 20)  

    pdf.cell(0, 10, 'Liste av sist oppdatert CVer', ln=True) 

    pdf.set_font('helvetica', '', 16)  

    req = "C:\\Users\\sldobler\\Downloads\\CV-partner.html"
    with open(req, 'r', encoding='utf-8') as htmlFile:
        soup = BeautifulSoup(htmlFile, "html.parser")
        quotes = soup.find_all("div", attrs={"class": "content_block title margin_bottom_tiny"})
        authors = soup.find_all("div", attrs={"class": "gray smaller_text anti_hover_text"})

        selected_authors = [author.text.strip() for author in authors if 'CV sist oppdatert' not in author.text.strip()]

        data = list(zip(quotes, selected_authors))

        def extract_number(text):
            try:
                return int(''.join(filter(str.isdigit, text)))
            except ValueError:
                return 0

        def custom_sort_key(item):
            text = item[1]
            if "år siden" in text:
                return (6, extract_number(text))
            elif "ca. et år siden" in text:
                return (5, extract_number(text))
            elif "måneder siden" in text:
                return (4, extract_number(text))
            elif "ca. en måned siden" in text:
                return (3, extract_number(text))
            elif "dager siden" in text:
                return (2, extract_number(text))
            elif "ca. timer siden" in text:
                return (1, extract_number(text))
            else:
                return (0, 0)

        # Her må du legge til datoer som du vil ikke skal dukke opp (la person ligge igjen)
        # Here you need to write down the dates you do not want to show up (let person stay)
        excluded_strings = ["år", "måneder", "måned", "dager", "timer", "Person"]

        sorted_data = sorted(data, key=custom_sort_key, reverse=True)

        for quote, author in sorted_data:
            if not any(excluded_string in author for excluded_string in excluded_strings):
                paragraph = f"Person: {quote.text.strip()} \nDato: {author} \n"
                pdf.multi_cell(0, 10, paragraph, ln=True)

    pdf.output('pdf_1_sortedCV.pdf')
    