import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

def run_bot():
    from users.bots.tg_bot import main
    main()

if __name__ == '__main__':
    run_bot()
