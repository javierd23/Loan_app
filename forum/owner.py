from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

#for this view, I will not request a log in ot alter the view since it will do the work.
class OwnerListView(ListView):
    """Sub-class the ListView to pass the request to the form."""
    

class OwnerDetailView(DetailView):
    """Sub-class the DetailView to pass the request to the form."""
    
class OwnerCreateView(LoginRequiredMixin, CreateView):
    
    def form_valid(self, form):
        #on here we add some code to override the view so I does not take from form the owner 
        #but it know that the form will be assgined to the logged in User
        
        create = form.save(commit=False)
        create.owner = self.request.user
        create.save()
        return super(OwnerCreateView, self).form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    #the user does not see the data that they cannot update we change this to the queryset

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    


