from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from rest_framework.reverse import reverse_lazy

from .models import Feedback


def home(request):
    return render(request, "home/main_page.html")

def about(request):
    response = render(request, "home/about.html")
    return response

def contact(request):
    return render(request, "home/contact.html")

def more(request):
    return render(request, "home/more.html")

class FeedbackCreateView(CreateView):
    model = Feedback
    fields = ["text"]
    template_name = "home/feedback.html"
    success_url = reverse_lazy("home:home")

    def form_valid(self, form):
        feed = form.save(commit=False)
        feed.user = self.request.user
        feed.save()

        messages.success(self.request, "Gracias por su Feedback!")
        return super().form_valid(form)


#this is a 404 http view.....

from django.shortcuts import render

def my_custom_page_not_found_view(request, exception):
    return render(request, "404.html", {}, status=404)

def my_custom_error_view(request):
    return render(request, "500.html", {}, status=500)


from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK")