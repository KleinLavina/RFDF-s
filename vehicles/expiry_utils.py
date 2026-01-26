# vehicles/expiry_utils.py
"""
Centralized expiry calculation utilities for vehicles and drivers.
Single source of truth for expiry status across all views.
"""
from datetime import date, timedelta
from django.utils import timezone


# =====================================================
# CONFIGURATION
# =====================================================
EXPIRY_WARNING_DAYS = 30  # Days before expiry to show warning


# =====================================================
# EXPIRY STATUS CONSTANTS
# =====================================================
class ExpiryStatus:
    VALID = 'valid'
    NEAR_EXPIRY = 'near_expiry'
    EXPIRED = 'expired'
    NO_DATE = 'no_date'


# =====================================================
# CORE EXPIRY CALCULATION
# =====================================================
def get_expiry_status(expiry_date):
    """
    Calculate expiry status for any date field.
    
    Args:
        expiry_date: date object or None
        
    Returns:
        tuple: (status, days_remaining, message)
        - status: ExpiryStatus constant
        - days_remaining: int or None
        - message: str (user-friendly message)
    """
    if not expiry_date:
        return (ExpiryStatus.NO_DATE, None, "No expiry date")
    
    today = date.today()
    days_remaining = (expiry_date - today).days
    
    if days_remaining < 0:
        return (
            ExpiryStatus.EXPIRED,
            days_remaining,
            "Expired – Renew Required"
        )
    elif days_remaining <= EXPIRY_WARNING_DAYS:
        return (
            ExpiryStatus.NEAR_EXPIRY,
            days_remaining,
            "Near Expiry – Renew Soon"
        )
    else:
        return (
            ExpiryStatus.VALID,
            days_remaining,
            "Valid"
        )


# =====================================================
# VEHICLE EXPIRY
# =====================================================
def get_vehicle_expiry_info(vehicle):
    """
    Get expiry information for a vehicle.
    Uses registration_expiry as the authoritative field.
    
    Args:
        vehicle: Vehicle model instance
        
    Returns:
        dict: {
            'status': ExpiryStatus constant,
            'days_remaining': int or None,
            'message': str,
            'expiry_date': date or None,
            'is_expired': bool,
            'is_near_expiry': bool,
            'needs_alert': bool
        }
    """
    status, days_remaining, message = get_expiry_status(vehicle.registration_expiry)
    
    return {
        'status': status,
        'days_remaining': days_remaining,
        'message': message,
        'expiry_date': vehicle.registration_expiry,
        'is_expired': status == ExpiryStatus.EXPIRED,
        'is_near_expiry': status == ExpiryStatus.NEAR_EXPIRY,
        'needs_alert': status in [ExpiryStatus.EXPIRED, ExpiryStatus.NEAR_EXPIRY]
    }


# =====================================================
# DRIVER EXPIRY
# =====================================================
def get_driver_expiry_info(driver):
    """
    Get expiry information for a driver.
    Uses license_expiry as the authoritative field.
    
    Args:
        driver: Driver model instance
        
    Returns:
        dict: {
            'status': ExpiryStatus constant,
            'days_remaining': int or None,
            'message': str,
            'expiry_date': date or None,
            'is_expired': bool,
            'is_near_expiry': bool,
            'needs_alert': bool
        }
    """
    status, days_remaining, message = get_expiry_status(driver.license_expiry)
    
    return {
        'status': status,
        'days_remaining': days_remaining,
        'message': message,
        'expiry_date': driver.license_expiry,
        'is_expired': status == ExpiryStatus.EXPIRED,
        'is_near_expiry': status == ExpiryStatus.NEAR_EXPIRY,
        'needs_alert': status in [ExpiryStatus.EXPIRED, ExpiryStatus.NEAR_EXPIRY]
    }


# =====================================================
# BULK PROCESSING
# =====================================================
def annotate_vehicles_with_expiry(vehicles):
    """
    Add expiry information to a queryset or list of vehicles.
    
    Args:
        vehicles: QuerySet or list of Vehicle instances
        
    Returns:
        list: Vehicles with added 'expiry_info' attribute
    """
    result = []
    for vehicle in vehicles:
        vehicle.expiry_info = get_vehicle_expiry_info(vehicle)
        result.append(vehicle)
    return result


def annotate_drivers_with_expiry(drivers):
    """
    Add expiry information to a queryset or list of drivers.
    
    Args:
        drivers: QuerySet or list of Driver instances
        
    Returns:
        list: Drivers with added 'expiry_info' attribute
    """
    result = []
    for driver in drivers:
        driver.expiry_info = get_driver_expiry_info(driver)
        result.append(driver)
    return result


# =====================================================
# TEMPLATE FILTERS (Optional - for direct use in templates)
# =====================================================
def get_expiry_css_class(status):
    """
    Get CSS class for expiry status.
    
    Args:
        status: ExpiryStatus constant
        
    Returns:
        str: CSS class name
    """
    if status == ExpiryStatus.EXPIRED:
        return 'expiry-expired'
    elif status == ExpiryStatus.NEAR_EXPIRY:
        return 'expiry-near'
    elif status == ExpiryStatus.VALID:
        return 'expiry-valid'
    else:
        return 'expiry-none'
