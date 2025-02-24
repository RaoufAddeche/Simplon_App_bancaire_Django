from django.db import models
from django.conf import settings

class Loan(models.Model):
    "Modèle pour stocker les informations des prêts localement."
    #L'utilisateur qui a demandé le prêt 
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2) #montant du prêt
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    ) #status du prêt
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.SET_NULL,
                                    null= True,
                                    blank= True,
                                    related_name= "assigned_loans") #conseiller assigné
    created_at = models.DateTimeField(auto_now_add=True) #Date de création
    updated_at = models.DateTimeField(auto_now=True) #Dernière mise à jour

    def __str__(self):
        return f"Loan{self.id} - {self.status}"