# Database Schema Analysis and Enhancement Plan

## Overview

This document analyzes the current database schema for the Deerfields Mall Gamification System and provides a comprehensive enhancement plan to meet all requirements.

## Current Database State

### ✅ **Existing Tables (from database.py)**
1. **users** - User management with basic fields
2. **receipts** - Receipt storage with AI verification
3. **missions** - Mission system with progress tracking
4. **companions** - Companion system
5. **stores** - Store information
6. **user_activities** - Activity logging
7. **admin_logs** - Admin action logging
8. **support_tickets** - Support ticket system
9. **environment_3d** - 3D environment data
10. **invites** - Invitation system

### ✅ **Existing Tables (from security_module.py)**
1. **security_audit_log** - Security event logging
2. **rate_limits** - Rate limiting data
3. **mfa_settings** - Multi-factor authentication settings
4. **mfa_attempts** - MFA verification attempts

## Required Tables Analysis

### ✅ **Already Implemented**
- ✅ **users** - Enhanced with additional fields needed
- ✅ **receipts** - Enhanced with status and verification
- ✅ **missions** - Enhanced with type and status
- ✅ **security_audit_log** - Enhanced with severity levels
- ✅ **rate_limits** - Enhanced with window management

### ❌ **Missing Tables**
1. **achievements** - Achievement system
2. **user_sessions** - Session management
3. **migrations** - Database migration tracking

## Required Indexes Analysis

### ✅ **Already Implemented**
- ✅ **idx_users_email** - User email lookup
- ✅ **idx_receipts_user_id** - Receipt user lookup
- ✅ **idx_missions_user_id** - Mission user lookup
- ✅ **idx_security_log_user** - Security log user lookup
- ✅ **idx_rate_limit_ip_endpoint** - Rate limit lookup

### ❌ **Missing Indexes**
1. **idx_receipt_date** - Receipt date sorting
2. **idx_mission_user_status** - Mission status filtering
3. **idx_achievements_user_id** - Achievement user lookup
4. **idx_sessions_user_id** - Session user lookup
5. **idx_sessions_token** - Session token lookup

## Enhancement Plan

### 1. **Missing Tables to Create**

#### **achievements Table**
```sql
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
);
```

#### **user_sessions Table**
```sql
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
);
```

#### **migrations Table**
```sql
CREATE TABLE IF NOT EXISTS migrations (
    migration_id TEXT PRIMARY KEY,
    version TEXT NOT NULL,
    description TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. **Missing Indexes to Create**

```sql
-- Receipt indexes
CREATE INDEX IF NOT EXISTS idx_receipt_date ON receipts(created_at);
CREATE INDEX IF NOT EXISTS idx_receipts_status ON receipts(status);
CREATE INDEX IF NOT EXISTS idx_receipts_store ON receipts(store_name);

-- Mission indexes
CREATE INDEX IF NOT EXISTS idx_mission_user_status ON missions(user_id, status);
CREATE INDEX IF NOT EXISTS idx_missions_type ON missions(mission_type);
CREATE INDEX IF NOT EXISTS idx_missions_expires ON missions(expires_at);

-- Achievement indexes
CREATE INDEX IF NOT EXISTS idx_achievements_user_id ON achievements(user_id);
CREATE INDEX IF NOT EXISTS idx_achievements_type ON achievements(achievement_type);
CREATE INDEX IF NOT EXISTS idx_achievements_earned ON achievements(earned_at);

-- Session indexes
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(token_hash);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_sessions_active ON user_sessions(is_active);

-- Security indexes
CREATE INDEX IF NOT EXISTS idx_security_log_action ON security_audit_log(action);
CREATE INDEX IF NOT EXISTS idx_security_log_timestamp ON security_audit_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_security_log_ip ON security_audit_log(ip_address);

-- Rate limit indexes
CREATE INDEX IF NOT EXISTS idx_rate_limit_window ON rate_limits(window_start);

-- Activity indexes
CREATE INDEX IF NOT EXISTS idx_activities_user_id ON user_activities(user_id);
CREATE INDEX IF NOT EXISTS idx_activities_type ON user_activities(activity_type);
CREATE INDEX IF NOT EXISTS idx_activities_created ON user_activities(created_at);
```

### 3. **Missing Columns to Add**

#### **users Table Enhancements**
```sql
ALTER TABLE users ADD COLUMN vip_points INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN total_spent REAL DEFAULT 0.0;
ALTER TABLE users ADD COLUMN total_purchases INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN visited_categories TEXT;  -- JSON array
ALTER TABLE users ADD COLUMN achievement_points INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN social_score INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN friends TEXT;  -- JSON array
ALTER TABLE users ADD COLUMN team_id TEXT;
ALTER TABLE users ADD COLUMN leaderboard_position INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN social_achievements TEXT;  -- JSON array
ALTER TABLE users ADD COLUMN event_participation TEXT;  -- JSON object
ALTER TABLE users ADD COLUMN seasonal_progress TEXT;  -- JSON object
ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en';
```

#### **receipts Table Enhancements**
```sql
ALTER TABLE receipts ADD COLUMN category TEXT;
ALTER TABLE receipts ADD COLUMN status TEXT DEFAULT 'pending';
ALTER TABLE receipts ADD COLUMN verified_at TIMESTAMP;
```

#### **missions Table Enhancements**
```sql
ALTER TABLE missions ADD COLUMN difficulty TEXT DEFAULT 'normal';
ALTER TABLE missions ADD COLUMN personalized BOOLEAN DEFAULT FALSE;
```

## Security Enhancements

### 1. **Parameterized Queries**
All database operations should use parameterized queries to prevent SQL injection:

```python
# ✅ Secure - Parameterized query
cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))

# ❌ Insecure - String concatenation
cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
```

### 2. **Input Validation**
Implement comprehensive input validation:

```python
def validate_user_input(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize user input"""
    validated = {}
    
    # Validate user_id
    if 'user_id' in user_data:
        user_id = str(user_data['user_id']).strip()
        if len(user_id) > 50:
            raise ValueError("User ID too long")
        validated['user_id'] = user_id
    
    # Validate email
    if 'email' in user_data:
        email = str(user_data['email']).strip().lower()
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError("Invalid email format")
        validated['email'] = email
    
    # Validate amount
    if 'amount' in user_data:
        try:
            amount = float(user_data['amount'])
            if amount <= 0 or amount > 100000:
                raise ValueError("Invalid amount")
            validated['amount'] = amount
        except (ValueError, TypeError):
            raise ValueError("Invalid amount format")
    
    return validated
```

### 3. **Column Whitelisting**
Implement column whitelisting for updates:

```python
def update_user_safe(self, user_id: str, updates: Dict[str, Any]) -> bool:
    """Safely update user with parameterized queries and column whitelisting"""
    # Whitelist allowed columns
    allowed_columns = {
        'name', 'email', 'phone', 'coins', 'xp', 'level', 'vip_tier', 
        'vip_points', 'login_streak', 'total_spent', 'language'
    }
    
    filtered_updates = {k: v for k, v in updates.items() if k in allowed_columns}
    
    if not filtered_updates:
        return False
    
    set_clause = ', '.join([f"{k} = ?" for k in filtered_updates.keys()])
    query = f"UPDATE users SET {set_clause} WHERE user_id = ?"
    values = list(filtered_updates.values()) + [user_id]
    
    self.conn.execute(query, values)
    self.conn.commit()
    return True
```

## Migration System

### 1. **Migration Table Structure**
```sql
CREATE TABLE migrations (
    migration_id TEXT PRIMARY KEY,
    version TEXT NOT NULL,
    description TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. **Migration Management**
```python
def run_migrations(self):
    """Run database migrations"""
    # Get applied migrations
    cursor = self.conn.execute("SELECT version FROM migrations")
    applied_migrations = {row['version'] for row in cursor.fetchall()}
    
    # Define migrations
    migrations = [
        {
            'version': '1.0.0',
            'description': 'Initial schema creation'
        },
        {
            'version': '1.1.0',
            'description': 'Add achievements table',
            'sql': 'CREATE TABLE IF NOT EXISTS achievements (...)'
        },
        # ... more migrations
    ]
    
    # Apply pending migrations
    for migration in migrations:
        if migration['version'] not in applied_migrations:
            if migration.get('sql'):
                self.conn.execute(migration['sql'])
            
            # Record migration
            self.conn.execute('''
                INSERT INTO migrations (migration_id, version, description)
                VALUES (?, ?, ?)
            ''', (str(uuid.uuid4()), migration['version'], migration['description']))
            
            self.conn.commit()
```

## Backup and Recovery

### 1. **Backup Procedures**
```python
def backup_database(self, backup_path: str = None) -> bool:
    """Create a backup of the database"""
    try:
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_mall_gamification_{timestamp}.db"
        
        # Close connection
        self.conn.close()
        
        # Copy database file
        shutil.copy2(self.db_path, backup_path)
        
        # Reopen connection
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        return True
    except Exception as e:
        self.logger.error(f"Error creating backup: {e}")
        return False
```

### 2. **Recovery Procedures**
```python
def restore_database(self, backup_path: str) -> bool:
    """Restore database from backup"""
    try:
        if not os.path.exists(backup_path):
            return False
        
        # Create current backup before restore
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        current_backup = f"pre_restore_backup_{timestamp}.db"
        shutil.copy2(self.db_path, current_backup)
        
        # Restore from backup
        shutil.copy2(backup_path, self.db_path)
        
        return True
    except Exception as e:
        self.logger.error(f"Error restoring database: {e}")
        return False
```

## Performance Optimizations

### 1. **Database Optimization**
```python
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
        return True
    except Exception as e:
        self.logger.error(f"Error optimizing database: {e}")
        return False
```

### 2. **Query Optimization**
- Use appropriate indexes for frequently queried columns
- Implement pagination for large result sets
- Use LIMIT clauses to prevent excessive data retrieval
- Implement caching for frequently accessed data

## Implementation Status

### ✅ **Completed**
- Basic table structure exists
- Some indexes are implemented
- Basic CRUD operations
- Security module integration

### 🔄 **In Progress**
- Schema enhancement
- Missing tables creation
- Index optimization
- Security hardening

### ❌ **Pending**
- Migration system implementation
- Backup/recovery procedures
- Performance optimization
- Comprehensive testing

## Next Steps

### 1. **Immediate Actions**
1. Create missing tables (achievements, user_sessions, migrations)
2. Add missing indexes for performance
3. Add missing columns to existing tables
4. Implement migration system

### 2. **Security Enhancements**
1. Implement parameterized queries everywhere
2. Add input validation and sanitization
3. Implement column whitelisting
4. Add audit logging for all operations

### 3. **Performance Optimizations**
1. Create all required indexes
2. Implement query optimization
3. Add database optimization procedures
4. Implement caching strategies

### 4. **Backup and Recovery**
1. Implement automated backup procedures
2. Create recovery procedures
3. Test backup and restore functionality
4. Document backup/recovery processes

### 5. **Testing and Validation**
1. Create comprehensive test suite
2. Test all CRUD operations
3. Test security features
4. Test performance under load
5. Test backup and recovery procedures

## Conclusion

The current database schema is well-structured but needs enhancements to meet all requirements. The main areas for improvement are:

1. **Missing Tables**: achievements, user_sessions, migrations
2. **Missing Indexes**: Performance optimization indexes
3. **Missing Columns**: Enhanced user and receipt tracking
4. **Security**: Parameterized queries and input validation
5. **Performance**: Query optimization and caching
6. **Reliability**: Backup and recovery procedures

Once these enhancements are implemented, the database will be production-ready with enterprise-level security, performance, and reliability features. 