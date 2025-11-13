from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import TestQuestion, TestResult, Child
from .forms import (
    ParentRegistrationForm, TeacherRegistrationForm, PsychologistRegistrationForm,
    ChildInfoForm, TestAnswerForm
)
import json
import time

def home(request):
    """Homepage view"""
    return render(request, 'main/home.html')

def about_ld(request):
    """Learning Disabilities information page"""
    return render(request, 'main/about_ld.html')

def register_choice(request):
    """Registration choice page - select user type"""
    return render(request, 'main/register_choice.html')

def register_parent(request):
    """Parent registration view"""
    if request.method == 'POST':
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = ParentRegistrationForm()
    return render(request, 'main/register_parent.html', {'form': form})

def register_teacher(request):
    """Teacher registration view"""
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'main/register_teacher.html', {'form': form})

def register_psychologist(request):
    """Psychologist registration view"""
    if request.method == 'POST':
        form = PsychologistRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = PsychologistRegistrationForm()
    return render(request, 'main/register_psychologist.html', {'form': form})

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'main/login.html')

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

def take_test(request):
    """Test taking main page - requires login"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please register and login first to access the screening test.')
        return redirect('register_choice')
    
    return render(request, 'main/take_test.html')

def test_guidelines(request):
    """Test guidelines page"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please register and login first to access the screening test.')
        return redirect('register_choice')
    
    return render(request, 'main/test_guidelines.html')

@login_required
def child_info(request):
    """Child information form"""
    if request.method == 'POST':
        form = ChildInfoForm(request.POST)
        if form.is_valid():
            child = form.save()
            request.session['child_id'] = child.id
            return redirect('test_questions')
    else:
        form = ChildInfoForm()
    return render(request, 'main/child_info.html', {'form': form})

@login_required
def test_questions(request):
    """Test questions view"""
    child_id = request.session.get('child_id')
    if not child_id:
        messages.error(request, 'Please fill child information first.')
        return redirect('child_info')
    
    # Get all test questions
    questions = TestQuestion.objects.all().order_by('question_number')
    
    if request.method == 'POST':
        form = TestAnswerForm(request.POST, questions=questions)
        if form.is_valid():
            # Process answers
            child = get_object_or_404(Child, id=child_id)
            answers = {}
            
            for question in questions:
                field_name = f'question_{question.question_number}'
                answers[str(question.question_number)] = int(form.cleaned_data[field_name])
            
            # Create test result
            test_result = TestResult.objects.create(
                user=request.user,
                child=child,
                answers=answers
            )
            
            request.session['test_result_id'] = test_result.id
            return redirect('test_results')
    else:
        form = TestAnswerForm(questions=questions)
    
    return render(request, 'main/test_questions.html', {
        'form': form,
        'questions': questions,
        'total_questions': questions.count()
    })

@login_required
def test_results(request):
    """Test results view with 2-second delays"""
    test_result_id = request.session.get('test_result_id')
    if not test_result_id:
        messages.error(request, 'No test results found.')
        return redirect('take_test')
    
    test_result = get_object_or_404(TestResult, id=test_result_id)
    
    # Clear session data
    if 'child_id' in request.session:
        del request.session['child_id']
    if 'test_result_id' in request.session:
        del request.session['test_result_id']
    
    return render(request, 'main/test_results.html', {
        'test_result': test_result,
        'child': test_result.child
    })

@require_http_methods(["GET"])
def get_result_data(request, result_id):
    """AJAX endpoint for progressive result display with delays"""
    try:
        test_result = get_object_or_404(TestResult, id=result_id)
        step = int(request.GET.get('step', 0))
        
        # Add 2-second delay as required
        time.sleep(2)
        
        if step == 0:
            # First step: Check if child has LD
            data = {
                'step': 0,
                'has_ld': test_result.has_ld,
                'total_score': test_result.total_score,
                'message': 'Learning Disability Detected' if test_result.has_ld else 'No Learning Disability Detected'
            }
        elif step == 1 and test_result.has_ld:
            # Second step: Specific LD types
            data = {
                'step': 1,
                'has_dyslexia': test_result.has_dyslexia,
                'has_dysgraphia': test_result.has_dysgraphia,
                'has_dyscalculia': test_result.has_dyscalculia,
                'dyslexia_score': test_result.dyslexia_score,
                'dysgraphia_score': test_result.dysgraphia_score,
                'dyscalculia_score': test_result.dyscalculia_score,
            }
        elif step == 2:
            # Third step: Psychological impact
            data = {
                'step': 2,
                'has_psychological_impact': test_result.has_psychological_impact,
                'psychological_score': test_result.psychological_score,
                'message': 'Psychological Impact Detected' if test_result.has_psychological_impact else 'No Significant Psychological Impact'
            }
        else:
            data = {'step': -1, 'message': 'Analysis Complete'}
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
