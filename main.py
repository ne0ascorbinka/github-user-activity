import requests
import sys
from handlers import handler_factory


SUPPORTED_EVENTS = [
    'PushEvent',
    'IssuesEvent',
]

def main() -> None:
    username = sys.argv[1]
    url = f'https://api.github.com/users/{username}/events'
    data = list(filter(lambda event: event['type'] in SUPPORTED_EVENTS, requests.get(url).json()))
    print('Output:')
    for event in data:
        handler = handler_factory(event)
        print('- ' + handler.handle())

if __name__ == '__main__':
    main()
