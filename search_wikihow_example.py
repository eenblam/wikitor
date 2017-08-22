from wikitor import pages, wikiproxy
from wikitor.logcolors import *
import stem.process

if __name__ == '__main__':
    wikihow = 'https://www.wikihow.com/api.php'
    # Be sure to run `schema.py sewing`
    db = pages.Pages('sewing.db', 'sewing')

    SOCKS_PORT = 7000
    proxy = wikiproxy.WikiProxy(wikihow, SOCKS_PORT)

    try:
        process = stem.process.launch_tor_with_config(
                config = {
                    'SocksPort': str(SOCKS_PORT),
                },
                init_msg_handler=print_bootstrap_lines)
        for pageid, title, content in proxy.gen_from_query('sewing'):
            db.add_pages(title, content)
            log_green('Stashed article: {}'.format(title))
    finally:
        log_red("Killing Tor process")
        process.kill()
