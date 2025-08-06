"""Simple guild system with basic guild wars."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Guild:
    name: str
    members: List[str]
    wins: int = 0
    coins: Dict[str, int] = field(default_factory=dict)


class GuildWars:
    """Manage guild creation and challenges."""

    def __init__(self) -> None:
        self.guilds: Dict[str, Guild] = {}

    def create_guild(self, name: str, members: List[str]) -> Guild:
        if len(members) > 10:
            raise ValueError("Guilds are limited to 10 members")
        guild = Guild(name=name, members=members)
        self.guilds[name] = guild
        return guild

    def guild_vs_guild_challenge(self, guild1: str, guild2: str, winner: Optional[str] = None) -> str:
        if guild1 not in self.guilds or guild2 not in self.guilds:
            raise KeyError("Guild not found")
        if winner is None:
            winner = guild1
        winning_guild = self.guilds[winner]
        winning_guild.wins += 1
        for member in winning_guild.members:
            winning_guild.coins[member] = winning_guild.coins.get(member, 0) + 1000
        return winner

    def member_balance(self, guild_name: str, member: str) -> int:
        return self.guilds[guild_name].coins.get(member, 0)
