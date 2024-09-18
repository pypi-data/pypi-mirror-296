class Colors:
    cyan = "\033[0;36m"
    white = "\033[0;37m"
    reset = "\033[0m"


c = Colors()


def pretty_print(key, value):
    if isinstance(value, dict):
        if len(value) == 0:
            print(f"{c.white}{key}: {{}}{c.reset}")
        else:
            print(f"{c.white}{key}: {{{c.reset}")
            for k, v in value.items():
                print(f'    {c.cyan}"{k}": {c.reset}"{v}",')
            print(f"{c.white}}}{c.reset}")
    else:
        print(f"{c.white}{key}:", f"{c.cyan}{value}{c.reset}")
