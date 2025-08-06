"""Basic live shopping stream system."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Stream:
    stream_id: str
    streamer_id: str
    shopping_goal: str
    viewers: List[str] = field(default_factory=list)
    donations: Dict[str, int] = field(default_factory=dict)
    votes: Dict[str, str] = field(default_factory=dict)
    active: bool = True


class LiveShoppingStream:
    """Simplified live streaming management."""

    def __init__(self) -> None:
        self._streams: Dict[str, Stream] = {}
        self._balances: Dict[str, int] = {}

    def start_stream(self, user_id: str, shopping_goal: str) -> Stream:
        stream_id = f"stream-{len(self._streams) + 1}"
        stream = Stream(stream_id=stream_id, streamer_id=user_id, shopping_goal=shopping_goal)
        self._streams[stream_id] = stream
        return stream

    def viewer_interactions(self, stream_id: str, user_id: str, donate: int = 0, vote: Optional[str] = None) -> None:
        if stream_id not in self._streams:
            raise KeyError("Stream not found")
        stream = self._streams[stream_id]
        if not stream.active:
            raise RuntimeError("Stream ended")
        if donate:
            stream.donations[user_id] = stream.donations.get(user_id, 0) + donate
            self._balances[stream.streamer_id] = self._balances.get(stream.streamer_id, 0) + donate
        if vote is not None:
            stream.votes[user_id] = vote
        if user_id not in stream.viewers:
            stream.viewers.append(user_id)

    def end_stream(self, stream_id: str) -> None:
        stream = self._streams.get(stream_id)
        if stream:
            stream.active = False

    def get_balance(self, user_id: str) -> int:
        return self._balances.get(user_id, 0)
