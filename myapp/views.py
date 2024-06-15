from django.shortcuts import render,redirect
from youtubesearchpython import VideosSearch
from .models import *
from .forms import *
from django.contrib import messages
from django.views import generic 
import requests
import wikipedia
from wikipedia.exceptions import DisambiguationError


# Create your views here.
def home(request):
    return render(request,'myapp/home.html')

def notes(request):
    if request.method=="POST":
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
            
        messages.success(request,f'Notes Added from {request.user.username} successfully')
        
    else:
        form=NotesForm()
        
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'myapp/notes.html',context)

def delete(request,pk):
    pi=Notes.objects.get(id=pk)
    pi.delete()
    return redirect('notes')

class NotesdetailView(generic.DetailView):
    model=Notes 

def homework(request):  
    if request.method=='POST':
        form=HomeWorkForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished =='on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
                homeworks=Homework(
                    user=request.user,
                    subject=request.POST['subject'],
                    title=request.POST['title'],
                    description=request.POST['description'],
                    due=request.POST['due'],
                    is_finished=finished
                )
                homeworks.save()
                messages.success(request,f'Homework Added from {request.user.username}!!')
                
    else:
        form=HomeWorkForm()
    homework=Homework.objects.filter(user=request.user)
    if len(homework) ==0:
        homework_done=True
    else:
        homework_done=False
    
    context={
        'homeworks':homework,
        'homeworks_done':homework_done,
        'form':form
        
    }
    return render(request,'myapp/homework.html',context)

def update_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished==True:
        homework.is_finished=False
        
    else:
        homework.is_finished=True
    homework.save()
    return redirect('homework')


def delete_homework(request,pk=None):
    pi=Homework.objects.get(id=pk)
    pi.delete()
    return redirect('homework')

def todo(request):
    if request.method=="POST":
        form=TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished =='on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            todos=Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()
            messages.success(request,f'Todo Added ')
    else:
        form=TodoForm()
  
    todo=Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done=True
    else:
        todos_done=False
        
        
    
    context={
        'form':form,
        'todos':todo,
        'todos_done':todos_done
    }
    return render(request,'myapp/todo.html',context)

def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

def books(request):
    
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r= requests.get(url)
        answer=r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories') ,
                'rating':answer['items'][i]['volumeInfo'].get('pageRating') ,
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
            } 
            result_list.append(result_dict)
        
        context = {
            'form': form,
            'results': result_list
        }
        
        return render(request, 'myapp/books.html', context)
    
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'myapp/books.html', context)
    
# def dictionary(request):
#     if request.method=="POST":
#         form=DashboardForm(request.POST)
#         text=request.POST['text']
#         url="https://api.dictionaryapi.dev/api/v2/entries/en_US"+text
#         r = requests.get(url)
#         answer = r.json()
#         try:
#             phonetics=answer[0]['phonetics'][0]['text']
#             audio=answer[0]['phonetics'][0]['audio']
#             definition=answer[0]['meanings'][0]['definitions'][0]['definition']
#             example=answer[0]['meanings'][0]['definitions'][0]['example']
#             synonmys=answer[0]['meanings'][0]['definitions'][0]['synonyms']
#             context={
#                 'form':form,
#                 'input':text,
#                 'phonetics':phonetics,
#                 'audio':audio,
#                 'definition':definition,
#                 'synonmys':synonmys,
#                 'example':example,
#             }
#         except:
#             context={
#                 'form':form,
#                 'input':''
#             }
            
#         return render(request,'myapp/dictionary.html',context)  
#     else:
#         form=DashboardForm()
#         context={'form':form}
#     return render(request,'myapp/dictionary.html',context)  

def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text'] 
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)
        
        try:
            answer = r.json()
            
            if isinstance(answer, list) and len(answer) > 0:
                phonetics = answer[0]['phonetics'][0]['text']
                audio = answer[0]['phonetics'][0]['audio']
                definition = answer[0]['meanings'][0]['definitions'][0]['definition']
                example = answer[0]['meanings'][0]['definitions'][0].get('example', '')
                synonyms = answer[0]['meanings'][0]['definitions'][0].get('synonyms', [])
                context = {
                    'form': form,
                    'input': text,
                    'phonetics': phonetics,
                    'audio': audio,
                    'definition': definition,
                    'synonyms': synonyms,
                    'example': example,
                }
            else:
                context = {
                    'form': form,
                    'input': '',
                }
        except Exception as e:
            print("Error:", e)
            context = {
                'form': form,
                'input': '',
            }
            
        return render(request, 'myapp/dictionary.html', context)  
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'myapp/dictionary.html', context)

def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
        
        context = {
            'form': form,
            'results': result_list
        }
        
        return render(request, 'myapp/youtube.html', context)
    
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'myapp/youtube.html', context)
    
def wiki(request):
    if request.method=="POST":
        text=request.POST['text']
        form=DashboardForm(request.POST)
        search=wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
            
        }
        return render(request,'myapp/wiki.html',context)
    else:
        form=DashboardForm()
        context={
            'form':form
        }
        
    return render(request,'myapp/wiki.html',context)

 
# def conversion(request):
#     if request.method=="POST":
        
#       form=ConversionForm()
#       if request.POST['measurement']=='length':
#           measurement_form=ConversionLengthForm()
#           context={
#             'form':form,
#             'm_form':measurement_form,
#             'input':True
#           }
          
#           if 'input' in request.POST:
#               first=request.POST['measure1']
#               second=request.POST['measure2']
#               input=request.POST['input']
#               answer=''
#               if input and int(input) >=0:
#                     if first =='yard' and second =='foot':
#                       answer=f'{input} yard ={int(input)*3} foot'
#                     if first =='foot' and second =='yard':
#                       answer=f'{input} yard ={int(input)/3} yard'
#               context={
#                   'form':form,
#                   'm_form':measurement_form,
#                   'input':True,
#                   'answer':answer
#               } 
              
#     if request.POST['measurement']=='mass':
#           measurement_form=ConversionMassForm()
#           context={
#             'form':form,
#             'm_form':measurement_form,
#             'input':True
#           }
          
#           if 'input' in request.POST:
#               first=request.POST['measure1']
#               second=request.POST['measure2']
#               input=request.POST['input']
#               answer=''
#               if input and int(input) >=0:
#                     if first =='pound' and second =='kilogram':
#                       answer=f'{input} yard ={int(input)*0.453592} kilogram'
#                     if first =='kilogram' and second =='pound':
#                       answer=f'{input} yard ={int(input)*2.20462} yard'
#               content={
#                   'form':form,
#                   'm_form':measurement_form,
#                   'input':True,
#                   'answer':answer
#               }
              
#     else:
#         form= ConversionForm()
#         context={
#             'form':form,
#             'input':False
#         }
                  
#     return render(request,'myapp/conversion.html',context)
    
    
from django.shortcuts import render
from .forms import ConversionForm, ConversionLengthForm, ConversionMassForm

def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if form.is_valid():
            measurement = request.POST.get('measurement')

            if measurement == 'length':
                measurement_form = ConversionLengthForm(request.POST)
            elif measurement == 'mass':
                measurement_form = ConversionMassForm(request.POST)
            else:
                # Handle unexpected measurement value
                measurement_form = None

            if measurement_form:
                if measurement_form.is_valid():
                    first = measurement_form.cleaned_data['measure1']
                    second = measurement_form.cleaned_data['measure2']
                    input_value = measurement_form.cleaned_data['input']
                    answer = ''

                    if input_value >= 0:
                        if first == 'yard' and second == 'foot':
                            answer = f'{input_value} yard = {input_value * 3} foot'
                        elif first == 'foot' and second == 'yard':
                            answer = f'{input_value} foot = {input_value / 3} yard'
                        elif first == 'pound' and second == 'kilogram':
                            answer = f'{input_value} pound = {input_value * 0.453592} kilogram'
                        elif first == 'kilogram' and second == 'pound':
                            answer = f'{input_value} kilogram = {input_value * 2.20462} pound'

                    context = {
                        'form': form,
                        'm_form': measurement_form,
                        'input': True,
                        'answer': answer,
                    }
                else:
                    context = {
                        'form': form,
                        'm_form': measurement_form,
                        'input': True,
                        'answer': '',  # No answer because form is not valid
                    }
            else:
                context = {
                    'form': form,
                    'input': True,
                    'answer': '',  # Handle case where measurement_form is None
                }
    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False,
            'answer': '',  # Default answer when no form is submitted
        }

    return render(request, 'myapp/conversion.html', context)


        
    
        
        
        
                    
                  
                
   