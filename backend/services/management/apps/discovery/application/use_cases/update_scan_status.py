class UpdateScanStatusUseCase:

    def execute(self, *, edge_id: str, status_payload: dict):
        # فعلاً فقط log / future extension
        print(f"[SCAN STATUS] edge={edge_id} status={status_payload}")
