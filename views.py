from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from review.models import Review
from review.forms import ReviewForm
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.db.models import Q, Count
from account.models import User

class IndexView(generic.ListView):
    paginate_by = 10

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        page_obj = Review.objects.order_by("-create_date")
        sort_sort = self.request.GET.get('sort', '')

        if sort_sort == 'like':
            sort_page_obj = Review.objects.annotate(like_count=Count('like_review')).order_by('-like_count', '-create_date')
            return sort_page_obj
        elif sort_sort == 'star':
            sort_page_obj = Review.objects.order_by('-star', '-create_date')
            return sort_page_obj
        elif sort_sort == 'date':
            sort_page_obj = Review.objects.order_by('-create_date')
            return sort_page_obj
        elif search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_page_obj = page_obj.filter(
                        Q(title__icontains=search_keyword) |
                        Q(movie__title__icontains=search_keyword) |
                        Q(content__icontains=search_keyword) |
                        Q(author__nickname__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_page_obj = page_obj.filter(
                        Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword))
                elif search_type == 'movie':
                    search_page_obj = page_obj.filter(movie__title__icontains=search_keyword)
                elif search_type == 'author':
                    search_page_obj = page_obj.filter(author__nickname__icontains=search_keyword)

                return search_page_obj  # Local variable 'search_page_obj' might be referenced before assignment/ global 붙여야하는지 질문
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')

        return page_obj


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 10
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type

        return context


# 리뷰등록 구현
@login_required(login_url='account:login')
def reviewCreate(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login') # 로그인 후 리뷰등록
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.create_date = timezone.now()
            review.author = request.user      # 회원가입 유저 변수명 받아오기
            review.save()
            return redirect('review:index')
    else:
        form = ReviewForm()
    context = {'form': form}
    return render(request, 'review/review_form.html', context)

# 상세리뷰 구현
def reviewDetail(request,review_id):
    review = get_object_or_404(Review, pk=review_id)
    reviewPerPage = Review.objects.order_by('-create_date')

    index = -1
    review_before = None
    review_after = None
    for r in reviewPerPage:
      index += 1
      if r.id == review.id:
          review = r
          break
    # 리뷰객체 찾는 인덱스 값
    if index > 0:
        review_before = reviewPerPage[index - 1]
    if index < len(reviewPerPage)-1 :
        review_after = reviewPerPage[index + 1]

    context = {
        'review': review,
        'review_before': review_before,
        'review_after': review_after,
    }
    return render(request, 'review/review_detail.html', context)

# 리뷰 수정 구현
@login_required(login_url='account:login')
def reviewModify(request,review_id):
    review = get_object_or_404(Review, pk=review_id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
           review = form.save(commit=False)
           review.modify_date = timezone.now()  # 수정일시 저장 재확인
           review.save()
           return redirect('review:review_detail', review_id=review.id)
    else:
        form = ReviewForm(instance=review)
    context = {'form': form}
    return render(request, 'review/review_form.html', context)

# user detail delete 구현
@login_required(login_url='account:login')
def reviewDelete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    review.delete()
    return redirect('review:index')

# like 구현
@login_required(login_url='account:login')
def like_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review.like_review.filter(pk=request.user.pk).exists():
        review.like_review.remove(request.user)
    else:
        review.like_review.add(request.user)
    return redirect('review:review_detail', review_id=review.id)

# unlike 구현
@login_required(login_url='account:login')
def unlike_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review.unlike_review.filter(pk=request.user.pk).exists():
        review.unlike_review.remove(request.user)
    else:
        review.unlike_review.add(request.user)
    return redirect('review:review_detail', review_id=review.id)



