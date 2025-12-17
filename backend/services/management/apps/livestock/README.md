apps/livestock/
├── domain/
│   ├── entities.py
│   │   ├── Animal
│   │   │   - id
│   │   │   - tag_id
│   │   │   - species
│   │   │   - birth_date
│   │   │   - status
│   │   │
│   │   └── Herd
│   │       - id
│   │       - farm_id
│   │
│   ├── value_objects.py
│   │   ├── AnimalId
│   │   ├── Age
│   │   ├── Species
│   │   └── HealthScore
│   │
│   └── rules.py
│       ├── can_mark_inactive()
│       └── is_production_age()
│
├── application/
│   ├── services.py
│   │   └── LivestockService
│   │       - register_animal()
│   │       - assign_device()
│   │       - update_health_score()
│   │
│   └── use_cases.py
│       ├── RegisterAnimal
│       ├── AssignDeviceToAnimal
│       └── UpdateAnimalHealth
│
├── infrastructure/
│   ├── models.py
│   │   ├── AnimalModel
│   │   └── HerdModel
│   │
│   ├── repositories.py
│   │   └── LivestockRepository
│   │
│   └── migrations/
│
├── api/
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── admin.py
└── apps.py
