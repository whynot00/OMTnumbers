from support_func import encode, removing_excess


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