from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    
    expiry_date = models.DateField(null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    quantity = models.CharField(max_length=5, null=True)
    
    

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-expiry_date']