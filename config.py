# -*- coding: utf-8 -*-

import ConfigParser


def loadconf():
    config = ConfigParser.SafeConfigParser()
    config.read('./config.ini')

    return dict(
            access_key_id=config.get('credentials', 'access_key_id'),
            secret_key=config.get('credentials', 'secret_key'),
            associate_tag=config.get('credentials', 'associate_tag'),
    )

if __name__ == "__main__":
    print loadconf()
