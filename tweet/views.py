from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# Create your views here.
def index(request):
    return render(request,'index.html')


def tweet_list(request):
    query = request.GET.get('q')  # Get the search query from the URL
    if query:
        tweets = Tweet.objects.filter(content__icontains=query).order_by('-created_at')  # Filter and order by created_at
    else:
        tweets = Tweet.objects.all().order_by('-created_at')  # Default: all tweets ordered by created_at
    return render(request, 'tweet_list.html', {'tweets': tweets, 'query': query})


@login_required
def tweet_create(request):
    if request.method=='POST':
      form=TweetForm(request.POST,request.FILES)
      if form.is_valid():
        #  form ko save kiye commit false isliye hua hai db me save nhi kro
         tweet=form.save(commit=False)
        # tweet me user bhi add kr rhe hai or user aata hai request se wo kiya
         tweet.user=request.user
        #  ab final tweet save kr rhe ahi db me
         tweet.save()
         return redirect('tweet_list')
    else:
       form=TweetForm()
    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_edit(request,tweet_id):
#    tweet mng rha hu kise pehla jo parameter hai wo model hai jha se tweet mng rha hau fir primary key ki bhaiya konsa tweet then user login hona chahiye tb edit kr paye nhi to koi bhi krdega instance =tweet isliye tki form prefill hojae.
   tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
   if request.method=='POST':
      form=TweetForm(request.POST,request.FILES,instance=tweet)
      if form.is_valid():
         tweet=form.save(commit=False)
         tweet.user=request.user
         tweet.save()
         return redirect('tweet_list')
    
   else:
    #   instance =tweet mtlb ki form me prefill rhega data jisko edit krna hai or data tweet se aarha hai
      form=TweetForm(instance=tweet)
   return render(request,'tweet_form.html',{'form':form})
@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
       tweet.delete()
       return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})

def register(request):
   if request.method=='POST':
      form=UserRegistrationForm(request.POST)
      if form.is_valid():
         user=form.save(commit=False)
         user.set_password(form.cleaned_data['password1'])
         user.save()
         login(request,user)
         return redirect('tweet_list')
     
   else:
     form=UserRegistrationForm
   return render(request,'registration/register.html',{'form':form})

