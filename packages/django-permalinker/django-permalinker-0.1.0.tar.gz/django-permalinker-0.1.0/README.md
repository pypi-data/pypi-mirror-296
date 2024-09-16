# Django Permalinker

`django_permalinker` is a Django application that provides an easy way to create, manage, and redirect permanent links (or permalinks). With customizable permalink ID generation, this app ensures that you have unique and efficient IDs to serve your redirecting needs.

## Features

- **Customizable Permalink ID Generation**: Adjust ID length, character set (uppercase, lowercase, digits), and more through Django settings.
- **Admin Interface**: Manage links via Django's admin panel.
- **404 Handling**: Automatically raise 404 errors for invalid or missing links.
- **Automatic Redirection**: Automatically redirect users to the destination URL based on the unique ID.

## Requirements

- Python: **3.10+**
- Django: **4+**

## Installation

1. Install the package:

```bash
pip install django-permalinker
```

2. Add `django_permalinker` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # Other apps
    'django_permalinker',
]
```

3. Include the `django_permalinker` URLs in your project’s `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # Other paths
    path("link/", include("django_permalinker.urls")),
]
```

4. Run migrations to create the necessary database tables:

```bash
python manage.py migrate
```

5. Start the Django development server:

```bash
python manage.py runserver
```

## Configuration

Customize the behavior of permalink ID generation in your Django project’s `settings.py` file:

- **PERMALINKER_ID_LENGTH**: Defines the length of the generated ID (default: 5).
- **PERMALINKER_ID_INCLUDE_UPPERCASE**: If set to `True`, uppercase letters will be included in the ID (default: `True`).
- **PERMALINKER_ID_INCLUDE_DIGITS**: If set to `True`, digits will be included in the ID (default: `True`).

Example:

```python
# settings.py

PERMALINKER_ID_LENGTH = 8  # Custom ID length
PERMALINKER_ID_INCLUDE_UPPERCASE = False  # Only lowercase letters
PERMALINKER_ID_INCLUDE_DIGITS = True  # Include digits
```

## Usage

### Creating and Managing Links

1. Access the **Django Admin** interface at `http://localhost:8000/admin/`.
2. Navigate to the **Permalinker** section and manage your links:
   - **Add New Link**: Create a new link with a destination URL, name, and description.
   - **List Links**: View all the existing links.
   - **Edit Existing Links**: Update or delete existing links.

### Redirecting

Once a link is created, you can access the link's permanent URL by visiting:

```
http://localhost:8000/link/<link_id>/
```

Django will handle the redirection to the destination URL automatically.

## Example

1. Create a new link in the admin panel:
   - **Name**: `Example link`
   - **Destination URL**: `https://example.com`
   
2. Access the permanent link:

```
http://localhost:8000/link/abc123/
```

You will be redirected to `https://example.com`.

## Screenshots

### 1. Admin: List Links View
View all the existing links in the Django admin.

![Admin: List Links View](img/admin-list-view.png)

### 2. Admin: Add New Link View
Create a new link by providing a name, destination URL, and description.

![Admin: Add New Link View](img/admin-add-view.png)

### 3. Admin: Edit Existing Link View
Edit an existing link’s details or delete it.

![Admin: Edit Existing Link View](img/admin-edit-view.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.