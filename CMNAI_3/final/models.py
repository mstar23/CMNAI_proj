from django.db import models

# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # 외래키로 질문글을 설정하고 on_delete값으로 CASCADE를 지정해서 답변글도 다 지워지도록
    # 질문글 1개에 여러 답변글이 달릴 수 있음.
    content = models.TextField()
    create_date = models.DateTimeField()
