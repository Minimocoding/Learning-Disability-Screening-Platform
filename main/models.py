from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# User Profile Models
class UserProfile(models.Model):
    USER_TYPES = [
        ('parent', 'Parent'),
        ('teacher', 'Teacher'),
        ('psychologist', 'Psychologist'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=12, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

class ParentProfile(models.Model):
    PARENT_TYPES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('sibling', 'Sibling'),
        ('other', 'Other'),
    ]
    
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    parent_type = models.CharField(max_length=10, choices=PARENT_TYPES)
    
    def __str__(self):
        return f"{self.user_profile.user.get_full_name()} - {self.get_parent_type_display()}"

class TeacherProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.user_profile.user.get_full_name()} - {self.school_name}"

class PsychologistProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    professional_qualification = models.CharField(max_length=200)
    organization_clinic = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.user_profile.user.get_full_name()} - {self.organization_clinic}"

# Child and Test Models
class Child(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(3), MaxValueValidator(18)])
    grade = models.CharField(max_length=20)
    school_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - Age {self.age}"

class TestQuestion(models.Model):
    CATEGORY_CHOICES = [
        ('dyslexia', 'Dyslexia'),
        ('dysgraphia', 'Dysgraphia'),
        ('dyscalculia', 'Dyscalculia'),
        ('psychological', 'Psychological Impact'),
    ]
    
    question_number = models.IntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(50)])
    question_text = models.TextField()
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    
    class Meta:
        ordering = ['question_number']
    
    def __str__(self):
        return f"Q{self.question_number}: {self.question_text[:50]}..."

class TestResult(models.Model):
    ANSWER_CHOICES = [
        (0, 'No'),
        (1, 'Sometimes'),
        (2, 'Yes'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    test_date = models.DateTimeField(auto_now_add=True)
    
    # Store individual question answers (0, 1, 2)
    answers = models.JSONField()  # Will store dict of question_number: answer_value
    
    # Calculated scores
    dyslexia_score = models.IntegerField(default=0)
    dysgraphia_score = models.IntegerField(default=0)
    dyscalculia_score = models.IntegerField(default=0)
    psychological_score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    
    # Predictions (Boolean fields)
    has_ld = models.BooleanField(default=False)
    has_dyslexia = models.BooleanField(default=False)
    has_dysgraphia = models.BooleanField(default=False)
    has_dyscalculia = models.BooleanField(default=False)
    has_psychological_impact = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.child.name} - Test on {self.test_date.strftime('%Y-%m-%d')}"
    
    def calculate_scores(self):
        """Calculate scores based on answers and question categories"""
        dyslexia_questions = list(range(1, 12))  # Q1-11
        dysgraphia_questions = list(range(12, 23))  # Q12-22
        dyscalculia_questions = list(range(23, 36))  # Q23-35
        psychological_questions = list(range(36, 51))  # Q36-50
        
        self.dyslexia_score = sum(self.answers.get(str(q), 0) for q in dyslexia_questions)
        self.dysgraphia_score = sum(self.answers.get(str(q), 0) for q in dysgraphia_questions)
        self.dyscalculia_score = sum(self.answers.get(str(q), 0) for q in dyscalculia_questions)
        self.psychological_score = sum(self.answers.get(str(q), 0) for q in psychological_questions)
        self.total_score = self.dyslexia_score + self.dysgraphia_score + self.dyscalculia_score + self.psychological_score
    
    def predict_ld(self):
        """Predict learning disabilities based on threshold values"""
        # Define threshold values (you can adjust these based on research)
        DYSLEXIA_THRESHOLD = 12  # out of 22 (11 questions * 2 max points)
        DYSGRAPHIA_THRESHOLD = 12  # out of 22 (11 questions * 2 max points)
        DYSCALCULIA_THRESHOLD = 15  # out of 26 (13 questions * 2 max points)
        PSYCHOLOGICAL_THRESHOLD = 18  # out of 30 (15 questions * 2 max points)
        TOTAL_LD_THRESHOLD = 35  # out of 100 total points
        
        self.has_dyslexia = self.dyslexia_score >= DYSLEXIA_THRESHOLD
        self.has_dysgraphia = self.dysgraphia_score >= DYSGRAPHIA_THRESHOLD
        self.has_dyscalculia = self.dyscalculia_score >= DYSCALCULIA_THRESHOLD
        self.has_psychological_impact = self.psychological_score >= PSYCHOLOGICAL_THRESHOLD
        self.has_ld = self.total_score >= TOTAL_LD_THRESHOLD or any([
            self.has_dyslexia, self.has_dysgraphia, self.has_dyscalculia
        ])
    
    def save(self, *args, **kwargs):
        self.calculate_scores()
        self.predict_ld()
        super().save(*args, **kwargs)
