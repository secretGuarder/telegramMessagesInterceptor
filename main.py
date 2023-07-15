"""

"""
import os
from Interceptor import Interceptor
from Banner import banner


def get_path():
    default_path = 'saved_data/'
    user_path = input('[-] Enter path for saving data (Enter <d> to use default): ')
    if user_path == 'd':
        print(f'[*] Used default path {default_path}')
        return default_path
    else:
        if os.path.exists(user_path):
            print(f'[*] Set path {user_path}')
            return user_path
        else:
            res = (f'[!] Incorrect path {user_path}, try again of use default {default_path}(y/n):')
            if res == 'y':
                get_path()
            elif res == 'n':
                print(f'[*] Used default path {default_path}')
                return default_path
            else:
                print(f'[!] Incorrect answer! Try again!')
                get_path()


if __name__ == "__main__":
    try:
        print('')
        print(banner)
        print("\033[0;34m")

        default_path = get_path()
        print('[-] Starting...')

        Interceptor().run(default_path)
    except KeyboardInterrupt:
        print("\n[!] Stoped by user\n\033[0m")

