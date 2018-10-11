from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": "form-control",
                                                                              "id": "name",
                                                                              "placeholder": "your full name"}))
    email = forms.EmailField(max_length=32, widget=forms.EmailInput(attrs={"class": "form-control",
                                                                           "id": "email",
                                                                           "placeholder": "your email"}))
    phone = forms.CharField(max_length=32, widget=forms.EmailInput(attrs={"class": "form-control",
                                                                           "id": "phone",
                                                                           "placeholder": "your phone must 8801"}))
    massage = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",
                                                           "id": "contact_message",
                                                           "placeholder": "your message"}))

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.length < 16 and phone.length >= 11:
            raise forms.ValidationError("Wrong format phone number!")
        elif not "8801" in phone:
            raise forms.ValidationError("Wrong formatphone number!")
        return phone
