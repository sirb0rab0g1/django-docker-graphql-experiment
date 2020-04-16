ROLE_ADMIN = 'admin'
ROLE_UNIT_OWNER = 'unit-owner'
ROLE_RESTAURANT = 'restaurant'
ROLE_SECURITY = 'security'
ROLE_BUILDING_MANAGER = 'building-manager'
ROLE_BUILDING_ENGINEER = 'building-engineer'
ROLE_CHOICES = (
    (ROLE_ADMIN, 'Admin'),
    (ROLE_UNIT_OWNER, 'Unit Owner'),
    (ROLE_RESTAURANT, 'Restaurant'),
    (ROLE_SECURITY, 'Security'),
    (ROLE_BUILDING_MANAGER, 'Building Manager'),
    (ROLE_BUILDING_ENGINEER, 'Building Engineer'),
)

PAYMENT_CASH = 'cash'
PAYMENT_CHECK = 'check'
PAYMENT_CARD = 'ccard'
PAYMENT_CHOICES = (
    (PAYMENT_CASH, 'Cash'),
    (PAYMENT_CHECK, 'Check'),
    (PAYMENT_CARD, 'Credit Card'),
)
