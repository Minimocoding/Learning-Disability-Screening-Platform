from django.core.management.base import BaseCommand
from main.models import TestQuestion

class Command(BaseCommand):
    help = 'Populate the database with 50 test questions for learning disability screening'

    def handle(self, *args, **options):
        # Clear existing questions
        TestQuestion.objects.all().delete()
        
        questions = [
            # Dyslexia questions (1-11)
            (1, "Does the child have difficulty recognizing letters or numbers?", "dyslexia"),
            (2, "Does the child struggle to read words aloud?", "dyslexia"),
            (3, "Does the child confuse similar looking letters (b/d, p/q)?", "dyslexia"),
            (4, "Does the child have trouble sounding out new words?", "dyslexia"),
            (5, "Does the child read very slowly compared to peers?", "dyslexia"),
            (6, "Does the child have difficulty understanding what they read?", "dyslexia"),
            (7, "Does the child avoid reading activities?", "dyslexia"),
            (8, "Does the child spell the same word differently in the same document?", "dyslexia"),
            (9, "Does the child have trouble remembering common sight words?", "dyslexia"),
            (10, "Does the child skip words or lines when reading?", "dyslexia"),
            (11, "Does the child have difficulty with rhyming words?", "dyslexia"),
            
            # Dysgraphia questions (12-22)
            (12, "Does the child have messy or illegible handwriting?", "dysgraphia"),
            (13, "Does the child hold pencils or pens awkwardly?", "dysgraphia"),
            (14, "Does the child write very slowly?", "dysgraphia"),
            (15, "Does the child have trouble forming letters correctly?", "dysgraphia"),
            (16, "Does the child use inconsistent spacing between words?", "dysgraphia"),
            (17, "Does the child have difficulty copying text from the board?", "dysgraphia"),
            (18, "Does the child avoid writing tasks?", "dysgraphia"),
            (19, "Does the child have trouble organizing thoughts on paper?", "dysgraphia"),
            (20, "Does the child make frequent spelling errors?", "dysgraphia"),
            (21, "Does the child have difficulty with fine motor skills?", "dysgraphia"),
            (22, "Does the child complain of hand pain when writing?", "dysgraphia"),
            
            # Dyscalculia questions (23-35)
            (23, "Does the child have trouble understanding number concepts?", "dyscalculia"),
            (24, "Does the child struggle with basic math facts (addition/subtraction)?", "dyscalculia"),
            (25, "Does the child have difficulty counting backwards?", "dyscalculia"),
            (26, "Does the child confuse mathematical symbols (+, -, =)?", "dyscalculia"),
            (27, "Does the child have trouble with word problems?", "dyscalculia"),
            (28, "Does the child struggle to understand place value?", "dyscalculia"),
            (29, "Does the child have difficulty estimating quantities?", "dyscalculia"),
            (30, "Does the child avoid math-related activities?", "dyscalculia"),
            (31, "Does the child have trouble telling time?", "dyscalculia"),
            (32, "Does the child struggle with money concepts?", "dyscalculia"),
            (33, "Does the child have difficulty with measurement?", "dyscalculia"),
            (34, "Does the child struggle with patterns and sequences?", "dyscalculia"),
            (35, "Does the child have trouble understanding fractions?", "dyscalculia"),
            
            # Psychological Impact questions (36-50)
            (36, "Does the child show signs of anxiety about school work?", "psychological"),
            (37, "Does the child have low self-esteem regarding academic abilities?", "psychological"),
            (38, "Does the child become easily frustrated with learning tasks?", "psychological"),
            (39, "Does the child avoid participating in class activities?", "psychological"),
            (40, "Does the child show behavioral problems in school?", "psychological"),
            (41, "Does the child seem withdrawn or isolated from peers?", "psychological"),
            (42, "Does the child express negative feelings about school?", "psychological"),
            (43, "Does the child have difficulty concentrating on tasks?", "psychological"),
            (44, "Does the child show signs of depression or sadness?", "psychological"),
            (45, "Does the child have trouble sleeping due to school worries?", "psychological"),
            (46, "Does the child complain of physical symptoms (headaches, stomachaches) before school?", "psychological"),
            (47, "Does the child show signs of perfectionism or fear of making mistakes?", "psychological"),
            (48, "Does the child have difficulty making friends at school?", "psychological"),
            (49, "Does the child show regression in previously learned skills when stressed?", "psychological"),
            (50, "Does the child express feelings of being 'stupid' or 'different'?", "psychological"),
        ]
        
        for question_number, question_text, category in questions:
            TestQuestion.objects.create(
                question_number=question_number,
                question_text=question_text,
                category=category
            )
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(questions)} test questions')
        )