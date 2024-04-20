from random_coffee.infrastructure.config import environment

imports = ('random_coffee.infrastructure.notifier.backends.telegram.tasks',
           'random_coffee.infrastructure.notifier.backends.email.tasks',)
broker_url = f"redis://{environment.redis_host}:{environment.redis_port}"
broker_connection_retry_on_startup = True
