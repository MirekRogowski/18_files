import os
import sys
import csv
import json
import pickle # rb ,wb
import pathlib


class AbstractReader:

    ALLOWED_EXTENSIONS = ("json", "csv", "pickle")

    def __init__(self, file_path_src, new_values):
        self.file_path_src = file_path_src
        self.file_name_read = ""
        self.file_path_read = ""
        self.new_value = new_values
        self.file_data = []
        self.file_type = self.check_filetype()
        self.validate = self.validate()

    def check_filetype(self):
        return pathlib.Path(self.file_name_read).suffix[1:]

    def validate(self):
        if self.file_type not in AbstractReader.ALLOWED_EXTENSIONS:
            return False
        return True

    def check_directory(self):
        if os.path.isdir(self.file_path_read):
            print(f"W katalogu {self.file_path_read}  nie ma pliku {self.file_name_read}")
            for line in os.listdir(self.file_path_read):
               print(f"{line:55} file") if os.path.isfile(line) else print(f"{line:55} <DIR>")
        else:
            print(f"Nie ma katalogu {self.file_path_read}. Nie można odczytać pliku: {self.file_name_read}")

    def check_file(self):
        self.read_file() if os.path.isfile(self.file_path_src) else self.list_directory()

    def read_file_path(self):
        self.file_name_read = pathlib.Path(self.file_path_src).name
        if not os.path.dirname(self.file_path_src):
            self.file_path_read = os.getcwd()
        else:
            self.file_path_read = os.path.dirname(self.file_path_src)

    def new_values(self):
        for row in self.new_value:
            item = row.split(",")
            y = int(item[0].strip())
            x = int(item[1].strip())
            value = item[2].strip()
            self.file_data[y][x] = value

    def read_data(self):
        self.read_file_path()
        try:
            self.read_file()
            try:
                self.new_values()
            except:
                print("Brak danych do zmian")
        except:
            self.check_directory()


class FileCsvReader(AbstractReader):
    def read_file(self):
        with open(self.file_path_src, newline="\n") as f:
            for line in csv.reader(f):
                self.file_data.append(line)


class FileJsonReader(AbstractReader):
    def read_file(self):
        with open(self.file_path_src) as f:
            temp_data = json.load(f)
            self.file_data = json.loads(temp_data)


class FilePickleReader(AbstractReader):
    def read_file(self):
        with open(self.file_path_src, "rb") as f:
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

    def write_data(self):
        self.read_file_path()
        try:
            self.write_file()
        except:
            print(f"Nie ma katalogu {self.file_path_writer}. Nie można odczytać pliku: {self.file_name_writer}")


class FileCsvWriter(AbstractWriter):
    def write_file(self):
        with open(os.path.join(self.file_path_writer, self.file_name_writer), "w", newline="") as f:
            csv_writer = csv.writer(f)
            for line in self.file_date:
                csv_writer.writerow(line)


class FileJsonWriter(AbstractWriter):
    def write_file(self):
        json_string = json.dumps(self.file_date) #read from object open_csv
        with open(os.path.join(self.file_path_writer, self.file_name_writer), "w") as f:
            json.dump(json_string, f)


class FilePickleWriter(AbstractWriter):
    def write_file(self):
        with open(os.path.join(self.file_path_writer, self.file_name_writer), "wb") as f:
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


def read_file_path(file_path_dst):
    file_name_writer = pathlib.Path(file_path_dst).name
    if not os.path.dirname(file_path_dst):
        file_path_writer = os.getcwd()
    else:
        file_path_writer = os.path.dirname(file_path_dst)
    return file_path_writer, file_name_writer


def main():
    fr = get_class_reader(sys.argv[1], sys.argv[3:])
    fr.read_data()
    if fr.file_data or fr.new_value:
        fw = get_class_writer(sys.argv[2], fr.file_data)
        fw.write_data()
    else:
        print("Brak danych")


main()
