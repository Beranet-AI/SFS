res = requests.post(url, json=data)

if res.status_code == 403:
    logger.warning(
        "Telemetry rejected: device not approved",
        extra={"deviceId": data["deviceId"]}
    )
    disable_device(data["deviceId"])

