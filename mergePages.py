import fitz  # PyMuPDF

def merge_pages_vertically(pdf_path):
    # Otwieramy oryginalny plik PDF
    doc = fitz.open(pdf_path)
    merged_doc = fitz.open()
    if len(doc)<2: return
    # Iterujemy przez pary stron, scalając je pionowo
    for i in range(0, len(doc), 2):
        # Pobieramy pierwszą stronę
        page1 = doc.load_page(i)
        page1_width, page1_height = page1.rect.width, page1.rect.height
        
        try:
            # Pobieramy drugą stronę, jeśli istnieje
            page2 = doc.load_page(i + 1)
            page2_height = page2.rect.height
        except IndexError:
            # Jeśli nie ma drugiej strony (w przypadku nieparzystej liczby stron)
            page2 = None
            page2_height = 0

        # Nowa wysokość strony to suma wysokości dwóch stron
        total_height = page1_height + page2_height

        # Tworzymy nową stronę o szerokości pierwszej strony i wysokości obu stron razem
        merged_page = merged_doc.new_page(width=page1_width, height=total_height)

        # Wstawiamy pierwszą stronę na górę
        merged_page.show_pdf_page(fitz.Rect(0, 0, page1_width, page1_height), doc, i)

        # Jeśli druga strona istnieje, wstawiamy ją poniżej pierwszej
        if page2:
            merged_page.show_pdf_page(fitz.Rect(0, page1_height, page1_width, total_height), doc, i + 1)

    # Zapisujemy wynikowy plik PDF bezpośrednio do pliku
    merged_doc.save(pdf_path)
    merged_doc.close()
    doc.close()
