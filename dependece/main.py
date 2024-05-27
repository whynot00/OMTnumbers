import requests, bs4, datetime, chardet, re, os, json, csv

from tkinter import filedialog as fd
import tkinter as tk


def encode(path):
   rawdata = open(path, "rb").readline()
   return chardet.detect(rawdata)['encoding']

def removing_excess(value):

   regex_excess = re.compile(r"[().\s+\\n-]")
   return list(map(lambda x: regex_excess.sub("", x), value)) if type(value) == list else regex_excess.sub("", value)

class GetReq:
    
    def __init__(self):

        resp = requests.get("https://opendata.digital.gov.ru/registry/numeric/downloads", verify=False)
        soup = bs4.BeautifulSoup(resp.content, "lxml")
        self.groups = soup.find_all("div", {"class": "pl-5 sm:pl-6"})

        self.create_folder()

class ParseUrl(GetReq):

    def __init__(self):
        super().__init__()

        self.data_dict = {"urls": {}}

        for group in self.groups:
            name = group.find("div").text.strip()
            url = group.find("a", href=True)["href"]

            self.data_dict["urls"].update({name: url})

        self.data_dict["data"] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')

        with open(f"csv_data/data.json", "w", encoding="utf-8") as file:
            json.dump(self.data_dict, file, ensure_ascii=False, indent=4)
        
    def create_folder(self):
        if "csv_data" not in os.listdir("."):
            os.makedirs("csv_data")

    def __call__(self, name, url):

        name = name.replace(' ', '_')
        url = url.strip()

        with open(f"csv_data/{name}.csv", "wb") as file:
            file.write(requests.get(url, verify=False).content)

    @property
    def urls_dict(self):
        return self.data_dict["urls"]

class Norm:

    def open_folder(self, path):
        encoding = encode(path)
        with open(path, "r", encoding=encoding) as file:
            data = file.readlines()
        
        self.normalize(data)

        return "\n".join(self._lst_data)

    def normalize(self, data):
        self._lst_data = []
        for string in data:
            if string != "\n":
                if len(string.split()) != 1:
                    self._lst_data += removing_excess(string.strip().split())
                    continue
                self._lst_data.append(removing_excess(string.strip()))

        for index, number in enumerate(self._lst_data):
            if len(number) == 11 and number[0] in ("7", "8"):
                self._lst_data[index] = number[1:]

    @property
    def norm_lst(self):
        return self._lst_data

class Ratio:

    def __init__(self, lst_in: list):
        
        self.__slected_numbers = []

        lst_9x = list(filter(lambda numer: numer[0] == "9", lst_in))
        lst_3x = list(filter(lambda numer: numer[0] == "3", lst_in))
        lst_4x = list(filter(lambda numer: numer[0] == "4", lst_in))
        lst_8x = list(filter(lambda numer: numer[0] == "8", lst_in))


        if len(lst_9x) > 0:
            csv_name = "Выписка_по_диапазону_9xx.csv"
            self.__slected_numbers += self.__select_numbers(csv_name, lst_9x)

        if len(lst_3x) > 0:
            csv_name = "Выписка_по_диапазону_3xx.csv"
            self.__slected_numbers += self.__select_numbers(csv_name, lst_3x)

        if len(lst_4x) > 0:
            csv_name = "Выписка_по_диапазону_4xx.csv"
            self.__slected_numbers += self.__select_numbers(csv_name, lst_4x)

        if len(lst_8x) > 0:

            csv_name = "Выписка_по_диапазону_8xx.csv"
            self.__slected_numbers += self.__select_numbers(csv_name, lst_8x)

    def __select_numbers(self, csv_name, lst_in):
        csv_lst = self.__open_csv(csv_name)

        lst = []

        for number in lst_in:
            num = [number[:3], number[3:]]
            operator = ""
            region = ""
            for line in csv_lst:
                if line[0] == num[0] and line[1] <= num[1] and line[2] >= num[1]:
                    operator = line[4]
                    region = line[6]
                    break
            lst.append((number, operator, region))

        return lst

    def __open_csv(self, csv_name):
        with open(f"csv_data\{csv_name}", "r", encoding="utf-8") as file:
            return list(csv.reader(file, delimiter=";"))

    @property
    def select_result(self):
        return self.__slected_numbers

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

class Export:

    def __init__(self, lst_in):
        self.messsage_lst = lst_in

    def export_txt(self):
        path = self.__dir_path("txt")
        if len(path) == 0:
            return
    
        if not re.search(".+\.txt", path):
            path += ".txt"
        
        with open(path, "w+", encoding="utf-8") as file:
            for item in list(map(" ".join, self.messsage_lst)):
                file.write(f"{item}\n")

    def export_csv(self):
        path = self.__dir_path("csv")
        fieldnames = ("Номер телефона", "Оператор", "Регион")
        if len(path) == 0:
            return
    
        if not re.search(".+\.csv", path):
            path += ".csv"

        with open(path, "w+", encoding="utf-8", newline="") as file:
            file_writer = csv.writer(file, delimiter = ",")
            file_writer.writerow(fieldnames)
            for item in self.messsage_lst:
                file_writer.writerow(item)

    def __dir_path(self, exp):
        filetype = (("Файлы", f"*.{exp}"),)
        return fd.asksaveasfilename(title="Папка сохранения", initialdir="/", filetypes=filetype)

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("ОМТ Телефоны")
        self.resizable(width=False, height=True)

        EntryFrame(self).grid(row=0, column=0, padx=(30, 30), pady=20)


app = App()
app.mainloop()