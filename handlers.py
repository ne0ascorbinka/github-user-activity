from abc import ABCMeta, abstractmethod
from language import plural


class Handler(metaclass=ABCMeta):
    def __init__(self, repo: str) -> None:
        self.repo = repo

    @abstractmethod
    def from_event_dict(self, event: dict) -> None:
        pass

    @abstractmethod
    def handle(self) -> str:
        pass


class PushEventHandler(Handler):
    def __init__(self, repo: str, size: int) -> None:
        super().__init__(repo)
        self.size = size
    
    @classmethod
    def from_event_dict(cls, event: dict) -> None:
        repo = event['repo']['name']
        size = event['payload']['size']
        return cls(repo, size)

    
    def handle(self) -> str:
        return f'Pushed {self.size} {plural('commit', self.size)} to {self.repo}'


class IssuesEventHandler(Handler):
    def __init__(self, repo: str, action: str) -> None:
        super().__init__(repo)
        self.action = action
    
    @classmethod
    def from_event_dict(cls, event: dict) -> None:
        repo = event['repo']['name']
        action = event['payload']['action']
        return cls(repo, action)
    
    def handle(self) -> str:
        if self.action == 'opened':
            return f'Opened a new issue in {self.repo}'
        
        return f'{self.action.capitalize()} an issue in {self.repo}'


class WatchEventHandler(Handler):
    @classmethod
    def from_event_dict(cls, event: dict) -> None:
        repo = event['repo']['name']
        return cls(repo)
    
    def handle(self) -> str:
        return f'Starred {self.repo}'


class CommitCommentEventHandler(Handler):
    @classmethod
    def from_event_dict(cls, event: dict) -> None:
        repo = event['repo']['name']
        return cls(repo)
    
    def handle(self) -> str:
        return f'Commented on a commit in {self.repo}'


class CreateEventHandler(Handler):
    def __init__(self, repo: str, ref_type: str) -> None:
        super().__init__(repo)
        self.ref_type = ref_type
    
    @classmethod
    def from_event_dict(cls, event: dict) -> None:
        repo = event['repo']['name']
        ref_type = event['payload']['ref_type']
        return cls(repo, ref_type)
    
    def handle(self) -> str:
        if self.ref_type == 'repository':
            return f'Created repository {self.repo}'
        return f'Created a {self.ref_type} in {self.repo}'


HANDLERS_MAP = {
    'PushEvent': PushEventHandler,
    'IssuesEvent': IssuesEventHandler,
    'WatchEvent': WatchEventHandler,
    'CommitCommentEvent': CommitCommentEventHandler,
    'CreateEvent': CreateEventHandler,
}


def handler_factory(event: dict) -> Handler:
    event_type = event['type']
    if event_type in HANDLERS_MAP:
        return HANDLERS_MAP[event_type].from_event_dict(event)
    raise ValueError(f'Unsupported event type: {event_type}')