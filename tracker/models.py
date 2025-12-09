from django.db import models

class Transaction(models.Model):
    """Transaction model to store financial transaction details."""
    transaction_id = models.AutoField(primary_key=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"


class Category(models.Model):
    """Category model to classify transactions."""
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES,
                            default='EXPENSE')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
