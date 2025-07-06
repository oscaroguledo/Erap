from django.db import models

# Create your models here.

# Company details
class Company(models.Model):
    name = models.CharField(max_length=255)
    fiscal_year_start = models.DateField()
    fiscal_year_end = models.DateField()
    currency = models.CharField(max_length=10)  # e.g., INR, USD
    address = models.TextField(blank=True, null=True)
    # Add more company-specific fields here

    def __str__(self):
        return self.name


# Chart of Accounts
class Account(models.Model):
    ACCOUNT_TYPES = [
        ('Asset', 'Asset'),
        ('Liability', 'Liability'),
        ('Equity', 'Equity'),
        ('Revenue', 'Revenue'),
        ('Expense', 'Expense'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='accounts')
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    parent_account = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f"{self.code} - {self.name}"


# Fiscal Year model (optional if you want to store fiscal years separately)
class FiscalYear(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.start_date} to {self.end_date}"


# Payment Terms
class PaymentTerm(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    days = models.PositiveIntegerField(help_text="Number of days before payment is due")

    def __str__(self):
        return self.name


# Mode of Payment
class PaymentMode(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Tax Masters
class TaxCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TaxTemplate(models.Model):
    name = models.CharField(max_length=100)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tax_category = models.ForeignKey(TaxCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.tax_rate}%)"


# Cost Center
class CostCenter(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Sales Invoice
class SalesInvoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=255)
    date = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tax_template = models.ForeignKey(TaxTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    payment_term = models.ForeignKey(PaymentTerm, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer_name}"


# Purchase Invoice
class PurchaseInvoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True)
    supplier_name = models.CharField(max_length=255)
    date = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tax_template = models.ForeignKey(TaxTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    payment_term = models.ForeignKey(PaymentTerm, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Purchase {self.invoice_number} - {self.supplier_name}"


# Journal Entry
class JournalEntry(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    reference = models.CharField(max_length=255, blank=True, null=True)
    narration = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Journal Entry on {self.date}"


# Journal Entry Line (debits and credits)
class JournalEntryLine(models.Model):
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cost_center = models.ForeignKey(CostCenter, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.account} - Debit: {self.debit}, Credit: {self.credit}"


# Payment Entry (incoming and outgoing payments)
class PaymentEntry(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    mode_of_payment = models.ForeignKey(PaymentMode, on_delete=models.SET_NULL, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    related_invoice = models.ForeignKey(SalesInvoice, on_delete=models.SET_NULL, null=True, blank=True)
    # Could add link to PurchaseInvoice as well for outgoing payments

    def __str__(self):
        return f"Payment {self.amount} on {self.payment_date}"


# Bank Account
class BankAccount(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    branch = models.CharField(max_length=255, blank=True, null=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"


# Bank Reconciliation Statement
class BankReconciliation(models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    reconciliation_date = models.DateField()
    statement_balance = models.DecimalField(max_digits=15, decimal_places=2)
    reconciled_balance = models.DecimalField(max_digits=15, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reconciliation {self.reconciliation_date} for {self.bank_account}"


# Subscription Plans & Subscriptions
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.company} - {self.subscription_plan}"


# Shareholder and Share Transfer
class Shareholder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    shares_owned = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.shares_owned} shares)"


class ShareTransfer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    from_shareholder = models.ForeignKey(Shareholder, related_name='shares_sold', on_delete=models.CASCADE)
    to_shareholder = models.ForeignKey(Shareholder, related_name='shares_bought', on_delete=models.CASCADE)
    shares_transferred = models.PositiveIntegerField()
    transfer_date = models.DateField()

    def __str__(self):
        return f"{self.shares_transferred} shares from {self.from_shareholder} to {self.to_shareholder}"


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

class Customer(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)


class PurchaseInvoiceItem(models.Model):
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=12, decimal_places=2)



class SalesInvoiceItem(models.Model):
    invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=12, decimal_places=2)


class LedgerEntry(models.Model):
    party_type = models.CharField(max_length=50, choices=[("Customer", "Customer"), ("Supplier", "Supplier")])
    party_name = models.CharField(max_length=255)
    account = models.CharField(max_length=255)
    date = models.DateField()
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
