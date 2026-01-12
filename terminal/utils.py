def format_route_display(route):
    if not route:
        return "Unassigned route"

    origin = getattr(route, "origin", "")
    destination = getattr(route, "destination", "")
    if origin and destination:
        return f"{origin} → {destination}"

    name = getattr(route, "name", "")
    if name:
        return name

    return str(route)
