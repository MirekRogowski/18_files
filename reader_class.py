import os
import sys
import csv
import json
import pickle  # rb ,wb
import pathlib


class AbstractPathToFile:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.file_name = ""
        self.path_directory = ""

    def read_name_file_and_path(self):
        self.file_name = pathlib.Path(self.path_to_file).name
        if not os.path.dirname(self.path_to_file):
            self.path_directory = os.getcwd()
        else:
            self.path_directory = os.path.dirname(self.path_to_file)

    def check_directory(self):
        if os.path.isdir(self.path_directory):
            print(f"W katalogu {self.path_directory}  nie ma pliku {self.file_name}")
            for line in os.listdir(self.path_directory):
               print(f"{line:55} file") if os.path.isfile(line) else print(f"{line:55} <DIR>")
        else:
            print(f"Nie ma katalogu {self.path_directory}. Nie można odczytać pliku: {self.file_name}")


class AbstractReader(AbstractPathToFile):
    def __init__(self, path_to_file, new_values):
        super().__init__(path_to_file)
        self.new_value = new_values
        self.file_data = []

    def new_values(self):
        for row in self.new_value:
            item = row.split(",")
            y = int(item[0].strip())
            x = int(item[1].strip())
            value = item[2].strip()
            self.file_data[y][x] = value

    def read_data(self):
        self.read_name_file_and_path()
        try:
            self.read_file()
            self.new_values()
        except:
            self.check_directory()


class FileCsvReader(AbstractReader):
    def read_file(self):
        with open(str(self.path_to_file), newline="\n") as f:
            for line in csv.reader(f):
                self.file_data.append(line)

class FileJsonReader(AbstractReader):
    def read_file(self):
        with open(self.path_to_file) as f:
            temp_data = json.load(f)
            self.file_data = json.loads(temp_data)


class FilePickleReader(AbstractReader):
    def read_file(self):
        with open(self.path_to_file, "rb") as f:
            self.file_data = pickle.load(f)


class AbstractWriter(AbstractPathToFile):
    def __init__(self, path_to_file,  file_date):
        super().__init__(path_to_file)
        self.file_date = file_date

    def write_data(self):
        self.read_name_file_and_path()
        try:
            self.write_file()
        except:
            print(f"Nie ma katalogu {self.file_path}. Nie można odczytać pliku: {self.file_name}")


class FileCsvWriter(AbstractWriter):
    def write_file(self):
        with open(self.path_to_file, "w", newline="") as f:
            csv_writer = csv.writer(f)
            for line in self.file_date:
                csv_writer.writerow(line)


class FileJsonWriter(AbstractWriter):
    def write_file(self):
        json_string = json.dumps(self.file_date) #read from object open_csv
        with open(self.path_to_file, "w") as f:
            json.dump(json_string, f)


class FilePickleWriter(AbstractWriter):
    def write_file(self):
        with open(self.path_to_file, "wb") as f:
            pickle.dump(self.file_date, f)


def get_class_reader(file_path_src, args):
    suffix = pathlib.Path(file_path_src).suffix[1:]
    if suffix == "csv":
        return FileCsvReader(file_path_src, args)
    if suffix == "json":
        return FileJsonReader(file_path_src, args)
    if suffix == "pickle":
        return FilePickleReader(file_path_src, args)


def get_class_writer(file_path_dst, file_date):
    suffix = pathlib.Path(file_path_dst).suffix[1:]
    if suffix == "csv":
        return FileCsvWriter(file_path_dst, file_date)
    if suffix == "json":
        return FileJsonWriter(file_path_dst, file_date)
    if suffix == "pickle":
        return FilePickleWriter(file_path_dst, file_date)

def main():
    fr = get_class_reader(sys.argv[1], sys.argv[3:])
    fr.read_data()
    fw = get_class_writer(sys.argv[2], fr.file_data)
    fw.write_data()

main()
