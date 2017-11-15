import time
import argparse
import requests


SLACK_API_URL = "https://slack.com/api"
RATE_LIMIT_SECONDS = 1


class SlactivityGenerator:
    def __init__(self, token):
        self._token = token
        self._last_slack_request = 0

    def get_last_message(self, channel_id):
        data = self._get_slack_data('conversations.history', 'channel={}'.format(channel_id))
        messages = data['messages']

        # find the first message which is an actual message (e.g. not a user leaving event)
        for message in messages:
            # we're only interested in a posted message, which will not have a subtype
            if 'subtype' not in message:
                return message

        return None

    def get_channels(self):
        data = self._get_slack_data('channels.list', 'exclude_archived=true')
        return data['channels']

    def _get_slack_data(self, method, *api_args):
        url = '{}/{}?token={}'.format(SLACK_API_URL, method, self._token)
        for arg in api_args:
            url += '&' + arg

        # wait for the rate limit seconds to pass between successive queries
        while time.time() < self._last_slack_request + RATE_LIMIT_SECONDS:
            time.sleep(.1)  # throttle the loop

        self._last_slack_request = time.time()
        r = requests.get(url)
        r.raise_for_status()

        return r.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the last message date for all slack channels')
    parser.add_argument('token', type=str, help='slack api token')
    args = parser.parse_args()

    generator = SlactivityGenerator(args.token)

    # print the date of the last message in each channel
    channels = generator.get_channels()
    for channel in channels:
        msg = generator.get_last_message(channel['id'])

        # if no message was ever posted, use the creation date of the channel
        msg_ts = float(msg['ts']) if msg else float(channel['created'])
        msg_date = time.strftime('%Y-%m-%d', time.gmtime(msg_ts))

        print('{},{}'.format(channel['name'], msg_date))
