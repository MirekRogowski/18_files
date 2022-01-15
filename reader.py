import os
import sys
import csv
import json
import pickle # rb ,wb
import pathlib


class AbstractReader:

    ALLOWED_EXTENSIONS = ("json", "csv", "pickle")

    def __init__(self, filename, filepath=f"{os.getcwd()}"):
        self.filename = filename
        self.filepath = filepath
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

    def list_directory(self):
        # print(f"Brak pliku: {self.filename} w katalogu: {self.filepath}")
        for line in os.listdir(self.filepath):
            print(f"{line:55} file") if os.path.isfile(line) else print(f"{line:55} <DIR>")
        return exit()

    def new_values(self, new_value):
        for lista in new_value:
            item = lista.split(",")
            y = int(item[0].strip())
            x = int(item[1].strip())
            value = item[2].strip()
            self.file_data[y][x] = value

    def print_data(self):
        # print(self.filename)
        # print(self.filepath)
        print(self.file_data)
        print(type(self.file_data))
        # print(self.file_type)
        # print(self.validate)


class FileCsvReader(AbstractReader):
    def check_file(self):
        self.read_file() if not os.path.join(self.filepath, self.filename) else self.list_directory()

    def read_file(self):
        print(os.path.join(self.filepath, self.filename))
        with open(os.path.join(self.filepath, self.filename), newline="\n") as f:
        # with open(self.filename, newline="\n") as f:
            for line in csv.reader(f):
                self.file_data.append(line)


class FileJsonReader(AbstractReader):
    def read_file(self):
        with open(self.filename) as f:
            temp_data = json.load(f)
            self.file_data = json.loads(temp_data)


class FilePickleReader(AbstractReader):
    def read_file(self):
        with open(self.filename, "rb") as f:
            self.file_data = pickle.load(f)


class FileCsvWriter:
    def __init__(self, filename, file_date):
        self.filename = filename
        self.file_date = file_date

    def write_file(self):
        with open(self.filename, "w", newline="") as f:
            csv_writer = csv.writer(f)
            for line in self.file_date:
                csv_writer.writerow(line)


class FileJsonWriter:
    def __init__(self, filename, file_date):
        self.filename = filename
        self.file_date = file_date

    def write_file(self):
        json_string = json.dumps(self.file_date) #read from object open_csv
        with open(self.filename, "w") as f:
            json.dump(json_string, f)


class FilePickleWriter:
    def __init__(self, filename, file_date):
        self.filename = filename
        self.file_date = file_date

    def write_file(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.file_date, f)


def get_class_reader(file_name, file_path):
    suffix = pathlib.Path(file_name).suffix[1:]
    if suffix == "csv":
        return FileCsvReader(file_name, file_path)
    if suffix == "json":
        return FileJsonReader(file_name, file_path)
    if suffix == "pickle":
        return FilePickleReader(file_name, file_path)


def get_class_writer(file_name, file_date):
    suffix = pathlib.Path(file_name).suffix[1:]
    if suffix == "csv":
        return FileCsvWriter(file_name, file_date)
    if suffix == "json":
        return FileJsonWriter(file_name, file_date)
    if suffix == "pickle":
        return FilePickleWriter(file_name, file_date)

def print_test():
    print(sys.argv[1])
    print(sys.argv[2])
    print("_" * 50)
    print(pathlib.Path(sys.argv[1]).name)
    print("_" * 50)
    print(pathlib.Path(sys.argv[1]).is_absolute())
    print("_" * 50)
    print(pathlib.Path(sys.argv[1]).joinpath())
    print("_" * 50)
    print(pathlib.Path(sys.argv[1]))
    print("_" * 50)
    print(sys.argv[1].split(os.sep)[-1])
    print("_" * 50)
    print(os.path.dirname(sys.argv[1]))


file_name_reader = pathlib.Path(sys.argv[1]).name
file_path_reader = os.path.dirname(sys.argv[1])
file_name_writer = pathlib.Path(sys.argv[2]).name
file_path_writer = os.path.dirname(sys.argv[2])

fr = get_class_reader(file_name_reader, file_path_reader)
print(fr.filename, fr.filepath)
fr.check_file()
fr.print_data()

# data = json.loads(fr.file_data)
# data1 = list(data)
# print(data, type(data))
# print(data1, type(data1) )

fw = get_class_writer(file_name_writer, fr.file_data)
fw.write_file()
