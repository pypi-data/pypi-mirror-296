def device_exists(self, devices, device_id):
        for device in devices:
            if device.device_id == device_id:
                return True
        return False