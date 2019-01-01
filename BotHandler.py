import requests
import json
from collections import deque


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.url = "https://api.telegram.org/bot{}/".format(token)
        self.updates = deque()

    # API methods:
    def get_updates(self, offset=None, timeout=10):
        method, params = 'getUpdates', {'offset': offset,
                                        'timeout': timeout}
        response = deque(requests.get(self.url + method, params).json()['result'])
        return response

    def get_last_update(self, offset=None, timeout=10):
        if len(self.updates) == 0:
            self.updates = self.get_updates(offset=offset, timeout=timeout)
        return self.updates.popleft() if len(self.updates) > 0 else None

    def send_message(self, chat_id, text, reply_to_message_id=None, parse_mode=None):
        method, params = 'sendMessage', {'chat_id': chat_id,
                                         'text': text,
                                         'reply_to_message_id': reply_to_message_id,
                                         'parse_mode': parse_mode}
        response = requests.post(self.url + method, data=params)
        return response

    def get_admins(self, chat_id):
        method, params = 'getChatAdministrators', {'chat_id': chat_id}
        response = json.loads(requests.post(self.url + method, data=params).text)
        admins = [x['user']['id'] for x in response['result']] if response['ok'] else []
        return admins

    def get_member(self, chat_id, user_id):
        method, params = 'getChatMember', {'chat_id': chat_id, 'user_id': user_id}
        response = requests.post(self.url + method, data=params)
        return json.loads(response.text)

    def restrict_member(self, chat_id, user_id, until_date,
                        can_send_messages=None, can_send_media_messages=None,
                        can_send_other_messages=None, can_add_web_page_previews=None):
        method, params = 'restrictChatMember', {'chat_id': chat_id,
                                                'user_id': user_id,
                                                'until_date': until_date,
                                                'can_send_messages': can_send_messages,
                                                'can_send_media_messages': can_send_media_messages,
                                                'can_send_other_messages': can_send_other_messages,
                                                'can_add_web_page_previews': can_add_web_page_previews}
        response = requests.post(self.url + method, data=params)
        return response

    def promote_member(self, chat_id, user_id,
                       can_change_info=False, can_post_messages=False,
                       can_edit_messages=False, can_delete_messages=False,
                       can_invite_users=False, can_restrict_members=False,
                       can_pin_messages=False, can_promote_members=False):
        method, params = 'promoteChatMember', {'chat_id': chat_id,
                                               'user_id': user_id,
                                               'can_change_info': can_change_info,
                                               'can_post_messages': can_post_messages,
                                               'can_edit_messages': can_edit_messages,
                                               'can_delete_messages': can_delete_messages,
                                               'can_invite_users': can_invite_users,
                                               'can_restrict_members': can_restrict_members,
                                               'can_pin_messages': can_pin_messages,
                                               'can_promote_members': can_promote_members}
        response = requests.post(self.url + method, data=params)
        return response
