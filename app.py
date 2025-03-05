import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# Set page configuration - using "centered" layout which is more mobile-friendly
st.set_page_config(
    page_title="Free Hotel Items Marketplace",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS to style the app with mobile-friendly design
st.markdown("""
<style>
    .main-header {
        font-size: 1.8rem;
        color: white;
        background-color: #4CAF50;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        text-align: center;
    }
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.5rem;
            padding: 0.8rem;
        }
    }
    .item-card {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 1rem;
        background-color: white;
        margin-bottom: 1rem;
        width: 100%;
        box-sizing: border-box;
    }
    .item-title {
        font-size: 1.2rem;
        font-weight: bold;
    }
    .item-hotel {
        color: #666;
    }
    .category-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 20px;
    }
    .cat-button {
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        cursor: pointer;
        text-align: center;
        border: 1px solid #ddd;
        background-color: white;
        color: #333;
        font-weight: normal;
        transition: all 0.3s;
    }
    .cat-button.active {
        background-color: #e8f5e9;
        color: #4CAF50;
        border-color: #4CAF50;
        font-weight: bold;
    }
    .free-tag {
        background-color: #e8f5e9;
        color: #4CAF50;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
    }
    .contact-button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        width: 100%;
        text-align: center;
        text-decoration: none;
        display: block;
        font-size: 1rem;
        margin: 1rem 0;
    }
    .contact-button:hover {
        background-color: #388E3C;
    }
    .back-button {
        margin-bottom: 1rem;
    }
    .breadcrumb {
        color: #666;
        margin-bottom: 1rem;
    }
    .divider {
        height: 1px;
        background-color: #eee;
        margin: 0.5rem 0 1rem 0;
    }
    .stButton > button {
        width: 100%;
    }
    .search-container {
        margin-bottom: 20px;
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Function to create dummy data
def create_dummy_data():
    items = [
        {
            "id": 1,
            "name": "Hotel Desk Chair",
            "category": "Furniture",
            "subcategory": "Chairs",
            "hotel": "Grand Hotel",
            "location": "Orlando, FL",
            "quantity": 5,
            "condition": "Good",
            "description": "Comfortable office chairs from our business center. Adjustable height and ergonomic design. Some minor wear but all mechanisms work perfectly.",
            "image": "chair.jpg",
            "contact_email": "facilities@grandhotel.com",
            "contact_phone": "407-555-0123"
        },
        {
            "id": 2,
            "name": "Bedside Lamps",
            "category": "Decor",
            "subcategory": "Lighting",
            "hotel": "Seaside Resort",
            "location": "Miami, FL",
            "quantity": 12,
            "condition": "Like New",
            "description": "Modern bedside lamps with LED bulbs included. Brushed nickel finish. Only used for 6 months before our recent renovation.",
            "image": "lamp.jpg",
            "contact_email": "inventory@seasideresort.com",
            "contact_phone": "305-555-9876"
        },
        {
            "id": 3,
            "name": "Coffee Tables",
            "category": "Furniture",
            "subcategory": "Tables",
            "hotel": "Mountain Lodge",
            "location": "Denver, CO",
            "quantity": 3,
            "condition": "Good",
            "description": "Solid wood coffee tables with rustic finish. 36\" diameter. Some minor scratches but structurally perfect.",
            "image": "coffee_table.jpg",
            "contact_email": "property@mountainlodge.com",
            "contact_phone": "303-555-4567"
        },
        {
            "id": 4,
            "name": "TV Stands",
            "category": "Furniture",
            "subcategory": "Storage",
            "hotel": "City View Hotel",
            "location": "Seattle, WA",
            "quantity": 8,
            "condition": "Fair",
            "description": "TV stands that can hold up to 55\" TVs. Includes cable management and drawer. Some wear and tear but fully functional.",
            "image": "tv_stand.jpg",
            "contact_email": "maintenance@cityviewhotel.com",
            "contact_phone": "206-555-7890"
        },
        {
            "id": 5,
            "name": "Mini Fridges",
            "category": "Appliances",
            "subcategory": "Refrigeration",
            "hotel": "Bayside Inn",
            "location": "San Diego, CA",
            "quantity": 4,
            "condition": "Good",
            "description": "Compact mini refrigerators, 3.2 cubic feet. Clean and in working order, some may have minor cosmetic blemishes on the exterior.",
            "image": "mini_fridge.jpg",
            "contact_email": "operations@baysideinn.com",
            "contact_phone": "619-555-2345"
        },
        {
            "id": 6,
            "name": "Office Desks",
            "category": "Furniture",
            "subcategory": "Desks",
            "hotel": "Business Suites",
            "location": "Chicago, IL",
            "quantity": 6,
            "condition": "Good",
            "description": "Standard office desks from our business center. Dimensions: 48\" × 30\" × 29\". In good condition with some minor scratches. Must pickup by March 30th.",
            "image": "desk.jpg",
            "contact_email": "items@businesssuites.com",
            "contact_phone": "312-555-6789"
        },
        {
            "id": 7,
            "name": "Bathroom Mirrors",
            "category": "Fixtures",
            "subcategory": "Bathroom",
            "hotel": "Luxury Downtown",
            "location": "New York, NY",
            "quantity": 10,
            "condition": "Excellent",
            "description": "Framed bathroom mirrors, 24\" × 36\". Excellent condition, removed during recent updating of decor.",
            "image": "mirror.jpg",
            "contact_email": "renovations@luxurydowntown.com",
            "contact_phone": "212-555-0987"
        },
        {
            "id": 8,
            "name": "Flat Screen TVs (32\")",
            "category": "Electronics",
            "subcategory": "Televisions",
            "hotel": "Resort & Spa",
            "location": "Phoenix, AZ",
            "quantity": 15,
            "condition": "Good",
            "description": "32-inch LCD TVs. All in working condition, minor scratches on some. HDMI and cable inputs. Remote controls included.",
            "image": "tv.jpg",
            "contact_email": "equipment@resortspa.com",
            "contact_phone": "480-555-3456"
        }
    ]
    return pd.DataFrame(items)

# Create email link for contacting about an item
def create_email_link(email, subject, body=""):
    params = {
        'subject': subject,
        'body': body
    }
    return f"mailto:{email}?{urllib.parse.urlencode(params)}"

# Session state initialization
if 'items_data' not in st.session_state:
    st.session_state.items_data = create_dummy_data()
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'selected_item_id' not in st.session_state:
    st.session_state.selected_item_id = None
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = 'All'

# Navigation functions
def navigate_to_item_details(item_id):
    st.session_state.current_page = 'item_details'
    st.session_state.selected_item_id = item_id

def back_to_home():
    st.session_state.current_page = 'home'
    st.session_state.selected_item_id = None

def set_category(category):
    st.session_state.selected_category = category
    st.session_state.current_page = 'home'

# Home page with item listings
def show_home_page():
    # Header
    st.markdown('<div class="main-header">Free Hotel Items Marketplace</div>', unsafe_allow_html=True)
    
    # Search bar
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    search_query = st.text_input("Search for items...", "")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Category navigation - more responsive approach
    categories = ['All', 'Furniture', 'Electronics', 'Decor', 'Fixtures', 'Appliances']
    
    # Using custom HTML buttons for better responsive layout
    st.markdown('<div class="category-buttons">', unsafe_allow_html=True)
    for category in categories:
        active_class = "active" if category == st.session_state.selected_category else ""
        if st.button(category, key=f"cat_{category}"):
            set_category(category)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter data based on selected category and search
    filtered_data = st.session_state.items_data
    if st.session_state.selected_category != 'All':
        filtered_data = filtered_data[filtered_data['category'] == st.session_state.selected_category]
    
    if search_query:
        filtered_data = filtered_data[filtered_data['name'].str.contains(search_query, case=False) | 
                                     filtered_data['description'].str.contains(search_query, case=False)]
    
    # Display items in a grid
    st.markdown(f"### Available Items ({len(filtered_data)})")
    
    if len(filtered_data) == 0:
        st.info("No items match your criteria. Try a different category or search term.")
    else:
        # Determine screen size automatically and adjust column count
        # We'll detect mobile based on screen width in the browser
        # For small screens (width < 768px), use 1 column
        # For medium screens, use 2 columns
        
        # Create rows with appropriate columns for device size
        col_count = 1  # Default to 1 column for mobile
        
        # For larger screens, we'll use 2 columns
        if not st.checkbox("Mobile view", value=False, key="mobile_toggle", label_visibility="collapsed"):
            col_count = 2
            
        for i in range(0, len(filtered_data), col_count):
            cols = st.columns(col_count)
            for j in range(col_count):
                if i+j < len(filtered_data):
                    item = filtered_data.iloc[i+j]
                    with cols[j]:
                        st.markdown(f'<div class="item-card">', unsafe_allow_html=True)
                        # Item image (placeholder)
                        st.markdown(f'<div style="height: 140px; background-color: #f0f0f0; display: flex; align-items: center; justify-content: center; border-radius: 5px; margin-bottom: 10px;">Item Photo</div>', unsafe_allow_html=True)
                        # Item name
                        st.markdown(f'<div class="item-title">{item["name"]}</div>', unsafe_allow_html=True)
                        # Hotel and quantity
                        st.markdown(f'<div class="item-hotel">{item["hotel"]} • {item["quantity"]} available</div>', unsafe_allow_html=True)
                        # View button
                        if st.button(f"View Details", key=f"view_{item['id']}"):
                            navigate_to_item_details(item['id'])
                        st.markdown('</div>', unsafe_allow_html=True)

# Item details page
def show_item_details():
    # Get the selected item
    item = st.session_state.items_data[st.session_state.items_data['id'] == st.session_state.selected_item_id].iloc[0]
    
    # Header
    st.markdown('<div class="main-header">Free Hotel Items Marketplace</div>', unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to listings", key="back_button"):
        back_to_home()
    
    # Breadcrumb
    st.markdown(f'<div class="breadcrumb">Home > {item["category"]} > {item["name"]}</div>', unsafe_allow_html=True)
    
    # Item details container
    st.markdown('<div style="background-color: white; padding: 20px; border-radius: 5px;">', unsafe_allow_html=True)
    
    # Determine if we should use mobile layout
    # For mobile, we'll stack everything vertically
    # For desktop, we'll use a two-column layout
    is_mobile = st.checkbox("Mobile view", value=False, key="mobile_toggle_detail", label_visibility="collapsed")
    
    if is_mobile:
        # Mobile layout - stack vertically
        # First image
        st.markdown(f'<div style="height: 200px; background-color: #f0f0f0; display: flex; align-items: center; justify-content: center; border-radius: 5px; margin-bottom: 15px;">Item Photo</div>', unsafe_allow_html=True)
        
        # Then details
        st.markdown(f"<h2>{item['name']}</h2>", unsafe_allow_html=True)
        st.markdown(f'<span class="free-tag">FREE</span> <span class="free-tag">{item["quantity"]} available</span>', unsafe_allow_html=True)
        
        # Item details
        st.markdown("<h3>Item Details</h3>", unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(f"**Condition:** {item['condition']}", unsafe_allow_html=True)
        st.markdown(f"**Category:** {item['category']} > {item['subcategory']}", unsafe_allow_html=True)
        
        # Description
        st.markdown("<h3>Description</h3>", unsafe_allow_html=True)
        st.markdown(f'<div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 15px;">{item["description"]}</div>', unsafe_allow_html=True)
        
        # Hotel information
        st.markdown("<h3>Offered By</h3>", unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(f"**{item['hotel']}**", unsafe_allow_html=True)
        st.markdown(f"{item['location']}", unsafe_allow_html=True)
        st.markdown(f"**Email:** {item['contact_email']}", unsafe_allow_html=True)
        st.markdown(f"**Phone:** {item['contact_phone']}", unsafe_allow_html=True)
        
    else:
        # Desktop layout - side by side
        col1, col2 = st.columns([4, 6])
        
        with col1:
            # Item image (placeholder)
            st.markdown(f'<div style="height: 300px; background-color: #f0f0f0; display: flex; align-items: center; justify-content: center; border-radius: 5px;">Item Photo</div>', unsafe_allow_html=True)
            
            # Description
            st.markdown("<h3>Description</h3>", unsafe_allow_html=True)
            st.markdown(f'<div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; border: 1px solid #ddd;">{item["description"]}</div>', unsafe_allow_html=True)
        
        with col2:
            # Item title
            st.markdown(f"<h2>{item['name']}</h2>", unsafe_allow_html=True)
            
            # Free tag and quantity
            st.markdown(f'<span class="free-tag">FREE</span> <span class="free-tag">{item["quantity"]} available</span>', unsafe_allow_html=True)
            
            # Item details
            st.markdown("<h3>Item Details</h3>", unsafe_allow_html=True)
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown(f"**Condition:** {item['condition']}", unsafe_allow_html=True)
            st.markdown(f"**Category:** {item['category']} > {item['subcategory']}", unsafe_allow_html=True)
            
            # Hotel information
            st.markdown("<h3>Offered By</h3>", unsafe_allow_html=True)
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown(f"**{item['hotel']}**", unsafe_allow_html=True)
            st.markdown(f"{item['location']}", unsafe_allow_html=True)
            st.markdown(f"**Email:** {item['contact_email']}", unsafe_allow_html=True)
            st.markdown(f"**Phone:** {item['contact_phone']}", unsafe_allow_html=True)
    
    # Create email subject and link
    email_subject = f"Interested in: {item['name']} (Free Hotel Marketplace)"
    email_body = f"Hello {item['hotel']},\n\nI am interested in the {item['name']} you have listed on the Free Hotel Marketplace.\n\nPlease let me know about availability and pickup arrangements.\n\nThank you!"
    email_link = create_email_link(item['contact_email'], email_subject, email_body)
    
    # Contact button - linked to email with pre-populated subject
    st.markdown(f'<a href="{email_link}" class="contact-button">Contact for Pickup</a>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Display the appropriate page based on state
if st.session_state.current_page == 'home':
    show_home_page()
elif st.session_state.current_page == 'item_details':
    show_item_details()

# Small footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #666; padding: 10px;'>© 2025 Free Hotel Items Marketplace</div>", unsafe_allow_html=True)