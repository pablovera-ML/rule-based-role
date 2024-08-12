class Shift:
    def __init__(self, day_of_week: str, shift_type: str) -> None:
        day_mapping = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}
        self.day_of_week = day_of_week
        self.shift_type = shift_type
        self.day_number = day_mapping[day_of_week]