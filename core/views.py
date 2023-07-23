from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task, Submission, Test
from .forms import SubmissionForm, TaskForm, TestForm, TestFormSet, TaskGradeForm
from django.contrib.auth.decorators import login_required
import chardet
from users.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from groups.models import TaskGrade
import docker
import shlex
import base64
import logging
from users.bots.tg_bot import send_telegram_message 
import asyncio

@login_required
def task_create(request):
    if request.user.choice != '2':
        # Если пользователь не является преподавателем, перенаправляем на страницу с ошибкой.
        return render(request, 'core/error.html', {'message': 'Вы не имеете прав для создания задач.'})
    user_language = request.user.language or 'python'   
    form = TaskForm(user_language=user_language)  
    formset = TestFormSet(prefix='tests')   
    if request.method == 'POST':
        formset = TestFormSet(request.POST, prefix='tests')
        form = TaskForm(request.POST, user_language=user_language)
        if form.is_valid() and formset.is_valid():
            task = form.save(commit=False)
            task.prepod = request.user.username
            task.save()
            tests = formset.save(commit=False)
            for test in tests:
                test.task = task
                test.save()
            return redirect('task_detail', slug=task.slug)

    return render(request, 'core/task_create.html', {'form': form, 'formset': formset, 'form_title': 'Создать новую задачу'})

@login_required
def task_edit(request, task_id):
    # Если пользователь не является преподавателем, перенаправляем на страницу с ошибкой.
    if request.user.choice != '2':
        return render(request, 'core/error.html', {'message': 'Вы не имеете прав для редактирования задач.'})

    # Получаем задачу, которую хотим редактировать
    task = get_object_or_404(Task, pk=task_id)

    # Проверяем, что текущий пользователь является автором задачи
    if task.prepod != request.user.username:
        return render(request, 'core/error.html', {'message': 'Вы не можете редактировать эту задачу.'})

    user_language = request.user.language or 'python'   
    form = TaskForm(instance=task, user_language=user_language)
    formset = TestFormSet(instance=task, prefix='tests')   

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user_language=user_language)
        formset = TestFormSet(request.POST, instance=task, prefix='tests')
        if form.is_valid() and formset.is_valid():
            form.prepod = request.user.username
            task = form.save()
            tests = formset.save(commit=False)
            for test in tests:
                test.task = task
                test.save()
            return redirect('task_detail', slug=task.slug)

    return render(request, 'core/task_create.html', {'form': form, 'formset': formset, 'form_title': 'Редактировать задачу'})


@login_required
def task_list(request):
    
    sort = request.GET.get('sort', 'name')  # получаем параметр сортировки из GET-запроса
    if sort == 'prepod':
        tasks = Task.objects.all().order_by('prepod')  # сортируем по полю "prepod"
    elif sort == 'difficulty':
        tasks = Task.objects.all().order_by('difficulty')  # сортируем по полю "difficulty"
    
    else:
        tasks = Task.objects.all().order_by('name')  # сортируем по умолчанию по полю "name"
    q = request.GET.get('q')
    if q:
        tasks = tasks.filter(Q(name__icontains=q) | Q(language__icontains=q) | Q(prepod__icontains=q))

    paginator = Paginator(tasks,5)
    page_number = request.GET.get('page', 1)

    page = paginator.get_page(page_number)
    
    context = {
        'tasks': page.object_list,
        'page': page,
        'sort': sort, 
        'q': q,
        }
    return render(request, 'core/task_list.html', context)


def author_tasks_view(request, prepod):
    tasks = Task.objects.filter(prepod=prepod).order_by('-created_at')
    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context = {
        'tasks': page,
        'page': page,
        'sort': request.GET.get('sort', ''),
        'q': request.GET.get('q', ''),
    }
    return render(request, 'core/task_list.html', context)

def difficulty_tasks_view(request, difficulty):
    tasks = Task.objects.filter(difficulty=difficulty).order_by('-created_at')
    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context = {
        'tasks': page,
        'page': page,
        'sort': request.GET.get('sort', ''),
        'q': request.GET.get('q', ''),
    }
    return render(request, 'core/task_list.html', context)


def language_tasks_view(request, language):
    tasks = Task.objects.filter(language=language).order_by('-created_at')
    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context = {
        'tasks': page,
        'page': page,
        'sort': request.GET.get('sort', ''),
        'q': request.GET.get('q', ''),
    }
    return render(request, 'core/task_list.html', context)


def task_detail(request, slug):
    task = get_object_or_404(Task, slug=slug)
    form = SubmissionForm()
    test = Test.objects.filter(task=task)
   # logger = logging.getLogger(__name__)
   # logger.info(test)
   # logger.info(test[0].output)
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            submission = Submission.objects.create(
                task=task,
                code=code,
                prepod=task.prepod,
                student=request.user.username,
            )
            return redirect('submission_detail', pk=submission.pk)
    
    return render(request, 'core/task_detail.html', {'task': task, 'test': test[0], 'form': form})
#'kotlinc', '-script'
#'python', '-c'
#'node', '-e'

def execute_code(code, language, input_data, user):
    if 'import' in code:
        return 'Import forbidden', ''
    client = docker.from_env()
    
    volume_name = user
    try:
        volume = client.volumes.get(volume_name)
    except docker.errors.NotFound:
        volume = client.volumes.create(volume_name)

    image_name = 'pythonmaks/contest'

    if language == 'python':
        code_command = f'python3 -c {shlex.quote(f"""{code}""")} < /code/input.txt'
    elif language == 'java':
        code_command = (f'echo {shlex.quote(code)} > /code/Main.java && '
                        f'javac /code/Main.java && '
                        f'java -cp /code Main < /code/input.txt')
    elif language == 'node':
        code_command = f'node -e {shlex.quote(code)} < /code/input.txt'
    elif language == 'kotlinc':
        code_command = (f'echo {shlex.quote(code)} > /code/Main.kt && '
                        f'kotlinc /code/Main.kt -include-runtime -d /code/main.jar && '
                        f'java -jar /code/main.jar < /code/input.txt')
                        
    #elif language == 'kotlinc':
     #   code_command = (f'echo {shlex.quote(code)} > /code/Main.kts && '
      #                  f'kotlinc -script /code/Main.kts < /code/input.txt')
                        
      
    else:
        raise ValueError(f'Unsupported language: {language}')

    input_data_command = f'echo {shlex.quote(input_data)} > /code/input.txt; {code_command}; rm -rf /code/*'

    container = client.containers.run(image_name,
                                      volumes={volume_name: {'bind': '/code', 'mode': 'rw'}},
                                      command=['/bin/sh', '-c', input_data_command],
                                      detach=True, working_dir="/code")

    container.wait()
    #logger = logging.getLogger(__name__)
    #logger.info(volume)
    stdout = container.logs(stdout=True, stderr=False)
    stderr = container.logs(stdout=False, stderr=True)

    container.remove()

    if stdout:
        if isinstance(stdout, bytes):
            stdout_encoding = chardet.detect(stdout)['encoding']
            stdout = stdout.decode(stdout_encoding).strip()

    if stderr:
        if isinstance(stderr, bytes):
            stderr_encoding = chardet.detect(stderr)['encoding']
            stderr = stderr.decode(stderr_encoding).strip()
        #logger.info(stderr)

    return stdout, stderr




    
@login_required
def submission_detail(request, pk):
    logger = logging.getLogger(__name__)
    submission = get_object_or_404(Submission, pk=pk)
    task = submission.task
    submission.prepod = submission.task.prepod
    language = {'python': '-c',
                'node': '-e',
                'java': 'Main',
                'kotlinc': '-script'
    }
    
    test_cases = Test.objects.filter(task=task)  # получение всех тестов для этого задания
                        
    passed = []   
    error = [] 
    output = []
    tests = []
    for test_case in test_cases:
        tests.append(test_case)
        input_data = test_case.input.strip()
        expected_output = test_case.output
       # logger.info(f'1 {expected_output}')             
        expected_output = test_case.output.strip()
        #logger.info(f'1 {expected_output}')       
        if input_data and expected_output:   
            output_i, error_i = execute_code(submission.code, task.language, input_data, request.user.username)
            try:
                #logger.info(f'2 {output_i}')
                #logger.info(f'3 {expected_output}')                
                if isinstance(output_i, bytes):
                    encoding = chardet.detect(output_i)['encoding']
                    output_i = output_i.decode(encoding).strip()

                output.append(output_i)                
                passed.append(output_i.splitlines() == expected_output.strip().splitlines())

            except Exception as e:
                if isinstance(error_i, bytes):
                        encoding = chardet.detect(error_i)['encoding']
                        logger.info(f'1 {error_i}')
                        try:
                            error_i = error_i.decode(encoding).strip()
                        except:
                            pass
                error.append(error_i)
            except:
                pass
                        
    if False in passed:
        passed = False
    for i in error:
        if i:
            error = i.strip()  
            break                 
    else:
        error = ''
    if error:
        submission.status = 'E'
        submission.save()
    elif passed:
        submission.status = 'AC'
        submission.save()
        professor = User.objects.get(username=submission.prepod)
        if professor.chat_id:  # проверить, что у профессора есть chat_id для оповещений в Telegram
            asyncio.create_task(send_telegram_message(professor.chat_id, f'Студент {submission.student} успешно решил вашу задачу {submission.task}!'))
    else:
        submission.status = 'WA'
        submission.save()
    try:
        grade = TaskGrade.objects.get(student=User.objects.get(username=submission.student), task=submission.task)
    except TaskGrade.DoesNotExist:
        grade = None

    if request.method == 'POST':
        form = TaskGradeForm(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.student = User.objects.get(username=submission.student)
            grade.task = submission.task
            grade.save()
    else:
        form = TaskGradeForm(instance=grade)
        
    return render(request, 'core/submission_detail.html', {'grade': grade, 'form': form, 'submission': submission, 'tests': tests, 'output': output, 'error': error, 'passed': passed})






