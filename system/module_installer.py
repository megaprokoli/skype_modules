import zipfile
import json
import os


class ModuleInstaller:
    tmp_dir = "tmp"
    mod_dir = "modules"

    def __init__(self, file_msg):
        self.file_msg = file_msg

        file_info = self.file_msg.file.name.split('.')
        self.mod_name = file_info[0]  # TODO if . in filename
        self.extension = file_info[-1]
        self.tmp_path = "{}/{}".format(self.tmp_dir, self.file_msg.file.name)

    def validate(self):

        if self.extension != "zip":
            return False

        with open(self.tmp_path, "wb+") as file:
            file.write(self.file_msg.fileContent)

        with zipfile.ZipFile(self.tmp_path, 'r') as zf:
            namelist = zf.namelist()
            index_location = "{}/index.json".format(self.mod_name)

            if index_location not in namelist:
                return False

            index_file = json.loads(zf.read(index_location).decode(), encoding="utf-8")

            try:
                if "{}/{}".format(self.mod_name, index_file["main_file"]) not in namelist:
                    return False
            except KeyError:
                return False

            return True

    def install(self):
        with zipfile.ZipFile(self.tmp_path, 'r') as zf:
            zf.extractall(self.mod_dir)

        self.clear_tmp()

    @staticmethod
    def clear_tmp():
        for f in os.listdir(ModuleInstaller.tmp_dir):
            os.remove("{}/{}".format(ModuleInstaller.tmp_dir, f))
