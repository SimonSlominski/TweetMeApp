from django import forms
from django.forms.utils import ErrorList


class FormUserNeededMixin(object):

    def form_valid(self, form): # don't allow the form to submit if user is not authenticated
        if self.request.user.is_authenticated():
            form.instance.user = self.request.user
            return super(FormUserNeededMixin, self).form_valid(form)
        else:   # This part will be seen after reopen page in incognito mode and try to make a tweet
                # Second option to code belowe: form.add_error("content","user must be logged in")
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(['User must be logged in to continue.'])
            return self.form_invalid(form)
