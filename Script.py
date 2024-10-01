# This code allows you to add many people to a group with ease, follow the steps below to get started

# 1) COPY PASTE THE ENTIRE CODE AND PASTE IT INTO GOOGLE COLLAB (https://colab.research.google.com/)

!pip install telethon

import asyncio
import time
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest

# The only changes you need to make are within the two asterisk lines below
# **********************************************************************************************************************************************

# 2) Replace api_id, api_hash, phone with your own values:
  # a) Log in to your Telegram core: https://my.telegram.org
  # b) Click on "API development tools" and fill out the form
  # c) Replace your api_id and api_hash required for user authorization below
  #  *** THIS ONLY NEEDS TO BE DONE ONCE, YOU CAN REUSE YOUR api_id & api_hash FOR AS OTHER GROUPS AND USERS) ***
api_id = '12345678'
api_hash = 'abcdefg123456hijklmnop7890123qrs'

# 3) replace your phone number in this format +6512345678
phone = '+6512345678'

# 4) Insert usernames here (with or without @ is okay)
csv = '''
    @insert_users_here
    @johnsmith
    jane_doe
    @michael_wilson
    '''
# 5) Insert the group chat link (e.g. https://t.me/+K3zmnN4sCjo1NWQ1)
group_link = 'https://t.me/insertlinkhere'

# 6) Insert your invite message here
my_invite_message = "Rewrite your invite message here"

# 7) Run the code in google collab when you have completed step 1 to step 6 by pressing the play button
# **********************************************************************************************************************************************

try:
    client.disconnect()
except:
    pass

try:
    client = TelegramClient(phone, api_id, api_hash)
except:
    pass

async def main():
    await client.connect()
    print('***connected***')
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            await client.sign_in(phone, input('Enter the code: '))
        except:
            password = input("Enter password: ")
            me = await client.sign_in(password=password)

    async def add_users_to_group_here(csv_file, group_link):
        users = []
        users_file = csv_file.split('\n')
        for user in users_file:
          while ' ' in user:
            user = user.replace(' ', '')
          if user != '':
            if user[0] != '@':
              user = '@' + user
            users.append(user)

        time.sleep(1)
        participants = await client.get_participants(group_link)
        group_members = []
        for participant in participants:
            group_members.append('@'+participant.username)

        for user in users:
            if user not in group_members:
                try:
                    user_to_add = await client.get_input_entity(user)
                    await client(InviteToChannelRequest(group_link, [user_to_add]))
                except Exception as e:
                    pass
        print('\nWait 5 seconds for the adding function to complete')
        time.sleep(5)
        print('Adding completed\n')
        participants = await client.get_participants(group_link)
        group_members = []
        for participant in participants:
            group_members.append('@'+participant.username)

        invalid = []
        sent_invite = []
        previously_sent_invte = []
        for user in users:
                try:
                    user_to_add = await client.get_input_entity(user)
                    if user not in group_members:
                        invite_message = my_invite_message + f"\n\n{group_link}"
                        past_ten_messages = await client.get_messages(user_to_add, 10)
                        sent = False
                        for message in past_ten_messages:
                            if message.message == invite_message:
                                sent = True
                        if not sent:
                            await client.send_message(user_to_add, invite_message)
                            sent_invite.append(user)
                        else:
                            previously_sent_invte.append(user)
                except Exception as e:
                    invalid.append(user)

        print(f'\nThe following users are currently in the group:\n{group_members}\n')
        print(f'\nThe following users have just been sent an invite link:\n{sent_invite}\n')
        print(f'\nThe following users have already been sent an invite link previously:\n{previously_sent_invte}\n')
        print(f'\nThese invalid usernames require your attention:\n{invalid}\n')

    await add_users_to_group_here(csv, group_link)

    await client.disconnect()
    print('***disconnected***')
await main()
