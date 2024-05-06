from django.db import models

# Create your models here.
class UnderContract(models.Model):
    address = models.CharField(max_length = 150, verbose_name = "Property")
    category = models.CharField(max_length = 20, choices = [("Buyer","Buyer"),("Seller","seller")], verbose_name = "Buyer/Seller")
    flex_organic = models.CharField(max_length=20, choices=[("Flex", "Flex"),("Team Lead","Team Lead"),("Organic","Organic")], verbose_name= "Flex/Organic")
    effective_date = models.DateField(verbose_name = "Effective Date")
    closing_date = models.DateField(null = True, verbose_name = "Closing date")
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Sale Price")
    escrow = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Escrow")
    commission = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Commission")
    mls_fee = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="MLS Fee")
    loop_closed = models.BooleanField(default=False, verbose_name="Loop Closed")
    notion_closed = models.BooleanField(default=False, verbose_name="Notion closed")
    flex_closed = models.BooleanField(default=False, verbose_name="Flex Tracker Updated")
    zillow_closed = models.BooleanField(default=False, verbose_name="Zillow Closed")
    kyn = models.BooleanField(default=False, verbose_name="Know Your Numbers Updated")
    close_pending = models.BooleanField(default=False, verbose_name="MVT Close and Pending Updated")
    notion = models.BooleanField(default = False, verbose_name = "Notion")
    congratulations = models.BooleanField(default = False, verbose_name = "Congrats Email")
    calendar = models.BooleanField(default = False, verbose_name = "Calendar Invites")
    flex_tracker = models.BooleanField(default = False, verbose_name = "Flex Tracker")
    loop = models.BooleanField(default = False, verbose_name = "Loop Created")
    da_requested = models.BooleanField(default = False, verbose_name = "DA requested")
    completed = models.BooleanField(verbose_name = "Completado")
    closed = models.BooleanField(default=False,verbose_name="Closed Deal")
    
    def save(self, *args, **kwargs):
        if self.congratulations and self.calendar and self.flex_tracker and self.notion and self.loop:
            self.completed = True
        else:
            self.completed = False
            
        if self.flex_organic == "Flex":
            if self.loop_closed and self.notion_closed and self.flex_closed and self.zillow_closed and self.kyn and self.close_pending:
                self.closed = True
            else:
                self.closed = False
        else:
            if self.loop_closed and self.notion_closed and self.flex_closed and self.kyn and self.close_pending:
                self.closed = True
            else:
                self.closed = False

       
        super().save(*args, **kwargs)  # Guardar el modelo después de actualizar el campo completed
    
    def __str__(self):
        return str(self.address)