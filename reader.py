import os
import sys
import csv
import json
import pickle # rb ,wb
import pathlib


class AbstractReader:

    ALLOWED_EXTENSIONS = ("json", "csv", "pickle")

    def __init__(self, file_path_dst):
        self.file_path_dst = file_path_dst
        self.file_name_read = ""
        self.file_path_read = ""
        self.file_data = []
        self.file_type = self.check_filetype()
        self.validate = self.validate()

    def check_filetype(self):
        return pathlib.Path(self.filename).suffix[1:]

    def validate(self):
        if self.file_type not in AbstractReader.ALLOWED_EXTENSIONS:
            return False
        return True

    def list_directory(self):
        if os.path.isdir(self.):
            for line in os.listdir(self.filepath):
                print(f"{line:55} file") if os.path.isfile(line) else print(f"{line:55} <DIR>")
        else:
            print(f"Brak katalogu {self.filepath}")

    def check_file(self):
        self.read_file() if os.path.isfile(self.filepath+os.sep+self.filename) else self.list_directory()

    def read_file_path(self):
        self.file_name_read = pathlib.Path(self.file_path_dst).name
        if not os.path.dirname(self.file_path_dst):
            self.file_path_read = os.getcwd()
        else:
            self.file_path_read = os.path.dirname(self.file_path_dst)

    def new_values(self, new_value):
        for lista in new_value:
            item = lista.split(",")
            y = int(item[0].strip())
            x = int(item[1].strip())
            value = item[2].strip()
            self.file_data[y][x] = value



    def print_data(self):
        print(self.file_name_read)
        print(self.file_path_read)
        print(self.file_data, type(self.file_data))
        # print(self.file_type)
        # print(self.validate)


class FileCsvReader(AbstractReader):
    def read_file(self):
        # print(os.path.join(self.filepath, self.filename))
        with open(os.path.join(self.filepath, self.filename), newline="\n") as f:
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


class AbstractWriter:
    def __init__(self, file_path_dst, file_date):
        self.file_path_dst = file_path_dst
        self.file_date = file_date
        self.file_name_writer = ""
        self.file_path_writer = ""

    def read_file_path(self):
        self.file_name_writer = pathlib.Path(self.file_path_dst).name
        if not os.path.dirname(self.file_path_dst):
            self.file_path_writer = os.getcwd()
        else:
            self.file_path_writer = os.path.dirname(self.file_path_dst)

    def write_file_path(self):
        self.read_file_path()
        try:
            self.write_file()
        except:
            print(f"Brak katalogu {self.file_path_writer} by zapisać plik: {self.file_name_writer}")

    def print_data(self):
        print(self.file_path_dst)
        print(self.file_date)
        print(self.file_name_writer)
        print(self.file_path_writer)


class FileCsvWriter(AbstractWriter):
    def write_file(self):
        with open(os.path.join(self.file_path_writer, self.file_name_writer), "w", newline="") as f:
            csv_writer = csv.writer(f)
            for line in self.file_date:
                csv_writer.writerow(line)


class FileJsonWriter(AbstractWriter):
    def write_file(self):
        json_string = json.dumps(self.file_date) #read from object open_csv
        with open(self.file_path_writer, "w") as f:
            json.dump(json_string, f)


class FilePickleWriter(AbstractWriter):
    def write_file(self):
        with open(self.file_path_writer, "wb") as f:
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


def read_file_path(file_path_dst):
    file_name_writer = pathlib.Path(file_path_dst).name
    if not os.path.dirname(file_path_dst):
        file_path_writer = os.getcwd()
    else:
        file_path_writer = os.path.dirname(file_path_dst)
    return file_path_writer, file_name_writer


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
if not os.path.dirname(sys.argv[1]):
    file_path_reader = os.getcwd()
else:
    file_path_reader = os.path.dirname(sys.argv[1])

# file_name_writer = pathlib.Path(sys.argv[2]).name
# if not os.path.dirname(sys.argv[2]):
#     file_path_writer = os.getcwd()
# else:
#     file_path_writer = os.path.dirname(sys.argv[2])



fr = get_class_reader(file_name_reader, file_path_reader)
# print(fr.filename, fr.filepath)
fw.read_file_path()
fr.check_file()
fr.print_data()

# data = json.loads(fr.file_data)
# data1 = list(data)
# print(data, type(data))
# print(data1, type(data1) )

fw = get_class_writer(sys.argv[2], fr.file_data)
fw.write_file_path()
