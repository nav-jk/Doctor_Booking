from django.db import models

class DoctorAvailability(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return str(self.date)


class Token(models.Model):
    patient_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    date = models.DateField()
    token_number = models.IntegerField()

    def __str__(self):
        return f"{self.patient_name} - {self.token_number} on {self.date}"
