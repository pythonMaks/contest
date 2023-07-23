import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

def run_bot():
    from users.bots.tg_bot import main
    main()

if __name__ == '__main__':
    run_bot()
