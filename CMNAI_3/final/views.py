from django.shortcuts import render, get_object_or_404, redirect  # 파이썬 데이터를 템플릿에 저장하고 html로 띄우기 / 없는 id오면 404 에러
from .models import Question, Answer
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')  # 조회 결과 정렬 / 역순으로 : -붙이기
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'final/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'final/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('final:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'final/question_detail.html', context)  # redirect : 페이지 이동 / 이동할 페이지 번호


def question_create(request):
    if request.method == 'POST':        # 질문 등록하면 POST로 방식 변경
        form = QuestionForm(request.POST)
        # request.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 자동으로 저장되어 객체가 생성
        if form.is_valid():  # 폼이 유효하다면
            question = form.save(commit=False)  # 임시 저장하여 question 객체를 리턴받는다.
            question.create_date = timezone.now()  # 실제 저장을 위해 작성일시를 설정한다.
            question.save()  # 데이터를 실제로 저장한다.
            return redirect('final:index')       # index 함수 호출하기
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'final/question_form.html', context)
    # 질문 목록 화면에서 "질문 등록하기" 버튼을 클릭한 경우에는 /pybo/question/create/ 페이지가 GET 방식으로 요청되어 question_create 함수가 실행된
    # <a href="{% url 'pybo:question_create' %}" class="btn btn-primary">질문 등록하기</a>와 같이 링크를 통해 페이지를 요청할 경우에는 무조건 GET 방식이 사용되기 때문