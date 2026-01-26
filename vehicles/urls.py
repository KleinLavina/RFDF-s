# vehicles/urls.py
from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    # ✅ Dedicated registration pages
    path('register-driver/', views.register_driver, name='register_driver'),
    path('register-vehicle/', views.register_vehicle, name='register_vehicle'),

    # ✅ Registered records
    path('registered/', views.registered_vehicles, name='registered_vehicles'),
    path('registered-drivers/', views.registered_drivers, name='registered_drivers'),
    
    # ✅ Detail/Profile pages
    path('driver/<int:driver_id>/', views.driver_detail, name='driver_detail'),
    path('vehicle/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),

    # ✅ QR / printable page (staff-only)
    path('vehicle/<int:vehicle_id>/qr/', views.vehicle_qr_view, name='vehicle_qr'),

    # ✅ AJAX / backend helpers
    path('ocr-process/', views.ocr_process, name='ocr_process'),
    path('ajax-register-driver/', views.ajax_register_driver, name='ajax_register_driver'),
    path('ajax-register-vehicle/', views.ajax_register_vehicle, name='ajax_register_vehicle'),
    path('get-wallet-balance/<int:driver_id>/', views.get_wallet_balance, name='get_wallet_balance'),
    path('ajax-deposit/', views.ajax_deposit, name='ajax_deposit'),
    path('get-by-driver/<int:driver_id>/', views.get_vehicles_by_driver, name='get_vehicles_by_driver'),

    path('drivers/edit-form/<int:driver_id>/', views.driver_edit_form, name='driver_edit_form'),
    path('drivers/edit/<int:driver_id>/', views.edit_driver, name='edit_driver'),
    path('vehicles/edit-form/<int:vehicle_id>/', views.vehicle_edit_form, name='vehicle_edit_form'),
    path('vehicles/edit/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('drivers/delete/<int:driver_id>/', views.delete_driver, name='delete_driver'),
    path('vehicles/delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),

    # ✅ QR Entry/Exit and Queue History
    path('qr-entry/', views.qr_entry, name='qr_entry'),
    path('qr-exit/', views.qr_exit, name='qr_exit'),
    path('queue-history/', views.queue_history, name='queue_history'),
]
