import csv, re
from tkinter import filedialog as fd


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