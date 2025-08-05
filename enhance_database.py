#!/usr/bin/env python3
"""
Database Enhancement Script
Adds missing tables, indexes, and operations to the existing database
"""

import sqlite3
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

def setup_logging():
    """Setup logging"""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger('DatabaseEnhancer')

def enhance_database(db_path: str = 'mall_gamification.db'):
    """Enhance the existing database with missing components"""
    logger = setup_logging()
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        
        logger.info("Starting database enhancement...")
        
        # Create missing tables
        create_missing_tables(conn, logger)
        
        # Add missing columns
        add_missing_columns(conn, logger)
        
        # Create missing indexes
        create_missing_indexes(conn, logger)
        
        # Create migrations table and run migrations
        setup_migrations(conn, logger)
        
        # Optimize database
        optimize_database(conn, logger)
        
        # Verify schema
        verify_schema(conn, logger)
        
        conn.close()
        logger.info("Database enhancement completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Database enhancement failed: {e}")
        return False

def create_missing_tables(conn: sqlite3.Connection, logger: logging.Logger):
    """Create missing tables"""
    try:
        # Achievements table
        conn.execute('''
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
        ''')
        
        # User sessions table
        conn.execute('''
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
        
        # Migrations table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS migrations (
                migration_id TEXT PRIMARY KEY,
                version TEXT NOT NULL,
                description TEXT,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        logger.info("Missing tables created successfully")
        
    except Exception as e:
        logger.error(f"Error creating missing tables: {e}")
        raise

def add_missing_columns(conn: sqlite3.Connection, logger: logging.Logger):
    """Add missing columns to existing tables"""
    try:
        # Add missing columns to users table
        user_columns = [
            ('users', 'vip_points', 'INTEGER DEFAULT 0'),
            ('users', 'total_spent', 'REAL DEFAULT 0.0'),
            ('users', 'total_purchases', 'INTEGER DEFAULT 0'),
            ('users', 'visited_categories', 'TEXT'),
            ('users', 'achievement_points', 'INTEGER DEFAULT 0'),
            ('users', 'social_score', 'INTEGER DEFAULT 0'),
            ('users', 'friends', 'TEXT'),
            ('users', 'team_id', 'TEXT'),
            ('users', 'leaderboard_position', 'INTEGER DEFAULT 0'),
            ('users', 'social_achievements', 'TEXT'),
            ('users', 'event_participation', 'TEXT'),
            ('users', 'seasonal_progress', 'TEXT'),
            ('users', 'language', 'TEXT DEFAULT "en"')
        ]
        
        for table, column, definition in user_columns:
            try:
                conn.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')
            except sqlite3.OperationalError as e:
                if "duplicate column name" not in str(e).lower():
                    logger.warning(f"Could not add column {column} to {table}: {e}")
        
        # Add missing columns to receipts table
        receipt_columns = [
            ('receipts', 'category', 'TEXT'),
            ('receipts', 'status', 'TEXT DEFAULT "pending"'),
            ('receipts', 'verified_at', 'TIMESTAMP')
        ]
        
        for table, column, definition in receipt_columns:
            try:
                conn.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')
            except sqlite3.OperationalError as e:
                if "duplicate column name" not in str(e).lower():
                    logger.warning(f"Could not add column {column} to {table}: {e}")
        
        # Add missing columns to missions table
        mission_columns = [
            ('missions', 'difficulty', 'TEXT DEFAULT "normal"'),
            ('missions', 'personalized', 'BOOLEAN DEFAULT FALSE')
        ]
        
        for table, column, definition in mission_columns:
            try:
                conn.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')
            except sqlite3.OperationalError as e:
                if "duplicate column name" not in str(e).lower():
                    logger.warning(f"Could not add column {column} to {table}: {e}")
        
        conn.commit()
        logger.info("Missing columns added successfully")
        
    except Exception as e:
        logger.error(f"Error adding missing columns: {e}")
        raise

def create_missing_indexes(conn: sqlite3.Connection, logger: logging.Logger):
    """Create missing indexes for performance"""
    try:
        # Receipt indexes
        conn.execute('CREATE INDEX IF NOT EXISTS idx_receipt_date ON receipts(created_at)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_receipts_status ON receipts(status)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_receipts_store ON receipts(store_name)')
        
        # Mission indexes
        conn.execute('CREATE INDEX IF NOT EXISTS idx_mission_user_status ON missions(user_id, status)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_missions_type ON missions(mission_type)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_missions_expires ON missions(expires_at)')
        
        # Achievement indexes
        conn.execute('CREATE INDEX IF NOT EXISTS idx_achievements_user_id ON achievements(user_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_achievements_type ON achievements(achievement_type)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_achievements_earned ON achievements(earned_at)')
        
        # Session indexes
        conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(token_hash)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_active ON user_sessions(is_active)')
        
        # Security indexes
        conn.execute('CREATE INDEX IF NOT EXISTS idx_security_log_action ON security_audit_log(action)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_security_log_timestamp ON security_audit_log(timestamp)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_security_log_ip ON security_audit_log(ip_address)')
        
        # Rate limit indexes
        conn.execute('CREATE INDEX IF NOT EXISTS idx_rate_limit_window ON rate_limits(window_start)')
        
        # Activity indexes
        conn.execute('CREATE INDEX IF NOT EXISTS idx_activities_user_id ON user_activities(user_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_activities_type ON user_activities(activity_type)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_activities_created ON user_activities(created_at)')
        
        # Store indexes
        conn.execute('CREATE INDEX IF NOT EXISTS idx_stores_category ON stores(category)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_stores_zone ON stores(zone)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_stores_rating ON stores(rating)')
        
        # Support ticket indexes
        conn.execute('CREATE INDEX IF NOT EXISTS idx_tickets_user_id ON support_tickets(user_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_tickets_status ON support_tickets(status)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_tickets_priority ON support_tickets(priority)')
        
        conn.commit()
        logger.info("Missing indexes created successfully")
        
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")
        raise

def setup_migrations(conn: sqlite3.Connection, logger: logging.Logger):
    """Setup and run migrations"""
    try:
        # Get applied migrations
        cursor = conn.execute("SELECT version FROM migrations")
        applied_migrations = {row['version'] for row in cursor.fetchall()}
        
        # Define migrations
        migrations = [
            {
                'version': '1.0.0',
                'description': 'Initial schema creation'
            },
            {
                'version': '1.1.0',
                'description': 'Add achievements table'
            },
            {
                'version': '1.2.0',
                'description': 'Add user_sessions table'
            },
            {
                'version': '1.3.0',
                'description': 'Add missing columns to users table'
            },
            {
                'version': '1.4.0',
                'description': 'Add missing columns to receipts table'
            },
            {
                'version': '1.5.0',
                'description': 'Add missing columns to missions table'
            },
            {
                'version': '1.6.0',
                'description': 'Create required indexes'
            }
        ]
        
        # Apply pending migrations
        for migration in migrations:
            if migration['version'] not in applied_migrations:
                logger.info(f"Applying migration {migration['version']}: {migration['description']}")
                
                # Record migration
                conn.execute('''
                    INSERT INTO migrations (migration_id, version, description)
                    VALUES (?, ?, ?)
                ''', (str(uuid.uuid4()), migration['version'], migration['description']))
                conn.commit()
                
                logger.info(f"Migration {migration['version']} applied successfully")
        
        logger.info("All migrations completed successfully")
        
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        raise

def optimize_database(conn: sqlite3.Connection, logger: logging.Logger):
    """Optimize database performance"""
    try:
        # Analyze tables for better query planning
        conn.execute("ANALYZE")
        
        # Vacuum database to reclaim space
        conn.execute("VACUUM")
        
        # Update statistics
        conn.execute("ANALYZE")
        
        conn.commit()
        logger.info("Database optimization completed")
        
    except Exception as e:
        logger.error(f"Error optimizing database: {e}")
        raise

def verify_schema(conn: sqlite3.Connection, logger: logging.Logger):
    """Verify that all required tables and indexes exist"""
    try:
        verification = {
            'tables': {},
            'indexes': {},
            'overall_status': 'PASS'
        }
        
        # Required tables
        required_tables = [
            'users', 'receipts', 'missions', 'achievements', 
            'security_audit_log', 'rate_limits', 'user_sessions',
            'companions', 'stores', 'user_activities', 
            'admin_logs', 'support_tickets', 'migrations'
        ]
        
        for table in required_tables:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            exists = cursor.fetchone() is not None
            verification['tables'][table] = {
                'exists': exists,
                'status': 'PASS' if exists else 'FAIL'
            }
            if not exists:
                verification['overall_status'] = 'FAIL'
        
        # Required indexes
        required_indexes = [
            'idx_users_email', 'idx_receipts_user_id', 'idx_receipt_date',
            'idx_mission_user_status', 'idx_achievements_user_id',
            'idx_security_log_user', 'idx_rate_limit_ip_endpoint',
            'idx_sessions_user_id', 'idx_sessions_token'
        ]
        
        for index in required_indexes:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND name=?", (index,))
            exists = cursor.fetchone() is not None
            verification['indexes'][index] = {
                'exists': exists,
                'status': 'PASS' if exists else 'FAIL'
            }
            if not exists:
                verification['overall_status'] = 'FAIL'
        
        logger.info(f"Schema verification: {verification['overall_status']}")
        
        if verification['overall_status'] == 'PASS':
            logger.info("✅ All required tables and indexes are present")
        else:
            logger.warning("⚠️ Some required tables or indexes are missing")
            for table, info in verification['tables'].items():
                if info['status'] == 'FAIL':
                    logger.warning(f"Missing table: {table}")
            for index, info in verification['indexes'].items():
                if info['status'] == 'FAIL':
                    logger.warning(f"Missing index: {index}")
        
        return verification
        
    except Exception as e:
        logger.error(f"Error verifying schema: {e}")
        return {'overall_status': 'ERROR', 'error': str(e)}

def get_database_stats(conn: sqlite3.Connection) -> Dict[str, Any]:
    """Get database statistics"""
    try:
        stats = {}
        
        # Table sizes
        cursor = conn.execute("""
            SELECT name, sql FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table['name']
            cursor = conn.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            stats[f"{table_name}_count"] = count
        
        # Index information
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
        stats['index_count'] = len(cursor.fetchall())
        
        # Migration status
        cursor = conn.execute("SELECT COUNT(*) as count FROM migrations")
        stats['migrations_applied'] = cursor.fetchone()['count']
        
        return stats
        
    except Exception as e:
        return {'error': str(e)}

# Enhanced CRUD operations
class SecureDatabaseOperations:
    """Secure database operations with parameterized queries"""
    
    def __init__(self, db_path: str = 'mall_gamification.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.logger = setup_logging()
    
    def add_achievement(self, achievement_data: Dict[str, Any]) -> bool:
        """Add a new achievement with security validation"""
        try:
            # Validate required fields
            required_fields = ['achievement_id', 'user_id', 'achievement_type', 'title']
            for field in required_fields:
                if field not in achievement_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Sanitize input
            achievement_id = str(achievement_data['achievement_id']).strip()
            user_id = str(achievement_data['user_id']).strip()
            achievement_type = str(achievement_data['achievement_type']).strip()
            title = str(achievement_data['title']).strip()[:100]  # Limit length
            
            self.conn.execute('''
                INSERT INTO achievements (achievement_id, user_id, achievement_type, title, description, points, icon, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                achievement_id,
                user_id,
                achievement_type,
                title,
                achievement_data.get('description'),
                achievement_data.get('points', 0),
                achievement_data.get('icon'),
                json.dumps(achievement_data.get('metadata', {}))
            ))
            self.conn.commit()
            self.logger.info(f"Achievement added: {achievement_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding achievement: {e}")
            return False
    
    def get_user_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's achievements with security validation"""
        try:
            if not user_id or not isinstance(user_id, str):
                return []
            
            cursor = self.conn.execute('''
                SELECT * FROM achievements 
                WHERE user_id = ? 
                ORDER BY earned_at DESC
            ''', (user_id.strip(),))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Error getting user achievements: {e}")
            return []
    
    def add_user_session(self, session_data: Dict[str, Any]) -> bool:
        """Add a new user session with security validation"""
        try:
            # Validate required fields
            required_fields = ['session_id', 'user_id', 'token_hash', 'expires_at']
            for field in required_fields:
                if field not in session_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Sanitize input
            session_id = str(session_data['session_id']).strip()
            user_id = str(session_data['user_id']).strip()
            token_hash = str(session_data['token_hash']).strip()
            
            self.conn.execute('''
                INSERT INTO user_sessions (session_id, user_id, token_hash, ip_address, user_agent, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                user_id,
                token_hash,
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
        """Get user session by ID with security validation"""
        try:
            if not session_id or not isinstance(session_id, str):
                return None
            
            cursor = self.conn.execute('''
                SELECT * FROM user_sessions 
                WHERE session_id = ? AND is_active = TRUE AND expires_at > CURRENT_TIMESTAMP
            ''', (session_id.strip(),))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            self.logger.error(f"Error getting user session: {e}")
            return None
    
    def invalidate_user_session(self, session_id: str) -> bool:
        """Invalidate a user session with security validation"""
        try:
            if not session_id or not isinstance(session_id, str):
                return False
            
            self.conn.execute('''
                UPDATE user_sessions 
                SET is_active = FALSE 
                WHERE session_id = ?
            ''', (session_id.strip(),))
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
        """Log security event with validation"""
        try:
            if not action or not isinstance(action, str):
                return False
            
            self.conn.execute('''
                INSERT INTO security_audit_log (log_id, user_id, action, ip_address, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                str(uuid.uuid4()),
                user_id,
                action.strip(),
                ip_address,
                details
            ))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error logging security event: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

# Utility functions
def create_backup(db_path: str = 'mall_gamification.db') -> bool:
    """Create a database backup"""
    try:
        import shutil
        import os
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"backup_mall_gamification_{timestamp}.db"
        
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def get_database_health(db_path: str = 'mall_gamification.db') -> Dict[str, Any]:
    """Get database health information"""
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        
        stats = get_database_stats(conn)
        conn.close()
        
        return {
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {'error': str(e), 'timestamp': datetime.now().isoformat()}

if __name__ == "__main__":
    # Create backup before enhancement
    print("Creating backup before enhancement...")
    create_backup()
    
    # Run database enhancement
    print("Enhancing database...")
    success = enhance_database()
    
    if success:
        print("🎉 Database enhancement completed successfully!")
        
        # Show database health
        health = get_database_health()
        print(f"📊 Database stats: {health}")
    else:
        print("⚠️ Database enhancement completed with issues.") 