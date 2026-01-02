class DetectHealthAnomalyUseCase:
    """
    Pure evaluation use case (بدون ذخیره)
    """
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def execute(self, input_dto):
        return {"fever": self.analyzer.is_fever(input_dto.temperature), "severe": self.analyzer.is_severe(input_dto.temperature)}
