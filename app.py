
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="ShopEase | Online Shopping",
    page_icon="🛍️",
    layout="wide"
)

# ==========================================
# 2. LOAD NVIDIA API KEY
# ==========================================

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

NVIDIA_MODEL = os.getenv(
    "NVIDIA_MODEL",
    "meta/llama-3.3-70b-instruct"
)

# ==========================================
# 3. NVIDIA API CONNECTION
# ==========================================

@st.cache_resource
def get_nvidia_client():

    if not NVIDIA_API_KEY:
        return None

    return OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_API_KEY,
        timeout=60.0,
        max_retries=2
    )


client = get_nvidia_client()

# ==========================================
# 4. PRODUCT DATABASE
# ==========================================

products = [
    {
        "id": 1,
        "name": "Wireless Headphones",
        "category": "Electronics",
        "price": 1499,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600",
        "description": "High-quality wireless headphones."
    },
    {
        "id": 2,
        "name": "Smart Watch",
        "category": "Electronics",
        "price": 2499,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600",
        "description": "Stylish smartwatch for everyday use."
    },
    {
        "id": 3,
        "name": "Running Shoes",
        "category": "Fashion",
        "price": 1999,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600",
        "description": "Comfortable shoes for running."
    },
    {
        "id": 4,
        "name": "Backpack",
        "category": "Accessories",
        "price": 999,
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600",
        "description": "Durable backpack for daily use."
    },
    {
        "id": 5,
        "name": "Sunglasses",
        "category": "Fashion",
        "price": 799,
        "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600",
        "description": "Trendy sunglasses for everyday use."
    },
    {
        "id": 6,
        "name": "Digital Camera",
        "category": "Electronics",
        "price": 12999,
        "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=600",
        "description": "Capture your special moments."
    }
]

# ==========================================
# 5. SESSION STATE
# ==========================================

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "order_number" not in st.session_state:
    st.session_state.order_number = 1000

if "orders" not in st.session_state:
    st.session_state.orders = []

# ==========================================
# 6. HELPER FUNCTIONS
# ==========================================

def add_to_cart(product_id):

    st.session_state.cart[product_id] = (
        st.session_state.cart.get(product_id, 0) + 1
    )


def calculate_total():

    total = 0

    for product_id, quantity in st.session_state.cart.items():

        product = next(
            p for p in products if p["id"] == product_id
        )

        total += product["price"] * quantity

    return total


# ==========================================
# 7. APPLICATION HEADER
# ==========================================

st.title("🛍️ ShopEase")

st.caption("Your Smart Online Shopping Destination")

st.markdown("---")

# ==========================================
# 8. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🛍️ ShopEase Menu")

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Products",
        "Shopping Cart",
        "AI Shopping Assistant",
        "Checkout",
        "Order History"
    ]
)

cart_count = sum(st.session_state.cart.values())

st.sidebar.metric("🛒 Cart Items", cart_count)

st.sidebar.markdown("---")

st.sidebar.success("Powered by NVIDIA AI")

st.sidebar.caption("Built using Python and Streamlit")


# ==========================================
# 9. HOME PAGE
# ==========================================

if page == "Home":

    st.header("Welcome to ShopEase!")

    st.subheader("Discover amazing products at great prices.")

    st.write(
        "Shop electronics, fashion and accessories "
        "from one convenient shopping destination."
    )

    st.success("🎉 Your smart shopping experience starts here!")

    st.markdown("---")

    st.subheader("Why Choose ShopEase?")

    col1, col2, col3 = st.columns(3)

    col1.metric("Available Products", len(products))

    col2.metric(
        "Categories",
        len(set(p["category"] for p in products))
    )

    col3.metric("AI Assistant", "Available")

    st.markdown("---")

    st.subheader("⭐ Featured Products")

    cols = st.columns(3)

    for index, product in enumerate(products[:3]):

        with cols[index]:

            st.image(
                product["image"],
                use_container_width=True
            )

            st.subheader(product["name"])

            st.write(f"₹{product['price']:,}")

            if st.button(
                "Add to Cart 🛒",
                key=f"home_{product['id']}",
                use_container_width=True
            ):

                add_to_cart(product["id"])

                st.success("Product added to cart!")


# ==========================================
# 10. PRODUCTS PAGE
# ==========================================

elif page == "Products":

    st.header("🛒 Explore Our Products")

    search = st.text_input(
        "🔍 Search Products",
        placeholder="Enter product name..."
    )

    categories = ["All"] + sorted(
        list(set(p["category"] for p in products))
    )

    category = st.selectbox(
        "Select Product Category",
        categories
    )

    filtered_products = products

    if search:

        filtered_products = [
            p for p in filtered_products
            if search.lower() in p["name"].lower()
        ]

    if category != "All":

        filtered_products = [
            p for p in filtered_products
            if p["category"] == category
        ]

    if not filtered_products:

        st.warning("No products found.")

    else:

        st.write(
            f"Showing {len(filtered_products)} products."
        )

        cols = st.columns(3)

        for index, product in enumerate(filtered_products):

            with cols[index % 3]:

                st.image(
                    product["image"],
                    use_container_width=True
                )

                st.subheader(product["name"])

                st.caption(product["category"])

                st.write(product["description"])

                st.markdown(
                    f"### ₹{product['price']:,}"
                )

                if st.button(
                    "Add to Cart 🛒",
                    key=f"product_{product['id']}",
                    use_container_width=True
                ):

                    add_to_cart(product["id"])

                    st.success("Added successfully!")


# ==========================================
# 11. SHOPPING CART
# ==========================================

elif page == "Shopping Cart":

    st.header("🛒 Your Shopping Cart")

    if not st.session_state.cart:

        st.info("Your shopping cart is empty.")

    else:

        for product_id in list(st.session_state.cart.keys()):

            product = next(
                p for p in products
                if p["id"] == product_id
            )

            quantity = st.session_state.cart[product_id]

            col1, col2, col3, col4, col5 = st.columns(
                [2, 1, 1, 1, 1]
            )

            with col1:
                st.write(f"**{product['name']}**")
                st.caption(f"₹{product['price']:,} each")

            with col2:

                if st.button(
                    "➖",
                    key=f"minus_{product_id}"
                ):

                    if quantity > 1:
                        st.session_state.cart[product_id] -= 1
                    else:
                        del st.session_state.cart[product_id]

                    st.rerun()

            with col3:
                st.write(f"Quantity: {quantity}")

            with col4:

                if st.button(
                    "➕",
                    key=f"plus_{product_id}"
                ):

                    st.session_state.cart[product_id] += 1

                    st.rerun()

            with col5:

                if st.button(
                    "🗑️",
                    key=f"delete_{product_id}"
                ):

                    del st.session_state.cart[product_id]

                    st.rerun()

            st.write(
                f"Subtotal: ₹{product['price'] * quantity:,}"
            )

            st.markdown("---")

        total = calculate_total()

        st.subheader(f"Total Amount: ₹{total:,}")

        if st.button("Clear Entire Cart"):

            st.session_state.cart = {}

            st.rerun()


# ==========================================
# 12. AI SHOPPING ASSISTANT
# ==========================================

elif page == "AI Shopping Assistant":

    st.header("🤖 NVIDIA AI Shopping Assistant")

    st.write(
        "Ask questions and get smart product recommendations "
        "from our AI shopping assistant."
    )

    if not NVIDIA_API_KEY:

        st.error(
            "NVIDIA API key not found. "
            "Please check your .env file."
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
                    f"{p['name']} - ₹{p['price']} - "
                    f"{p['category']} - {p['description']}"
                    for p in products
                ]
            )

            system_prompt = f"""
            You are ShopEase's friendly AI shopping assistant.

            Help customers select suitable products.

            Recommend only products from the following catalog.

            Never invent product names, prices or availability.

            Product Catalog:

            {product_information}

            Give simple, friendly and helpful answers.
            """

            try:

                with st.chat_message("assistant"):

                    with st.spinner(
                        "NVIDIA AI is generating a response..."
                    ):

                        response = client.chat.completions.create(

                            model=NVIDIA_MODEL,

                            messages=[
                                {
                                    "role": "system",
                                    "content": system_prompt
                                }
                            ] + st.session_state.chat_history,

                            temperature=0.5,

                            max_tokens=500
                        )

                        answer = response.choices[0].message.content

                        if not answer:
                            answer = "Sorry, I could not generate an answer."

                        st.markdown(answer)

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(f"NVIDIA API Error: {str(e)}")

                st.write("Error Type:", type(e).__name__)

                if hasattr(e, "status_code"):
                 st.write("HTTP Status:", e.status_code)

                if hasattr(e, "response"):
                 st.write("Detailed NVIDIA Response:")

                 st.code(e.response.text)

        st.info(
        "Please check the model availability "
        "and NVIDIA API configuration."
    )
        if st.button("Clear Chat History"):

            st.session_state.chat_history = []

            st.rerun()


# ==========================================
# 13. CHECKOUT PAGE
# ==========================================

elif page == "Checkout":

    st.header("💳 Customer Checkout")

    if not st.session_state.cart:

        st.warning(
            "Your shopping cart is empty. "
            "Please add products before checkout."
        )

    else:

        total = calculate_total()

        st.subheader(f"Order Total: ₹{total:,}")

        with st.form("checkout_form"):

            customer_name = st.text_input("Full Name")

            email = st.text_input("Email Address")

            phone = st.text_input("Phone Number")

            address = st.text_area("Delivery Address")

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Cash on Delivery",
                    "Demo Online Payment"
                ]
            )

            submitted = st.form_submit_button(
                "Place Order"
            )

            if submitted:

                if not all(
                    [
                        customer_name.strip(),
                        email.strip(),
                        phone.strip(),
                        address.strip()
                    ]
                ):

                    st.error("Please complete all fields.")

                elif (
                    "@" not in email
                    or "." not in email.split("@")[-1]
                ):

                    st.error("Please enter a valid email address.")

                elif (
                    not phone.strip().isdigit()
                    or len(phone.strip()) != 10
                ):

                    st.error(
                        "Please enter a valid 10-digit phone number."
                    )

                else:

                    st.session_state.order_number += 1

                    order_id = (
                        f"SE{st.session_state.order_number}"
                    )

                    order = {
                        "order_id": order_id,
                        "customer": customer_name,
                        "email": email,
                        "phone": phone,
                        "address": address,
                        "total": total,
                        "payment": payment_method
                    }

                    st.session_state.orders.append(order)

                    st.success(
                        "🎉 Your demo order was placed successfully!"
                    )

                    st.write(f"**Order ID:** {order_id}")

                    st.write(f"**Customer:** {customer_name}")

                    st.write(f"**Total:** ₹{total:,}")

                    st.write(f"**Payment:** {payment_method}")

                    st.info(
                        "This is a demonstration checkout. "
                        "No real payment has been processed."
                    )

                    st.session_state.cart = {}


# ==========================================
# 14. ORDER HISTORY
# ==========================================

elif page == "Order History":

    st.header("📦 Your Order History")

    if not st.session_state.orders:

        st.info("No orders have been placed yet.")

    else:

        for order in reversed(st.session_state.orders):

            with st.expander(order["order_id"]):

                st.write(
                    f"Customer: {order['customer']}"
                )

                st.write(
                    f"Email: {order['email']}"
                )

                st.write(
                    f"Delivery Address: {order['address']}"
                )

                st.write(
                    f"Order Total: ₹{order['total']:,}"
                )

                st.write(
                    f"Payment: {order['payment']}"
                )


# ==========================================
# 15. FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "© 2026 ShopEase | Built with Python, "
    "Streamlit and NVIDIA NIM AI"
)
