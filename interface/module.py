from abc import ABC, abstractmethod


class Module(ABC):
    instances = []    # list of all instances

    def __init__(self):
        super().__init__()
        self.cmd_map = {}    # (str)name : (func)function
        self.name = None
        self.version = None
        self.author = None
        self.update = None
        self.skype = None
        self.current_event = None
        self.needs_skype = True
        Module.instances.append(self)

        self.register_cmd("help", self.help)
        self.register_cmd("info", self.get_info)

    @staticmethod
    def get_instance():
        pass

    @abstractmethod
    def help(self):
        pass

    def set_event(self, event):
        self.current_event = event

    def get_info(self):
        print("\nName: " + self.name + "\nAuthor: " + self.author
              + "\nLast Update: " + self.update + "\nVersion: " + self.version)
        return "\nName: " + self.name + "\nAuthor: " + self.author \
               + "\nLast Update: " + self.update + "\nVersion: " + self.version

    def set_info(self, name, author, update, version):
        self.name = name
        self.author = author
        self.update = update
        self.version = version

    def set_name(self, name):
        self.name = name

    def set_skype(self, skype):
        self.skype = skype

    def register_cmd(self, cmd, func):
        self.cmd_map.update({cmd: func})

    def exec(self, cmd, arg=None):
        func = self.cmd_map[cmd]

        if arg is None:
            return func()
        elif hasattr(arg, "__iter__"):  # is iterable
            return func(*arg)
        else:
            return func(arg)

