from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
        

class Product(models.Model):
    choices_category = (
        ('Food','Food'),
        ('Drink', 'Drink'),
        ('Dessert', 'Dessert'),
    )
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(null=True)
    category = models.CharField(max_length=10, choices=choices_category, default='')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def is_available(self):
        return self.stock >= 1
	
    def is_sold_out(self):
        return self.stock <= 0
	
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        if self.stock < 0:
            self.stock = 0
        super().save(*args, **kwargs)

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def is_available(self):
		return self.product.stock >= self.quantity

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

	def save(self, *args, **kwargs):
		existing_order_item = OrderItem.objects.filter(order=self.order, product=self.product).first()

		if existing_order_item:
			existing_order_item.delete()

		super(OrderItem, self).save(*args, **kwargs)

class CheckoutDetail(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	full_name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=15, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address