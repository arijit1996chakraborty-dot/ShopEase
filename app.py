import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from copy import deepcopy

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="ShopEase - Online Shopping",
    page_icon="🛍️",
    layout="wide"
)

# ==========================================
# 2. NVIDIA API CONFIGURATION
# ==========================================

load_dotenv()


def get_setting(name):
    """Read a setting from Streamlit Secrets first, then from .env."""
    try:
        value = st.secrets.get(name)
        if value:
            return value
    except Exception:
        pass

    return os.getenv(name)


NVIDIA_API_KEY = get_setting("NVIDIA_API_KEY")
NVIDIA_MODEL = get_setting("NVIDIA_MODEL")

client = None

if NVIDIA_API_KEY and NVIDIA_MODEL:
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_API_KEY
    )

# ==========================================
# 3. CUSTOM CSS
# ==========================================

st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #2563eb;
    }

    .subtitle {
        font-size: 18px;
        color: #64748b;
    }

    .product-name {
        font-size: 20px;
        font-weight: bold;
    }

    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. SESSION STATE
# ==========================================

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "orders" not in st.session_state:
    st.session_state.orders = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "checkout_open" not in st.session_state:
    st.session_state.checkout_open = False

if "checkout_message" not in st.session_state:
    st.session_state.checkout_message = ""

# ==========================================
# 5. PRODUCT DATABASE WITH IMAGES
# ==========================================

products = [
    {
        "id": 1,
        "name": "Wireless Headphones",
        "category": "Electronics",
        "price": 1999,
        "description": "Premium wireless headphones with comfortable ear cushions.",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=700",
    },
    {
        "id": 2,
        "name": "Smart Watch",
        "category": "Electronics",
        "price": 2499,
        "description": "Modern smartwatch for everyday fitness tracking.",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=700",
    },
    {
        "id": 3,
        "name": "Running Shoes",
        "category": "Fashion",
        "price": 1799,
        "description": "Comfortable running shoes for everyday use.",
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700",
    },
    {
        "id": 4,
        "name": "Men's T-Shirt",
        "category": "Fashion",
        "price": 599,
        "description": "Comfortable cotton T-shirt with a modern style.",
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=700",
    },
    {
        "id": 5,
        "name": "Laptop Backpack",
        "category": "Accessories",
        "price": 999,
        "description": "Durable backpack for carrying your laptop.",
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=700",
    },
    {
        "id": 6,
        "name": "Coffee Maker",
        "category": "Home",
        "price": 2999,
        "description": "Make your favourite coffee at home.",
        "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=700",
    },
    {
        "id": 7,
        "name": "Bluetooth Speaker",
        "category": "Electronics",
        "price": 1499,
        "description": "Portable speaker with wireless connectivity.",
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=700",
    },
    {
        "id": 8,
        "name": "Sunglasses",
        "category": "Accessories",
        "price": 799,
        "description": "Stylish sunglasses for everyday use.",
        "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=700",
    }
]

# ==========================================
# 6. CART HELPER FUNCTIONS
# ==========================================

def add_to_cart(product_id):
    """Add one unit of a product to the cart."""
    st.session_state.cart[product_id] = (
        st.session_state.cart.get(product_id, 0) + 1
    )


def decrease_cart_quantity(product_id):
    """Decrease quantity by one; delete only when it reaches zero."""
    if product_id not in st.session_state.cart:
        return

    new_quantity = st.session_state.cart[product_id] - 1

    if new_quantity <= 0:
        del st.session_state.cart[product_id]
    else:
        st.session_state.cart[product_id] = new_quantity


def get_cart_total():
    """Calculate the current cart total."""
    total = 0
    for product_id, quantity in st.session_state.cart.items():
        product = next(
            (p for p in products if p["id"] == product_id),
            None
        )
        if product:
            total += product["price"] * quantity
    return total


# ==========================================
# 7. HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🛍️ ShopEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your Smart Online Shopping Destination</div>',
    unsafe_allow_html=True
)

st.divider()

# ==========================================
# 8. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🛍️ ShopEase")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Products",
        "Shopping Cart",
        "AI Shopping Assistant",
        "Order History"
    ]
)

st.sidebar.divider()
st.sidebar.subheader("AI Connection")

if client:
    st.sidebar.success("NVIDIA AI Connected")
else:
    st.sidebar.warning("NVIDIA credentials not found")

st.sidebar.metric(
    "Items in Cart",
    sum(st.session_state.cart.values())
)

# ==========================================
# 9. HOME PAGE
# ==========================================

if page == "Home":

    st.header("Welcome to ShopEase! 🎉")
    st.write("Discover amazing products at affordable prices.")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Products", len(products))
    col2.metric("Cart Items", sum(st.session_state.cart.values()))
    col3.metric("Total Orders", len(st.session_state.orders))

    st.divider()
    st.subheader("⭐ Featured Products")

    cols = st.columns(4)

    for index, product in enumerate(products[:4]):
        with cols[index]:
            st.image(
                product["image"],
                use_container_width=True
            )
            st.markdown(f"**{product['name']}**")
            st.write(f"₹{product['price']:,}")

            if st.button(
                "Add to Cart",
                key=f"home_{product['id']}",
                use_container_width=True
            ):
                add_to_cart(product["id"])
                st.success("Added to cart!")
                st.rerun()

# ==========================================
# 10. PRODUCTS PAGE
# ==========================================

elif page == "Products":

    st.header("🛒 Explore Our Products")

    search = st.text_input(
        "🔍 Search Products",
        placeholder="Search headphones, shoes, watches..."
    )

    categories = ["All"] + sorted(
        list(set(p["category"] for p in products))
    )

    selected_category = st.selectbox(
        "Choose Product Category",
        categories
    )

    filtered_products = products

    if search:
        filtered_products = [
            p for p in filtered_products
            if search.lower() in p["name"].lower()
            or search.lower() in p["description"].lower()
        ]

    if selected_category != "All":
        filtered_products = [
            p for p in filtered_products
            if p["category"] == selected_category
        ]

    if not filtered_products:
        st.info("No matching products found.")
    else:
        cols = st.columns(3)

        for index, product in enumerate(filtered_products):
            with cols[index % 3]:
                with st.container(border=True):
                    st.image(
                        product["image"],
                        use_container_width=True
                    )
                    st.markdown(f"**{product['name']}**")
                    st.caption(product["category"])
                    st.write(product["description"])
                    st.subheader(f"₹{product['price']:,}")

                    if st.button(
                        "🛒 Add to Cart",
                        key=f"product_{product['id']}",
                        use_container_width=True
                    ):
                        add_to_cart(product["id"])
                        st.success("Product added!")
                        st.rerun()

# ==========================================
# 11. SHOPPING CART AND CHECKOUT
# ==========================================

elif page == "Shopping Cart":

    st.header("🛒 Your Shopping Cart")

    if not st.session_state.cart:
        st.info("Your shopping cart is empty.")
        st.session_state.checkout_open = False

    else:
        for product_id in list(st.session_state.cart.keys()):
            product = next(
                (p for p in products if p["id"] == product_id),
                None
            )

            if not product:
                continue

            quantity = st.session_state.cart[product_id]
            subtotal = product["price"] * quantity

            col1, col2, col3 = st.columns([1.3, 3, 1.7])

            with col1:
                st.image(
                    product["image"],
                    width=120
                )

            with col2:
                st.write(f"**{product['name']}**")
                st.write(f"Price: ₹{product['price']:,}")
                st.write(f"Quantity: {quantity}")
                st.write(f"Subtotal: ₹{subtotal:,}")

            with col3:
                button_col1, button_col2 = st.columns(2)

                with button_col1:
                    if st.button(
                        "➖",
                        key=f"decrease_{product_id}",
                        help="Remove one unit"
                    ):
                        decrease_cart_quantity(product_id)
                        st.rerun()

                with button_col2:
                    if st.button(
                        "➕",
                        key=f"increase_{product_id}",
                        help="Add one unit"
                    ):
                        add_to_cart(product_id)
                        st.rerun()

                if st.button(
                    "Remove Product",
                    key=f"remove_all_{product_id}",
                    use_container_width=True
                ):
                    del st.session_state.cart[product_id]
                    st.rerun()

            st.divider()

        total = get_cart_total()
        st.subheader(f"Total Amount: ₹{total:,}")

        clear_col, checkout_col = st.columns(2)

        with clear_col:
            if st.button(
                "Clear Entire Cart",
                use_container_width=True
            ):
                st.session_state.cart = {}
                st.session_state.checkout_open = False
                st.session_state.checkout_message = ""
                st.rerun()

        with checkout_col:
            if st.button(
                "Proceed to Checkout",
                type="primary",
                use_container_width=True
            ):
                st.session_state.checkout_open = True
                st.session_state.checkout_message = ""
                st.rerun()

        if st.session_state.checkout_open:
            st.divider()
            st.subheader("🧾 Checkout")
            st.write(
                "Review your selection below. Your cart will remain unchanged "
                "after placing the order."
            )

            checkout_choice = st.radio(
                "Choose an action:",
                ["Place Order", "Cancel Order"],
                index=1,
                key="checkout_choice"
            )

            confirm_col, cancel_col = st.columns(2)

            with confirm_col:
                if st.button(
                    "Confirm Selection",
                    type="primary",
                    use_container_width=True
                ):
                    if checkout_choice == "Place Order":
                        # Save a separate snapshot of the order.
                        # The shopping cart is deliberately not cleared.
                        order_items = []

                        for product_id, quantity in st.session_state.cart.items():
                            product = next(
                                (
                                    p for p in products
                                    if p["id"] == product_id
                                ),
                                None
                            )

                            if product:
                                order_items.append({
                                    "name": product["name"],
                                    "quantity": quantity,
                                    "unit_price": product["price"],
                                    "subtotal": product["price"] * quantity
                                })

                        order = {
                            "order_id": len(st.session_state.orders) + 1,
                            "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                            "items": deepcopy(order_items),
                            "total": total,
                            "status": "Placed"
                        }

                        st.session_state.orders.append(order)
                        st.session_state.checkout_message = (
                            f"Order #{order['order_id']} placed successfully! "
                            "Your cart has been preserved."
                        )
                        st.session_state.checkout_open = False
                        st.rerun()

                    else:
                        st.session_state.checkout_open = False
                        st.session_state.checkout_message = (
                            "Checkout cancelled. Your cart has not been changed."
                        )
                        st.rerun()

            with cancel_col:
                if st.button(
                    "Close Checkout",
                    use_container_width=True
                ):
                    st.session_state.checkout_open = False
                    st.session_state.checkout_message = (
                        "Checkout closed. Your cart has not been changed."
                    )
                    st.rerun()

    if st.session_state.checkout_message:
        st.success(st.session_state.checkout_message)

# ==========================================
# 12. AI SHOPPING ASSISTANT
# ==========================================

elif page == "AI Shopping Assistant":

    st.header("🤖 AI Shopping Assistant")
    st.write(
        "Tell me what you need. "
        "I'll help you find the right product."
    )

    if not client:
        st.error(
            "NVIDIA API credentials are missing. "
            "Check your .env file or Streamlit Cloud Secrets."
        )
    else:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_question = st.chat_input(
            "Ask me about our products..."
        )

        if user_question:
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            with st.chat_message("user"):
                st.markdown(user_question)

            product_information = "\n".join(
                [
                    f"{p['name']} | Category: {p['category']} "
                    f"| Price: ₹{p['price']} "
                    f"| Description: {p['description']}"
                    for p in products
                ]
            )

            system_prompt = f"""
            You are the friendly AI Shopping Assistant of ShopEase.

            Help customers find products, compare prices,
            and understand product descriptions.

            Recommend only products in the catalogue.
            Never invent prices, discounts or stock availability.

            Be polite, helpful and concise.

            PRODUCT CATALOGUE:
            {product_information}
            """

            with st.chat_message("assistant"):
                with st.spinner("AI is thinking..."):
                    try:
                        response = client.chat.completions.create(
                            model=NVIDIA_MODEL,
                            messages=[
                                {
                                    "role": "system",
                                    "content": system_prompt
                                },
                                *st.session_state.chat_history
                            ],
                            temperature=0.5,
                            max_tokens=700
                        )

                        answer = response.choices[0].message.content
                        st.markdown(answer)

                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": answer
                        })

                    except Exception as error:
                        st.error(f"NVIDIA API Error: {error}")

        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

# ==========================================
# 13. ORDER HISTORY
# ==========================================

elif page == "Order History":

    st.header("📦 Your Order History")

    if not st.session_state.orders:
        st.info("You haven't placed any orders yet.")
    else:
        for order in reversed(st.session_state.orders):
            order_number = order.get("order_id", "N/A")

            with st.expander(f"Order #{order_number}"):
                st.write(f"Order Date: {order['date']}")
                st.write(f"Status: {order.get('status', 'Placed')}")

                for item in order["items"]:
                    st.write(
                        f"{item['name']} × {item['quantity']} "
                        f"— ₹{item.get('subtotal', 0):,}"
                    )

                st.subheader(f"Total: ₹{order['total']:,}")

# ==========================================
# 14. FOOTER
# ==========================================

st.divider()

st.caption(
    "© 2026 ShopEase | Powered by Streamlit and NVIDIA AI"
)
