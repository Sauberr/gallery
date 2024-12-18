### Gallery: Online subscription service

Gallery is an online service where users can download unique artworks from artists through subscription plans, processed via PayPal. The platform offers three subscription tiers: Basic, Premium, and Enterprise, each granting access to different levels of content.

The search functionality is powered by Elasticsearch, providing fast and efficient query execution. User authentication includes social login, two-factor authentication (2FA), email verification, and custom authentication via email or phone number. Data caching is implemented using Redis, with global caching enhanced by Django-Cachalot for performance optimization. The system leverages PostgreSQL as its database, Docker for containerization, and Celery for handling background tasks.

To maintain clean and efficient code, the project uses tools like Flake8, Ruff, isort, and Black. A robust CI/CD pipeline ensures smooth deployment and quality control. The codebase includes 85% test coverage with unit and API tests for reliability. A comprehensive RESTful API is implemented with JWT authentication, filters, and search capabilities. SQL query performance is further optimized using tools and techniques like select_related and Redis caching. The Faker library aids in generating test data, contributing to a scalable and reliable architecture.

Additionally, small JavaScript scripts have been developed for features such as photo downloads and timer-based messages. The frontend utilizes HTML, CSS, and JavaScript to enhance user interactions and deliver a seamless experience.

## Stack:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Docker](https://www.docker.com/)
- [DRF](https://www.django-rest-framework.org/)
- [Elasticsearch](https://www.elastic.co/elasticsearch)

## Local Developing

All actions should be executed from the source directory of the project and only after installing all requirements.

1. Firstly, create and activate a new virtual environment:
   ```bash
   python3.12 -m venv ../venv
   source ../venv/bin/activate
   ```
   
2. Install packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   
3. Run project dependencies, migrations, fill the database with the fixture data etc.:
   ```bash
   ./manage.py migrate
   ./manage.py loaddata <path_to_fixture_files> 
   ```

4. Install redis:
   ```bash
   redis-server
   ```

5. Install celery:
   ```bash
   celery -A app name worker -l INFO --pool=solo
   ```
   
6. Docker :
   ```bash
   docker compose build .
   
   docker-compose up
   ```

## License

This project uses the [MIT] license(https://github.com/Sauberr/gallery/blob/master/LICENSE)
