from skpy import SkypeEventLoop
from skpy import SkypeNewMessageEvent
from skpy.msg import SkypeFileMsg
import system.cmd_parsing as parsing
from system import module_loader as loader
from system import module_installer as installer
import logging


class InputHandler(SkypeEventLoop):

    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent) and not event.msg.userId == self.userId:
            logger = logging.getLogger("SkyModules")
            msg = event.msg.content

            logger.debug("received " + str(type(event.msg)))

            if isinstance(event.msg, SkypeFileMsg):
                result = self.__handle_file(event)
                event.msg.chat.sendMsg(result)
                return

            if not self.__user_authorized(event.msg.userId):
                logger.warning("unauthorized access from " + event.msg.userId)
                return

            if parsing.is_command(msg):
                (module, command, args) = parsing.parse(msg)  # TODO handle list index

                mod_loader = loader.ModuleLoader.instance   # TODO bad design
                mod = mod_loader.get_module(module)

                if mod is None:
                    event.msg.chat.sendMsg("ERROR: module " + module + " or  function " + command + " not found!")
                    logger.error("module " + module + " or  function " + command + " not found!")
                else:
                    mod.set_event(event)

                    try:
                        resp = mod.exec(command, arg=args)
                    except Exception as err:
                        resp = "Some Exception occured in " + mod.name + "!\n" + str(err)

                    event.msg.chat.sendMsg(resp)
                    logger.info("send response")

    def __handle_file(self, event):
        inst = installer.ModuleInstaller(event.msg)

        if not inst.validate():
            return "provided file is no valid module!"

        try:
            inst.install()
        except Exception as err:
            return "failed to install module\n" + str(err)
        else:
            return "Module successfully installed. Please restart your bot to use it."

    def __user_authorized(self, user_name):
        with open("auth_users.txt") as auth_list:

            for user in auth_list:
                if user.split("\n")[0] == user_name:
                    return True
            return False
