#!/usr/bin/env python3
"""
Enhanced Database System for Deerfields Mall Gamification System
Provides persistent storage for all system data with security, performance, and reliability features
"""

import sqlite3
import json
import os
import shutil
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
import uuid
from pathlib import Path

class MallDatabase:
    """Enhanced database manager for mall gamification system"""
    
    def __init__(self, db_path: str = 'mall_gamification.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.setup_logging()
        self.create_tables()
        self.create_indexes()
        self.run_migrations()
    
    def setup_logging(self):
        """Setup database logging"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('MallDatabase')
    
    def create_tables(self):
        """Create all necessary database tables"""
        try:
            # Users table (enhanced)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    coins INTEGER DEFAULT 0,
                    xp INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    vip_tier TEXT DEFAULT 'Bronze',
                    vip_points INTEGER DEFAULT 0,
                    login_streak INTEGER DEFAULT 0,
                    max_streak INTEGER DEFAULT 0,
                    total_spent REAL DEFAULT 0.0,
                    total_purchases INTEGER DEFAULT 0,
                    visited_categories TEXT,  -- JSON array
                    achievement_points INTEGER DEFAULT 0,
                    social_score INTEGER DEFAULT 0,
                    friends TEXT,  -- JSON array of friend IDs
                    team_id TEXT,
                    leaderboard_position INTEGER DEFAULT 0,
                    social_achievements TEXT,  -- JSON array
                    event_participation TEXT,  -- JSON object
                    seasonal_progress TEXT,  -- JSON object
                    language TEXT DEFAULT 'en',
                    last_login TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Receipts table (enhanced)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS receipts (
                    receipt_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    store TEXT NOT NULL,
                    category TEXT,
                    amount REAL NOT NULL,
                    currency TEXT DEFAULT 'AED',
                    status TEXT DEFAULT 'pending',  -- pending, verified, rejected, suspicious
                    ai_verification_status TEXT DEFAULT 'pending',
                    ai_confidence REAL,
                    verification_notes TEXT,
                    items TEXT,  -- JSON array of items
                    receipt_image TEXT,  -- Base64 encoded image
                    verified_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Missions table (enhanced)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS missions (
                    mission_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    type TEXT NOT NULL,  -- daily, weekly, seasonal, special
                    target INTEGER NOT NULL,
                    current_progress INTEGER DEFAULT 0,
                    reward_coins INTEGER NOT NULL,
                    reward_xp INTEGER NOT NULL,
                    status TEXT DEFAULT 'active',  -- active, completed, expired, failed
                    difficulty TEXT DEFAULT 'normal',  -- easy, normal, hard, expert
                    personalized BOOLEAN DEFAULT FALSE,
                    expires_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Achievements table (NEW)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS achievements (
                    achievement_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    achievement_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    points INTEGER DEFAULT 0,
                    icon TEXT,
                    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,  -- JSON object for additional data
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Security audit log table (enhanced)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS security_audit_log (
                    log_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    action TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    details TEXT,  -- JSON object for additional details
                    severity TEXT DEFAULT 'info',  -- info, warning, error, critical
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Rate limits table (enhanced)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS rate_limits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT NOT NULL,
                    endpoint TEXT NOT NULL,
                    request_count INTEGER DEFAULT 1,
                    window_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_request TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(ip_address, endpoint)
                )
            ''')
            
            # User sessions table (NEW)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    token_hash TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Companion table (enhanced)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS companions (
                    companion_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    companion_type TEXT NOT NULL,
                    level INTEGER DEFAULT 1,
                    xp INTEGER DEFAULT 0,
                    happiness INTEGER DEFAULT 100,
                    hunger INTEGER DEFAULT 100,
                    power REAL DEFAULT 1.0,
                    abilities TEXT,  -- JSON array of abilities
                    last_fed TIMESTAMP,
                    last_played TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Stores table (enhanced)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS stores (
                    store_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    zone TEXT NOT NULL,
                    brand TEXT,
                    offers TEXT,  -- JSON array of offers
                    rating REAL DEFAULT 0.0,
                    review_count INTEGER DEFAULT 0,
                    total_sales REAL DEFAULT 0.0,
                    customer_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User activities table (enhanced)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS user_activities (
                    activity_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    description TEXT,
                    coins_earned INTEGER DEFAULT 0,
                    xp_earned INTEGER DEFAULT 0,
                    metadata TEXT,  -- JSON object for additional data
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Admin logs table (enhanced)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS admin_logs (
                    log_id TEXT PRIMARY KEY,
                    admin_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    target_type TEXT,
                    target_id TEXT,
                    details TEXT,
                    ip_address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Support tickets table (enhanced)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS support_tickets (
                    ticket_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    description TEXT NOT NULL,
                    priority TEXT DEFAULT 'medium',
                    status TEXT DEFAULT 'open',
                    assigned_to TEXT,
                    response TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolved_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Teams table (NEW)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS teams (
                    team_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    creator_id TEXT NOT NULL,
                    description TEXT,
                    members TEXT,  -- JSON array of member IDs
                    score INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (creator_id) REFERENCES users (user_id)
                )
            ''')
            
            # Team challenges table (NEW)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS team_challenges (
                    challenge_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    target_score INTEGER NOT NULL,
                    reward TEXT,  -- JSON object with coins, xp, etc.
                    duration_days INTEGER DEFAULT 7,
                    teams TEXT,  -- JSON object with team scores
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP
                )
            ''')
            
            # Events table (NEW)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    event_type TEXT NOT NULL,  -- seasonal, special, limited
                    bonus_multiplier REAL DEFAULT 1.0,
                    start_date TIMESTAMP NOT NULL,
                    end_date TIMESTAMP NOT NULL,
                    participants TEXT,  -- JSON array of user IDs
                    rewards TEXT,  -- JSON object with rewards
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Deer table (NEW)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS deer (
                    deer_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    level INTEGER DEFAULT 1,
                    xp INTEGER DEFAULT 0,
                    health INTEGER DEFAULT 100,
                    happiness INTEGER DEFAULT 80,
                    energy INTEGER DEFAULT 90,
                    hunger INTEGER DEFAULT 20,
                    abilities TEXT,  -- JSON array
                    visual_effects TEXT,  -- JSON array
                    preferred_food TEXT,  -- JSON array
                    entertainment TEXT,  -- JSON array
                    shelter TEXT,
                    last_fed TIMESTAMP,
                    last_entertained TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_care TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Empires table (NEW)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS empires (
                    empire_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    level INTEGER DEFAULT 1,
                    xp INTEGER DEFAULT 0,
                    total_income INTEGER DEFAULT 0,
                    total_visitors INTEGER DEFAULT 0,
                    facilities TEXT,  -- JSON array
                    active_events TEXT,  -- JSON array
                    empire_bonuses TEXT,  -- JSON object
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_income_collection TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Notifications table (NEW)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    notification_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    action TEXT,
                    data TEXT,  -- JSON object
                    priority TEXT DEFAULT 'medium',
                    icon TEXT,
                    color TEXT,
                    auto_dismiss BOOLEAN DEFAULT FALSE,
                    sound TEXT,
                    read BOOLEAN DEFAULT FALSE,
                    dismissed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Notification settings table (NEW)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS notification_settings (
                    user_id TEXT PRIMARY KEY,
                    enabled BOOLEAN DEFAULT TRUE,
                    sound_enabled BOOLEAN DEFAULT TRUE,
                    vibration_enabled BOOLEAN DEFAULT TRUE,
                    types TEXT,  -- JSON object
                    quiet_hours TEXT,  -- JSON object
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Database migrations table (NEW)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS migrations (
                    migration_id TEXT PRIMARY KEY,
                    version TEXT NOT NULL,
                    description TEXT,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            self.logger.info("Database tables created successfully")
            
        except Exception as e:
            self.logger.error(f"Error creating tables: {e}")
            raise
    
    def create_indexes(self):
        """Create all necessary database indexes for performance"""
        try:
            # User indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_users_vip_tier ON users(vip_tier)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_users_level ON users(level)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_users_last_login ON users(last_login)')
            
            # Receipt indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_receipts_user_id ON receipts(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_receipts_date ON receipts(created_at)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_receipts_status ON receipts(status)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_receipts_store ON receipts(store)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_receipts_category ON receipts(category)')
            
            # Mission indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_missions_user_id ON missions(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_mission_user_status ON missions(user_id, status)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_missions_type ON missions(type)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_missions_expires ON missions(expires_at)')
            
            # Achievement indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_achievements_user_id ON achievements(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_achievements_type ON achievements(achievement_type)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_achievements_earned ON achievements(earned_at)')
            
            # Security audit log indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_security_log_user ON security_audit_log(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_security_log_action ON security_audit_log(action)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_security_log_timestamp ON security_audit_log(timestamp)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_security_log_ip ON security_audit_log(ip_address)')
            
            # Rate limit indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_rate_limit_ip_endpoint ON rate_limits(ip_address, endpoint)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_rate_limit_window ON rate_limits(window_start)')
            
            # User session indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(token_hash)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_active ON user_sessions(is_active)')
            
            # Activity indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_activities_user_id ON user_activities(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_activities_type ON user_activities(activity_type)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_activities_created ON user_activities(created_at)')
            
            # Store indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_stores_category ON stores(category)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_stores_zone ON stores(zone)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_stores_rating ON stores(rating)')
            
            # Support ticket indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_tickets_user_id ON support_tickets(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_tickets_status ON support_tickets(status)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_tickets_priority ON support_tickets(priority)')
            
            # Team indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_teams_creator ON teams(creator_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_teams_score ON teams(score)')
            
            # Event indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_events_dates ON events(start_date, end_date)')
            
            # Deer indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_deer_user_id ON deer(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_deer_type ON deer(type)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_deer_level ON deer(level)')
            
            # Empire indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_empires_user_id ON empires(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_empires_level ON empires(level)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_empires_income ON empires(total_income)')
            
            # Notification indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_notifications_type ON notifications(type)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_notifications_priority ON notifications(priority)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(read)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_notifications_created ON notifications(created_at)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_notifications_expires ON notifications(expires_at)')
            
            # Notification settings indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_notification_settings_user_id ON notification_settings(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_notification_settings_enabled ON notification_settings(enabled)')
            
            self.conn.commit()
            self.logger.info("Database indexes created successfully")
            
        except Exception as e:
            self.logger.error(f"Error creating indexes: {e}")
            raise
    
    def run_migrations(self):
        """Run database migrations to ensure schema is up to date"""
        try:
            # Check if migrations table exists
            cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='migrations'")
            if not cursor.fetchone():
                self.logger.info("Migrations table not found, creating...")
                self.conn.execute('''
                    CREATE TABLE migrations (
                        migration_id TEXT PRIMARY KEY,
                        version TEXT NOT NULL,
                        description TEXT,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                self.conn.commit()
            
            # Get applied migrations
            cursor = self.conn.execute("SELECT version FROM migrations")
            applied_migrations = {row['version'] for row in cursor.fetchall()}
            
            # Define migrations
            migrations = [
                {
                    'version': '1.0.0',
                    'description': 'Initial schema creation',
                    'sql': None  # Already handled by create_tables
                },
                {
                    'version': '1.1.0',
                    'description': 'Add achievements table',
                    'sql': '''
                        CREATE TABLE IF NOT EXISTS achievements (
                            achievement_id TEXT PRIMARY KEY,
                            user_id TEXT NOT NULL,
                            achievement_type TEXT NOT NULL,
                            title TEXT NOT NULL,
                            description TEXT,
                            points INTEGER DEFAULT 0,
                            icon TEXT,
                            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            metadata TEXT,
                            FOREIGN KEY (user_id) REFERENCES users (user_id)
                        )
                    '''
                },
                {
                    'version': '1.2.0',
                    'description': 'Add user_sessions table',
                    'sql': '''
                        CREATE TABLE IF NOT EXISTS user_sessions (
                            session_id TEXT PRIMARY KEY,
                            user_id TEXT NOT NULL,
                            token_hash TEXT NOT NULL,
                            ip_address TEXT,
                            user_agent TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            expires_at TIMESTAMP NOT NULL,
                            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            is_active BOOLEAN DEFAULT TRUE,
                            FOREIGN KEY (user_id) REFERENCES users (user_id)
                        )
                    '''
                },
                {
                    'version': '1.3.0',
                    'description': 'Add missing columns to users table',
                    'sql': '''
                        ALTER TABLE users ADD COLUMN vip_points INTEGER DEFAULT 0;
                        ALTER TABLE users ADD COLUMN total_spent REAL DEFAULT 0.0;
                        ALTER TABLE users ADD COLUMN total_purchases INTEGER DEFAULT 0;
                        ALTER TABLE users ADD COLUMN visited_categories TEXT;
                        ALTER TABLE users ADD COLUMN achievement_points INTEGER DEFAULT 0;
                        ALTER TABLE users ADD COLUMN social_score INTEGER DEFAULT 0;
                        ALTER TABLE users ADD COLUMN friends TEXT;
                        ALTER TABLE users ADD COLUMN team_id TEXT;
                        ALTER TABLE users ADD COLUMN leaderboard_position INTEGER DEFAULT 0;
                        ALTER TABLE users ADD COLUMN social_achievements TEXT;
                        ALTER TABLE users ADD COLUMN event_participation TEXT;
                        ALTER TABLE users ADD COLUMN seasonal_progress TEXT;
                        ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en';
                    '''
                },
                {
                    'version': '1.4.0',
                    'description': 'Add missing columns to receipts table',
                    'sql': '''
                        ALTER TABLE receipts ADD COLUMN category TEXT;
                        ALTER TABLE receipts ADD COLUMN status TEXT DEFAULT 'pending';
                        ALTER TABLE receipts ADD COLUMN verified_at TIMESTAMP;
                    '''
                },
                {
                    'version': '1.5.0',
                    'description': 'Add missing columns to missions table',
                    'sql': '''
                        ALTER TABLE missions ADD COLUMN difficulty TEXT DEFAULT 'normal';
                        ALTER TABLE missions ADD COLUMN personalized BOOLEAN DEFAULT FALSE;
                    '''
                }
            ]
            
            # Apply pending migrations
            for migration in migrations:
                if migration['version'] not in applied_migrations:
                    self.logger.info(f"Applying migration {migration['version']}: {migration['description']}")
                    
                    if migration['sql']:
                        try:
                            self.conn.execute(migration['sql'])
                            self.conn.commit()
                        except sqlite3.OperationalError as e:
                            if "duplicate column name" not in str(e).lower():
                                raise
                    
                    # Record migration
                    self.conn.execute('''
                        INSERT INTO migrations (migration_id, version, description)
                        VALUES (?, ?, ?)
                    ''', (str(uuid.uuid4()), migration['version'], migration['description']))
                    self.conn.commit()
                    
                    self.logger.info(f"Migration {migration['version']} applied successfully")
            
            self.logger.info("All migrations completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error running migrations: {e}")
            raise
    
    def backup_database(self, backup_path: str = None) -> bool:
        """Create a backup of the database"""
        try:
            if not backup_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"backup_mall_gamification_{timestamp}.db"
            
            # Create backup directory if it doesn't exist
            backup_dir = Path(backup_path).parent
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Close current connection
            self.conn.close()
            
            # Copy database file
            shutil.copy2(self.db_path, backup_path)
            
            # Reopen connection
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            
            self.logger.info(f"Database backup created: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            # Reopen connection in case of error
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            return False
    
    def restore_database(self, backup_path: str) -> bool:
        """Restore database from backup"""
        try:
            if not os.path.exists(backup_path):
                self.logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Close current connection
            self.conn.close()
            
            # Create current database backup before restore
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            current_backup = f"pre_restore_backup_{timestamp}.db"
            shutil.copy2(self.db_path, current_backup)
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            
            # Reopen connection
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            
            self.logger.info(f"Database restored from: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error restoring database: {e}")
            # Reopen connection in case of error
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            return False
    
    def optimize_database(self) -> bool:
        """Optimize database performance"""
        try:
            # Analyze tables for better query planning
            self.conn.execute("ANALYZE")
            
            # Vacuum database to reclaim space
            self.conn.execute("VACUUM")
            
            # Update statistics
            self.conn.execute("ANALYZE")
            
            self.conn.commit()
            self.logger.info("Database optimization completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Error optimizing database: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics and health information"""
        try:
            stats = {}
            
            # Table sizes
            cursor = self.conn.execute("""
                SELECT name, sql FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table['name']
                cursor = self.conn.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                count = cursor.fetchone()['count']
                stats[f"{table_name}_count"] = count
            
            # Database file size
            if os.path.exists(self.db_path):
                stats['file_size_mb'] = round(os.path.getsize(self.db_path) / (1024 * 1024), 2)
            
            # Index information
            cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
            stats['index_count'] = len(cursor.fetchall())
            
            # Migration status
            cursor = self.conn.execute("SELECT COUNT(*) as count FROM migrations")
            stats['migrations_applied'] = cursor.fetchone()['count']
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting database stats: {e}")
            return {}
    
    # Enhanced CRUD operations with security
    
    def add_user(self, user_data: Dict[str, Any]) -> bool:
        """Add a new user to the database with enhanced security"""
        try:
            # Validate required fields
            required_fields = ['user_id', 'name']
            for field in required_fields:
                if field not in user_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Sanitize input
            user_id = str(user_data['user_id']).strip()
            name = str(user_data['name']).strip()[:100]  # Limit length
            
            self.conn.execute('''
                INSERT INTO users (user_id, name, email, phone, coins, xp, level, vip_tier, language)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                name,
                user_data.get('email'),
                user_data.get('phone'),
                user_data.get('coins', 0),
                user_data.get('xp', 0),
                user_data.get('level', 1),
                user_data.get('vip_tier', 'Bronze'),
                user_data.get('language', 'en')
            ))
            self.conn.commit()
            self.logger.info(f"User added: {user_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding user: {e}")
            return False
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID with enhanced security"""
        try:
            if not user_id or not isinstance(user_id, str):
                return None
            
            cursor = self.conn.execute('''
                SELECT * FROM users WHERE user_id = ?
            ''', (user_id.strip(),))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            self.logger.error(f"Error getting user: {e}")
            return None
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user data with enhanced security"""
        try:
            if not updates:
                return False
            
            # Whitelist allowed columns for security
            allowed_columns = {
                'name', 'email', 'phone', 'coins', 'xp', 'level', 'vip_tier', 
                'vip_points', 'login_streak', 'max_streak', 'total_spent', 
                'total_purchases', 'visited_categories', 'achievement_points',
                'social_score', 'friends', 'team_id', 'leaderboard_position',
                'social_achievements', 'event_participation', 'seasonal_progress',
                'language', 'last_login'
            }
            
            filtered_updates = {k: v for k, v in updates.items() if k in allowed_columns}
            
            if not filtered_updates:
                return False
            
            set_clause = ', '.join([f"{k} = ?" for k in filtered_updates.keys()])
            set_clause += ', updated_at = CURRENT_TIMESTAMP'
            
            query = f"UPDATE users SET {set_clause} WHERE user_id = ?"
            values = list(filtered_updates.values()) + [user_id]
            
            self.conn.execute(query, values)
            self.conn.commit()
            self.logger.info(f"User updated: {user_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating user: {e}")
            return False
    
    def add_receipt(self, receipt_data: Dict[str, Any]) -> bool:
        """Add a new receipt with enhanced security"""
        try:
            # Validate required fields
            required_fields = ['receipt_id', 'user_id', 'store', 'amount']
            for field in required_fields:
                if field not in receipt_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate amount
            amount = float(receipt_data['amount'])
            if amount <= 0 or amount > 100000:  # Reasonable limits
                raise ValueError("Invalid amount")
            
            self.conn.execute('''
                INSERT INTO receipts (receipt_id, user_id, store, category, amount, currency, status, items, receipt_image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                receipt_data['receipt_id'],
                receipt_data['user_id'],
                receipt_data['store'],
                receipt_data.get('category'),
                amount,
                receipt_data.get('currency', 'AED'),
                receipt_data.get('status', 'pending'),
                json.dumps(receipt_data.get('items', [])),
                receipt_data.get('receipt_image')
            ))
            self.conn.commit()
            self.logger.info(f"Receipt added: {receipt_data['receipt_id']}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding receipt: {e}")
            return False
    
    def add_achievement(self, achievement_data: Dict[str, Any]) -> bool:
        """Add a new achievement"""
        try:
            required_fields = ['achievement_id', 'user_id', 'achievement_type', 'title']
            for field in required_fields:
                if field not in achievement_data:
                    raise ValueError(f"Missing required field: {field}")
            
            self.conn.execute('''
                INSERT INTO achievements (achievement_id, user_id, achievement_type, title, description, points, icon, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                achievement_data['achievement_id'],
                achievement_data['user_id'],
                achievement_data['achievement_type'],
                achievement_data['title'],
                achievement_data.get('description'),
                achievement_data.get('points', 0),
                achievement_data.get('icon'),
                json.dumps(achievement_data.get('metadata', {}))
            ))
            self.conn.commit()
            self.logger.info(f"Achievement added: {achievement_data['achievement_id']}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding achievement: {e}")
            return False
    
    def get_user_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's achievements"""
        try:
            cursor = self.conn.execute('''
                SELECT * FROM achievements 
                WHERE user_id = ? 
                ORDER BY earned_at DESC
            ''', (user_id,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Error getting user achievements: {e}")
            return []
    
    def add_user_session(self, session_data: Dict[str, Any]) -> bool:
        """Add a new user session"""
        try:
            required_fields = ['session_id', 'user_id', 'token_hash', 'expires_at']
            for field in required_fields:
                if field not in session_data:
                    raise ValueError(f"Missing required field: {field}")
            
            self.conn.execute('''
                INSERT INTO user_sessions (session_id, user_id, token_hash, ip_address, user_agent, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session_data['session_id'],
                session_data['user_id'],
                session_data['token_hash'],
                session_data.get('ip_address'),
                session_data.get('user_agent'),
                session_data['expires_at']
            ))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error adding user session: {e}")
            return False
    
    def get_user_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get user session by ID"""
        try:
            cursor = self.conn.execute('''
                SELECT * FROM user_sessions 
                WHERE session_id = ? AND is_active = TRUE AND expires_at > CURRENT_TIMESTAMP
            ''', (session_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            self.logger.error(f"Error getting user session: {e}")
            return None
    
    def invalidate_user_session(self, session_id: str) -> bool:
        """Invalidate a user session"""
        try:
            self.conn.execute('''
                UPDATE user_sessions 
                SET is_active = FALSE 
                WHERE session_id = ?
            ''', (session_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error invalidating session: {e}")
            return False
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return count of cleaned sessions"""
        try:
            cursor = self.conn.execute('''
                UPDATE user_sessions 
                SET is_active = FALSE 
                WHERE expires_at <= CURRENT_TIMESTAMP AND is_active = TRUE
            ''')
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            self.logger.error(f"Error cleaning up expired sessions: {e}")
            return 0
    
    def log_security_event(self, user_id: str, action: str, ip_address: str = None, details: str = None) -> bool:
        """Log security event"""
        try:
            self.conn.execute('''
                INSERT INTO security_audit_log (log_id, user_id, action, ip_address, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                str(uuid.uuid4()),
                user_id,
                action,
                ip_address,
                details
            ))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error logging security event: {e}")
            return False
    
    def get_security_logs(self, user_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get security audit logs"""
        try:
            if user_id:
                cursor = self.conn.execute('''
                    SELECT * FROM security_audit_log 
                    WHERE user_id = ?
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (user_id, limit))
            else:
                cursor = self.conn.execute('''
                    SELECT * FROM security_audit_log 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Error getting security logs: {e}")
            return []
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        try:
            stats = {}
            
            # User stats
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM users')
            stats['total_users'] = cursor.fetchone()['count']
            
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM users WHERE last_login > datetime("now", "-1 day")')
            stats['active_users_today'] = cursor.fetchone()['count']
            
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM users WHERE vip_tier != "Bronze"')
            stats['vip_users'] = cursor.fetchone()['count']
            
            # Receipt stats
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM receipts')
            stats['total_receipts'] = cursor.fetchone()['count']
            
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM receipts WHERE status = "verified"')
            stats['verified_receipts'] = cursor.fetchone()['count']
            
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM receipts WHERE status = "suspicious"')
            stats['suspicious_receipts'] = cursor.fetchone()['count']
            
            cursor = self.conn.execute('SELECT SUM(amount) as total FROM receipts WHERE status = "verified"')
            result = cursor.fetchone()
            stats['total_verified_amount'] = result['total'] if result['total'] else 0
            
            # Mission stats
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM missions WHERE status = "completed"')
            stats['completed_missions'] = cursor.fetchone()['count']
            
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM missions WHERE status = "active"')
            stats['active_missions'] = cursor.fetchone()['count']
            
            # Achievement stats
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM achievements')
            stats['total_achievements'] = cursor.fetchone()['count']
            
            # Session stats
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM user_sessions WHERE is_active = TRUE')
            stats['active_sessions'] = cursor.fetchone()['count']
            
            # Security stats
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM security_audit_log WHERE timestamp > datetime("now", "-1 day")')
            stats['security_events_today'] = cursor.fetchone()['count']
            
            # Store stats
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM stores')
            stats['total_stores'] = cursor.fetchone()['count']
            
            # Support stats
            cursor = self.conn.execute('SELECT COUNT(*) as count FROM support_tickets WHERE status = "open"')
            stats['open_tickets'] = cursor.fetchone()['count']
            
            return stats
        except Exception as e:
            self.logger.error(f"Error getting system stats: {e}")
            return {}
    
    # Deer Care System Methods
    def save_deer(self, deer_data: Dict[str, Any]) -> bool:
        """Save deer data to database"""
        try:
            self.conn.execute('''
                INSERT OR REPLACE INTO deer (
                    deer_id, user_id, type, name, description, level, xp,
                    health, happiness, energy, hunger, abilities, visual_effects,
                    preferred_food, entertainment, shelter, last_fed, last_entertained,
                    created_at, last_care
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                deer_data['deer_id'], deer_data['user_id'], deer_data['type'],
                deer_data['name'], deer_data['description'], deer_data['level'],
                deer_data['xp'], deer_data['health'], deer_data['happiness'],
                deer_data['energy'], deer_data['hunger'],
                json.dumps(deer_data['abilities']),
                json.dumps(deer_data['visual_effects']),
                json.dumps(deer_data['preferred_food']),
                json.dumps(deer_data['entertainment']),
                deer_data['shelter'], deer_data['last_fed'],
                deer_data['last_entertained'], deer_data['created_at'],
                deer_data['last_care']
            ))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error saving deer: {e}")
            return False
    
    def get_deer(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get deer data for user"""
        try:
            row = self.conn.execute('''
                SELECT * FROM deer WHERE user_id = ?
            ''', (user_id,)).fetchone()
            
            if row:
                deer_data = dict(row)
                deer_data['abilities'] = json.loads(deer_data['abilities'])
                deer_data['visual_effects'] = json.loads(deer_data['visual_effects'])
                deer_data['preferred_food'] = json.loads(deer_data['preferred_food'])
                deer_data['entertainment'] = json.loads(deer_data['entertainment'])
                return deer_data
            return None
        except Exception as e:
            self.logger.error(f"Error getting deer: {e}")
            return None
    
    def update_deer(self, deer_id: str, deer_data: Dict[str, Any]) -> bool:
        """Update deer data"""
        try:
            self.conn.execute('''
                UPDATE deer SET
                    level = ?, xp = ?, health = ?, happiness = ?, energy = ?, hunger = ?,
                    abilities = ?, visual_effects = ?, shelter = ?, last_fed = ?,
                    last_entertained = ?, last_care = ?
                WHERE deer_id = ?
            ''', (
                deer_data['level'], deer_data['xp'], deer_data['health'],
                deer_data['happiness'], deer_data['energy'], deer_data['hunger'],
                json.dumps(deer_data['abilities']),
                json.dumps(deer_data['visual_effects']),
                deer_data['shelter'], deer_data['last_fed'],
                deer_data['last_entertained'], deer_data['last_care'],
                deer_id
            ))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error updating deer: {e}")
            return False
    
    # Empire Management System Methods
    def save_empire(self, empire_data: Dict[str, Any]) -> bool:
        """Save empire data to database"""
        try:
            self.conn.execute('''
                INSERT OR REPLACE INTO empires (
                    empire_id, user_id, name, level, xp, total_income, total_visitors,
                    facilities, active_events, empire_bonuses, created_at, last_income_collection
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                empire_data['empire_id'], empire_data['user_id'], empire_data['name'],
                empire_data['level'], empire_data['xp'], empire_data['total_income'],
                empire_data['total_visitors'], json.dumps(empire_data['facilities']),
                json.dumps(empire_data['active_events']),
                json.dumps(empire_data['empire_bonuses']),
                empire_data['created_at'], empire_data['last_income_collection']
            ))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error saving empire: {e}")
            return False
    
    def get_empire(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get empire data for user"""
        try:
            row = self.conn.execute('''
                SELECT * FROM empires WHERE user_id = ?
            ''', (user_id,)).fetchone()
            
            if row:
                empire_data = dict(row)
                empire_data['facilities'] = json.loads(empire_data['facilities'])
                empire_data['active_events'] = json.loads(empire_data['active_events'])
                empire_data['empire_bonuses'] = json.loads(empire_data['empire_bonuses'])
                return empire_data
            return None
        except Exception as e:
            self.logger.error(f"Error getting empire: {e}")
            return None
    
    def update_empire(self, empire_id: str, empire_data: Dict[str, Any]) -> bool:
        """Update empire data"""
        try:
            self.conn.execute('''
                UPDATE empires SET
                    level = ?, xp = ?, total_income = ?, total_visitors = ?,
                    facilities = ?, active_events = ?, empire_bonuses = ?,
                    last_income_collection = ?
                WHERE empire_id = ?
            ''', (
                empire_data['level'], empire_data['xp'], empire_data['total_income'],
                empire_data['total_visitors'], json.dumps(empire_data['facilities']),
                json.dumps(empire_data['active_events']),
                json.dumps(empire_data['empire_bonuses']),
                empire_data['last_income_collection'], empire_id
            ))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error updating empire: {e}")
            return False
    
    # Notification System Methods
    def save_notification(self, notification_data: Dict[str, Any]) -> bool:
        """Save notification data to database"""
        try:
            self.conn.execute('''
                INSERT OR REPLACE INTO notifications (
                    notification_id, user_id, type, title, message, action, data,
                    priority, icon, color, auto_dismiss, sound, read, dismissed,
                    created_at, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                notification_data['notification_id'], notification_data['user_id'],
                notification_data['type'], notification_data['title'],
                notification_data['message'], notification_data['action'],
                json.dumps(notification_data['data']), notification_data['priority'],
                notification_data['icon'], notification_data['color'],
                notification_data['auto_dismiss'], notification_data['sound'],
                notification_data['read'], notification_data['dismissed'],
                notification_data['created_at'], notification_data['expires_at']
            ))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error saving notification: {e}")
            return False
    
    def get_user_notifications(self, user_id: str, include_read: bool = False, limit: int = 50) -> List[Dict[str, Any]]:
        """Get notifications for user"""
        try:
            query = '''
                SELECT * FROM notifications WHERE user_id = ?
            '''
            params = [user_id]
            
            if not include_read:
                query += ' AND read = 0'
            
            query += ' ORDER BY created_at DESC LIMIT ?'
            params.append(limit)
            
            rows = self.conn.execute(query, params).fetchall()
            notifications = []
            
            for row in rows:
                notification_data = dict(row)
                notification_data['data'] = json.loads(notification_data['data'])
                notifications.append(notification_data)
            
            return notifications
        except Exception as e:
            self.logger.error(f"Error getting notifications: {e}")
            return []
    
    def mark_notification_read(self, notification_id: str) -> bool:
        """Mark notification as read"""
        try:
            self.conn.execute('''
                UPDATE notifications SET read = 1 WHERE notification_id = ?
            ''', (notification_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error marking notification read: {e}")
            return False
    
    def dismiss_notification(self, notification_id: str) -> bool:
        """Dismiss notification"""
        try:
            self.conn.execute('''
                UPDATE notifications SET dismissed = 1 WHERE notification_id = ?
            ''', (notification_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error dismissing notification: {e}")
            return False
    
    def mark_all_notifications_read(self, user_id: str) -> int:
        """Mark all notifications as read for user"""
        try:
            cursor = self.conn.execute('''
                UPDATE notifications SET read = 1 WHERE user_id = ? AND read = 0
            ''', (user_id,))
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            self.logger.error(f"Error marking all notifications read: {e}")
            return 0
    
    def clear_expired_notifications(self, current_time: str) -> int:
        """Clear expired notifications"""
        try:
            cursor = self.conn.execute('''
                DELETE FROM notifications WHERE expires_at < ?
            ''', (current_time,))
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            self.logger.error(f"Error clearing expired notifications: {e}")
            return 0
    
    def get_notification_settings(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get notification settings for user"""
        try:
            row = self.conn.execute('''
                SELECT * FROM notification_settings WHERE user_id = ?
            ''', (user_id,)).fetchone()
            
            if row:
                settings = dict(row)
                settings['types'] = json.loads(settings['types'])
                settings['quiet_hours'] = json.loads(settings['quiet_hours'])
                return settings
            return None
        except Exception as e:
            self.logger.error(f"Error getting notification settings: {e}")
            return None
    
    def update_notification_settings(self, user_id: str, settings: Dict[str, Any]) -> bool:
        """Update notification settings for user"""
        try:
            self.conn.execute('''
                INSERT OR REPLACE INTO notification_settings (
                    user_id, enabled, sound_enabled, vibration_enabled, types, quiet_hours
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id, settings['enabled'], settings['sound_enabled'],
                settings['vibration_enabled'], json.dumps(settings['types']),
                json.dumps(settings['quiet_hours'])
            ))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error updating notification settings: {e}")
            return False
    
    def get_notification_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get notification statistics for user"""
        try:
            stats = self.conn.execute('''
                SELECT 
                    COUNT(*) as total_notifications,
                    COUNT(CASE WHEN read = 1 THEN 1 END) as read_notifications,
                    COUNT(CASE WHEN dismissed = 1 THEN 1 END) as dismissed_notifications,
                    COUNT(CASE WHEN priority = 'critical' THEN 1 END) as critical_count,
                    COUNT(CASE WHEN priority = 'high' THEN 1 END) as high_count,
                    COUNT(CASE WHEN priority = 'medium' THEN 1 END) as medium_count,
                    COUNT(CASE WHEN priority = 'low' THEN 1 END) as low_count
                FROM notifications WHERE user_id = ?
            ''', (user_id,)).fetchone()
            
            stats_dict = dict(stats)
            stats_dict["notifications_by_priority"] = {
                "critical": stats_dict.get("critical_count", 0),
                "high": stats_dict.get("high_count", 0),
                "medium": stats_dict.get("medium_count", 0),
                "low": stats_dict.get("low_count", 0)
            }
            return stats_dict
        except Exception as e:
            self.logger.error(f"Error getting notification statistics: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed")

# Global database instance
db = MallDatabase()

# Database utility functions
def create_backup():
    """Create a database backup"""
    return db.backup_database()

def restore_from_backup(backup_path: str):
    """Restore database from backup"""
    return db.restore_database(backup_path)

def optimize_database():
    """Optimize database performance"""
    return db.optimize_database()

def get_database_health():
    """Get database health information"""
    return db.get_database_stats()

def cleanup_expired_data():
    """Clean up expired data"""
    expired_sessions = db.cleanup_expired_sessions()
    return {
        'expired_sessions_cleaned': expired_sessions,
        'timestamp': datetime.now().isoformat()
    } 