import requests, bs4, datetime, json, os


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