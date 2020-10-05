from django.shortcuts import render,get_object_or_404

from .models import Post

# Create your views here.
def allposts(request):
#    return render(request,'posts/allposts.html')
    posts = Post.objects
    categories = return_unique_cats()
    post_per_cat = get_latest_post_per_cat(posts)
    context = create_status_for_tabs('home')
    return render(request,'posts/allposts.html',{'post_per_cat':post_per_cat,'feature_post':post_per_cat[0],'categories':categories,'context':context})

def create_status_for_tabs(cat_req=''):
    categories = return_unique_cats()
    context = {cat:"muted_tab" for cat in categories}
    context['home'] = "active_tab" if cat_req=='' else "muted_tab"
    context['about'] = "muted_tab"
    context[cat_req] = "active_tab"
    return context

def about(request):
    categories = return_unique_cats()
    context = create_status_for_tabs('about')
    return render(request,'posts/about.html',{'categories':categories,'context':context})


def return_unique_cats():
    posts = Post.objects
    categories = []
    for item in posts.all():
        categories.append(item.category.strip())
    categories = list(set(categories))
    categories.sort() 
    return categories

def get_latest_post_per_cat(posts):
    categories = return_unique_cats()
    posts_for_home = {cat:[] for cat in categories}
    posts_to_send = []
    for item in posts.all():
        posts_for_home[item.category.strip()].append(item)
    for i,cat_posts in posts_for_home.items():
        cat_posts = sorted(cat_posts,key=lambda x: x.pub_date,reverse=True) 
        posts_for_home[i] = cat_posts
    for sorted_posts in posts_for_home.values():
        posts_to_send.extend(sorted_posts)
    return posts_to_send
    
def return_cat_based_posts(request,cat):
    posts = Post.objects
    categories = return_unique_cats()
    cat_based_posts = []
    for item in posts.all():
        if item.category.strip().lower() == cat.strip().lower():
            cat_based_posts.append(item)
    context = create_status_for_tabs(cat)
    return render(request,'posts/catpost.html',{'cat_based_posts':cat_based_posts,'feature_post':cat_based_posts[0],'categories':categories,'context':context})    

def detail(request,feature_post_id):
    categories = return_unique_cats()
    detailpost = get_object_or_404(Post,pk=feature_post_id)
    context = create_status_for_tabs(detailpost.category.strip())
    posts = Post.objects
    post_per_cat = get_latest_post_per_cat(posts)
    return render(request,'posts/post.html',{'post_per_cat':post_per_cat,'categories':categories,'detailpost':detailpost,'context':context})
