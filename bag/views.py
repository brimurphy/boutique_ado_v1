from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404)
from django.contrib import messages

from products.models import Product


# Create your views here.
def view_bag(request):

    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):

    """ Add a quantity of the specific product to the shopping bag """
    product = get_object_or_404(Product, pk=item_id)
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
                messages.success(
                    request, f'Update size {size.upper()} {product.name}\
                        quantity to {bag[item_id]["items_by_size"][size]}')
            # otherwise set it to equal quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(
                    request, f'Added size {size.upper()} {product.name}\
                        to your bag')
        # if not in the bag set it to equal quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(
                request, f'Added size {size.upper()} {product.name}\
                    to your bag')
    # if item has no size
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(
                request, f'Updated {product.name}, quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):

    """ Adjust the quantity of the specified item to the specified amount """
    product = get_object_or_404(Product, pk=item_id)
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
            messages.success(
                request, f'Update size {size.upper()} {product.name}\
                    quantity to {bag[item_id]["items_by_size"][size]}')
        # if 0 items delete
        else:
            del bag[item_id]['items_by_size'][size]
            # If that was the only size they had in the bag
            # remove the entire item id
            # so no empty items by size dictionary is left hanging around
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(
                request, f'Removed size {size.upper()} {product.name}\
                from your bag')
    # if item has no size
    else:
        # if more than 0 items
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(
                request, f'Updated {product.name}, quantity to {bag[item_id]}')
        # if 0 items delete
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name}, from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):

    """ Remove the item from the shopping bag """
    try:
        product = get_object_or_404(Product, pk=item_id)
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
            messages.success(
                request, f'Removed size {size.upper()} {product.name}\
                    from your bag')
        # if item has no size
        else:
            # pop item out of bag
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name}, from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item {e}')
        return HttpResponse(status=500)
