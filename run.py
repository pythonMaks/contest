from multiprocessing import Process
from django.core.management import call_command

def run_bot():
    from users.bots.tg_bot import main
    main()

def run_django():
    call_command('runserver', '0.0.0.0:8000')

if __name__ == '__main__':
    p1 = Process(target=run_bot)
    p1.start()
    p2 = Process(target=run_django)
    p2.start()