<h1 align="center"> 🎨 Gallery - Online Subscription Art Service 🎨 </h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Django-4.2+-green?style=for-the-badge&logo=django&logoColor=white">
  </br>
  <img src="https://img.shields.io/badge/PostgreSQL-13+-blue?style=for-the-badge&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/Redis-6.0+-red?style=for-the-badge&logo=redis&logoColor=white">
  </br>
  <img src="https://img.shields.io/badge/Elasticsearch-8.0+-orange?style=for-the-badge&logo=elasticsearch&logoColor=white">
  <img src="https://img.shields.io/badge/PayPal-Integration-blue?style=for-the-badge&logo=paypal&logoColor=white">
  </br>
  <img src="https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
  <img src="https://img.shields.io/badge/Test_Coverage-85%25-brightgreen?style=for-the-badge">
  </br>
</p>

<h1 align="left"> 📋 About</h1> 

</br>

Gallery is a sophisticated online subscription service where users can discover and download unique artworks from talented artists around the world. Built with Django 4.2+ and Python 3.12+, this platform offers a premium art discovery experience through flexible subscription plans powered by secure PayPal integration.

The service features three carefully crafted subscription tiers - Basic, Premium, and Enterprise - each providing access to different levels of exclusive content and features. Users can explore an extensive collection of high-quality artworks through an intelligent search system powered by Elasticsearch, ensuring lightning-fast and precise results.

Gallery prioritizes security and user experience with comprehensive authentication options including social login integration, two-factor authentication (2FA), email verification, and flexible login methods via email or phone number. The platform leverages advanced caching strategies using Redis and Django-Cachalot for optimal performance and seamless user interactions.

This project exemplifies modern web development practices with a robust CI/CD pipeline, comprehensive test coverage (85%), and clean, maintainable code enforced by industry-standard tools like Flake8, Ruff, isort, and Black. The platform also features custom JavaScript implementations for enhanced user interactions, including intuitive photo download functionality and dynamic timer-based messaging systems.

## Stack:

 - **Backend**: [**`Python 3.12+`**](https://python.org/)
 - **Framework**: [**`Django 4.2+`**](https://djangoproject.com/)
 - **Database**: [**`PostgreSQL`**](https://postgresql.org/)
 - **Search Engine**: [**`Elasticsearch 8.0+`**](https://elastic.co/elasticsearch)
 - **Cache**: [**`Redis`**](https://redis.io/) with [**`Django-Cachalot`**](https://django-cachalot.readthedocs.io/)
 - **Task Queue**: [**`Celery`**](https://docs.celeryq.dev/en/stable/)
 - **API**: [**`Django REST Framework`**](https://django-rest-framework.org/)
 - **Deployment**: [**`Docker`**](https://docker.com/)

## 🚀 Features

### User Experience
* Three-tier subscription system (Basic, Premium, Enterprise)
* Secure PayPal payment integration
* Advanced artwork search powered by Elasticsearch
* High-resolution artwork downloads
* Personalized user profiles and galleries
* Social media authentication (Google, GitHub, Facebook)
* Two-factor authentication (2FA) for enhanced security
* Email and phone number verification
* Password recovery and reset functionality

### Content Management
* Comprehensive artwork catalog with advanced filtering
* Artist profiles and portfolio management
* Artwork categorization and tagging system
* High-quality image processing and optimization
* Batch download capabilities for premium users
* Favorites and wishlist functionality

### Performance & Scalability
* Redis caching with Django-Cachalot for global optimization
* Elasticsearch integration for lightning-fast search
* SQL query optimization with select_related techniques
* Background task processing with Celery
* Responsive design for all devices
* Progressive web app (PWA) capabilities

### Development Features
* Comprehensive REST API with JWT authentication
* 85% test coverage with unit and API tests
* CI/CD pipeline for automated deployment
* Code quality tools (Flake8, Ruff, isort, Black)
* Type safety with Django-Stubs
* Faker library for realistic test data generation
* Custom JavaScript utilities for enhanced UX

### Administrative Tools
* Powerful Django admin panel for content management
* User subscription and payment tracking
* Artist onboarding and content approval workflow
* Analytics dashboard with subscription metrics
* Content moderation and quality control
* Email notification management system

## 🛠️ Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sauberr/gallery.git
   cd gallery
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3.12 -m venv ../venv
   source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate
   ```
   
3. **Install dependencies with Poetry:**
   ```bash
   poetry update
   poetry install
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Open `.env` file and fill in all required environment variables:
   
   ```env
   # Django Configuration
   DEBUG=True
   SECRET_KEY=django-insecure-your-secret-key-here
   DOMAIN_NAME=http://localhost:8000/
   
   # Database Configuration (PostgreSQL)
   DATABASE_NAME=gallery
   DATABASE_USER=postgres
   DATABASE_PASSWORD=postgres
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   
   # Redis Configuration
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=1
   
   # Elasticsearch Configuration
   ELASTICSEARCH_HOST=localhost
   ELASTICSEARCH_PORT=9200
   
   # PayPal Configuration
   PAYPAL_CLIENT_ID=your_paypal_client_id
   PAYPAL_CLIENT_SECRET=your_paypal_client_secret
   PAYPAL_MODE=sandbox  # or 'live' for production
   
   # Email Configuration
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password_here
   
   # JWT Configuration
   JWT_SECRET_KEY=your_jwt_secret_key
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_DELTA=3600
   ```

5. **Set up database:**
   ```bash
   # Create PostgreSQL database (make sure PostgreSQL is installed and running)
   createdb gallery_db
   
   # Run migrations
   ./manage.py migrate
   
   # Load fixture data (optional)
   ./manage.py loaddata <path_to_fixture_files>
   ```

6. **Create Django superuser:**
   ```bash
   ./manage.py createsuperuser
   ```

7. **Start Elasticsearch:**
   ```bash
   # Using Docker
   docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 \
     -e "discovery.type=single-node" \
     -e "xpack.security.enabled=false" \
     elasticsearch:8.0.0
   
   # Or install Elasticsearch locally and run
   elasticsearch
   ```

8. **Start Redis server:**
   ```bash
   # Using Docker
   docker run -it --rm --name redis -p 6379:6379 redis
   
   # Or install Redis locally and run
   redis-server
   ```

9. **Start Celery worker (in a separate terminal):**
   ```bash
   # Activate virtual environment first
   source ../venv/bin/activate
   
   # Start Celery worker
   celery -A app worker -l INFO --pool=solo
   ```

10. **Run the Django development server:**
    ```bash
    ./manage.py runserver
    ```

11. **Access the application:**
    - **Main site**: http://localhost:8000
    - **Admin panel**: http://localhost:8000/admin
    - **API documentation**: http://localhost:8000/api/docs/
    - **Elasticsearch**: http://localhost:9200

## 🐳 Docker Deployment

### Quick Start
```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Create superuser via Docker
```bash
docker-compose exec web python manage.py createsuperuser
```

### Load fixture data via Docker
```bash
docker-compose exec web python manage.py loaddata <path_to_fixture_files>
```

### Run tests via Docker
```bash
docker-compose exec web python manage.py test
```

## 🧪 Testing

The project maintains 85% test coverage with comprehensive unit and API tests:

```bash
# Run all tests
./manage.py test

# Run tests with coverage report
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML coverage report
```

## 🌐 API Endpoints

The application provides a comprehensive REST API with JWT authentication:

- **Authentication**: `/api/auth/` - User registration, login, token refresh
- **Users**: `/api/users/` - User profiles and management
- **Artworks**: `/api/artworks/` - Browse and search artworks
- **Subscriptions**: `/api/subscriptions/` - Manage subscription plans
- **Downloads**: `/api/downloads/` - Track and manage downloads
- **Artists**: `/api/artists/` - Artist profiles and portfolios

Full API documentation with interactive testing is available at `/api/docs/` when running the development server.

## 🔧 Code Quality

The project uses several tools to maintain high code quality:

```bash
# Format code
black .
isort .

# Lint code
flake8 .
ruff check .

# Type checking
mypy .
```

## 📈 Performance Optimization

- **Database**: Optimized queries using `select_related` and `prefetch_related`
- **Caching**: Multi-layer caching with Redis and Django-Cachalot
- **Search**: Elasticsearch for fast full-text search capabilities
- **Images**: Optimized image processing and CDN integration
- **Background Tasks**: Celery for heavy operations like image processing

## 🚀 Deployment

### Production Environment
- Docker containerization for consistent deployments
- CI/CD pipeline with automated testing and deployment
- Environment-specific configuration management
- Health checks and monitoring integration
- Automated database migrations
- Static file optimization and CDN integration

## 📄 License

This project uses the [MIT License](https://github.com/Sauberr/gallery/blob/master/LICENSE)

## 📞 Contact 

To contact the author of the project, write to email **dmitriybirilko@gmail.com**
