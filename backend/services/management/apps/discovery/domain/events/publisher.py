class DomainEventPublisher:
    """
    Simple in-memory domain event dispatcher.
    Can be replaced later with Celery / Kafka / MQTT.
    """

    def publish(self, event):
        self.handle(event)

    def handle(self, event):
        # placeholder
        pass
