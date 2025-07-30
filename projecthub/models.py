from django.db import models
from django.core.exceptions import ValidationError

class Project(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def clean(self):
        super().clean()

        if self.start_date > self.end_date:
            raise ValidationError('End date should be greater than start date')

class Task(models.Model):

    class TaskStatusEnum(models.IntegerChoices):
        TO_DO = 1, 'To Do'
        IN_PROGRESS = 2, 'In Progress'
        COMPLETED = 3, 'Completed'

    class TaskPriorityEnum(models.IntegerChoices):
        LOWEST = 1, 'Lowest'
        LOW = 2, 'Low'
        MEDIUM = 3, 'Medium'
        HIGH = 4, 'High'
        HIGHEST = 5, 'Highest'

    title=models.CharField(max_length=100)
    description=models.TextField()
    status=models.IntegerField(choices=TaskStatusEnum.choices, default=TaskStatusEnum.TO_DO)
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    priority=models.IntegerField(choices=TaskPriorityEnum.choices, default=TaskPriorityEnum.LOWEST)
    due_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task=models.ForeignKey(Task, on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class Tag(models.Model):
    name=models.CharField(max_length=100)
    task=models.ManyToManyField(Task)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name