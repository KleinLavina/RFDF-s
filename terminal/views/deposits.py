from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, DecimalField, OuterRef, Q, Subquery, Sum
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from accounts.utils import is_staff_admin_or_admin
from terminal.models import SystemSettings
from vehicles.models import Deposit, Driver, Vehicle, Wallet


@login_required(login_url='accounts:login')
@user_passes_test(is_staff_admin_or_admin)
@never_cache
def deposit_menu(request):
    settings = SystemSettings.get_solo()
    min_deposit = settings.min_deposit_amount
    wallet_search = request.GET.get("search_query", "").strip()
    wallet_sort = request.GET.get("wallet_sort", "newest").lower()
    if wallet_sort not in ("newest", "largest", "smallest", "driver_asc", "driver_desc"):
        wallet_sort = "newest"

    driver_qs = Driver.objects.filter(vehicles__isnull=False).distinct().prefetch_related("vehicles").order_by("last_name", "first_name")

    driver_options = []
    for driver in driver_qs:
        full_name = f"{driver.first_name} {driver.last_name}"
        license_text = driver.license_number or driver.driver_id or ""
        for vehicle in driver.vehicles.all():
            driver_options.append({
                "vehicle_id": vehicle.id,
                "license_plate": vehicle.license_plate,
                "driver_name": full_name,
                "license_number": license_text,
                "display": f"{full_name} · {vehicle.license_plate}",
            })

    wallets_qs = Wallet.objects.select_related("vehicle__assigned_driver").annotate(
        last_deposit_amount=Subquery(
            Deposit.objects.filter(wallet=OuterRef("pk"))
            .order_by("-created_at")
            .values("amount")[:1],
            output_field=DecimalField(max_digits=12, decimal_places=2),
        ),
        last_deposit_at=Subquery(
            Deposit.objects.filter(wallet=OuterRef("pk"))
            .order_by("-created_at")
            .values("created_at")[:1]
        ),
        deposit_count=Count("deposits"),
    )

    if wallet_search:
        wallets_qs = wallets_qs.filter(
            Q(vehicle__license_plate__icontains=wallet_search)
            | Q(vehicle__assigned_driver__first_name__icontains=wallet_search)
            | Q(vehicle__assigned_driver__last_name__icontains=wallet_search)
            | Q(vehicle__assigned_driver__license_number__icontains=wallet_search)
            | Q(vehicle__assigned_driver__driver_id__icontains=wallet_search)
        )

    if wallet_sort == "largest":
        ordering = ["-last_deposit_amount", "-last_deposit_at"]
    elif wallet_sort == "smallest":
        ordering = ["last_deposit_amount", "-last_deposit_at"]
    elif wallet_sort == "driver_asc":
        ordering = [
            "vehicle__assigned_driver__last_name",
            "vehicle__assigned_driver__first_name",
            "-last_deposit_at",
        ]
    elif wallet_sort == "driver_desc":
        ordering = [
            "-vehicle__assigned_driver__last_name",
            "-vehicle__assigned_driver__first_name",
            "-last_deposit_at",
        ]
    else:
        ordering = ["-last_deposit_at", "-updated_at"]

    wallets_count = wallets_qs.count()
    wallets_sorted = wallets_qs.order_by(*ordering)
    wallets = wallets_sorted[:80]

    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle_id")
        amount_str = request.POST.get("amount", "").strip()

        if not vehicle_id or not amount_str:
            messages.error(request, "⚠️ Please fill in all required fields.")
            return redirect('terminal:deposit_menu')

        try:
            amount = Decimal(amount_str)
        except:
            messages.error(request, "❌ Invalid deposit amount.")
            return redirect('terminal:deposit_menu')

        if amount <= 0:
            messages.error(request, "⚠️ Deposit amount must be greater than zero.")
            return redirect('terminal:deposit_menu')

        vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        if not vehicle:
            messages.error(request, "❌ Vehicle not found.")
            return redirect('terminal:deposit_menu')

        wallet, _ = Wallet.objects.get_or_create(vehicle=vehicle)
        Deposit.objects.create(wallet=wallet, amount=amount)

        messages.success(request, f"✅ Successfully deposited ₱{amount} to {vehicle.license_plate}.")
        return redirect('terminal:deposit_menu')

    toast_messages = [msg.message for msg in messages.get_messages(request)]

    context = {
        "min_deposit": min_deposit,
        "wallets": wallets,
        "wallets_total": wallets_count,
        "wallet_sort": wallet_sort,
        "wallet_search": wallet_search,
        "driver_options": driver_options,
        "toast_messages": toast_messages,
    }
    return render(request, "terminal/deposit_menu.html", context)


@login_required(login_url='accounts:login')
@user_passes_test(is_staff_admin_or_admin)
@never_cache
def deposit_history(request):
    history_sort = request.GET.get("history_sort", "newest").lower()
    if history_sort not in ("newest", "largest", "smallest", "driver_asc", "driver_desc"):
        history_sort = "newest"
    history_query = request.GET.get("history_query", "").strip()

    deposits = Deposit.objects.select_related("wallet__vehicle__assigned_driver")

    if history_query:
        deposits = deposits.filter(
            Q(wallet__vehicle__license_plate__icontains=history_query)
            | Q(wallet__vehicle__assigned_driver__first_name__icontains=history_query)
            | Q(wallet__vehicle__assigned_driver__last_name__icontains=history_query)
            | Q(wallet__vehicle__assigned_driver__license_number__icontains=history_query)
            | Q(wallet__vehicle__assigned_driver__driver_id__icontains=history_query)
        )

    if history_sort == "largest":
        ordering = ["-amount", "-created_at"]
    elif history_sort == "smallest":
        ordering = ["amount", "-created_at"]
    elif history_sort == "driver_asc":
        ordering = [
            "wallet__vehicle__assigned_driver__last_name",
            "wallet__vehicle__assigned_driver__first_name",
            "-created_at",
        ]
    elif history_sort == "driver_desc":
        ordering = [
            "-wallet__vehicle__assigned_driver__last_name",
            "-wallet__vehicle__assigned_driver__first_name",
            "-created_at",
        ]
    else:
        ordering = ["-created_at"]

    deposits = deposits.order_by(*ordering)
    total_amount = deposits.aggregate(Sum("amount"))["amount__sum"] or 0
    total_count = deposits.count()

    context = {
        "history_deposits": deposits[:200],
        "history_sort": history_sort,
        "history_query": history_query,
        "total_amount": total_amount,
        "total_count": total_count,
    }
    return render(request, "terminal/deposit_history.html", context)


@login_required(login_url='accounts:login')
@user_passes_test(is_staff_admin_or_admin)
@never_cache
def deposits(request):
    """Unified deposit management page with wallets and history."""
    import json
    
    settings = SystemSettings.get_solo()
    min_deposit = settings.min_deposit_amount
    
    # Get tab parameter
    active_tab = request.GET.get("tab", "wallets")
    
    # Driver options for modal
    driver_qs = Driver.objects.filter(vehicles__isnull=False).distinct().prefetch_related("vehicles").order_by("last_name", "first_name")
    driver_options = []
    for driver in driver_qs:
        full_name = f"{driver.first_name} {driver.last_name}"
        license_text = driver.license_number or driver.driver_id or ""
        for vehicle in driver.vehicles.all():
            driver_options.append({
                "vehicle_id": vehicle.id,
                "license_plate": vehicle.license_plate,
                "driver_name": full_name,
                "license_number": license_text,
                "display": f"{full_name} · {vehicle.license_plate}",
            })
    
    # WALLETS TAB DATA
    wallet_search = request.GET.get("search_query", "").strip()
    wallet_sort = request.GET.get("wallet_sort", "newest").lower()
    if wallet_sort not in ("newest", "largest", "smallest", "driver_asc", "driver_desc"):
        wallet_sort = "newest"
    
    wallets_qs = Wallet.objects.select_related("vehicle__assigned_driver").annotate(
        last_deposit_amount=Subquery(
            Deposit.objects.filter(wallet=OuterRef("pk"))
            .order_by("-created_at")
            .values("amount")[:1],
            output_field=DecimalField(max_digits=12, decimal_places=2),
        ),
        last_deposit_at=Subquery(
            Deposit.objects.filter(wallet=OuterRef("pk"))
            .order_by("-created_at")
            .values("created_at")[:1]
        ),
        deposit_count=Count("deposits"),
    )
    
    if wallet_search:
        wallets_qs = wallets_qs.filter(
            Q(vehicle__license_plate__icontains=wallet_search)
            | Q(vehicle__assigned_driver__first_name__icontains=wallet_search)
            | Q(vehicle__assigned_driver__last_name__icontains=wallet_search)
            | Q(vehicle__assigned_driver__license_number__icontains=wallet_search)
            | Q(vehicle__assigned_driver__driver_id__icontains=wallet_search)
        )
    
    if wallet_sort == "largest":
        ordering = ["-balance", "-last_deposit_at"]
    elif wallet_sort == "smallest":
        ordering = ["balance", "-last_deposit_at"]
    elif wallet_sort == "driver_asc":
        ordering = [
            "vehicle__assigned_driver__last_name",
            "vehicle__assigned_driver__first_name",
            "-last_deposit_at",
        ]
    elif wallet_sort == "driver_desc":
        ordering = [
            "-vehicle__assigned_driver__last_name",
            "-vehicle__assigned_driver__first_name",
            "-last_deposit_at",
        ]
    else:
        ordering = ["-last_deposit_at", "-updated_at"]
    
    wallets_count = wallets_qs.count()
    wallets_sorted = wallets_qs.order_by(*ordering)
    wallets = wallets_sorted[:80]
    
    # Wallet stats
    total_balance = wallets_qs.aggregate(Sum("balance"))["balance__sum"] or 0
    low_balance_count = wallets_qs.filter(balance__lt=min_deposit).count()
    total_deposits_count = Deposit.objects.count()
    
    # HISTORY TAB DATA
    history_sort = request.GET.get("history_sort", "newest").lower()
    if history_sort not in ("newest", "largest", "smallest", "driver_asc", "driver_desc"):
        history_sort = "newest"
    history_query = request.GET.get("history_query", "").strip()
    
    deposits_qs = Deposit.objects.select_related("wallet__vehicle__assigned_driver")
    
    if history_query:
        deposits_qs = deposits_qs.filter(
            Q(wallet__vehicle__license_plate__icontains=history_query)
            | Q(wallet__vehicle__assigned_driver__first_name__icontains=history_query)
            | Q(wallet__vehicle__assigned_driver__last_name__icontains=history_query)
            | Q(wallet__vehicle__assigned_driver__license_number__icontains=history_query)
            | Q(wallet__vehicle__assigned_driver__driver_id__icontains=history_query)
        )
    
    if history_sort == "largest":
        ordering = ["-amount", "-created_at"]
    elif history_sort == "smallest":
        ordering = ["amount", "-created_at"]
    elif history_sort == "driver_asc":
        ordering = [
            "wallet__vehicle__assigned_driver__last_name",
            "wallet__vehicle__assigned_driver__first_name",
            "-created_at",
        ]
    elif history_sort == "driver_desc":
        ordering = [
            "-wallet__vehicle__assigned_driver__last_name",
            "-wallet__vehicle__assigned_driver__first_name",
            "-created_at",
        ]
    else:
        ordering = ["-created_at"]
    
    deposits_sorted = deposits_qs.order_by(*ordering)
    history_total = deposits_sorted.aggregate(Sum("amount"))["amount__sum"] or 0
    history_count = deposits_sorted.count()
    history_deposits = deposits_sorted[:200]
    
    # HANDLE POST (Add Deposit)
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle_id")
        amount_str = request.POST.get("amount", "").strip()
        
        if not vehicle_id or not amount_str:
            messages.error(request, "⚠️ Please fill in all required fields.")
            return redirect('terminal:deposits')
        
        try:
            amount = Decimal(amount_str)
        except:
            messages.error(request, "❌ Invalid deposit amount.")
            return redirect('terminal:deposits')
        
        if amount <= 0:
            messages.error(request, "⚠️ Deposit amount must be greater than zero.")
            return redirect('terminal:deposits')
        
        vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        if not vehicle:
            messages.error(request, "❌ Vehicle not found.")
            return redirect('terminal:deposits')
        
        wallet, _ = Wallet.objects.get_or_create(vehicle=vehicle)
        Deposit.objects.create(wallet=wallet, amount=amount)
        
        messages.success(request, f"✅ Successfully deposited ₱{amount} to {vehicle.license_plate}.")
        return redirect('terminal:deposits')
    
    context = {
        "min_deposit": min_deposit,
        "wallets": wallets,
        "wallets_total": wallets_count,
        "wallet_sort": wallet_sort,
        "wallet_search": wallet_search,
        "total_balance": total_balance,
        "low_balance_count": low_balance_count,
        "total_deposits": total_deposits_count,
        "driver_options": json.dumps(driver_options),
        "history_deposits": history_deposits,
        "history_sort": history_sort,
        "history_query": history_query,
        "history_total": history_total,
        "history_count": history_count,
        "active_tab": active_tab,
    }
    return render(request, "terminal/deposits.html", context)
