backend/services/management/apps/users/
├── admin.py
├── apps.py
├── managers.py
├── models.py
├── application/
│   └── use_cases/
│       ├── create_user/
│       │   ├── input_dto.py
│       │   ├── output_dto.py
│       │   └── use_case.py
│       ├── update_user/
│       │   ├── input_dto.py
│       │   ├── output_dto.py
│       │   └── use_case.py
│       └── delete_user/
│           ├── input_dto.py
│           ├── output_dto.py
│           └── use_case.py
├── domain/
│   ├── entities/
│   │   └── user.py
│   ├── value_objects/
│   │   └── email.py
│   ├── exceptions/
│   │   └── user_exceptions.py
│   ├── repositories/
│   │   └── user_repo.py
│   ├── domain_events/
│   ├── domain_services/
│   └── specifications/
├── api/
│   ├── forms/
│   │   ├── create_user_form.py
│   │   ├── update_user_form.py
│   │   └── delete_user_form.py
│   ├── serializers/
│   │   ├── create_user_serializer.py
│   │   ├── update_user_serializer.py
│   │   └── delete_user_serializer.py
│   ├── views/
│   │   ├── create_user_view.py
│   │   ├── update_user_view.py
│   │   └── delete_user_view.py
│   └── urls/
│       └── users_urls.py
└── infrastructure/
    ├── admin/
    │   └── users_admin.py
    ├── mappers/
    │   └── users_mapper.py
    ├── models/
    │   └── users_model.py
    ├── repositories/
    │   └── users_repo_imp.py
    └── migrations/
        └── 0001_initial.py
