from django.shortcuts import render, redirect


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
