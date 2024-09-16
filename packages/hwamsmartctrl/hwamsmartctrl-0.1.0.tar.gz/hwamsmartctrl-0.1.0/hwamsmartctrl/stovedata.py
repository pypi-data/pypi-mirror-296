import datetime


class StoveData:
    def __init__(self):
        self.updating = None
        self.message_id = None
        self.phase = None
        self.night_lowering = None
        self.new_fire_wood_time = None
        self.burn_level = None
        self.operation_mode = None
        self.maintenance_alarms = None
        self.safety_alarms = None
        self.refill_alarm = None
        self.remote_refill_alarm = None
        self.time_since_remote_msg = None
        self.version = None
        self.remote_version = None
        self.wifi_version = None
        self.current_datetime = None
        self.night_begin_time = None
        self.night_end_time = None
        self.stove_temperature = None
        self.room_temperature = None
        self.oxygen_level = None
        self.valve1_position = None
        self.valve2_position = None
        self.valve3_position = None
        self.algorithm = None
        self.door_open = None
        self.service_date = None
        self.remote_refill_beeps = None


def stoveDataOf(json: dict) -> StoveData:
    data = StoveData()
    data.updating = json["updating"] == 1
    data.message_id = json["message_id"]
    data.phase = json["phase"]
    data.night_lowering = json["night_lowering"] == 1
    data.new_fire_wood_time = datetime.time(
        hour=json["new_fire_wood_hours"], minute=json["new_fire_wood_minutes"])
    data.burn_level = json["burn_level"]
    data.operation_mode = json["operation_mode"]
    data.maintenance_alarms = json["maintenance_alarms"]
    data.safety_alarms = json["safety_alarms"]
    data.refill_alarm = json["refill_alarm"]
    data.remote_refill_alarm = json["remote_refill_alarm"]
    data.time_since_remote_msg = json["time_since_remote_msg"]
    data.version = "%i.%i.%i" % (
        json["version_major"], json["version_minor"], json["version_build"])
    data.remote_version = "%i.%i.%i" % (json["remote_version_major"], json[
        "remote_version_minor"], json["remote_version_build"])
    data.wifi_version = "%i.%i.%i" % (json["wifi_version_major"], json[
        "wifi_version_minor"], json["wifi_version_build"])
    data.current_datetime = datetime.datetime(
        year=json["year"], month=json["month"], day=json["day"], hour=json["hours"], minute=json["minutes"], second=json["seconds"])
    data.night_begin_time = datetime.time(
        hour=json["night_begin_hour"], minute=json["night_begin_minute"])
    data.night_end_time = datetime.time(
        hour=json["night_end_hour"], minute=json["night_end_minute"])
    data.stove_temperature = json["stove_temperature"]
    data.room_temperature = json["room_temperature"]
    data.oxygen_level = json["oxygen_level"]
    data.valve1_position = json["valve1_position"]
    data.valve2_position = json["valve2_position"]
    data.valve3_position = json["valve3_position"]
    data.algorithm = json["algorithm"]
    data.door_open = json["door_open"] == 1
    data.service_date = datetime.datetime.strptime(
        json["service_date"], "%Y-%m-%d").date()
    data.remote_refill_beeps = json["remote_refill_beeps"]
    return data
