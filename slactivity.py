import argparse
import requests


SLACK_API_URL = "https://slack.com/api"


class SlactivityGenerator:
    def __init__(self, token):
        self._token = token

    def get_channels(self):
        data = self._get_slack_data('channels.list', 'exclude_archived=true')
        return data['channels']

    def _get_slack_data(self, method, *api_args):
        url = '{}/{}?token={}'.format(SLACK_API_URL, method, self._token)
        for arg in api_args:
            url += '&' + arg

        r = requests.get(url)
        r.raise_for_status()

        return r.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the last message date for all slack channels')
    parser.add_argument('token', type=str, help='slack api token')
    args = parser.parse_args()

    generator = SlactivityGenerator(args.token)
    channels = generator.get_channels()

    for channel in channels:
        print(channel['name'])
