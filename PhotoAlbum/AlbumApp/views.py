from django.shortcuts import render

# Create your views here.
def gallery(request):
    return render(request,'photos/gallery.html')

def photo(request,pk):
    return render(request,'photos/photo.html')
    
def add(request):
    return render(request,'photos/add.html')

