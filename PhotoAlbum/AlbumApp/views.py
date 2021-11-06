from django.shortcuts import render, redirect
from .models import Album,Photo

def base(request):
    return render(request,'photos/base.html')

def gallery(request):
    album = request.GET.get('album')
    print('album:',album)

    if album == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(album__name=album)

    albums = Album.objects.all()

    context = {'albums':albums, 'photos':photos}
    #print(context)
    return render(request,'photos/gallery.html',context)




def photo(request,pk):
    photo = Photo.objects.get(id=pk)
    return render(request,'photos/photo.html', {'photo':photo})




def add(request):
    albums = Album.objects.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        print('data:' , data)
        print('image:' , images)

        if data['album'] != 'none':
            album=Album.objects.get(id=data['album'])
        elif data['album'] != "":
            album , created = Album.objects.get_or_create(name = data['album_new'])
        else:
            category = None
        
        for image in images:
            photo = Photo.objects.create(
                album = album,
                description = data['description'],
                image=image,
            )

        return redirect('gallery')

    context = {'albums':albums}
    return render(request,'photos/add.html', context)

