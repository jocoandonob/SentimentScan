import hashlib
import logging

logger = logging.getLogger(__name__)

def generate_device_fingerprint(request):
    """
    Generate a device fingerprint from request information.
    
    Args:
        request: Flask request object
        
    Returns:
        str: Device fingerprint hash
    """
    # Get user agent
    user_agent = request.headers.get('User-Agent', '')
    
    # Get accept language
    accept_language = request.headers.get('Accept-Language', '')
    
    # Create a fingerprint from combined data
    fingerprint_base = f"{user_agent}|{accept_language}"
    
    # Hash the fingerprint
    fingerprint = hashlib.sha256(fingerprint_base.encode()).hexdigest()
    
    logger.debug(f"Generated fingerprint: {fingerprint}")
    return fingerprint

def get_client_ip(request):
    """
    Get client IP from request.
    
    Args:
        request: Flask request object
        
    Returns:
        str: Client IP address
    """
    # Check for X-Forwarded-For header first (behind proxy)
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        # Otherwise, use the remote address
        ip = request.remote_addr or "127.0.0.1"
    
    logger.debug(f"Client IP: {ip}")
    return ip


def check_usage_limit(user_usage, max_usage=7):
    """
    Check if user has reached usage limit.
    
    Args:
        user_usage: UserUsage model instance
        max_usage: Maximum allowed usage
        
    Returns:
        dict: Status information with keys:
            - allowed: bool, Whether user is allowed to use the service
            - remaining: int, Number of remaining uses
            - used: int, Number of used attempts
            - max: int, Maximum allowed usage
    """
    if not user_usage:
        return {
            "allowed": True,
            "remaining": max_usage,
            "used": 0,
            "max": max_usage
        }
    
    remaining = max(0, max_usage - user_usage.usage_count)
    allowed = user_usage.usage_count < max_usage
    
    return {
        "allowed": allowed,
        "remaining": remaining,
        "used": user_usage.usage_count,
        "max": max_usage
    }