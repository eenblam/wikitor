from wikitor.wikiproxy import WikiProxy
from wikitor.logcolors import *
import stem.process

if __name__ == '__main__':
    SOCKS_PORT = 7000
    wikihow = 'https://www.wikihow.com/api.php'
    proxy = WikiProxy(wikihow, SOCKS_PORT)
    try:
        process = stem.process.launch_tor_with_config(
                config = {
                    'SocksPort': str(SOCKS_PORT),
                },
                init_msg_handler=print_bootstrap_lines)
        for title in proxy.titles_from_query('sewing'):
            log_green('\t' + title)
    finally:
        log_red("Killing Tor process")
        process.kill()
