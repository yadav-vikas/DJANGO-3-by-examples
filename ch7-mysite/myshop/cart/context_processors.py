# A context processor is a Python function that takes the request object as an
# argument and returns a dictionary that gets added to the request context. Context
# processors come in handy when you need to make something available globally
# to all templates.

# The cart context processor will be executed every time a template is rendered
# using Django's RequestContext. The cart variable will be set in the context
# of your templates. You can read more about RequestContext at https://
# docs.djangoproject.com/en/3.0/ref/templates/api/#django.template.
# RequestContext.

# By default, when you create a new project using the startproject command,
# your project contains the following template context processors in the
# context_processors option inside the TEMPLATES setting

# • django.template.context_processors.debug: This sets the Boolean
# debug and sql_queries variables in the context, representing the list of
# SQL queries executed in the request

# • django.template.context_processors.request: This sets the request
# variable in the context

# • django.contrib.auth.context_processors.auth: This sets the user
# variable in the request

# • django.contrib.messages.context_processors.messages: This sets
# a messages variable in the context containing all the messages that have
# been generated using the messages framework

from .cart import Cart

def cart(request):
    """In your context processor, instantiate the cart using the request object and make
    it available for the templates as a variable named cart.

    added context_manager in settings as well in templates 

    The cart context processor will be executed every time a template is rendered
    using Django's RequestContext. The cart variable will be set in the context
    of your templates. You can read more about RequestContext at 
    https://docs.djangoproject.com/en/3.0/ref/templates/api/#django.template.RequestContext.

    Args:
        request (dict): request

    Returns:
        request: all args of cart
    """
    return {'cart': Cart(request)}