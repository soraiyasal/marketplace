import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import gspread
from google.oauth2 import service_account
import re

# Set page configuration
st.set_page_config(
    page_title="4C Group - Free Items Marketplace",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Define category emojis
category_emojis = {
    "Furniture": "🪑",
    "Electrical": "🔌",
    "Crockery": "🍽️",
    "Decor": "🎨",
    "Fixtures": "💡",
    "Others": "📦"
}

# Get emoji for a category (with fallback)
def get_category_emoji(category):
    return category_emojis.get(category, "📦")  # Default to package emoji if not found

# Custom CSS for better mobile experience
st.markdown("""
<style>
    .main-header {
        font-size: 1.8rem;
        color: white;
        background-color: #14289c;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        text-align: center;
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
    .view-image-button {
        background-color: #2196F3;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 0.4rem 0.8rem;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    .view-image-button:hover {
        background-color: #0b7dda;
    }
    .placeholder-image {
        height: 120px;
        background-color: #f0f0f0;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 5px;
        margin-bottom: 10px;
        text-align: center;
        color: #666;
    }
    .emoji-category {
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
    .stButton > button {
        width: 100%;
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Function to connect to Google Sheets
@st.cache_resource
def connect_to_sheets():
    try:
        # Create a connection object using the credentials
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets"            ],
        )
        
        # Create a gspread client
        client = gspread.authorize(credentials)
        
        # Return the connected client
        return client
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

# Function to load data from Google Sheets
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def load_data():
    try:
        # Connect to Google Sheets
        client = connect_to_sheets()
        
        if not client:
            return create_dummy_data()
            
        # Open the spreadsheet by key from secrets
        sheet_key = st.secrets["sheet_key"]
        sheet = client.open_by_key(sheet_key)
        
        # Get the first worksheet (assuming Form Responses is the first sheet)
        worksheet = sheet.get_worksheet(0)  # Index 0 is the first sheet
        
        # Get all records
        records = worksheet.get_all_records()
        
        # Convert to DataFrame
        df = pd.DataFrame(records)
        
        # Rename columns to match our app's expected format
        column_mapping = {
            'Timestamp': 'timestamp',
            'Category': 'category',
            'Name of the Item': 'name',
            'Location of the Hotel': 'location',
            'Quantity (Enter number)': 'quantity',
            'Contact Email Address': 'contact_email',
            'Contact Number': 'contact_phone',
            'Upload a photo of the item': 'image_url',
            'Ready to pick up by': 'pickup_date'
        }
        
        # Rename columns based on the mapping
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        # Create a unique ID for each item if not present
        if 'id' not in df.columns:
            df['id'] = range(1, len(df) + 1)
            
        # Set hotel name from location if hotel column doesn't exist
        if 'hotel' not in df.columns and 'location' in df.columns:
            df['hotel'] = df['location'].apply(lambda x: x.split(',')[0].strip() if isinstance(x, str) and ',' in x else x)
            
        # Set a default condition if not present
        if 'condition' not in df.columns:
            df['condition'] = 'Good'
            
        # Set a default subcategory if not present
        if 'subcategory' not in df.columns and 'category' in df.columns:
            df['subcategory'] = df['category']
            
        # Filter out items with quantity 0 or missing
        if 'quantity' in df.columns:
            df = df[df['quantity'].astype(str).str.strip() != '']
            df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
            df = df[df['quantity'] > 0]
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Fall back to dummy data in case of error
        return create_dummy_data()

# Fallback function to create dummy data
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
            "description": "Comfortable office chairs from our business center.",
            "image_url": "",
            "contact_email": "facilities@grandhotel.com",
            "contact_phone": "407-555-0123",
            "pickup_date": "2025-03-30"
        },
        {
            "id": 2,
            "name": "Bedside Lamps",
            "category": "Fixtures",
            "subcategory": "Lighting",
            "hotel": "Disney Land",
            "location": "Disney Land",
            "quantity": 12,
            "condition": "Like New",
            "description": "Modern bedside lamps with LED bulbs included.",
            "image_url": "",
            "contact_email": "inventory@seasideresort.com",
            "contact_phone": "305-555-9876",
            "pickup_date": "2025-04-15"
        },
        {
            "id": 3,
            "name": "Coffee Tables",
            "category": "Furniture",
            "subcategory": "Tables",
            "hotel": "Disney Land",
            "location": "Disney Land",
            "quantity": 3,
            "condition": "Good",
            "description": "Solid wood coffee tables with rustic finish.",
            "image_url": "",
            "contact_email": "property@mountainlodge.com",
            "contact_phone": "303-555-4567",
            "pickup_date": "2025-03-25"
        }
    ]
    return pd.DataFrame(items)

# Function to create email link
def create_email_link(email, subject, body=""):
    params = {
        'subject': subject,
        'body': body
    }
    return f"mailto:{email}?{urllib.parse.urlencode(params)}"

# Function to refresh data
def refresh_data():
    st.cache_data.clear()
    st.session_state.items_data = load_data()
    st.success("Data refreshed successfully!")

# Session state initialization
if 'items_data' not in st.session_state:
    st.session_state.items_data = load_data()
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

# Get unique categories from data
def get_categories():
    categories = ['All']
    if 'items_data' in st.session_state and 'category' in st.session_state.items_data.columns:
        unique_categories = st.session_state.items_data['category'].dropna().unique().tolist()
        categories.extend(sorted(unique_categories))
    return categories

# Home page with item listings
def show_home_page():
    # Header
    st.markdown('<div class="main-header">4C Group - Free Items Marketplace</div>', unsafe_allow_html=True)
    
    # Refresh data button
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("↻ Refresh Data", use_container_width=True):
            refresh_data()
            
    with col2:
        st.write("Data automatically refreshes every 60 seconds")
    
    # Search bar
    search_query = st.text_input("Search for items...", "")
    
    # Category buttons - dynamically generated from data
    st.markdown("**Filter by Category:**")
    categories = get_categories()
    
    # Use flexible wrapping for category buttons
    # Calculate how many columns to use based on number of categories
    num_cols = min(3, len(categories))  # Max 3 columns
    cols = st.columns(num_cols)
    
    for i, category in enumerate(categories):
        with cols[i % num_cols]:
            button_type = "primary" if category == st.session_state.selected_category else "secondary"
            # Add emoji to category button if it's not "All"
            button_label = category
            if category != 'All':
                emoji = get_category_emoji(category)
                button_label = f"{emoji} {category}"
                
            if st.button(button_label, key=f"cat_{category}", type=button_type, use_container_width=True):
                set_category(category)
    
    # Filter data based on selected category and search
    filtered_data = st.session_state.items_data
    if st.session_state.selected_category != 'All':
        filtered_data = filtered_data[filtered_data['category'] == st.session_state.selected_category]
    
    if search_query:
        # Safe string contains check with na=False to handle missing values
        filtered_data = filtered_data[
            filtered_data['name'].str.contains(search_query, case=False, na=False) | 
            filtered_data['location'].str.contains(search_query, case=False, na=False)
        ]
    
    # Display items in a grid
    st.markdown(f"### Available Items ({len(filtered_data)})")
    
    if len(filtered_data) == 0:
        st.info("No items match your criteria. Try a different category or search term.")
    else:
        # Display items in a 1 or 2-column layout depending on screen size
        use_one_column = st.checkbox("Single column view", value=False, key="single_col")
        cols_per_row = 1 if use_one_column else 2
        
        # Calculate rows needed
        num_items = len(filtered_data)
        rows_needed = (num_items + cols_per_row - 1) // cols_per_row
        
        # Create the grid
        for row in range(rows_needed):
            cols = st.columns(cols_per_row)
            for col in range(cols_per_row):
                item_idx = row * cols_per_row + col
                if item_idx < num_items:
                    item = filtered_data.iloc[item_idx]
                    with cols[col]:
                        with st.container():
                            # Show category emoji with name
                            emoji = get_category_emoji(item['category'])
                            st.markdown(f"### {emoji} {item['name']}")
                            
                            # Instead of displaying image, show placeholder and a button to view image
                            if 'image_url' in item and item['image_url'] and str(item['image_url']).strip() != '':
                                st.markdown(f'<div class="placeholder-image">📷 Photo Available</div>', unsafe_allow_html=True)
                                st.markdown(f'<a href="{item["image_url"]}" target="_blank" class="view-image-button">View Photo</a>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="placeholder-image">No Photo Available</div>', unsafe_allow_html=True)
                            
                            # Item details
                            st.markdown(f"**Location:** {item['location']}")
                            st.markdown(f"**Available:** {int(item['quantity'])}")
                            
                            # Show pickup date if available
                            if 'pickup_date' in item and item['pickup_date'] and str(item['pickup_date']).strip() != '':
                                st.markdown(f"**Ready by:** {item['pickup_date']}")
                            
                            # View button
                            if st.button(f"View Details", key=f"view_{item['id']}", use_container_width=True):
                                navigate_to_item_details(item['id'])
                            
                            st.markdown("---")

# Item details page
def show_item_details():
    try:
        # Get the selected item
        item = st.session_state.items_data[st.session_state.items_data['id'] == st.session_state.selected_item_id].iloc[0]
        
        # Header
        st.markdown('<div class="main-header">Free Hotel Items Marketplace</div>', unsafe_allow_html=True)
        
        # Back button
        if st.button("← Back to listings", key="back_button"):
            back_to_home()
        
        # Breadcrumb
        emoji = get_category_emoji(item['category'])
        st.markdown(f"**Home > {emoji} {item['category']} > {item['name']}**")
        st.markdown("---")
        
        # Check if mobile size
        use_mobile_layout = st.checkbox("Mobile layout", value=False, key="mobile_layout", label_visibility="collapsed")
        
        if use_mobile_layout:
            # MOBILE LAYOUT - Stack vertically
            
            # Instead of displaying image, show placeholder and a button to view image
            if 'image_url' in item and item['image_url'] and str(item['image_url']).strip() != '':
                st.markdown(f'<div style="height: 200px; background-color: #f0f0f0; display: flex; align-items: center; justify-content: center; border-radius: 5px; margin-bottom: 15px; flex-direction: column;">'
                            f'<div style="font-size: 2rem; margin-bottom: 10px;">📷</div>'
                            f'<div>Photo Available</div>'
                            f'</div>', unsafe_allow_html=True)
                st.markdown(f'<a href="{item["image_url"]}" target="_blank" class="view-image-button" style="display: block; width: 150px; margin: 0 auto 20px auto; text-align: center;">View Full Photo</a>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="height: 200px; background-color: #f0f0f0; display: flex; align-items: center; justify-content: center; border-radius: 5px; margin-bottom: 15px;">No Photo Available</div>', unsafe_allow_html=True)
            
            # Item title and tags
            emoji = get_category_emoji(item['category'])
            st.markdown(f"## {emoji} {item['name']}")
            st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 15px;">
                <span class="free-tag">FREE</span>
                <span class="free-tag">{int(item['quantity'])} available</span>
                <span class="free-tag">{item['category']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Item details
            st.markdown("### Item Details")
            st.markdown(f"**Category:** {emoji} {item['category']}")
            
            # Pickup date
            if 'pickup_date' in item and item['pickup_date'] and str(item['pickup_date']).strip() != '':
                st.markdown(f"**Ready for pickup by:** {item['pickup_date']}")
            
            # Hotel information
            st.markdown("### Location & Contact")
            st.markdown(f"**Location:** {item['location']}")
            st.markdown(f"**Email:** {item['contact_email']}")
            if 'contact_phone' in item and item['contact_phone']:
                st.markdown(f"**Phone:** {item['contact_phone']}")
            
            # Timestamp
            if 'timestamp' in item and item['timestamp']:
                st.markdown(f"**Listed on:** {item['timestamp']}")
            
        else:
            # DESKTOP LAYOUT - Side by side
            col1, col2 = st.columns([4, 6])
            
            with col1:
                # Instead of displaying image, show placeholder and a button to view image
                if 'image_url' in item and item['image_url'] and str(item['image_url']).strip() != '':
                    st.markdown(f'<div style="height: 250px; background-color: #f0f0f0; display: flex; align-items: center; justify-content: center; border-radius: 5px; margin-bottom: 15px; flex-direction: column;">'
                                f'<div style="font-size: 2.5rem; margin-bottom: 10px;">📷</div>'
                                f'<div>Photo Available</div>'
                                f'</div>', unsafe_allow_html=True)
                    st.markdown(f'<a href="{item["image_url"]}" target="_blank" class="view-image-button" style="display: block; width: 150px; margin: 0 auto 20px auto; text-align: center;">View Full Photo</a>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="height: 300px; background-color: #f0f0f0; display: flex; align-items: center; justify-content: center; border-radius: 5px; margin-bottom: 15px;">No Photo Available</div>', unsafe_allow_html=True)
                
                # Timestamp
                if 'timestamp' in item and item['timestamp']:
                    st.markdown(f"**Listed on:** {item['timestamp']}")
            
            with col2:
                # Item title and tags
                emoji = get_category_emoji(item['category'])
                st.markdown(f"## {emoji} {item['name']}")
                st.markdown(f"""
                <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 15px;">
                    <span class="free-tag">FREE</span>
                    <span class="free-tag">{int(item['quantity'])} available</span>
                    <span class="free-tag">{item['category']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Item details
                st.markdown("### Item Details")
                st.markdown(f"**Category:** {emoji} {item['category']}")
                
                # Pickup date
                if 'pickup_date' in item and item['pickup_date'] and str(item['pickup_date']).strip() != '':
                    st.markdown(f"**Ready for pickup by:** {item['pickup_date']}")
                
                # Hotel information
                st.markdown("### Location & Contact")
                st.markdown(f"**Location:** {item['location']}")
                st.markdown(f"**Email:** {item['contact_email']}")
                if 'contact_phone' in item and item['contact_phone']:
                    st.markdown(f"**Phone:** {item['contact_phone']}")
        
        # Create email subject and link
        email_subject = f"Interested in: {item['name']} (Free Hotel Marketplace)"
        email_body = f"Hello,\n\nI am interested in the {item['name']} you have listed on the Free Hotel Marketplace.\n\nPlease let me know about availability and pickup arrangements.\n\nThank you!"
        email_link = create_email_link(item['contact_email'], email_subject, email_body)        
        # Contact button
        st.markdown(f'<a href="{email_link}" class="contact-button">Contact for Pickup</a>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error displaying item details: {e}")
        st.button("Go back to listings", on_click=back_to_home)

# Display the appropriate page based on state
if st.session_state.current_page == 'home':
    show_home_page()
elif st.session_state.current_page == 'item_details':
    show_item_details()

# Small footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>© 2025 Free Hotel Items Marketplace</div>", unsafe_allow_html=True)