import os
import sys
import csv
import json
import pickle # rb ,wb
import pathlib


class AbstractReader:

    ALLOWED_EXTENSIONS = ("json", "csv", "pickle")

    def __init__(self, filename, filepath=f"{os.getcwd()}"):
        print("create object")
        self.filename = filename
        self.filepath = filepath
        # self.filepath_new =
        self.file_data = []
        self.file_type = self.check_filetype()
        self.validate = self.validate()

    def check_filetype(self):
        return pathlib.Path(self.filename).suffix[1:]

    def validate(self):
        if self.file_type not in AbstractReader.ALLOWED_EXTENSIONS:
            return False
        return True

    def get_filepath(self):
        if self.filepath:
            return os.path.join(self.filepath, self.filename)
        return self.filename

    def check_file(self):
        self.open_file() if os.path.exists(self.filename) else self.list_directory()

    def list_directory(self):
        print(f"Brak pliku: {self.filename} w katalogu: {self.filepath}")
        for line in os.listdir(self.filepath):
            print(f"{line:55} file") if os.path.isfile(line) else print(f"{line:55} <DIR>")
        return exit()

    def new_values(self, new_value):
        for lista in new_value:
            item = lista.split(",")
            print(item)
            y = int(item[0].strip())
            x = int(item[1].strip())
            value = item[2].strip()
            print(value)
            self.file_data[y][x] = value

    def print_data(self):
        print(self.filename)
        print(self.filepath)
        print(self.file_data)
        print(self.file_type)
        print(self.validate)


class FileCsv(AbstractReader):
    # def __init__(self, filename, filepath=""):
    #     super.__init__(filename, filepath)
        # print(super.__init__(filename, filepath))

    def open_file(self):
        with open(self.filename, newline="\n") as f:
            for line in csv.reader(f):
                self.file_data.append(line)

    def write_file(self):
        t = input("\nZapisac dane do pliku: (T/N)? ")
        if t.lower() == "t":
            with open("test.csv", "w", newline="") as f:
                csv_writer = csv.writer(f)
                for line in self.file_data:
                    csv_writer.writerow(line)
            print(f"\nDane zapisane w pliku: ")
        else:
            print("\nNie zapisano zmian")
            exit()


class FileJson(AbstractReader):

    def write_file(self):
        json_string = json.dumps(open_csv.file_data) #read from object open_csv
        with open(self.filename, "w") as f:
            json.dump(json_string, f)

    def read_file(self):
        # print("funkcja read_from_json_file ")
        with open(self.filename) as f:
            self.file_data = json.load(f)


        # response = requests.request("GET", url, headers=headers, params=querystring)
        # out_url = response.json()
        # with open("out.json", 'w') as json_file:
        #     json.dump(out_url, json_file)




        # t = input("\nZapisac dane do pliku: (T/N)? ")
        # json_object = json.dump(self.file_data)
        # if t.lower() == "t":
        #     with open(self.filename, "w") as f:
        #         f.write(json_object)
        #     print(f"\nDane zapisane w pliku: ")
        # else:
        #     print("\nNie zapisano zmian")
        #     exit()


    # with open("out.json", 'w') as json_file:
    #     json.dump(out_url, json_file)
    #


    # def read_from_csv_file(self):
    #     with open("data.csv", newline='') as f:
    #         reader = csv.reader(f)
    #         for i in reader:
    #             self.file_data.append([i[0], i[1]])


# abstract = AbstractReader("data.txt")
# print(abstract.file_type)
# print(abstract.validate)
# file = pathlib.Path("c:\tool\data.csv")
# print(file.suffix)
# print(file.name)
# print(file.parts)
open_csv = FileCsv("data.csv")
open_csv.check_file()
# open_csv.print_data()
print(sys.argv[1:])
open_csv.new_values(sys.argv[1:])
open_csv.print_data()
open_csv.write_file()

open_json = FileJson("data.json")
open_json.write_file()
open_json.print_data()
print("reda file")
open_json.read_file()
open_json.print_data()
