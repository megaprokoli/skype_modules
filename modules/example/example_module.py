import interface.module as mod
from modules.example import another_test


class ExampleModule(mod.Module):

    def __init__(self):
        super().__init__()

        self.register_cmd("ls", self.list_modules)
        self.register_cmd("one", self.return_val)
        self.register_cmd("single", self.single_arg)
        self.register_cmd("multi", self.multi_arg)
        self.register_cmd("class", another_test.AnotherTest.do_something)

    @staticmethod
    def get_instance():
        return ExampleModule()

    def help(self):
        print("help info")
        return "help info"

    def multi_arg(self, arg1, arg2):
        print("multi arg: ", arg1, " - ", arg2)
        return "multi arg: " + arg1 + " - " + arg2

    def single_arg(self, arg):
        print("single arg: ", arg)
        return "single arg: " + arg

    def return_val(self):
        return "return value"

    def list_modules(self):
        print(mod.Module.instances)
        return mod.Module.instances

