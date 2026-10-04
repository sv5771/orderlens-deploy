import streamlit as st
import sqlite3
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------

st.set_page_config(
    page_title="OrderLens",
    page_icon="📦",
    layout="wide"
)

DB_PATH = Path("orders.db")


# -----------------------------
# Database
# -----------------------------

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


def add_order(customer, product, quantity):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO orders (customer, product, quantity, status)
        VALUES (?, ?, ?, ?)
        """,
        (customer, product, quantity, "Pending")
    )

    conn.commit()
    conn.close()


def get_orders():
    conn = get_connection()

    orders = conn.execute(
        """
        SELECT id, customer, product, quantity, status
        FROM orders
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return orders


def update_order_status(order_id, status):
    conn = get_connection()

    conn.execute(
        """
        UPDATE orders
        SET status = ?
        WHERE id = ?
        """,
        (status, order_id)
    )

    conn.commit()
    conn.close()


# -----------------------------
# Initialize
# -----------------------------

initialize_database()


# -----------------------------
# Application Header
# -----------------------------

st.title("📦 OrderLens")
st.caption("Cloud-based Order Management Application")

st.divider()


# -----------------------------
# Create Order
# -----------------------------

st.subheader("Create Order")

col1, col2, col3 = st.columns(3)

with col1:
    customer = st.text_input("Customer", placeholder="ABC Foods")

with col2:
    product = st.text_input("Product", placeholder="Rice")

with col3:
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1,
        step=1
    )

if st.button("Add Order", type="primary"):

    if not customer.strip() or not product.strip():
        st.warning("Please enter both customer and product.")

    else:
        add_order(
            customer.strip(),
            product.strip(),
            quantity
        )

        st.success("Order added successfully.")
        st.rerun()


st.divider()


# -----------------------------
# Orders
# -----------------------------

st.subheader("Orders")

orders = get_orders()

if not orders:

    st.info("No orders have been created yet.")

else:

    for order in orders:

        with st.container(border=True):

            col1, col2, col3, col4, col5, col6 = st.columns(
                [0.5, 1.5, 1.5, 0.7, 1.3, 1.5]
            )

            with col1:
                st.write(f"**#{order['id']}**")

            with col2:
                st.write(order["customer"])

            with col3:
                st.write(order["product"])

            with col4:
                st.write(f"x{order['quantity']}")

            with col5:
                st.write(f"**{order['status']}**")

            with col6:

                new_status = st.selectbox(
                    "Update status",
                    ["Pending", "Processing", "Completed"],
                    index=[
                        "Pending",
                        "Processing",
                        "Completed"
                    ].index(order["status"]),
                    key=f"status_{order['id']}",
                    label_visibility="collapsed",
                    format_func=lambda x: f"Update → {x}"
                )

                if new_status != order["status"]:

                    update_order_status(
                        order["id"],
                        new_status
                    )

                    st.rerun()


st.divider()


# -----------------------------
# Application Information
# -----------------------------

st.subheader("Application Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Database", "SQLite / SQL")

with col2:
    st.metric("Application", "Streamlit")



st.caption(
    "OrderLens demonstrates application development, SQL database "
    "integration, deployment and production troubleshooting concepts."
)