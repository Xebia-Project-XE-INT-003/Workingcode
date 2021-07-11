from django import forms
# from App.models import Appointment

# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model=Appointment
#         fields=['name','description','date','time','urgency']

# class DateInput(forms.DateInput):
#     input_type='date'


#     # date = forms.DateTimeField(
#     #     input_formats=['%d/%m/%Y'],
#     #     widget=forms.DateTimeInput(attrs={
#     #         'class': 'form-control datetimepicker-input',
#     #         'data-target': '#datetimepicker1'
#     #     })
#     # )
# class AppointmentForm(forms.Form):
#      date=forms.DateField(widget=DateInput)