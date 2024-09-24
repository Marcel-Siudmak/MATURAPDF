import fitz  # PyMuPDF

def find_tasks_in_pdf(name):
    doc = fitz.open(name)
    tasks = []
    last_task = None
    task_started = False

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        words = page.get_text("words")
        
        for i, word in enumerate(words):
            # Sprawdzamy, czy aktualne słowo to "Zadanie"
            if word[4] == "Zadanie" and i + 2 < len(words):
                # Pobieramy numer zadania i nazwę, korzystając z kolejnych słów
                task_number, task_name = extract_task_info(words[i+1], words[i+2])

                if task_started:
                    # Zakończenie poprzedniego zadania
                    if word[1]<85:
                        last_task["pend"] = page_num-1  # Strona końca poprzedniego zadania
                        last_task["bottom"] = 842-60  # Koniec poprzedniego zadania
                    else:
                        last_task["pend"] = page_num  # Strona końca poprzedniego zadania
                        last_task["bottom"] = word[1]  # Koniec poprzedniego zadania
                    
                    tasks.append(last_task)  # Zapisujemy poprzednie zadanie
                    
                # Zaczynamy nowe zadanie
                last_task = {
                    "number": task_number,
                    "name": task_name,
                    "pstart": page_num,
                    "pend": None,  # Zostanie wypełnione później
                    "up": word[1],  # Pozycja pionowa początku zadania
                    "bottom": None  # Zostanie wypełnione przy końcu
                }
                task_started = True

            # Sprawdzamy, czy słowo to "Brudnopis", co wyznacza koniec ostatniego zadania
            if word[4].upper() == "BRUDNOPIS" and last_task:
                last_task["pend"] = page_num-1
                last_task["bottom"] = 842-60
                tasks.append(last_task)  # Dodajemy ostatnie zadanie
                task_started = False  # Zakończyliśmy przetwarzanie zadań
    
    doc.close()
    return tasks


def extract_task_info(task_number_word, task_name_word):
    """Wydobywa numer zadania i nazwę zadania z kolejnych słów."""
    try:
        # Pobieramy numer zadania i nazwę zadania
        task_number = task_number_word[4] # Usuwamy kropkę z numeru zadania
        task_name = task_name_word[4]  # Zakładamy, że nazwa zadania to kolejne słowo
        return task_number, task_name
    except IndexError:
        return None, None


# Przykład użycia:

# pdf_name = "test.pdf"
# zadania = find_tasks_in_pdf("test.pdf")

# # Wyświetlenie wyników:
# for zadanie in zadania:
#     print(zadanie)

