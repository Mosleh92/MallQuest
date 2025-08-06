from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import uuid

from database import db


@dataclass
class Voucher:
    """Represents a stored voucher record."""

    code: str
    value: float
    user_id: Optional[str]
    status: str
    issued_at: datetime
    expires_at: Optional[datetime]
    redeemed_at: Optional[datetime]


class VoucherSystem:
    """Manages voucher issuance, redemption, and tracking"""

    def __init__(self):
        self.conn = db.conn
        self._create_tables()

    def _create_tables(self) -> None:
        """Create voucher tables if they do not exist"""
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS vouchers (
                code TEXT PRIMARY KEY,
                value REAL NOT NULL,
                user_id TEXT,
                status TEXT NOT NULL,
                issued_at TIMESTAMP NOT NULL,
                expires_at TIMESTAMP,
                redeemed_at TIMESTAMP
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS voucher_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voucher_code TEXT NOT NULL,
                action TEXT NOT NULL,
                user_id TEXT,
                performed_by TEXT,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    # -----------------------------
    # Internal helpers
    # -----------------------------
    def _log_action(self, voucher_code: str, action: str, user_id: Optional[str] = None,
                    performed_by: Optional[str] = None, details: Optional[str] = None) -> None:
        """Record voucher actions for auditing"""
        self.conn.execute(
            """INSERT INTO voucher_audit (voucher_code, action, user_id, performed_by, details)
                VALUES (?, ?, ?, ?, ?)""",
            (voucher_code, action, user_id, performed_by, details),
        )
        self.conn.commit()

    # -----------------------------
    # Voucher operations
    # -----------------------------
    def issue_voucher(
        self,
        value: float,
        user_id: Optional[str] = None,
        expires_in_days: Optional[int] = None,
        performed_by: Optional[str] = None,
    ) -> str:
        """Create a new voucher and return its code"""
        code = uuid.uuid4().hex[:12].upper()
        issued_at = datetime.utcnow()
        expires_at = (
            issued_at + timedelta(days=expires_in_days) if expires_in_days is not None else None
        )
        self.conn.execute(
            """INSERT INTO vouchers (code, value, user_id, status, issued_at, expires_at)
                VALUES (?, ?, ?, 'issued', ?, ?)""",
            (code, value, user_id, issued_at, expires_at),
        )
        self.conn.commit()
        self._log_action(code, "issued", user_id, performed_by)
        return code

    def redeem_voucher(
        self, code: str, user_id: str, performed_by: Optional[str] = None
    ) -> Dict[str, Optional[str]]:
        """Redeem an issued voucher"""
        cur = self.conn.execute(
            "SELECT * FROM vouchers WHERE code = ?", (code,)
        )
        row = cur.fetchone()
        if not row:
            self._log_action(code, "redeem_failed", user_id, performed_by, "not_found")
            return {"success": False, "error": "Voucher not found"}
        if row["status"] == "redeemed":
            self._log_action(code, "redeem_failed", user_id, performed_by, "already_redeemed")
            return {"success": False, "error": "Voucher already redeemed"}
        if row["expires_at"] and datetime.fromisoformat(row["expires_at"]) < datetime.utcnow():
            self._log_action(code, "redeem_failed", user_id, performed_by, "expired")
            return {"success": False, "error": "Voucher expired"}

        redeemed_at = datetime.utcnow()
        self.conn.execute(
            """UPDATE vouchers SET status = 'redeemed', user_id = ?, redeemed_at = ? WHERE code = ?""",
            (user_id, redeemed_at, code),
        )
        self.conn.commit()
        self._log_action(code, "redeemed", user_id, performed_by)
        return {"success": True, "value": row["value"]}

    def get_voucher(self, code: str) -> Optional[Dict[str, any]]:
        """Fetch voucher details"""
        cur = self.conn.execute(
            "SELECT * FROM vouchers WHERE code = ?", (code,)
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def validate_voucher(self, code: str, performed_by: Optional[str] = None) -> Dict[str, any]:
        """Check if a voucher is valid for redemption"""
        voucher = self.get_voucher(code)
        if not voucher:
            self._log_action(code, "lookup_failed", performed_by=performed_by)
            return {"valid": False, "reason": "Voucher not found"}
        if voucher["status"] == "redeemed":
            self._log_action(code, "lookup_failed", performed_by=performed_by, details="redeemed")
            return {"valid": False, "reason": "Voucher already redeemed"}
        if voucher["expires_at"] and datetime.fromisoformat(voucher["expires_at"]) < datetime.utcnow():
            self._log_action(code, "lookup_failed", performed_by=performed_by, details="expired")
            return {"valid": False, "reason": "Voucher expired"}
        self._log_action(code, "lookup_success", performed_by=performed_by)
        return {"valid": True, "value": voucher["value"]}

    def list_vouchers(self, status: Optional[str] = None) -> List[Dict[str, any]]:
        """List vouchers, optionally filtered by status"""
        query = "SELECT * FROM vouchers"
        params: List[str] = []
        if status:
            query += " WHERE status = ?"
            params.append(status)
        cur = self.conn.execute(query, params)
        return [dict(row) for row in cur.fetchall()]

    def get_audit_logs(self, limit: int = 100) -> List[Dict[str, any]]:
        """Retrieve recent voucher audit logs"""
        cur = self.conn.execute(
            "SELECT * FROM voucher_audit ORDER BY timestamp DESC LIMIT ?", (limit,)
        )
        return [dict(row) for row in cur.fetchall()]


# Global instance
voucher_system = VoucherSystem()
