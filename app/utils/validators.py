from datetime import datetime, time, timedelta

def validate_operating_hours(opening_time: time, closing_time: time):
    """function to ensure closing time is at least 1 hour after opening."""
    if opening_time and opening_time.tzinfo is not None:
        raise ValueError("Timezone-aware times are not supported for opening_time. Please use naive time (e.g., '06:00:00').")
    if closing_time and closing_time.tzinfo is not None:
        raise ValueError("Timezone-aware times are not supported for closing_time. Please use naive time (e.g., '18:00:00').")

    if not opening_time or not closing_time:
        return

    dummy_date = datetime.today()
    opened_at = datetime.combine(dummy_date, opening_time)
    closed_at = datetime.combine(dummy_date, closing_time)

    if closed_at <= opened_at:
        raise ValueError("Closing time must be after opening time")

    if (closed_at - opened_at) < timedelta(hours=1):
        raise ValueError("Branch must be open for at least 1 hour")

def validate_lab_visit_fields(cls, values):
    from app.Enum.LaboratoryFacilityType import LaboratoryFacilityType
    facility_type = values.facility_type
    
    if facility_type != LaboratoryFacilityType.INTERNAL:
        raise ValueError("Lab visits can currently only be created for internal laboratories.")
        
    required_fields = [
        values.visited_date,
        values.visit_time,
        values.name,
        values.email,
        values.speciality,
        values.from_facility,
        values.notes
    ]
    if not all(field is not None for field in required_fields):
        raise ValueError("All lab visit fields (visited_date, visit_time, name, email, speciality, from_facility, notes) are required for internal facility type.")

    return values