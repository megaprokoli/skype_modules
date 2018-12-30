
def is_command(cmd):
    if cmd[0] == '!' and '!' not in cmd[1:]:
        return True
    else:
        return False


def parse(cmd):
    if not is_command(cmd):
        return None

    split_cmd = cmd.split('!')[1]
    split_cmd = split_cmd.split(' ')

    if len(split_cmd) < 2:
        return split_cmd[0], split_cmd[1], None
    return split_cmd[0], split_cmd[1], split_cmd[2:]
