from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tkinter import scrolledtext
from selenium import webdriver
import tkinter as tk
import time
import sys
import os

class Redirect:
    def __init__(self, text_widget):
        self.output = text_widget

    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)  # Scroll to the bottom

    def flush(self):
        pass  # Needed for file-like compatibility

# Fenster erstellen
root = tk.Tk()
root.title("Web Scraper")
root.geometry("300x500+0+0")

# URL Eingabe
url_label = tk.Label(root, text="Start URL:")
url_label.pack()
url_entry = tk.Entry(root, width=30)
url_entry.insert(0, "https://www.startpage.com/")
url_entry.pack(padx=10)

# Suchbegriff
search_label = tk.Label(root, text="Suchbegriff:")
search_label.pack()
search_entry = tk.Entry(root, width=30)
search_entry.insert(0, "hi")
search_entry.pack(padx=10)

# Seitenzahl
page_label = tk.Label(root, text="Seitenanzahl:")
page_label.pack()
page_entry = tk.Spinbox(root, from_=1, to=100, width=5)  # Setzt den Bereich von 1 bis 100
page_entry.pack(padx=10)

collected_urls = []

# Scraperlogik
def start_scraping():
    pages_to_scrape = int(page_entry.get())
    driver = webdriver.Firefox()
    driver.set_window_size(1000, 600)
    driver.set_window_position(301, 0)
    driver.get(url_entry.get())
    time.sleep(3)
    search_field = driver.find_element(By.ID, 'q')
    search_field.send_keys(search_entry.get())
    search_field.submit()
    time.sleep(10)

    for page_number in range(pages_to_scrape):
        print(f"Scraping Seite {page_number + 1}")
        root.update()  # GUI aktualisieren
        elements = driver.find_elements(By.CSS_SELECTOR, 'a.w-gl__result-title.result-link')
        for element in elements:
            collected_urls.append(element.get_attribute('href'))
            #time.sleep(1)

        if page_number < pages_to_scrape - 1:
            try:
                time.sleep(1)
                driver.execute_script("window.scrollBy(0, 3500)")
                time.sleep(1)
                next_page = driver.find_element(By.CSS_SELECTOR, 'button.pagination__next-prev-button.next')
                next_page.click()
                print(f"Navigation zur Seite {page_number + 2} .")
                root.update()  # GUI aktualisieren
            except Exception as e:
                print(f"Fehler beim Wechseln zur Seite {page_number + 2}: {e}")
                break

            time.sleep(3)

    driver.quit()
    print("Scraping abgeschlossen.")
    root.update()  # GUI aktualisieren

# Resetbutton
def restart_app():
    root.destroy()  # Schließt das aktuelle Fenster
    os.execl(sys.executable, sys.executable, *sys.argv)  # Startet das Programm neu

# Speicherlogik
def save_results():
    new_folder = '/home/mint/Schreibtisch/projekt/results'
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    filename = f"{search_entry.get()}_{len(collected_urls)}.txt"
    file_path = os.path.join(new_folder, filename)

    with open(file_path, 'w') as file:
        for url in collected_urls:
            file.write(url + '\n')

    print(f"Ergebnisse gespeichert in: {filename}")

# Startknopf
start_button = tk.Button(root, text="Start Scraping", command=start_scraping)
start_button.pack(pady=3)

# Speicherknopf
speicher_button = tk.Button(root, text="Save Results", command=save_results)
speicher_button.pack(pady=2)

# Textfeld für die Ausgabe
output_text = scrolledtext.ScrolledText(root, height=10)
output_text.pack(padx=10, pady=10)

# Umleitung der Standard-Ausgabe und Fehlerausgabe
sys.stdout = Redirect(output_text)
sys.stderr = Redirect(output_text)

# Reset-Button
reset_button = tk.Button(root, text="Reset", command=restart_app)
reset_button.pack(pady=2)

# Fenster starten
root.mainloop()