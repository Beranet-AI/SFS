backend/services/ai_decision/
├── app/
│   ├── domain/
│   │   ├── entities.py            # Prediction, FeatureVector
│   │   ├── value_objects.py       # ModelVersion, Confidence
│   │   └── rules.py               # "no prediction without min features"
│   │
│   ├── application/
│   │   ├── predict_use_case.py    # load model -> infer -> save result
│   │   ├── train_pipeline.py      # optional training jobs
│   │   └── feature_builder.py     # build features from telemetry
│   │
│   ├── infrastructure/
│   │   ├── model_registry.py      # انتخاب مدل فعال + نسخه
│   │   ├── data_loader.py         # گرفتن داده از TSDB/Management
│   │   ├── storage.py             # ذخیره predictionها (management یا db جدا)
│   │   └── clients/
│   │       ├── management_client.py
│   │       └── tsdb_client.py
│   │
│   ├── api/
│   │   ├── routes.py              # /predict
│   │   └── schemas.py
│   │
│   └── main.py
│
└── models/
    ├── mastitis/
    │   ├── v1/
    │   │   ├── model.onnx
    │   │   └── manifest.json
    │   └── v2/
    └── registry.json              # کدام مدل active است
