from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, \
                                      DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, \
                                       PermissionRequiredMixin
from django.forms.models import modelform_factory
from django.apps import apps
# from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from .models import Course, Module, Content
from .forms import ModuleFormSet


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin,
                       LoginRequiredMixin,
                       PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'

class CourseModuleUpdateView(TemplateResponseMixin, View):
    """The CourseModuleUpdateView view handles the formset to add, update, and
    delete modules for a specific course. This view inherits from the following mixins
    and views:
    • TemplateResponseMixin: This mixin takes charge of rendering templates
    and returning an HTTP response. It requires a template_name attribute
    that indicates the template to be rendered and provides the render_to_
    response() method to pass it a context and render the template.
    • View: The basic class-based view provided by Django.

    Args:
        TemplateResponseMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """
    template_name = 'courses/manage/module/formset.html'
    courses = None

    def get_formset(self, data=None):
        """: You define this method to avoid repeating the code to build
            the formset. You create a ModuleFormSet object for the given Course object
            with optional data.

        Args:
            request (_type_): request
            pk (id): primary key

        Returns:
            respose: formset
        """
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        """Executed for GET requests. You build an empty ModuleFormSet
            formset and render it to the template together with the current
            Course object using the render_to_response() method provided by
            TemplateResponseMixin.

        Args:
            request (dict): request

        Returns:
            respose: dict
        """ 
        formset = self.get_formset()
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })

class ContentCreateUpdateView(TemplateResponseMixin, View):
    """. It will allow you to create
and update different models' contents.

    Args:
        TemplateResponseMixin (mixin): template response
        View (view): respose

    Returns:
        form: dict
    """
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        """you check that the given model name is one of the four
            content models: Text, Video, Image, or File. Then, you use Django's apps
            module to obtain the actual class for the given model name. If the given
            model name is not one of the valid ones, you return None.

        Args:
            model_name (model): get model name

        Returns:
            model : model name
        """
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """You build a dynamic form using the modelform_factory()
            function of the form's framework. Since you are going to build a form for
            the Text, Video, Image, and File models, you use the exclude parameter
            to specify the common fields to exclude from the form and let all other
            attributes be included automatically. By doing so, you don't have to know
            which fields to include depending on the model.

        Args:
            model (model): model name

        Returns:
            form: model form
        """
        Form = modelform_factory(model, exclude=['owner', 'order', 'created','updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """° module_id: The ID for the module that the content is/will be
                associated with.
                ° model_name: The model name of the content to create/update.
                ° id: The ID of the object that is being updated. It's None to create new
                objects.

        Args:
            request (_type_): _description_
            module_id (_type_): _description_
            model_name (_type_): _description_
            id (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)
    
    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({
            'form': form,
            'object': self.obj
        })
    
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            self.model,
            instance = self.obj,
            data = request.POST,
            files = request.FILES
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module_id)
        return self.render_to_response({
            'form': form,
            'object':self.obj
        })

class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner = request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner = request.user)
        return self.render_to_response({
            'module': module
        })