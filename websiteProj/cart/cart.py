from buyerStore.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        # Returning user
        cart = self.session.get('session_key')

        # If user is new, no session key. Create one.
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of site
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()

        # Use ids to lookup products in db model
        products = Product.objects.filter(id__in=product_ids)

        # Return Products
        return products
    
    def get_quants(self):

        # Get qty from cart
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get cart
        oldCart = self.cart
        # Update Dictionary/cart
        oldCart[product_id] = product_qty

        self.session.modified = True

        updatedCart = self.cart
        return updatedCart

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True

    def cart_total(self):
        # Get product IDS
        product_ids = self.cart.keys()
        # Lookup keys in products DB model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0
        for key, value in quantities.items():
            # Convert key string into int to do math
            key = int(key)
            for product in products:
                if product.id == key and product.is_sale:
                    total = total + (product.sale_price * value)
                elif product.id == key and not product.is_sale:
                    total = total + (product.price * value)
        return total
