from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View, generic

from .forms import CommentForm, RecipeForm
from .models import Recipe, Comment


class IndexView(generic.ListView):
    paginate_by = 6
    context_object_name = 'recipe_list'
    template_name = 'index.html'

    def get_queryset(self):

        return Recipe.objects.order_by('-created_at')


def detail(request, slug):
    print('Called details')
    latest_posts = Recipe.objects.order_by('-created_at')[:5]
    recipe = get_object_or_404(Recipe, slug=slug)
    comments = Comment.objects.filter(recipe=recipe)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
            return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {
        'latest_posts': latest_posts,
        'recipe': recipe,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'detail.html', context)


def search(request):
    print('Got here')
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        recipe_list = Recipe.objects.filter(Q(title__icontains=q))
        # music_list = Recipe.objects.filter(Q(title__icontains=q) | Q(artist__icontains=q))
        context = {'query': q, 'recipe_list': recipe_list}
        template = 'results.html'

    else:
        template = 'index.html'
        context = {}
    return render(request, template, context)


def add_recipe(request):
    if request.method == 'POST':
        print(request.POST.get('image'))
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            # Create a new Recipe instance with the form data
            new_recipe = Recipe(
                author=request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                ingredients=form.cleaned_data['ingredients'],
                instructions=form.cleaned_data['instructions'],
                image=form.cleaned_data['image']  # If an image is uploaded, it will be saved to the model's image field
            )
            print(form.cleaned_data['image'])
            new_recipe.save()
            return redirect('recipe:index')  # Redirect to a success page after saving the recipe
    else:
        form = RecipeForm()  # Create an empty form for GET requests

    return render(request, 'index.html', {'form': form})
