from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.user.models import Account,Addresses,Country,State,City

class AccountAdmin(UserAdmin):
    # Customizing the admin interface for the Account model
    list_display = ('email', 'username', 'is_active', 'is_staff','is_verified')
    list_filter = ('is_active', 'is_staff',)
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'birth_date', 'bio', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('created_at', 'last_updated')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
        ),
    )
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('created_at', 'last_updated')
class AddressesAdmin(admin.ModelAdmin):
    list_display = ('user_id','zip_code','country','state','country','is_default','rest_of_address')
    search_fields = ('user_id__email', 'rest_of_address', 'city', 'state', 'zip_code', 'country')
    list_filter = ('is_default','country')
    ordering = ('user_id__email', 'city')
admin.site.register(Account, AccountAdmin)
admin.site.register(Addresses,AddressesAdmin)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)