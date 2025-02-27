from django.db import models
from user.models import User

class LoanRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=2)
    naics = models.IntegerField()
    new_exist = models.IntegerField()
    retained_job = models.IntegerField()
    franchise_code = models.IntegerField()
    urban_rural = models.IntegerField()
    gr_appv = models.FloatField()
    bank = models.CharField(max_length=255)
    term = models.IntegerField()
    prediction = models.FloatField(null=True, blank=True)  # Stockera la prédiction

    def __str__(self):
        return f"LoanRequest {self.id} - {self.state}"
