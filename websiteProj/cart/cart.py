from buyerStore.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request

        # Get the current session key if it exists
        # Returning user
        cart = self.session.get('cart_session_key')

        # If user is new, no session key. Create one.
        if 'cart_session_key' not in request.session:
            cart = self.session['cart_session_key'] = {}

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

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # {'3': 1, '4': 3} to {"3": 1, "4": 3}
            cart_edit = str(self.cart)
            cart_edit = cart_edit.replace("\'", "\"")
            # Save cart_edit to profile
            current_user.update(old_cart=str(cart_edit))
            
    def db_add(self, product_id, quantity):
        product_id = str(product_id)
        product_qty = int(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = product_qty

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # {'3': 1, '4': 3} to {"3": 1, "4": 3}
            cart_edit = str(self.cart)
            cart_edit = cart_edit.replace("\'", "\"")
            # Save cart_edit to profile
            current_user.update(old_cart=str(cart_edit))

    def __len__(self):
        if len(self.cart) == 0:
            return 0
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

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # {'3': 1, '4': 3} to {"3": 1, "4": 3}
            cart_edit = str(self.cart)
            cart_edit = cart_edit.replace("\'", "\"")
            # Save cart_edit to profile
            current_user.update(old_cart=str(cart_edit))

        updatedCart = self.cart
        return updatedCart

    def clear(self):
        # Clear cart
        self.cart = {}
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            cart_edit = self.cart.clear()
            # Save cart_edit to profile
            current_user.update(old_cart=str(cart_edit))
            
        

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # {'3': 1, '4': 3} to {"3": 1, "4": 3}
            cart_edit = str(self.cart)
            cart_edit = cart_edit.replace("\'", "\"")
            # Save cart_edit to profile
            current_user.update(old_cart=str(cart_edit))


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

    def cart_item_prices(self):
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