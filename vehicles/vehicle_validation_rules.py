# vehicles/vehicle_validation_rules.py
"""
Single source of truth for vehicle registration validation rules.
Used by both frontend (via template context) and backend (Django forms).
"""

VEHICLE_VALIDATION_RULES = {
    'vehicle_name': {
        'required': False,
        'max_length': 100,
        'placeholder': 'e.g., Toyota Grandia 2023',
        'label': 'Vehicle Name',
        'icon': 'fa-car',
        'help_text': 'Optional: Enter the vehicle model and make',
        'error_messages': {
            'max_length': '❌ Vehicle name cannot exceed 100 characters.',
        }
    },
    'vehicle_type': {
        'required': True,
        'type': 'select',
        'label': 'Vehicle Type',
        'icon': 'fa-truck-pickup',
        'help_text': 'Select the type of vehicle',
        'error_messages': {
            'required': '❌ Vehicle type is required.',
            'invalid_choice': '❌ Invalid vehicle type selected.',
        }
    },
    'ownership_type': {
        'required': True,
        'type': 'select',
        'label': 'Ownership Type',
        'icon': 'fa-key',
        'help_text': 'Select the ownership type',
        'error_messages': {
            'required': '❌ Ownership type is required.',
            'invalid_choice': '❌ Invalid ownership type selected.',
        }
    },
    'assigned_driver': {
        'required': True,
        'type': 'select',
        'label': 'Assigned Driver',
        'icon': 'fa-id-card-alt',
        'help_text': 'Search and select the driver assigned to this vehicle',
        'error_messages': {
            'required': '❌ Assigned driver is required.',
            'invalid_choice': '❌ Invalid driver selected.',
        }
    },
    'route': {
        'required': False,
        'type': 'select',
        'label': 'Route',
        'icon': 'fa-route',
        'help_text': 'Optional: Select the regular route for this vehicle',
        'error_messages': {
            'invalid_choice': '❌ Invalid route selected.',
        }
    },
    'seat_capacity': {
        'required': False,
        'type': 'number',
        'min_value': 1,
        'max_value': 100,
        'placeholder': 'e.g., 12',
        'label': 'Seat Capacity',
        'icon': 'fa-users',
        'help_text': 'Optional: Enter the maximum number of passengers',
        'error_messages': {
            'invalid': '❌ Invalid seat capacity.',
            'min_value': '❌ Seat capacity must be at least 1.',
            'max_value': '❌ Seat capacity cannot exceed 100.',
        }
    },
    'cr_number': {
        'required': True,
        'min_length': 5,
        'max_length': 50,
        'pattern': r'^\d+$',
        'placeholder': 'e.g., 123456789012',
        'label': 'CR Number',
        'icon': 'fa-file-certificate',
        'help_text': 'Enter the Certificate of Registration number (digits only)',
        'error_messages': {
            'required': '❌ CR (Certificate of Registration) number is required.',
            'min_length': '❌ CR number is too short. Minimum 5 characters required.',
            'max_length': '❌ CR number is too long. Maximum 50 characters allowed.',
            'invalid': '❌ CR number must contain digits only (no spaces or special characters).',
            'unique': '❌ This CR number is already registered in the system.',
        }
    },
    'or_number': {
        'required': True,
        'min_length': 5,
        'max_length': 50,
        'pattern': r'^\d+$',
        'placeholder': 'e.g., 123456789012',
        'label': 'OR Number',
        'icon': 'fa-receipt',
        'help_text': 'Enter the Official Receipt number (digits only)',
        'error_messages': {
            'required': '❌ OR (Official Receipt) number is required.',
            'min_length': '❌ OR number is too short. Minimum 5 characters required.',
            'max_length': '❌ OR number is too long. Maximum 50 characters allowed.',
            'invalid': '❌ OR number must contain digits only (no spaces or special characters).',
            'unique': '❌ This OR number is already registered in the system.',
        }
    },
    'vin_number': {
        'required': True,
        'length': 17,
        'pattern': r'^[A-HJ-NPR-Z0-9]{17}$',
        'placeholder': 'e.g., JT2BF22K1W0123456',
        'label': 'VIN Number',
        'icon': 'fa-barcode',
        'help_text': 'Enter the 17-character Vehicle Identification Number (no I, O, Q)',
        'error_messages': {
            'required': '❌ VIN (Vehicle Identification Number) is required.',
            'invalid': '❌ Invalid VIN format. VIN must be exactly 17 characters (excluding I, O, Q).',
            'unique': '❌ This VIN is already registered in the system.',
        }
    },
    'year_model': {
        'required': True,
        'type': 'number',
        'min_value': 1886,
        'max_value': None,  # Will be set to current_year + 1
        'label': 'Year Model',
        'icon': 'fa-calendar-alt',
        'help_text': 'Select the vehicle\'s manufacturing year',
        'error_messages': {
            'required': '❌ Year model is required.',
            'invalid': '❌ Invalid year format. Please enter a valid year.',
            'min_value': '❌ Invalid year. Vehicles didn\'t exist before 1886.',
            'max_value': '❌ Invalid year. Year cannot be in the future.',
        }
    },
    'registration_number': {
        'required': True,
        'min_length': 5,
        'max_length': 50,
        'pattern': r'^[A-Z0-9\-]+$',
        'placeholder': 'e.g., NX123456',
        'label': 'Registration Number',
        'icon': 'fa-hashtag',
        'help_text': 'Enter the vehicle\'s registration number',
        'error_messages': {
            'required': '❌ Registration number is required.',
            'min_length': '❌ Registration number is too short. Minimum 5 characters required.',
            'max_length': '❌ Registration number is too long. Maximum 50 characters allowed.',
            'invalid': '❌ Registration number can only contain letters, numbers, and hyphens (no spaces or symbols).',
            'unique': '❌ This registration number is already registered to another vehicle.',
        }
    },
    'registration_expiry': {
        'required': True,
        'type': 'date',
        'min_date': 'today',
        'label': 'Registration Expiry',
        'icon': 'fa-calendar-times',
        'help_text': 'Select the registration expiry date (must be valid)',
        'error_messages': {
            'required': '❌ Registration expiry date is required.',
            'invalid': '❌ Invalid date format.',
            'expired': '❌ Registration has expired. Please renew before registering.',
        }
    },
    'license_plate': {
        'required': True,
        'min_length': 2,
        'max_length': 12,
        'pattern': r'^[A-Z0-9][A-Z0-9\s\-]{1,11}$',
        'placeholder': 'e.g., ABC 123',
        'label': 'License Plate',
        'icon': 'fa-rectangle-list',
        'help_text': 'Enter the vehicle\'s license plate number',
        'error_messages': {
            'required': '❌ License plate is required.',
            'min_length': '❌ License plate is too short. Minimum 2 characters required.',
            'max_length': '❌ License plate is too long. Maximum 12 characters allowed.',
            'invalid': '❌ Invalid license plate format. Use only letters, numbers, spaces, or hyphens.',
            'unique': '❌ This license plate is already registered to another vehicle.',
        }
    },
}


def get_vehicle_field_rules(field_name):
    """Get validation rules for a specific vehicle field."""
    return VEHICLE_VALIDATION_RULES.get(field_name, {})


def get_all_vehicle_rules():
    """Get all vehicle validation rules."""
    return VEHICLE_VALIDATION_RULES


def get_vehicle_frontend_validation_config():
    """
    Generate frontend-compatible validation configuration for vehicles.
    Returns a dictionary that can be serialized to JSON for JavaScript.
    """
    config = {}
    for field_name, rules in VEHICLE_VALIDATION_RULES.items():
        config[field_name] = {
            'required': rules.get('required', False),
            'minLength': rules.get('min_length'),
            'maxLength': rules.get('max_length'),
            'length': rules.get('length'),
            'pattern': rules.get('pattern'),
            'type': rules.get('type', 'text'),
            'minValue': rules.get('min_value'),
            'maxValue': rules.get('max_value'),
            'errors': rules.get('error_messages', {})
        }
    return config
