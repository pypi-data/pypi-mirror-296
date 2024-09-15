def device_exists(devices, device_id):
        for device in devices:
            if device.device_id == device_id:
                return True
        return False