import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from bs4 import BeautifulSoup


class Main:
    win1 = None
    root = None
    html_path = None
    csv_path = None
    data = None

    def __init__(self):
        self.init_gui()
        self.root.mainloop()

    def init_gui(self):
        self.root = tk.Tk()
        self.root.title("NotaCerta")
        self.root.geometry("400x240")
        self.root.configure(bg='#2b2b2b')

        tk.Label(self.root, text="Caminho do arquivo HTML:", bg='#2b2b2b', fg='white').grid(row=0, column=0, padx=10,
                                                                                            pady=10, sticky='w')
        self.html_path = tk.Entry(self.root, width=40)
        self.html_path.grid(row=1, column=0, padx=10, pady=5)

        tk.Button(self.root, text="Procurar", command=lambda: self.select_file(self.html_path)).grid(row=1, column=1,
                                                                                                     padx=10, pady=5)

        tk.Label(self.root, text="Caminho do arquivo CSV:", bg='#2b2b2b', fg='white').grid(row=2, column=0, padx=10,
                                                                                           pady=10, sticky='w')
        self.csv_path = tk.Entry(self.root, width=40)
        self.csv_path.grid(row=3, column=0, padx=10, pady=5)

        tk.Button(self.root, text="Procurar", command=lambda: self.save_file(self.csv_path)).grid(row=3, column=1,
                                                                                                  padx=10, pady=5)

        tk.Button(self.root, text="Converter", command=self.convert).grid(row=4, column=0, columnspan=2, pady=20)

    def select_file(self, entry):
        filepath = filedialog.askopenfilename(filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
        entry.delete(0, tk.END)
        entry.insert(0, filepath)

    def save_file(self, entry):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        entry.delete(0, tk.END)
        entry.insert(0, filepath)

    def convert(self):
        html_file = self.html_path.get()
        csv_file = self.csv_path.get()
        if not html_file or not csv_file:
            messagebox.showwarning("Campos vazios", "Por favor, selecione os arquivos de entrada e saída.")
            return
        self.analisar_html()

    def analisar_html(self):
        with open(self.html_path.get(), "r", encoding='utf-8') as html_file:
            html_doc = html_file.read()

        soup = BeautifulSoup(html_doc, "html.parser")

        nome_tags = soup.select('td.fixo-prod-serv-descricao span')
        nome_vals = [tag.get_text() for tag in nome_tags]

        print('NOME TAGS')
        print(nome_tags)
        print('\nNOME VALS')
        print(nome_vals)

        qtd_tags = soup.select('td.fixo-prod-serv-qtd span')
        qtd_vals = [tag.get_text() for tag in qtd_tags]

        print('\n\nQTD TAGS')
        print(qtd_tags)
        print('\nQTD VALS')
        print(qtd_vals)

        um_tags = soup.select('td.fixo-prod-serv-uc span')
        um_vals = [tag.get_text() for tag in um_tags]

        print('\n\nMEDIDA TAGS')
        print(um_tags)
        print('\nMEDIDA VALS')
        print(um_vals)

        self.data = (nome_vals, qtd_vals, um_vals)

        self.create_csv()

    def create_csv(self):
        linhas = zip(*self.data)
        with open(self.csv_path.get(), "w", encoding='utf-8') as csv_file:
            escritor = csv.writer(csv_file)
            escritor.writerow(['Nome', 'Quantidade', 'Medida'])
            escritor.writerows(linhas)

        messagebox.showinfo(title="CSV criado com sucesso!")


if __name__ == '__main__':
    Main()
