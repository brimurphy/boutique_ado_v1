from django.shortcuts import render, redirect, reverse, HttpResponse


# Create your views here.
def view_bag(request):

    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):

    """ Add a quantity of the specific product to the shopping bag """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # store items in session storage, if empty create one
    bag = request.session.get('bag', {})

    # check if item has a size
    if size:
        # if already in the bag add one
        if item_id in list(bag.keys()):
            # check if another item of same size and id already exists
            if size in bag[item_id]['items_by_size'].keys():
                # if so, increment the quantity for that size
                bag[item_id]['items_by_size'][size] += quantity
            # otherwise set it to equal quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        # if not in the bag set it to equal quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    # if item has no size
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):

    """ Adjust the quantity of the specified item to the specified amount """
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # store items in session storage, if empty create one
    bag = request.session.get('bag', {})

    # check if item has a size
    if size:
        # if more than 0 items
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        # if 0 items delete
        else:
            del bag[item_id]['items_by_size'][size]
            # If that was the only size they had in the bag
            # remove the entire item id
            # so no empty items by size dictionary is left hanging around
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    # if item has no size
    else:
        # if more than 0 items
        if quantity > 0:
            bag[item_id] = quantity
        # if 0 items delete
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):

    """ Remove the item from the shopping bag """
    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        # store items in session storage, if empty create one
        bag = request.session.get('bag', {})

        # check if item has a size
        if size:
            # Delete that size key by size dictionary
            del bag[item_id]['items_by_size'][size]
            # If that was the only size they had in the bag
            # remove the entire item id
            # so no empty items by size dictionary is left hanging around
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        # if item has no size
        else:
            # pop item out of bag
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
