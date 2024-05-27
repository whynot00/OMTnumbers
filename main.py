import tkinter as tk
from tkinter import filedialog as fd
import os, json

from download_numbers_db import ParseUrl
from normalize_txt import Norm
from number_ratio import Ratio
from export import Export

class EntryFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.normalize = Norm()
        
        tk.Label(self, text="Информация о последнем обновлении данных:").grid(row=0, column=0)

        self._get_data()

        self._set_entry_window()

    def _get_data(self):
        
        message =  "Файлы не обнаружены"

        if "csv_data" in os.listdir(".") and "data.json" in os.listdir("csv_data"):
            with open("csv_data/data.json", "r", encoding="utf-8") as file:
                message =  f"Последнее обновление {json.load(file)["data"]}"

        tk.Label(self, text=message).grid(row=1, column=0, sticky=tk.W)
        tk.Button(self, text="Обновить", width=10, height=2, command=self._update_data).grid(row=0, column=1, rowspan=2, sticky=tk.W, padx=(10, 0))

    def _update_data(self):
        parce_csv = ParseUrl()
        for name, url in parce_csv.urls_dict.items():
            parce_csv(name, url)

    def _set_entry_window(self):
        
        tk.Label(self, text="Вставьте в данное окно необходимые абоненсткие номера:").grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(15, 0))
        self.number_box = tk.Text(self, width=45, height=10)
        tk.Button(self, text="Загрузить .txt файл", height=1, width= 17, command=self.__search_file).grid(row=4, column=0, sticky=tk.W, pady=(10, 0))
        tk.Button(self, text="Начать",width=10, height=1, command=self.__get_box_data).grid(row=4, column=1, sticky=tk.E, pady=(10, 0))

        self.number_box.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(7, 0))

    
    def __search_file(self):

        filetype = (("Текстовый файл", "*.txt"),)
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/",filetypes=filetype)

        self.number_box.insert(1.0, self.normalize.open_folder(filename))

    def __get_box_data(self):

        self.normalize.normalize(self.number_box.get(1.0, "end-1c").split())

        ratio = Ratio(self.normalize.norm_lst)
        selected_numbers = ratio.select_result

        tk.Label(self, text="Готово к экспорту:").grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)

        self.export = Export(selected_numbers)

        tk.Button(self, text="TXT", width=15, pady=2, command=self.export.export_txt).grid(row=6, column=0, sticky=tk.W)
        tk.Button(self, text="CSV", width=15, pady=2, command=self.export.export_csv).grid(row=7, column=0, sticky=tk.W, pady=(10,0))

class App(tk.Tk):

    def __init__(self):

        super().__init__()
        self.title("ОМТ Телефоны")
        self.resizable(width=False, height=True)

        EntryFrame(self).grid(row=0, column=0, padx=(30, 30), pady=20)

        
app = App()
app.mainloop()
