from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from mainapp.models import UserRating, SaveForLater, Book
import json


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def search(request):
    """
    AJAX request for search bar functionality
    """
    if request.method == "POST" and is_ajax(request=request):
        query = request.POST.get("bookName", None)
        top5_result = Book.objects.filter(title__icontains=query)[:5]
        book_data = []
        for book in top5_result:
            book_data.append({
                'book_id': book.id,
                'original_title': book.title,
                'authors': book.authors,
                'image_url': book.image_url,
                'average_rating': book.average_rating,
                'summary': book.description[:500] + ' ...',
            })
        top5_result_json = json.dumps(book_data)
        return JsonResponse({"success": True, "top5_result": top5_result_json}, status=200)


def get_book_details(request):
    """
    AJAX request for book details
    """
    if request.method == "POST" and is_ajax(request=request):
        bookid = request.POST.get("bookid", None)
        book_details = Book.objects.get(id=bookid)
        if not book_details:
            return JsonResponse({"success": False}, status=200)
        book_data = {
            'original_title': book_details.title,
            'authors': book_details.authors,
            'image_url': book_details.image_url,
            'average_rating': book_details.average_rating,
            'summary': book_details.description[:500] + ' ...',
        }
        book_details = json.dumps(book_data)
        return JsonResponse({"success": True, "book_details": book_details}, status=200, safe=False)


@login_required
def user_rate_book(request):
    """
    AJAX request when user rates book
    """
    if request.method == "POST" and is_ajax(request=request):
        book_id = request.POST.get("bookid", None)
        book_rating = request.POST.get("bookrating", None)

        # Using Inbuilt Model
        query = UserRating.objects.filter(user=request.user).filter(book_id=book_id)
        if not query:
            # Create Rating
            UserRating.objects.create(
                user=request.user, book_id=book_id, book_rating=book_rating
            )
        else:
            # Update Rating
            rating_object = query[0]
            rating_object.book_rating = book_rating
            rating_object.save()
        return JsonResponse({"success": True}, status=200)

@login_required
def save_book(request):
    """AJAX request when user saves book"""
    if request.method == "POST" and is_ajax(request=request):
        book_id = request.POST.get("bookid", None)
        if SaveForLater.objects.filter(user=request.user, book_id=book_id).exists():
            return JsonResponse({"success": False}, status=200)
        SaveForLater.objects.create(user=request.user, book_id=book_id)
        return JsonResponse({"success": True}, status=200)

@login_required
def remove_saved_book(request):
    """AJAX request when user removes book"""
    if request.method == "POST" and is_ajax(request=request):
        book_id = request.POST.get("bookid", None)
        try:
            saved_book = SaveForLater.objects.get(user=request.user, book_id=book_id)
            saved_book.delete()
            return JsonResponse({"success": True}, status=200)
        except SaveForLater.DoesNotExist:
            return JsonResponse({"success": False}, status=200)


def check_saved_book(request):
    """AJAX request for check book in saved list"""
    if request.method == "POST" and is_ajax(request=request):
        book_id = request.POST.get("bookid", None)
        is_saved = SaveForLater.objects.filter(user=request.user).filter(book_id=book_id).exists()
        return JsonResponse({"success": True, "is_saved": is_saved}, status=200)
