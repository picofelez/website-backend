from django import forms


class RatingForm(forms.Form):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    comment = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    rating = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=RATING_CHOICES,
        required=False
    )
