
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

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
# 6. HEADER
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
# 7. SIDEBAR NAVIGATION
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
# 8. HOME PAGE
# ==========================================

if page == "Home":

    st.header("Welcome to ShopEase! 🎉")

    st.write(
        "Discover amazing products at affordable prices."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Products", len(products))
    col2.metric(
        "Cart Items",
        sum(st.session_state.cart.values())
    )
    col3.metric(
        "Total Orders",
        len(st.session_state.orders)
    )

    st.divider()

    st.subheader("⭐ Featured Products")

    cols = st.columns(4)

    for index, product in enumerate(products[:4]):

        with cols[index]:

            st.image(
                product["image"],
                use_container_width=True
            )

            st.markdown(
                f"**{product['name']}**"
            )

            st.write(f"₹{product['price']:,}")

            if st.button(
                "Add to Cart",
                key=f"home_{product['id']}",
                use_container_width=True
            ):

                product_id = product["id"]

                st.session_state.cart[product_id] = (
                    st.session_state.cart.get(product_id, 0) + 1
                )

                st.success("Added to cart!")
                st.rerun()

# ==========================================
# 9. PRODUCTS PAGE
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

                    st.markdown(
                        f"**{product['name']}**"
                    )

                    st.caption(product["category"])

                    st.write(product["description"])

                    st.subheader(
                        f"₹{product['price']:,}"
                    )

                    if st.button(
                        "🛒 Add to Cart",
                        key=f"product_{product['id']}",
                        use_container_width=True
                    ):

                        product_id = product["id"]

                        st.session_state.cart[product_id] = (
                            st.session_state.cart.get(product_id, 0) + 1
                        )

                        st.success("Product added!")
                        st.rerun()

# ==========================================
# 10. SHOPPING CART
# ==========================================

elif page == "Shopping Cart":

    st.header("🛒 Your Shopping Cart")

    if not st.session_state.cart:

        st.info("Your shopping cart is empty.")

    else:

        total = 0

        for product_id in list(st.session_state.cart.keys()):

            product = next(
                p for p in products if p["id"] == product_id
            )

            quantity = st.session_state.cart[product_id]

            subtotal = product["price"] * quantity

            total += subtotal

            col1, col2, col3 = st.columns([2, 2, 1])

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
                if st.button(
                    "Remove",
                    key=f"remove_{product_id}"
                ):
                    del st.session_state.cart[product_id]
                    st.rerun()

            st.divider()

        st.subheader(f"Total Amount: ₹{total:,}")

        if st.button("Clear Cart"):
            st.session_state.cart = {}
            st.rerun()

        if st.button(
            "Proceed to Checkout",
            type="primary"
        ):

            order = {
                "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "items": [
                    {
                        "name": next(
                            p["name"] for p in products
                            if p["id"] == product_id
                        ),
                        "quantity": quantity
                    }
                    for product_id, quantity
                    in st.session_state.cart.items()
                ],
                "total": total
            }

            st.session_state.orders.append(order)

            st.session_state.cart = {}

            st.session_state.checkout_message = (
                "Your demo order has been placed successfully!"
            )

            st.rerun()

        if st.session_state.checkout_message:

            st.success(st.session_state.checkout_message)

            st.session_state.checkout_message = ""

# ==========================================
# 11. AI SHOPPING ASSISTANT
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

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": user_question
                }
            )

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

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": answer
                            }
                        )

                    except Exception as error:

                        st.error(f"NVIDIA API Error: {error}")

        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

# ==========================================
# 12. ORDER HISTORY
# ==========================================

elif page == "Order History":

    st.header("📦 Your Order History")

    if not st.session_state.orders:

        st.info("You haven't placed any orders yet.")

    else:

        for index, order in enumerate(
            reversed(st.session_state.orders),
            start=1
        ):

            with st.expander(f"Order #{index}"):

                st.write(f"Order Date: {order['date']}")

                for item in order["items"]:

                    st.write(
                        f"{item['name']} × {item['quantity']}"
                    )

                st.subheader(
                    f"Total: ₹{order['total']:,}"
                )

# ==========================================
# 13. FOOTER
# ==========================================

st.divider()

st.caption(
    "© 2026 ShopEase | Powered by Streamlit and NVIDIA AI"
)
