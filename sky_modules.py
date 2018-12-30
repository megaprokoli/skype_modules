import system.module_loader as loader
import system.module_installer as installer
import system.cmd_parsing as parser
import skype.skype_connect as skcon
import sys
import argparse
import getpass
import logging


def run_terminal_mode():

    while True:
        user_input = input("\nenter cmd: ")

        if user_input == "exit":
            return

        if not parser.is_command(user_input):
            print("ERROR: enter a ! before any command.", end=" ")
            print("(Note: commands can't contain any !)")
            continue

        try:
            (module, command, args) = parser.parse(user_input)

            mod = mod_loader.get_module(module)

            if mod is None:
                print("ERROR: module " + module + " or  function " + command + " not found!")
                continue

            mod.exec(command, arg=args)

        except TypeError as err:
            print("ERROR: " + str(err))
            continue

if __name__ == "__main__":
    argp = argparse.ArgumentParser(description="A small tool to parse commands over Skype that can be implemented as module.")
    argp.add_argument("-d", "--debug", required=False, help="enable debug mode", action="store_true")
    argp.add_argument("-t", "--terminal", required=False, help="enable terminal mode for testing without skype", action="store_true")
    argp.add_argument("-n", "--name", required=False, help="your skype name")
    argp.add_argument("-p", "--pwd", required=False, help="your skype password")
    args = vars(argp.parse_args())

    if args["debug"]:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger("SkyModules")
    log_handler = logging.FileHandler("events.log")
    log_handler.setLevel(logging.DEBUG)
    logger.addHandler(log_handler)

    if args["name"] is None:
        sk_name = input("Enter Skype name: ")
    else:
        sk_name = args["name"]

    if args["pwd"] is None:
        sk_pwd = getpass.getpass("Enter Skype password: ")
    else:
        sk_pwd = args["pwd"]

    installer.ModuleInstaller.clear_tmp()   # clear temporary directory

    skype = skcon.SkypeConnector(sk_name, sk_pwd)

    if not args["terminal"]:    # prevent unnecessary skype connect
        skype.connect()

    mod_loader = loader.ModuleLoader()
    mod_loader.load()
    mod_loader.list_modules()
    logger.info("modules loaded")

    if args["terminal"]:
        logger.info("entering terminal mode")
        run_terminal_mode()
        print("Good Bye")
        sys.exit(0)

    try:
        logger.info("entering event loop")
        skype.run()
    except KeyboardInterrupt:
        # TODO cleanup

        print("Good Bye")
