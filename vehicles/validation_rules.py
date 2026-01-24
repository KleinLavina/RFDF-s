# vehicles/validation_rules.py
"""
Single source of truth for driver registration validation rules.
Used by both frontend (via template context) and backend (Django forms).
"""

DRIVER_VALIDATION_RULES = {
    'first_name': {
        'required': True,
        'min_length': 2,
        'max_length': 50,
        'pattern': r'^[a-zA-Z\s\-\.]+$',
        'placeholder': 'Enter first name',
        'label': 'First Name',
        'icon': 'fa-signature',
        'error_messages': {
            'required': '❌ First name is required.',
            'min_length': '❌ First name must be at least 2 characters.',
            'max_length': '❌ First name cannot exceed 50 characters.',
            'invalid': '❌ First name contains invalid characters. Use only letters, spaces, hyphens, and periods.',
        }
    },
    'middle_name': {
        'required': False,
        'max_length': 50,
        'pattern': r'^[a-zA-Z\s\-\.]*$',
        'placeholder': 'Enter middle name (optional)',
        'label': 'Middle Name',
        'icon': 'fa-signature',
        'error_messages': {
            'max_length': '❌ Middle name cannot exceed 50 characters.',
            'invalid': '❌ Middle name contains invalid characters.',
        }
    },
    'last_name': {
        'required': True,
        'min_length': 2,
        'max_length': 50,
        'pattern': r'^[a-zA-Z\s\-\.]+$',
        'placeholder': 'Enter last name',
        'label': 'Last Name',
        'icon': 'fa-signature',
        'error_messages': {
            'required': '❌ Last name is required.',
            'min_length': '❌ Last name must be at least 2 characters.',
            'max_length': '❌ Last name cannot exceed 50 characters.',
            'invalid': '❌ Last name contains invalid characters. Use only letters, spaces, hyphens, and periods.',
        }
    },
    'suffix': {
        'required': False,
        'max_length': 10,
        'placeholder': 'e.g., Jr., Sr., III',
        'label': 'Suffix',
        'icon': 'fa-text-height',
        'error_messages': {
            'max_length': '❌ Suffix cannot exceed 10 characters.',
        }
    },
    'birth_date': {
        'required': True,
        'type': 'date',
        'min_age': 18,
        'max_age': 100,
        'label': 'Birth Date',
        'icon': 'fa-birthday-cake',
        'error_messages': {
            'required': '❌ Birth date is required.',
            'invalid': '❌ Invalid date format.',
            'min_age': '❌ Driver must be at least 18 years old.',
            'max_age': '❌ Invalid birth date.',
        }
    },
    'birth_place': {
        'required': True,
        'min_length': 3,
        'max_length': 100,
        'placeholder': 'City/Municipality, Province',
        'label': 'Birth Place',
        'icon': 'fa-map-marker-alt',
        'error_messages': {
            'required': '❌ Birth place is required.',
            'min_length': '❌ Birth place must be at least 3 characters.',
            'max_length': '❌ Birth place cannot exceed 100 characters.',
        }
    },
    'blood_type': {
        'required': True,
        'type': 'select',
        'choices': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'N/A'],
        'label': 'Blood Type',
        'icon': 'fa-tint',
        'error_messages': {
            'required': '❌ Blood type is required.',
            'invalid_choice': '❌ Invalid blood type selected.',
        }
    },
    'mobile_number': {
        'required': True,
        'pattern': r'^(\+639|09)\d{9}$',
        'placeholder': 'e.g., 09123456789 or +639123456789',
        'label': 'Mobile Number',
        'icon': 'fa-mobile-alt',
        'help_text': 'Format: 09123456789 or +639123456789',
        'error_messages': {
            'required': '❌ Mobile number is required.',
            'invalid': '❌ Invalid mobile number format. Use 09XXXXXXXXX or +639XXXXXXXXX.',
        }
    },
    'email': {
        'required': True,
        'type': 'email',
        'max_length': 100,
        'placeholder': 'e.g., juan.delacruz@example.com',
        'label': 'Email Address',
        'icon': 'fa-envelope',
        'error_messages': {
            'required': '❌ Email address is required.',
            'invalid': '❌ Invalid email format.',
            'max_length': '❌ Email cannot exceed 100 characters.',
        }
    },
    'street': {
        'required': True,
        'min_length': 3,
        'max_length': 100,
        'placeholder': 'e.g., 123 Main Street',
        'label': 'Street',
        'icon': 'fa-road',
        'error_messages': {
            'required': '❌ Street address is required.',
            'min_length': '❌ Street address must be at least 3 characters.',
            'max_length': '❌ Street address cannot exceed 100 characters.',
        }
    },
    'barangay': {
        'required': True,
        'min_length': 3,
        'max_length': 100,
        'placeholder': 'e.g., Barangay 123',
        'label': 'Barangay',
        'icon': 'fa-map-pin',
        'error_messages': {
            'required': '❌ Barangay is required.',
            'min_length': '❌ Barangay must be at least 3 characters.',
            'max_length': '❌ Barangay cannot exceed 100 characters.',
        }
    },
    'zip_code': {
        'required': True,
        'pattern': r'^\d{4}$',
        'placeholder': 'e.g., 1000',
        'label': 'ZIP Code',
        'icon': 'fa-mail-bulk',
        'help_text': '4-digit ZIP code',
        'error_messages': {
            'required': '❌ ZIP code is required.',
            'invalid': '❌ ZIP code must be exactly 4 digits.',
        }
    },
    'city_municipality': {
        'required': True,
        'min_length': 3,
        'max_length': 100,
        'placeholder': 'e.g., Manila, Quezon City',
        'label': 'City / Municipality',
        'icon': 'fa-city',
        'error_messages': {
            'required': '❌ City/Municipality is required.',
            'min_length': '❌ City/Municipality must be at least 3 characters.',
            'max_length': '❌ City/Municipality cannot exceed 100 characters.',
        }
    },
    'province': {
        'required': True,
        'min_length': 3,
        'max_length': 100,
        'placeholder': 'e.g., Metro Manila, Bulacan',
        'label': 'Province',
        'icon': 'fa-map',
        'error_messages': {
            'required': '❌ Province is required.',
            'min_length': '❌ Province must be at least 3 characters.',
            'max_length': '❌ Province cannot exceed 100 characters.',
        }
    },
    'license_number': {
        'required': True,
        'min_length': 5,
        'max_length': 25,
        'pattern': r'^[A-Z0-9\-]+$',
        'placeholder': 'Enter license number',
        'label': 'License Number',
        'icon': 'fa-file-alt',
        'help_text': 'Enter your driver\'s license number (minimum 5 characters)',
        'error_messages': {
            'required': '❌ License number is required.',
            'min_length': '❌ License number must be at least 5 characters.',
            'max_length': '❌ License number cannot exceed 25 characters.',
            'invalid': '❌ License number can only contain letters, numbers, and hyphens (no spaces or symbols).',
            'unique': '❌ Driver license number is already registered.',
        }
    },
    'license_expiry': {
        'required': True,
        'type': 'date',
        'min_date': 'today',
        'label': 'License Expiry',
        'icon': 'fa-calendar-times',
        'error_messages': {
            'required': '❌ License expiry date is required.',
            'invalid': '❌ Invalid date format.',
            'expired': '❌ License has expired. Please renew before registering.',
        }
    },
    'license_type': {
        'required': True,
        'readonly': True,
        'default': 'Professional Driver\'s License',
        'label': 'License Type',
        'icon': 'fa-car',
        'help_text': 'Only professional licenses accepted',
        'error_messages': {
            'required': '❌ License type is required.',
        }
    },
    'emergency_contact_name': {
        'required': True,
        'min_length': 3,
        'max_length': 100,
        'placeholder': 'Full name of emergency contact',
        'label': 'Contact Name',
        'icon': 'fa-user-friends',
        'error_messages': {
            'required': '❌ Emergency contact name is required.',
            'min_length': '❌ Contact name must be at least 3 characters.',
            'max_length': '❌ Contact name cannot exceed 100 characters.',
        }
    },
    'emergency_contact_number': {
        'required': True,
        'pattern': r'^(\+639|09)\d{9}$',
        'placeholder': 'e.g., 09123456789 or +639123456789',
        'label': 'Contact Number',
        'icon': 'fa-phone',
        'help_text': 'Format: 09123456789 or +639123456789',
        'error_messages': {
            'required': '❌ Emergency contact number is required.',
            'invalid': '❌ Invalid phone number format. Use 09XXXXXXXXX or +639XXXXXXXXX.',
            'same_as_driver': '⚠️ Emergency contact should be different from driver\'s number.',
        }
    },
    'emergency_contact_relationship': {
        'required': True,
        'min_length': 3,
        'max_length': 50,
        'placeholder': 'e.g., Spouse, Parent, Sibling',
        'label': 'Relationship',
        'icon': 'fa-heart',
        'error_messages': {
            'required': '❌ Relationship is required.',
            'min_length': '❌ Relationship must be at least 3 characters.',
            'max_length': '❌ Relationship cannot exceed 50 characters.',
        }
    },
    'driver_photo': {
        'required': True,
        'type': 'image',
        'max_size_mb': 5,
        'accepted_formats': ['image/jpeg', 'image/jpg', 'image/png'],
        'label': 'Driver Photo',
        'icon': 'fa-camera',
        'error_messages': {
            'required': '❌ Driver photo is required for identity verification.',
            'invalid': '❌ Invalid image file.',
            'missing': '❌ No photo was uploaded.',
            'empty': '❌ The uploaded photo file is empty.',
            'too_large': '❌ Photo is too large. Maximum 5MB allowed.',
            'invalid_format': '❌ Invalid file type. Must be an image (JPEG, JPG, or PNG).',
        }
    },
}


def get_field_rules(field_name):
    """Get validation rules for a specific field."""
    return DRIVER_VALIDATION_RULES.get(field_name, {})


def get_all_rules():
    """Get all validation rules."""
    return DRIVER_VALIDATION_RULES


def get_frontend_validation_config():
    """
    Generate frontend-compatible validation configuration.
    Returns a dictionary that can be serialized to JSON for JavaScript.
    """
    config = {}
    for field_name, rules in DRIVER_VALIDATION_RULES.items():
        config[field_name] = {
            'required': rules.get('required', False),
            'minLength': rules.get('min_length'),
            'maxLength': rules.get('max_length'),
            'pattern': rules.get('pattern'),
            'type': rules.get('type', 'text'),
            'errors': rules.get('error_messages', {})
        }
    return config
