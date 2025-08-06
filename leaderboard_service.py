import json
import time
from typing import Generator

from flask import Response, stream_with_context
from mall_gamification_system import MallGamificationSystem


class LeaderboardService:
    """Service that streams leaderboard updates using Server-Sent Events."""

    def __init__(self, mall_system: MallGamificationSystem):
        self.mall_system = mall_system

    def stream(self, leaderboard_type: str = "coins", interval: int = 5) -> Response:
        """Return a streaming response for the requested leaderboard.

        Args:
            leaderboard_type: The type of leaderboard to stream, e.g., ``"coins"``.
            interval: Seconds between leaderboard updates.
        """

        @stream_with_context
        def event_stream() -> Generator[str, None, None]:
            while True:
                leaderboard = self.mall_system.get_leaderboard(leaderboard_type, 10)
                # Only send fields needed for display to avoid JSON serialization issues
                sanitized = [
                    {
                        "user_id": entry.get("user_id"),
                        "score": entry.get("score", 0),
                    }
                    for entry in leaderboard
                ]
                yield f"data: {json.dumps(sanitized)}\n\n"
                time.sleep(interval)

        return Response(event_stream(), mimetype="text/event-stream", headers={"Cache-Control": "no-cache"})

