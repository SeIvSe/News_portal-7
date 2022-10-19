from django.apps import AppConfig
import redis

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals


red = redis.Redis(
    host='redis-19126.c1.eu-west-1-3.ec2.cloud.redislabs.com',
    port=19126,
    password='tG960lWD0Px5XgbPVboCpmka9peqfaIn'
)