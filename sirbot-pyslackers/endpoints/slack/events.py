import os
import asyncio
import logging

from slack import methods
from slack.events import Message

LOG = logging.getLogger(__name__)
ANNOUCEMENTS_CHANNEL = os.environ.get('SLACK_ANNOUCEMENTS_CHANNEL') or 'annoucements'


def create_endpoints(plugin):
    plugin.on_event('team_join', team_join, wait=False)
    plugin.on_event('team_join', total_members, wait=False)


async def team_join(event, app):
    await asyncio.sleep(60)

    message = Message()
    message['text'] = f'''Welcome to the community <@{event["user"]["id"]}> :tada: !\n''' \
                      '''We are glad that you have decided to join us.\n\n''' \
                      '''We have documented a few things in the ''' \
                      '''<https://github.com/pyslackers/community/blob/master/introduction.md|intro doc> to help ''' \
                      '''you along from the beginning because we are grand believers in the Don't Repeat Yourself ''' \
                      '''principle, and it just seems so professional!\n\n''' \
                      '''If you wish you can tell us a bit about yourself in this channel.\n\n''' \
                      '''May your :taco:s be plentiful!'''

    message['channel'] = 'introductions'
    message['user'] = event['user']['id']

    await app.plugins['slack'].api.query(url=methods.CHAT_POST_EPHEMERAL, data=message)


async def total_members(event, app):
    LOG.debug('Calculating total members')
    total_users = 0
    async for user in app.plugins['slack'].api.iter(url=methods.USERS_LIST, minimum_time=15):
        if not user['is_bot'] and not user['deleted']:
            total_users += 1

    if total_users and total_users % 1000 == 0:
        message = Message()
        message['channel'] = ANNOUCEMENTS_CHANNEL
        message['text'] = f''':tada: Everyone give a warm welcome to <@{event['user']['id']}>  our {total_users} ''' \
                          '''members ! :tada:'''
        await app.plugins['slack'].api.query(url=methods.CHAT_POST_MESSAGE, data=message)
    LOG.debug("There is %s members", total_users)
