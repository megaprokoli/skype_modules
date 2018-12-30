import interface.module as mod


class Info(mod.Module):

    def __init__(self):
        super().__init__()

        self.register_cmd("ls", self.list_modules)

    @staticmethod
    def get_instance():
        return Info()

    def help(self):
        return "ls - list all loaded modules"

    def list_modules(self):
        output = ""

        for module in self.instances:
            output += module.name + "\n\tAuthor: " + module.author + "\n\tVersion: " + module.version + "\n\tLast Update: " + module.update + "\n"

        return output
