import os
import importlib
import inspect
import json
import logging
import skype.skype_connect as sk_conn


class ModuleLoader:
    instance = None

    def __init__(self):
        self.has_loaded = False
        self.module_root = "modules"
        self.unnamed_count = 0
        self.modules = {}

        ModuleLoader.instance = self

    def load(self):
        logger = logging.getLogger("SkyModules")
        sk_instance = sk_conn.SkypeConnector.get_instance()

        for file in os.listdir("modules"):
            if file == "__pycache__":
                continue

            try:
                with open(self.module_root + "/" + file + "/index.json") as index_file:
                    index = json.load(index_file)
                    main_file = index["main_file"]
            except FileNotFoundError:
                logger.error("index.json for " + file + " not found")
                continue

            imported = importlib.import_module(self.module_root + "." + file + "." + main_file.split(".")[0])
            class_obj = inspect.getmembers(imported)[0][1]

            instance = class_obj.get_instance()
            try:
                instance.set_info(index["module_name"], index["author"], index["last_update"], index["version"])
            except KeyError:
                logger.error("index file for " + file + " may be corrupted")
                continue

            if instance.name is None:
                instance.name = "unnamed_module_" + str(self.unnamed_count + 1)     # TODO maybe remove

            if sk_instance is not None:
                instance.set_skype(sk_instance)

            self.modules.update({instance.name: instance})
        self.has_loaded = True

    def get_module(self, name):
        try:
            module = self.modules[name]
        except KeyError as err:
            logger = logging.getLogger("SkyModules")
            logger.warning(err)
            return None
        return module

    def list_modules(self):
        for mod_name in self.modules:
            print("- ", mod_name, " loaded")
