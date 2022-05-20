from tabnanny import verbose
from django.db import models
from django.urls import reverse
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name     = models.CharField(max_length=200, db_index=True)
    slug     = models.SlugField(max_length=200, db_index=True)
    image    = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug',),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def save(self, ** kwargs):
        """we are chopping down the size of user profile if in case the image large and takes lof of time
        to load on the browser
        Note:When you are overriding model's save method in Django, you should also pass *args and **kwargs to overridden method.
        ERROR - u might get an error called ------- save() got an unexpected keyword argument 'force_insert'-------- 
        because in save method by defualt force_insert=True , to overcome this we must pass ** kwargs as well.
        Why ? 
        >>>>>>>every function has a "signature", a pattern of arguments. 
        If you override save with a new definition that doesn't take any arguments (except the implicit self), 
        you get the reported error when it is passed an argument it is expected to handle, e.g. force_insert. 
        The *args, **kwargs syntax says, "collect all positional args in the args list and all keyword args in the kwargs dict".
         Then they can be passed along via the super call to do their work.
        """
        super().save()# saving the image from the class

        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300 :#chopp the image to (300,300) size
            output_size = (300,300)
            image.thumbnail(output_size)
            image.save(self.image.path)


class ItemOptions(models.Model):
    # option_id 
    Product_name_item_options = models.ForeignKey(Product, related_name='item_options', on_delete=models.CASCADE)
    option_name_item_options = models.CharField(max_length=50, db_index=True)
    price_item_options = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.option_name_item_options

class ExtraItemOptions(models.Model):
    Product_name_extra_item_options = models.ForeignKey(Product, related_name='item_extra_options', on_delete=models.CASCADE)
    option_name_extra_item_options  = models.CharField(max_length=50, db_index=True)
    price_extra_item_options = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.option_name_extra_item_options
