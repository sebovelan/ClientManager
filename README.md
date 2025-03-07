# Client Management API

This is a Django-based application with a REST API for managing clients (alta, baja, modificación) and Django Admin for authentication. It uses PostgreSQL as the intended database and Authentication for API access.

## Features
-- **Django Admin**: GUI for user management at `/admin/` (port `8080` via HAProxy).
- **REST API**: Client CRUD operations:
  - `GET /api/clients/`: List all clients.
  - `POST /api/clients/add/`: Add a client (alta).
  - `PATCH /api/clients/<id>/update/`: Update a client (modificación).
  - `PUT /api/clients/<id>/delete/`: Soft-delete a client (baja).
  - Returns JSON responses.
- **Authentication**: Token-based (DRF `authtoken`) tied to Admin users.
- **Database**: PostgreSQL on port `5432`.
- **Load Balancing**: HAProxy on port `8080`, balancing Django instances.
## Project Structure

* client_system/
* ├── client_system/
* │   ├── init.py
* │   ├── settings.py
* │   ├── urls.py
* │   └── wsgi.py
* ├── clients/
* │   ├── init.py
* │   ├── admin.py
* │   ├── models.py
* │   ├── serializers.py
* │   ├── urls.py
* │   ├── views.py
* │   └── migrations/
* ├── haproxy/
* │   └── haproxy.cfg  # HAProxy config
* └── manage.py


## Setup
### Prerequisites
- Python 3.x
- PostgreSQL
- HAProxy
- Git

### Installation
1. **Clone the Repository** (after GitHub push):
   ```bash
   git clone https://github.com/yourusername/client_system.git
   cd client_system
