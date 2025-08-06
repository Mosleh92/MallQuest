from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio
import json
from flask_socketio import SocketIO, emit, join_room, leave_room
import redis
from sqlalchemy import and_, or_


@dataclass
class SocialConfig:
    """Configuration for social features"""
    max_friends: int = 500
    max_team_size: int = 10
    max_clan_size: int = 100
    proximity_radius_meters: int = 50
    voice_chat_duration_seconds: int = 900  # 15 minutes


class EnhancedSocialFeatures:
    """Complete implementation of social features for MallQuest"""

    def __init__(self, socketio: SocketIO, redis_client, db_session):
        self.socketio = socketio
        self.redis = redis_client
        self.db = db_session
        self.config = SocialConfig()

    # ============= CHAT SYSTEM =============

    async def send_team_chat(self, user_id: str, team_id: str, message: Dict):
        """Real-time team chat with features"""
        # Validate user is in team
        if not self.is_user_in_team(user_id, team_id):
            return {"error": "Not a team member"}

        # Check for rate limiting
        if await self.is_chat_rate_limited(user_id):
            return {"error": "Too many messages"}

        # Process message
        processed_message = {
            "id": self.generate_message_id(),
            "user_id": user_id,
            "username": self.get_username(user_id),
            "team_id": team_id,
            "content": self.sanitize_message(message["content"]),
            "type": message.get("type", "text"),  # text, image, voice, location
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {
                "user_level": self.get_user_level(user_id),
                "user_avatar": self.get_user_avatar(user_id),
                "location": message.get("location"),
                "reply_to": message.get("reply_to"),
            },
        }

        # Store in Redis for recent history
        await self.redis.lpush(
            f"chat:team:{team_id}",
            json.dumps(processed_message),
        )
        await self.redis.ltrim(f"chat:team:{team_id}", 0, 100)  # Keep last 100 messages

        # Emit to team members
        self.socketio.emit(
            "team_message",
            processed_message,
            room=f"team_{team_id}",
            namespace="/chat",
        )

        # Send push notifications to offline members
        await self.notify_offline_members(team_id, processed_message)

        return {"success": True, "message_id": processed_message["id"]}

    async def proximity_chat(self, user_id: str, location: Dict, message: str):
        """Location-based chat - talk to nearby players"""
        nearby_users = await self.find_nearby_users(
            location, self.config.proximity_radius_meters
        )

        chat_data = {
            "user_id": user_id,
            "username": self.get_username(user_id),
            "message": message,
            "location": location,
            "timestamp": datetime.utcnow().isoformat(),
            "radius": self.config.proximity_radius_meters,
        }

        # Send to nearby users only
        for nearby_user in nearby_users:
            if nearby_user["id"] != user_id:
                self.socketio.emit(
                    "proximity_message",
                    chat_data,
                    room=f"user_{nearby_user['id']}",
                    namespace="/chat",
                )

        return {"recipients": len(nearby_users) - 1}

    async def battle_voice_chat(self, battle_id: str, team_id: str, user_id: str):
        """Voice chat during battles with WebRTC signaling"""
        # Verify battle is active
        battle = await self.get_battle(battle_id)
        if battle["status"] != "ACTIVE":
            return {"error": "Battle not active"}

        # Create/join voice room
        voice_room = f"voice_battle_{battle_id}_team_{team_id}"

        # WebRTC signaling
        signaling_data = {
            "type": "join_voice",
            "room": voice_room,
            "user_id": user_id,
            "ice_servers": self.get_ice_servers(),
            "max_duration": self.config.voice_chat_duration_seconds,
        }

        self.socketio.emit(
            "voice_chat_signal",
            signaling_data,
            room=f"team_{team_id}",
            namespace="/voice",
        )

        return {
            "voice_room": voice_room,
            "expires_in": self.config.voice_chat_duration_seconds,
        }

    # ============= SOCIAL GRAPH =============

    async def add_friend(self, user_id: str, friend_id: str):
        """Enhanced friend system with features"""
        # Check friend limit
        current_friends = await self.get_friend_count(user_id)
        if current_friends >= self.config.max_friends:
            return {"error": f"Friend limit reached ({self.config.max_friends})"}

        # Check if already friends or pending
        existing = self.db.query(Friendship).filter(
            or_(
                and_(Friendship.user_id == user_id, Friendship.friend_id == friend_id),
                and_(Friendship.user_id == friend_id, Friendship.friend_id == user_id),
            )
        ).first()

        if existing:
            return {"error": "Already friends or request pending"}

        # Create friend request
        friendship = Friendship(
            user_id=user_id,
            friend_id=friend_id,
            status="pending",
            created_at=datetime.utcnow(),
        )
        self.db.add(friendship)
        self.db.commit()

        # Notify friend
        await self.send_notification(
            friend_id,
            {
                "type": "friend_request",
                "from": self.get_username(user_id),
                "user_id": user_id,
            },
        )

        return {"success": True, "status": "pending"}

    async def create_team(self, creator_id: str, team_data: Dict):
        """Create persistent team with advanced features"""
        team = Team(
            id=self.generate_team_id(),
            name=team_data["name"],
            creator_id=creator_id,
            description=team_data.get("description"),
            avatar=team_data.get("avatar"),
            is_public=team_data.get("is_public", True),
            max_members=min(
                team_data.get("max_members", 10), self.config.max_team_size
            ),
            settings={
                "auto_accept": team_data.get("auto_accept", False),
                "min_level": team_data.get("min_level", 1),
                "preferred_mall": team_data.get("preferred_mall"),
                "play_times": team_data.get("play_times", []),
                "language": team_data.get("language", "en"),
            },
            stats={
                "total_battles": 0,
                "wins": 0,
                "total_coins": 0,
                "ranking": None,
            },
            created_at=datetime.utcnow(),
        )

        self.db.add(team)
        self.db.commit()

        # Add creator as leader
        self.add_team_member(team.id, creator_id, role="leader")

        # Create team chat room
        join_room(f"team_{team.id}", sid=creator_id, namespace="/chat")

        return {"team_id": team.id, "success": True}

    async def create_clan(self, founder_id: str, clan_data: Dict):
        """Create larger clan organization"""
        clan = Clan(
            id=self.generate_clan_id(),
            name=clan_data["name"],
            tag=clan_data["tag"],  # 3-5 character tag
            founder_id=founder_id,
            description=clan_data.get("description"),
            banner=clan_data.get("banner"),
            requirements={
                "min_level": clan_data.get("min_level", 10),
                "min_trophies": clan_data.get("min_trophies", 100),
                "approval_needed": clan_data.get("approval_needed", True),
            },
            perks={
                "coin_bonus": 0.05,  # 5% bonus starts
                "xp_bonus": 0.05,
                "exclusive_quests": False,
                "clan_wars_enabled": False,
            },
            treasury=0,  # Clan bank for shared resources
            created_at=datetime.utcnow(),
        )

        self.db.add(clan)
        self.db.commit()

        return {"clan_id": clan.id, "tag": clan.tag}

    async def add_rival(self, user_id: str, rival_id: str):
        """Track competition between players"""
        rivalry = Rivalry(
            user_id=user_id,
            rival_id=rival_id,
            stats={
                "battles_fought": 0,
                "user_wins": 0,
                "rival_wins": 0,
                "last_battle": None,
            },
            created_at=datetime.utcnow(),
        )

        self.db.add(rivalry)
        self.db.commit()

        # Notify rival
        await self.send_notification(
            rival_id,
            {
                "type": "new_rival",
                "from": self.get_username(user_id),
                "message": f"{self.get_username(user_id)} added you as a rival!",
            },
        )

        return {"success": True}

    # ============= SHARING & VIRAL =============

    async def share_achievement(self, user_id: str, achievement_id: str, platform: str):
        """Share achievements on social media"""
        achievement = self.get_achievement(achievement_id)
        user = self.get_user(user_id)

        share_data = {
            "title": f"{user.username} unlocked: {achievement.name}",
            "description": achievement.description,
            "image": self.generate_achievement_card(user, achievement),
            "hashtags": ["MallQuest", "Gaming", achievement.category],
            "deep_link": f"mallquest://achievement/{achievement_id}",
        }

        if platform == "instagram":
            return await self.share_to_instagram(share_data)
        elif platform == "twitter":
            return await self.share_to_twitter(share_data)
        elif platform == "whatsapp":
            return await self.share_to_whatsapp(share_data)
        elif platform == "snapchat":
            return await self.share_to_snapchat(share_data)

        # Track sharing for rewards
        await self.track_social_share(user_id, achievement_id, platform)

        return {"shared": True, "bonus_coins": 50}

    async def save_and_share_replay(self, battle_id: str, user_id: str):
        """Save battle highlights for sharing"""
        battle_data = await self.get_battle_data(battle_id)

        # Generate replay
        replay = {
            "id": self.generate_replay_id(),
            "battle_id": battle_id,
            "user_id": user_id,
            "highlights": self.extract_highlights(battle_data),
            "duration": battle_data["duration"],
            "participants": battle_data["participants"],
            "final_scores": battle_data["final_scores"],
            "thumbnail": self.generate_replay_thumbnail(battle_data),
            "share_url": f"https://mallquest.game/replay/{replay_id}",
        }

        # Store replay
        await self.redis.setex(
            f"replay:{replay['id']}",
            86400 * 7,  # 7 days
            json.dumps(replay),
        )

        return {"replay_id": replay["id"], "share_url": replay["share_url"]}

    async def send_referral(self, user_id: str, method: str, target: str):
        """Enhanced referral system"""
        referral_code = self.generate_referral_code(user_id)

        referral_data = {
            "code": referral_code,
            "sender_id": user_id,
            "sender_name": self.get_username(user_id),
            "rewards": {
                "referrer": 500,  # Coins for referrer
                "referred": 200,  # Bonus for new user
            },
            "deep_link": f"mallquest://join/{referral_code}",
            "message": f"Join me in MallQuest! Use my code {referral_code} for 200 bonus coins!",
        }

        if method == "sms":
            result = await self.send_sms_invite(target, referral_data)
        elif method == "email":
            result = await self.send_email_invite(target, referral_data)
        elif method == "qr":
            result = self.generate_qr_invite(referral_data)

        # Track referral
        await self.track_referral(user_id, referral_code, method)

        return {"code": referral_code, "sent": True}
