from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from zipfile import ZipFile
from PIL import Image
from os import makedirs
import os
import shutil
from .forms import FileUploadForm
import datetime
from django.contrib import messages


def get_directory_name():
    return datetime.datetime.now().strftime("%m%d%Y%H%M%S%f")


def get_all_file_paths(directory):
    file_paths = []
    for root, directory, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths


def rgb_to_greyscale(directory, gray_photo_directory_name):
    # os.mkdir(os.path.join(os.getcwd() + "/media", gray_photo_directory_name))
    makedirs(os.path.join(os.getcwd() + "/media", gray_photo_directory_name), exist_ok=True)
    for root, directory, files in os.walk("media/" + directory):
        makedirs(f"media/{gray_photo_directory_name}/{'/'.join(root.split('/')[2:])}", exist_ok=True)
        for filename in files:
            try:
                img = Image.open(root + "/" + filename).convert('LA').convert('RGB')
            except:
                return False
            img.save(f"media/{gray_photo_directory_name}/{'/'.join(root.split('/')[2:])}/{filename}")
    return True


def extract_zip_file(myfile, color_photo_directory_name):
    try:
        with ZipFile(myfile, 'r') as zip:
            os.mkdir(os.path.join(os.getcwd() + "/media", color_photo_directory_name))
            zip.extractall(path=f"media/{color_photo_directory_name}")
            os.remove("media/" + myfile.name)
            return True
    except:
        return False


def main(request, color_photo_directory_name, gray_photo_directory_name, output_photo_directory_name, myfile, **kwargs):
    directory = f'{color_photo_directory_name}/'
    if kwargs.get('single_file'):
        os.mkdir(os.path.join(os.getcwd() + "/media", gray_photo_directory_name))
    if not rgb_to_greyscale(directory, gray_photo_directory_name):
        return False
    zippath = f'media/{gray_photo_directory_name}/'
    filePaths = get_all_file_paths(zippath)
    makedirs(os.path.join(os.getcwd() + "/media", output_photo_directory_name), exist_ok=True)
    if kwargs.get('single_file'):
        with ZipFile(f"media/{output_photo_directory_name}/" + 'greyscale.zip', 'w') as zip:
            for file in filePaths:
                zip.write(file)
    else:
        with ZipFile(f"media/{output_photo_directory_name}/" + myfile.name, 'w') as zip:
            for file in filePaths:
                zip.write(file)

    shutil.rmtree(os.path.join(os.getcwd() + '/media', color_photo_directory_name))
    shutil.rmtree(os.path.join(os.getcwd() + '/media', gray_photo_directory_name))
    return True


def single_file_photo(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES) or None
        if form.is_valid():
            myfile = request.FILES['file']
            size = myfile.size // 1024
            if myfile and size <= 10000:
                color_photo_directory_name = get_directory_name()
                gray_photo_directory_name = get_directory_name()
                output_photo_directory_name = get_directory_name()
                fs = FileSystemStorage()
                os.mkdir(os.path.join(os.getcwd() + "/media", output_photo_directory_name))
                filename = fs.save(f"{os.getcwd()}/media/{color_photo_directory_name}/{myfile.name}", myfile)
                if not main(request, color_photo_directory_name, gray_photo_directory_name, output_photo_directory_name, myfile, single_file=True):
                    messages.error(request, "Sorry, your image is invalid")
                    return redirect("single_photo")
                # filename = fs.save("custome"+myfile.name, myfile)
                output_file = FileSystemStorage(base_url=f"/media/{output_photo_directory_name}")
                uploaded_file_url = output_file.url('greyscale.zip')
                return render(request, 'fileupload/fileupload.html', {
                    'uploaded_file_url': uploaded_file_url
                })
            else:
                messages.error(request, "File size is to big upload less than or equal 10 mb zip file.")
                return redirect("single_photo")
    else:
        form = FileUploadForm()
        data = {
            'form': form,
            'single_photo': True
        }
        return render(request, 'fileupload/fileupload.html', data)


# import glob
def simple_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES) or None
        if form.is_valid():
            # files = glob.glob('/media')
            # for f in files:
            #     os.remove(f)
            # shutil.rmtree("media/")
            myfile = request.FILES['file']
            size = myfile.size // 1024
            if myfile and size <= 50000:
                color_photo_directory_name = get_directory_name()
                gray_photo_directory_name = get_directory_name()
                output_photo_directory_name = get_directory_name()
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                if not extract_zip_file(myfile, color_photo_directory_name):
                    messages.error(request, "File is not zip. Please upload zip flle.")
                    return redirect("upload")
                if not main(request, color_photo_directory_name, gray_photo_directory_name, output_photo_directory_name, myfile):
                    messages.error(request, "Sorry, your image is invalid")
                    return redirect("upload")
                # filename = fs.save("custome"+myfile.name, myfile)
                output_file = FileSystemStorage(base_url=f"/media/{output_photo_directory_name}")
                uploaded_file_url = output_file.url(filename)
                return render(request, 'fileupload/fileupload.html', {
                    'uploaded_file_url': uploaded_file_url
                })
            else:
                messages.error(request, "File size is to big upload less than or equal 50 mb zip file.")
                return redirect("upload")
    form = FileUploadForm()
    data = {
        'form': form,
        'small_size_zip': True,
    }
    return render(request, 'fileupload/fileupload.html', data)
