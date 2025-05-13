from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserUsage(db.Model):
    """Model to track user usage based on IP and device fingerprint"""
    
    __tablename__ = 'user_usage'
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)  # IPv6 can be up to 45 chars
    device_fingerprint = db.Column(db.String(64), nullable=False)
    usage_count = db.Column(db.Integer, default=0)
    last_used = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserUsage {self.ip_address}:{self.device_fingerprint} ({self.usage_count})>'

    @classmethod
    def get_or_create(cls, ip_address, device_fingerprint):
        """Get existing user usage record or create a new one"""
        usage = cls.query.filter_by(
            ip_address=ip_address,
            device_fingerprint=device_fingerprint
        ).first()
        
        if not usage:
            usage = cls(
                ip_address=ip_address,
                device_fingerprint=device_fingerprint,
                usage_count=0
            )
            db.session.add(usage)
            db.session.commit()
            
        return usage
    
    def increment_usage(self):
        """Increment usage count and update last_used timestamp"""
        self.usage_count += 1
        self.last_used = datetime.utcnow()
        db.session.commit()
        return self.usage_count
    
    def has_remaining_usage(self, max_usage=7):
        """Check if user has remaining usage"""
        return self.usage_count < max_usage