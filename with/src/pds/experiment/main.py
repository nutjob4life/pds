# encoding: utf-8

import pds.api_client


def main():
    print('👋 Hello from namespaced pds')
    print(f'📖 The contents of `pds.api_client` is {", ".join(dir(pds.api_client))}')


if __name__ == '__main__':
    main()
