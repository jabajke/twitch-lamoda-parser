from enum import Enum


class TwitchTypes(tuple, Enum):
    game = ('game', 'games')
    stream = ('stream', 'streams')
    streamer = ('streamer', 'streamers')
