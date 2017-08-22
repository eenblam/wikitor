from stem.util import term
def log_blue(line):
    print(term.format(line, term.Color.BLUE))

def log_red(line):
    print(term.format(line, term.Color.RED))

def log_green(line):
    print(term.format(line, term.Color.GREEN))

def print_bootstrap_lines(line):
    if "Bootstrapped" in line:
        log_blue(line)
