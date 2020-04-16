from celery import shared_task

def send():
    print('this is a celery implementation')

@shared_task
def hello():
    send()
