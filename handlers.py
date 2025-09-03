from abc import ABCMeta, abstractmethod
from language import plural


class Handler(metaclass=ABCMeta):
    @abstractmethod
    def from_event_dict(self, event: dict) -> None:
        pass

    @abstractmethod
    def handle(self) -> str:
        pass


class PushEventHandler(Handler):
    def __init__(self, repo: str, size: int) -> None:
        self.repo = repo
        self.size = size
    
    @classmethod
    def from_event_dict(cls, event: dict) -> None:
        repo = event['repo']['name']
        size = event['payload']['size']
        return cls(repo, size)

    
    def handle(self) -> str:
        return f'Pushed {self.size} {plural('commit', self.size)} to {self.repo}'


HANDLERS_MAP = {
    'PushEvent': PushEventHandler,
}


def handler_factory(event: dict) -> Handler:
    event_type = event['type']
    if event_type in HANDLERS_MAP:
        return HANDLERS_MAP[event_type].from_event_dict(event)
    raise ValueError(f'Unsupported event type: {event_type}')