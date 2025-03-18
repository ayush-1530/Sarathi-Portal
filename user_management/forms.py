from django import forms



class SearchUserForm(forms.Form):
    user_id = forms.CharField(label="USER ID : ")

    def __init__(self, *args, **kwargs):
        super(SearchUserForm, self).__init__(*args, **kwargs)


class EditUserForm(forms.Form):
    userid = forms.IntegerField(label="USER ID : ")
    firstname = forms.CharField(label= "First Name : ", max_length=10)
    lastname = forms.CharField(label= "Last Name : ", max_length=10)
    gender = forms.ChoiceField(label= "GENDER : ", choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    dob = forms.DateField(label= "DATE OF BIRTH : ", widget= forms.DateInput(attrs={"type" : "date"}))
    
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)