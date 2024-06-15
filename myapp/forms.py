from django import forms 
from .models import *
from django.forms import widgets

class NotesForm(forms.ModelForm):
    class Meta:
        model=Notes
        fields=['title','description']
        
class DateInput(forms.DateInput):
    input_type='date'
        
class HomeWorkForm(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':DateInput()}
        fields=['subject','title','description','due','is_finished']
        
class DashboardForm(forms.Form):
    text=forms.CharField(max_length=100,label='Enter the Search')
    
class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title','is_finished']
        
class ConversionForm(forms.Form):
    CHOICES=[('length','Length'),('mass',"Mass")]
    measurement=forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)
    
class ConversionLengthForm(forms.Form):
     CHOICES=[('yard','Yard'),('foot',"Foot")]
     input=forms.CharField(required=False, label=False, widget=forms.TextInput(attrs={'type':'number','placeholder':'Enter the Number'}))
     
     measure1=forms.CharField(
         label='',widget=forms.Select(choices=CHOICES)
     )
     
     measuree2= forms.CharField(
         label='',widget=forms.Select(choices=CHOICES)
     )
     

class ConversionMassForm(forms.Form):
     CHOICES=[('pound','Pound'),('kilogram',"Kilogram")]
     input=forms.CharField(required=False, label=False, widget=forms.TextInput(attrs={'type':'number','placeholder':'Enter the Number'}))
     
     measure1=forms.CharField(
         label='',widget=forms.Select(choices=CHOICES)
     )
     
     measuree2= forms.CharField(
         label='',widget=forms.Select(choices=CHOICES)
     )
     

    
    
    
    
    