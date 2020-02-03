from django.contrib import auth

User = auth.get_user_model()


def _build_initial_user(data):
    user_field_names = '__all__'
    user_data = {}
    for field_name in user_field_names:
        if field_name in data:
            user_data[field_name] = data[field_name]
    user_class = User
    return user_class(**user_data)
