from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginator(request, images, results):

    page = request.GET.get("page")
    paginator = Paginator(images, results)

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        images = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        images = paginator.page(page)

    leftindex = int(page) - 4
    if leftindex < 1:
        leftindex = 1
    rightindex = int(page) + 5
    if rightindex > paginator.num_pages:
        rightindex = paginator.num_pages + 1

    custom_range = range(leftindex, rightindex)

    return custom_range, images
