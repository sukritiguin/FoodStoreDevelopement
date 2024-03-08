

def detectUser(user):
    if user.role == 1:
        return 'vendorDashboard'
    if user.role == 2:
        return 'customerDashboard'
    if user.role == None and user.is_superadmin:
        return '/admin'