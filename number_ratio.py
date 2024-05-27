import csv


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
