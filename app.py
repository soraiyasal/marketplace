

# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import urllib.parse
# import gspread
# from google.oauth2 import service_account
# import re

# # Set page configuration
# st.set_page_config(
#     page_title="4C Group - Marketplace",
#     page_icon="♻️",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # Define category emojis
# category_emojis = {
#     "Furniture": "🪑",
#     "Electrical": "🔌",
#     "Crockery": "🍽️",
#     "Decor": "🎨",
#     "Fixtures": "💡",
#     "Bag - Suitcase": "🎒",
#     "Water Bottle": "💧",
#     "Clothing":"👗",
#     "Entertainment": "🎲",
#     "Others": "📦"
# }

# # Get emoji for a category (with fallback)
# def get_category_emoji(category):
#     return category_emojis.get(category, "📦")

# # Steve Jobs inspired CSS (with added donation button styling)
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
#     * {
#         font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
#     }
    
#     .main {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         min-height: 100vh;
#         padding: 0.5rem;
#     }
    
#     .hero-header {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 2rem 1rem;
#         border-radius: 15px;
#         text-align: center;
#         color: white;
#         margin-bottom: 1.5rem;
#         box-shadow: 0 10px 30px rgba(0,0,0,0.1);
#     }
    
#     .hero-title {
#         font-size: 2rem;
#         font-weight: 700;
#         margin-bottom: 0.5rem;
#     }
    
#     .hero-subtitle {
#         font-size: 1rem;
#         opacity: 0.9;
#         margin-bottom: 1.5rem;
#     }
    
#     .stats-container {
#         display: flex;
#         gap: 1rem;
#         margin: 1rem 0;
#         justify-content: center;
#         flex-wrap: wrap;
#     }
    
#     .stat-card {
#         background: white;
#         padding: 1rem;
#         border-radius: 10px;
#         text-align: center;
#         min-width: 80px;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.08);
#         flex: 1;
#         max-width: 120px;
#     }
    
#     .stat-number {
#         font-size: 1.5rem;
#         font-weight: 700;
#         color: #667eea;
#     }
    
#     .stat-label {
#         font-size: 0.8rem;
#         color: #666;
#         margin-top: 0.2rem;
#     }
    
#     .item-card {
#         background: white;
#         border-radius: 12px;
#         overflow: hidden;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.08);
#         margin-bottom: 1rem;
#         transition: transform 0.2s ease;
#     }
    
#     .item-card:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 8px 25px rgba(0,0,0,0.12);
#     }
    
#     .item-content {
#         padding: 1rem;
#     }
    
#     .item-title {
#         font-size: 1.1rem;
#         font-weight: 600;
#         color: #2c3e50;
#         margin-bottom: 0.5rem;
#     }
    
#     .item-category {
#         background: linear-gradient(45deg, #667eea, #764ba2);
#         color: white;
#         padding: 0.2rem 0.6rem;
#         border-radius: 12px;
#         font-size: 0.7rem;
#         font-weight: 500;
#         display: inline-block;
#         margin-bottom: 0.8rem;
#     }
    
#     .quantity-badge {
#         background: linear-gradient(45deg, #4ecdc4, #44a08d);
#         color: white;
#         padding: 0.3rem 0.6rem;
#         border-radius: 15px;
#         font-size: 0.7rem;
#         font-weight: 600;
#         display: inline-block;
#         margin-left: 0.5rem;
#     }
    
#     .item-description-box {
#         background: #f8fafc;
#         padding: 0.8rem;
#         border-radius: 8px;
#         font-size: 0.85rem;
#         color: #4a5568;
#         line-height: 1.4;
#         margin: 0.8rem 0;
#         border-left: 3px solid #667eea;
#     }
    
#     .contact-section {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 1.5rem;
#         border-radius: 12px;
#         margin: 1rem 0;
#         text-align: center;
#     }
    
#     .donation-section {
#         background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
#         color: white;
#         padding: 1.5rem;
#         border-radius: 12px;
#         margin: 1rem 0;
#         text-align: center;
#         box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
#     }
    
#     .donation-section h4 {
#         margin: 0 0 0.5rem 0;
#         font-size: 1.3rem;
#     }
    
#     .donation-section p {
#         margin: 0.5rem 0;
#         font-size: 0.95rem;
#         opacity: 0.95;
#     }
    
#     .photo-available {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 1rem;
#         border-radius: 10px;
#         text-align: center;
#         margin: 1rem 0;
#         font-size: 1.2rem;
#     }
    
#     .photo-not-available {
#         background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
#         color: #8b4513;
#         padding: 1rem;
#         border-radius: 10px;
#         text-align: center;
#         margin: 1rem 0;
#         font-size: 1.2rem;
#     }
    
#     /* Mobile responsive */
#     @media (max-width: 768px) {
#         .hero-title {
#             font-size: 1.8rem;
#         }
        
#         .hero-subtitle {
#             font-size: 0.9rem;
#         }
        
#         .stats-container {
#             gap: 0.5rem;
#         }
        
#         .stat-card {
#             min-width: 70px;
#             padding: 0.8rem;
#         }
#     }
    
#     /* Hide Streamlit elements */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     .stDeployButton {display: none;}
# </style>
# """, unsafe_allow_html=True)

# # Function to connect to Google Sheets
# @st.cache_resource
# def connect_to_sheets():
#     try:
#         credentials = service_account.Credentials.from_service_account_info(
#             st.secrets["gcp_service_account"],
#             scopes=["https://www.googleapis.com/auth/spreadsheets"],
#         )
#         client = gspread.authorize(credentials)
#         return client
#     except Exception as e:
#         st.error(f"Error connecting to Google Sheets: {e}")
#         return None

# # Function to load data from Google Sheets
# @st.cache_data(ttl=60)
# def load_data():
#     try:
#         client = connect_to_sheets()
        
#         if not client:
#             return create_dummy_data()
            
#         sheet_key = st.secrets["sheet_key"]
#         sheet = client.open_by_key(sheet_key)
#         worksheet = sheet.get_worksheet(0)
#         records = worksheet.get_all_records()
#         df = pd.DataFrame(records)
        
#         column_mapping = {
#             'Timestamp': 'timestamp',
#             'Category': 'category',
#             'Name of the Item': 'name',
#             'Location of the Hotel': 'location',
#             'Quantity (Enter number)': 'quantity',
#             'Contact Email Address': 'contact_email',
#             'Contact Number': 'contact_phone',
#             'Upload a photo of the item': 'image_url',
#             'Ready to pick up by': 'pickup_date',
#             'Description': 'description',
#             'Description (Can include cost)': 'description'
#         }
        
#         for old_name, new_name in column_mapping.items():
#             if old_name in df.columns:
#                 df = df.rename(columns={old_name: new_name})
        
#         if 'id' not in df.columns:
#             df['id'] = range(1, len(df) + 1)
            
#         if 'hotel' not in df.columns and 'location' in df.columns:
#             df['hotel'] = df['location'].apply(lambda x: x.split(',')[0].strip() if isinstance(x, str) and ',' in x else x)
            
#         if 'condition' not in df.columns:
#             df['condition'] = 'Good'
            
#         if 'subcategory' not in df.columns and 'category' in df.columns:
#             df['subcategory'] = df['category']
        
#         if 'description' not in df.columns:
#             df['description'] = 'Contact for more details'
            
#         if 'quantity' in df.columns:
#             df = df[df['quantity'].astype(str).str.strip() != '']
#             df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
#             df = df[df['quantity'] > 0]
            
#         return df
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         return create_dummy_data()

# # Fallback function to create dummy data
# def create_dummy_data():
#     items = [
#         {
#             "id": 1,
#             "name": "Hotel Desk Chair",
#             "category": "Furniture",
#             "subcategory": "Chairs",
#             "hotel": "Grand Hotel",
#             "location": "Orlando, FL",
#             "quantity": 5,
#             "condition": "Good",
#             "description": "Comfortable ergonomic office chairs from our business center. Perfect for home offices. Some minor wear on armrests but fully functional. Originally $150 each.",
#             "image_url": "",
#             "contact_email": "facilities@grandhotel.com",
#             "contact_phone": "407-555-0123",
#             "pickup_date": "2025-03-30"
#         },
#         {
#             "id": 2,
#             "name": "Bedside Lamps",
#             "category": "Fixtures",
#             "subcategory": "Lighting",
#             "hotel": "Disney Land",
#             "location": "Disney Land",
#             "quantity": 12,
#             "condition": "Like New",
#             "description": "Modern bedside lamps with LED bulbs included. Contemporary design with touch controls. Originally $80 each, now free! Perfect for bedrooms or living rooms.",
#             "image_url": "",
#             "contact_email": "inventory@seasideresort.com",
#             "contact_phone": "305-555-9876",
#             "pickup_date": "2025-04-15"
#         },
#         {
#             "id": 3,
#             "name": "Coffee Tables",
#             "category": "Furniture",
#             "subcategory": "Tables",
#             "hotel": "Disney Land",
#             "location": "Disney Land",
#             "quantity": 3,
#             "condition": "Good",
#             "description": "Solid wood coffee tables with rustic finish. Minor scratches on surface but structurally sound. Great for living rooms or offices. Retail value $200 each.",
#             "image_url": "",
#             "contact_email": "property@mountainlodge.com",
#             "contact_phone": "303-555-4567",
#             "pickup_date": "2025-03-25"
#         }
#     ]
#     return pd.DataFrame(items)

# # Function to create email link
# def create_email_link(email, subject, body=""):
#     params = {
#         'subject': subject,
#         'body': body
#     }
#     return f"mailto:{email}?{urllib.parse.urlencode(params)}"

# # Function to refresh data
# def refresh_data():
#     st.cache_data.clear()
#     st.session_state.items_data = load_data()
#     st.success("✨ Data refreshed successfully!")

# # Session state initialization
# if 'items_data' not in st.session_state:
#     st.session_state.items_data = load_data()
# if 'current_page' not in st.session_state:
#     st.session_state.current_page = 'home'
# if 'selected_item_id' not in st.session_state:
#     st.session_state.selected_item_id = None
# if 'selected_category' not in st.session_state:
#     st.session_state.selected_category = 'All'

# # Navigation functions
# def navigate_to_item_details(item_id):
#     st.session_state.current_page = 'item_details'
#     st.session_state.selected_item_id = item_id

# def back_to_home():
#     st.session_state.current_page = 'home'
#     st.session_state.selected_item_id = None

# def set_category(category):
#     st.session_state.selected_category = category

# # Get unique categories from data
# def get_categories():
#     categories = ['All']
#     if 'items_data' in st.session_state and 'category' in st.session_state.items_data.columns:
#         unique_categories = st.session_state.items_data['category'].dropna().unique().tolist()
#         categories.extend(sorted(unique_categories))
#     return categories

# # Enhanced home page
# def show_home_page():
#     st.markdown("""
#     <div class="hero-header">
#         <div class="hero-title">♻️ Marketplace</div>
#         <div class="hero-subtitle">Transform waste into opportunity. Find quality items from hotels either for free or for a small price.</div>
#     </div>
#     """, unsafe_allow_html=True)
    
#     st.link_button("🎁 Have something to give away? Click on this button to add your items", "https://forms.gle/TNvTKqgkoayQRudKA", use_container_width=True)
    
#     total_items = len(st.session_state.items_data)
#     total_quantity = st.session_state.items_data['quantity'].sum() if 'quantity' in st.session_state.items_data.columns else 0
#     categories_count = len(get_categories()) - 1
    
#     st.markdown(f"""
#     <div class="stats-container">
#         <div class="stat-card">
#             <div class="stat-number">{total_items}</div>
#             <div class="stat-label">Items</div>
#         </div>
#         <div class="stat-card">
#             <div class="stat-number">{int(total_quantity)}</div>
#             <div class="stat-label">Total Qty</div>
#         </div>
#         <div class="stat-card">
#             <div class="stat-number">{categories_count}</div>
#             <div class="stat-label">Categories</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
    
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         search_query = st.text_input("🔍 Search items...", "", placeholder="Search by name, location, or description")
#     with col2:
#         st.write("")
#         if st.button("🔄 Refresh", help="Refresh data", use_container_width=True):
#             refresh_data()
    
#     st.markdown("**📂 Categories**")
#     categories = get_categories()
    
#     cols = st.columns(3)
#     for i, category in enumerate(categories):
#         with cols[i % 3]:
#             button_type = "primary" if category == st.session_state.selected_category else "secondary"
#             emoji = "🌟" if category == "All" else get_category_emoji(category)
#             if st.button(f"{emoji} {category}", key=f"cat_{category}", type=button_type, use_container_width=True):
#                 set_category(category)
    
#     filtered_data = st.session_state.items_data
#     if st.session_state.selected_category != 'All':
#         filtered_data = filtered_data[filtered_data['category'] == st.session_state.selected_category]
    
#     if search_query:
#         mask = (
#             filtered_data['name'].str.contains(search_query, case=False, na=False) | 
#             filtered_data['location'].str.contains(search_query, case=False, na=False) |
#             filtered_data['description'].str.contains(search_query, case=False, na=False)
#         )
#         filtered_data = filtered_data[mask]
    
#     st.subheader(f"🛍️ Available Items ({len(filtered_data)})")
    
#     if len(filtered_data) == 0:
#         st.info("🔍 No items found. Try a different category or search term.")
#     else:
#         for idx, item in filtered_data.iterrows():
#             emoji = get_category_emoji(item['category'])
            
#             with st.container():
#                 col1, col2 = st.columns([3, 1])
#                 with col1:
#                     st.markdown(f"**{emoji} {item['name']}**")
#                     st.caption(f"{item['category']} • {int(item['quantity'])} Available")
                
#                 with col2:
#                     if item.get('image_url') and str(item['image_url']).strip():
#                         st.link_button("📸", item['image_url'], use_container_width=True)
                
#                 st.write(f"📍 **Location:** {item['location']}")
#                 if item.get('pickup_date') and str(item['pickup_date']).strip():
#                     st.write(f"📅 **Ready by:** {item['pickup_date']}")
                
#                 description = str(item.get('description', 'Contact for more details'))
#                 if len(description) > 120:
#                     st.write(f"💬 {description[:120]}...")
#                 else:
#                     st.write(f"💬 {description}")
                
#                 if st.button(f"View Details", key=f"view_{item['id']}", use_container_width=True, type="primary"):
#                     navigate_to_item_details(item['id'])
                
#                 st.markdown("---")

# # Enhanced item details page with donation button
# def show_item_details():
#     try:
#         item = st.session_state.items_data[st.session_state.items_data['id'] == st.session_state.selected_item_id].iloc[0]
        
#         if st.button("← Back to Marketplace", key="back_button", type="primary"):
#             back_to_home()
        
#         emoji = get_category_emoji(item['category'])
#         st.markdown(f"""
#         <div class="hero-header">
#             <div class="hero-title">{emoji} {item['name']}</div>
#             <div class="hero-subtitle">{item['location']} • {int(item['quantity'])} Available</div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         if item.get('image_url') and str(item['image_url']).strip():
#             st.markdown('<div class="photo-available">📸 Photo Available</div>', unsafe_allow_html=True)
#             st.link_button("View Full Photo", item['image_url'], use_container_width=True)
#         else:
#             st.markdown('<div class="photo-not-available">📷 No Photo Available</div>', unsafe_allow_html=True)
        
#         st.subheader("📋 Item Details")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.write(f"🏷️ **Category:** {item['category']}")
#             st.write(f"📦 **Quantity:** {int(item['quantity'])}")
#             st.write(f"✅ **Condition:** {item.get('condition', 'Good')}")
        
#         with col2:
#             st.write(f"📍 **Location:** {item['location']}")
#             st.write(f"🏨 **Hotel:** {item.get('hotel', item['location'])}")
#             if item.get('pickup_date') and str(item['pickup_date']).strip():
#                 st.write(f"📅 **Ready by:** {item['pickup_date']}")
        
#         st.subheader("📝 Description")
#         st.markdown(f'<div class="item-description-box">{item.get("description", "Contact for more details")}</div>', unsafe_allow_html=True)
        
#         # DONATION SECTION - Added here
#         st.markdown("""
#         <div class="donation-section">
#             <h4>💝 Support Our Cause</h4>
#             <p>Before claiming this item, please consider making a donation to help us continue reducing waste and supporting the community.</p>
#             <p><strong>Every contribution makes a difference!</strong></p>
#         </div>
#         """, unsafe_allow_html=True)
        
#         st.link_button("❤️ Donate to Great Ormond Street Hospital Children's Charity", 
#                       "https://www.justgiving.com/page/4c-group-3?utm_medium=FR&utm_source=CL", 
#                       use_container_width=True,
#                       type="primary")
        
#         st.markdown("---")
        
#         # Contact section
#         email_subject = f"Interested in: {item['name']} (Free Hotel Marketplace)"
#         email_body = f"Hello,\n\nI am interested in the {item['name']} you have listed on the Free Hotel Marketplace.\n\nPlease let me know about availability and pickup arrangements.\n\nThank you!"
#         email_link = create_email_link(item['contact_email'], email_subject, email_body)
        
#         st.markdown(f"""
#         <div class="contact-section">
#             <h4>📞 Ready to pick this up?</h4>
#             <p><strong>📧 Email:</strong> {item['contact_email']}</p>
#             {f'<p><strong>📱 Phone:</strong> {item["contact_phone"]}</p>' if item.get('contact_phone') else ''}
#         </div>
#         """, unsafe_allow_html=True)
        
#         st.link_button("✉️ Contact for Pickup", email_link, use_container_width=True)
        
#         # Related items
#         st.subheader("🔍 More from this category")
#         related_items = st.session_state.items_data[
#             (st.session_state.items_data['category'] == item['category']) & 
#             (st.session_state.items_data['id'] != item['id'])
#         ].head(2)
        
#         if not related_items.empty:
#             for _, related_item in related_items.iterrows():
#                 related_emoji = get_category_emoji(related_item['category'])
#                 col1, col2 = st.columns([3, 1])
#                 with col1:
#                     st.write(f"{related_emoji} **{related_item['name']}**")
#                     st.caption(f"📍 {related_item['location']} • {int(related_item['quantity'])} available")
#                 with col2:
#                     if st.button("View", key=f"related_{related_item['id']}", use_container_width=True):
#                         navigate_to_item_details(related_item['id'])
#         else:
#             st.info("No other items in this category.")
            
#         if item.get('timestamp'):
#             st.caption(f"🕒 Listed on: {item['timestamp']}")
    
#     except Exception as e:
#         st.error(f"Error displaying item details: {e}")
#         st.button("🏠 Go back to marketplace", on_click=back_to_home)

# # Display the appropriate page
# if st.session_state.current_page == 'home':
#     show_home_page()
# elif st.session_state.current_page == 'item_details':
#     show_item_details()

# # Beautiful footer
# st.markdown("---")
# st.markdown("**♻️ 4C Group - Marketplace**")
# st.caption("© 2025 • Transforming waste into opportunity")

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
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
    "Water Bottle": "💧",
    "Accessory": "👓",
    "Others": "📦"
}

# Get emoji for a category (with fallback)
def get_category_emoji(category):
    return category_emojis.get(category, "📦")

# Custom CSS for better mobile experience
st.markdown("""
<style>
    /* Hero header styling */
    .hero-header {
        background: linear-gradient(135deg, #14289c 0%, #1e3db8 100%);
        padding: 2rem 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .hero-title {
        font-size: 2rem;
        font-weight: bold;
        color: white;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: rgba(255,255,255,0.9);
    }
    
    /* Stats container */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: bold;
        color: #14289c;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.25rem;
    }
    
    /* Item cards */
    .item-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        background-color: white;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Badges */
    .reserved-badge {
        background-color: #ff9800;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.8rem;
        display: inline-block;
        margin-left: 0.5rem;
    }
    
    .fully-reserved-badge {
        background-color: #f44336;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.8rem;
        display: inline-block;
        margin-left: 0.5rem;
    }
    
    .quantity-badge {
        background-color: #4CAF50;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    /* Photo availability badges */
    .photo-available {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
    }
    .photo-not-available {
        background-color: #f44336;
        color: white;
        padding: 0.5rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
    }
    
    /* Item description box */
    .item-description-box {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #14289c;
    }
    
    /* Contact section */
    .contact-section {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Donation section */
    .donation-section {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        border-left: 4px solid #ff9800;
    }
    .donation-section h4 {
        margin-top: 0;
        color: #e65100;
    }
    
    /* Reservation info box */
    .reservation-info {
        background-color: #fff9c4;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #fbc02d;
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
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

# Function to load data from Google Sheets
@st.cache_data(ttl=60)
def load_data():
    try:
        client = connect_to_sheets()
        
        if not client:
            return pd.DataFrame()
            
        sheet_key = st.secrets["sheet_key"]
        sheet = client.open_by_key(sheet_key)
        worksheet = sheet.get_worksheet(0)
        records = worksheet.get_all_records()
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
            'Ready to pick up by': 'pickup_date',
            'Description (Can include cost)': 'description',
            'Reserved By Name': 'reserved_by_name',
            'Reserved By Email': 'reserved_by_email',
            'Reserved Quantity': 'reserved_quantity',
            'Reservation Pickup Date': 'reservation_pickup_date'
        }
        
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        # Create unique ID for each item
        if 'id' not in df.columns:
            df['id'] = range(1, len(df) + 1)
            
        # Set hotel name from location
        if 'hotel' not in df.columns and 'location' in df.columns:
            df['hotel'] = df['location'].apply(lambda x: x.split(',')[0].strip() if isinstance(x, str) and ',' in x else x)
            
        # Set default condition
        if 'condition' not in df.columns:
            df['condition'] = 'Good'
            
        # Set default subcategory
        if 'subcategory' not in df.columns and 'category' in df.columns:
            df['subcategory'] = df['category']
        
        # Calculate remaining quantity
        if 'reserved_quantity' not in df.columns:
            df['reserved_quantity'] = 0
        else:
            df['reserved_quantity'] = pd.to_numeric(df['reserved_quantity'], errors='coerce').fillna(0)
        
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
        df['remaining_quantity'] = df['quantity'] - df['reserved_quantity']
        
        # Ensure remaining quantity doesn't go negative
        df['remaining_quantity'] = df['remaining_quantity'].apply(lambda x: max(0, x))
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Function to save reservation to Google Sheets
def save_reservation(item_id, name, email, quantity, pickup_date):
    try:
        client = connect_to_sheets()
        if not client:
            return False, "Could not connect to Google Sheets"
            
        sheet_key = st.secrets["sheet_key"]
        sheet = client.open_by_key(sheet_key)
        worksheet = sheet.get_worksheet(0)
        
        # Get all data to find the row
        all_data = worksheet.get_all_values()
        headers = all_data[0]
        
        # Find the row index for this item (searching by item ID in the data)
        item_row = None
        for idx, row in enumerate(all_data[1:], start=2):  # Start from row 2 (after header)
            # Match based on the item data
            item_df = st.session_state.items_data[st.session_state.items_data['id'] == item_id]
            if not item_df.empty:
                item = item_df.iloc[0]
                # Match by name and location to find correct row
                if len(row) > 2 and row[2] == item['name'] and row[3] == item['location']:
                    item_row = idx
                    break
        
        if not item_row:
            return False, "Could not find item in spreadsheet"
        
        # Find column indices for reservation fields
        reserved_name_col = None
        reserved_email_col = None
        reserved_qty_col = None
        reserved_pickup_col = None
        
        for idx, header in enumerate(headers, start=1):
            if header == 'Reserved By Name':
                reserved_name_col = idx
            elif header == 'Reserved By Email':
                reserved_email_col = idx
            elif header == 'Reserved Quantity':
                reserved_qty_col = idx
            elif header == 'Reservation Pickup Date':
                reserved_pickup_col = idx
        
        # If columns don't exist, create them
        if not all([reserved_name_col, reserved_email_col, reserved_qty_col, reserved_pickup_col]):
            # Add headers if they don't exist
            current_headers = worksheet.row_values(1)
            new_headers = []
            
            if 'Reserved By Name' not in current_headers:
                new_headers.append('Reserved By Name')
            if 'Reserved By Email' not in current_headers:
                new_headers.append('Reserved By Email')
            if 'Reserved Quantity' not in current_headers:
                new_headers.append('Reserved Quantity')
            if 'Reservation Pickup Date' not in current_headers:
                new_headers.append('Reservation Pickup Date')
            
            if new_headers:
                start_col = len(current_headers) + 1
                worksheet.update(f'{chr(64 + start_col)}1', [new_headers])
                
                # Update column indices
                reserved_name_col = start_col
                reserved_email_col = start_col + 1 if len(new_headers) > 1 else start_col
                reserved_qty_col = start_col + 2 if len(new_headers) > 2 else start_col
                reserved_pickup_col = start_col + 3 if len(new_headers) > 3 else start_col
        
        # Get current reserved quantity
        current_reserved = worksheet.cell(item_row, reserved_qty_col).value
        current_reserved = int(current_reserved) if current_reserved and str(current_reserved).isdigit() else 0
        new_reserved = current_reserved + quantity
        
        # Update the cells
        worksheet.update_cell(item_row, reserved_name_col, name)
        worksheet.update_cell(item_row, reserved_email_col, email)
        worksheet.update_cell(item_row, reserved_qty_col, new_reserved)
        worksheet.update_cell(item_row, reserved_pickup_col, pickup_date)
        
        return True, "Reservation saved successfully!"
        
    except Exception as e:
        return False, f"Error saving reservation: {str(e)}"

# Function to create email link
def create_email_link(email, subject, body):
    return f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"

# Initialize session state
if 'items_data' not in st.session_state:
    st.session_state.items_data = load_data()

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

if 'selected_category' not in st.session_state:
    st.session_state.selected_category = 'All'

if 'selected_item_id' not in st.session_state:
    st.session_state.selected_item_id = None

if 'show_reservation_form' not in st.session_state:
    st.session_state.show_reservation_form = False

if 'reservation_item_id' not in st.session_state:
    st.session_state.reservation_item_id = None

# Navigation functions
def navigate_to_item_details(item_id):
    st.session_state.selected_item_id = item_id
    st.session_state.current_page = 'item_details'
    st.rerun()

def back_to_home():
    st.session_state.current_page = 'home'
    st.session_state.selected_item_id = None
    st.rerun()

def set_category(category):
    st.session_state.selected_category = category
    st.rerun()

def refresh_data():
    st.cache_data.clear()
    st.session_state.items_data = load_data()
    st.rerun()

def get_categories():
    categories = ['All']
    if 'items_data' in st.session_state and 'category' in st.session_state.items_data.columns:
        unique_categories = st.session_state.items_data['category'].dropna().unique().tolist()
        categories.extend(sorted(unique_categories))
    return categories

# Reservation Dialog using st.dialog
@st.dialog("🎯 Reserve This Item")
def show_reservation_dialog(item_id):
    item = st.session_state.items_data[st.session_state.items_data['id'] == item_id].iloc[0]
    
    st.markdown(f"### {item['name']}")
    st.write(f"📍 **Location:** {item['location']}")
    st.write(f"📦 **Available:** {int(item['remaining_quantity'])} items")
    
    st.markdown("---")
    st.subheader("📝 Your Details")
    
    with st.form("reservation_form"):
        name = st.text_input("Your Name *", placeholder="Enter your full name")
        email = st.text_input("Your Email *", placeholder="your.email@example.com")
        
        max_quantity = int(item['remaining_quantity'])
        quantity = st.number_input(
            "Quantity to Reserve *", 
            min_value=1, 
            max_value=max_quantity, 
            value=1,
            help=f"Maximum available: {max_quantity}"
        )
        
        # Default pickup date: 7 days from now
        default_pickup = datetime.now() + timedelta(days=7)
        pickup_date = st.date_input(
            "When will you pick it up? *",
            value=default_pickup,
            min_value=datetime.now().date(),
            help="Select the date you plan to collect this item"
        )
        
        st.markdown("---")
        st.caption("* Required fields")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("✅ Confirm Reservation", use_container_width=True, type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit:
            if not name or not email:
                st.error("⚠️ Please fill in all required fields!")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("⚠️ Please enter a valid email address!")
            else:
                # Save reservation
                success, message = save_reservation(
                    item_id, 
                    name, 
                    email, 
                    quantity, 
                    pickup_date.strftime("%d/%m/%Y")
                )
                
                if success:
                    st.success("🎉 " + message)
                    st.balloons()
                    st.info(f"📧 A confirmation will be sent to {email}")
                    
                    # Refresh data
                    st.cache_data.clear()
                    st.session_state.items_data = load_data()
                    
                    # Wait a moment then close
                    import time
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        if cancel:
            st.rerun()

# Enhanced home page with reservation functionality
def show_home_page():
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">♻️ Marketplace</div>
        <div class="hero-subtitle">Transform waste into opportunity. Find quality items from hotels either for free or for a small price.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.link_button("🎁 Have something to give away? Click here to add your items", 
                   "https://forms.gle/TNvTKqgkoayQRudKA", 
                   use_container_width=True)
    
    # Calculate stats
    total_items = len(st.session_state.items_data)
    total_available = int(st.session_state.items_data['remaining_quantity'].sum()) if 'remaining_quantity' in st.session_state.items_data.columns else 0
    categories_count = len(get_categories()) - 1
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-number">{total_items}</div>
            <div class="stat-label">Items</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{total_available}</div>
            <div class="stat-label">Available</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{categories_count}</div>
            <div class="stat-label">Categories</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Search and refresh
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input("🔍 Search items...", "", placeholder="Search by name, location, or description")
    with col2:
        st.write("")
        if st.button("🔄", help="Refresh data", use_container_width=True):
            refresh_data()
    
    # Category filters
    st.markdown("**📂 Categories**")
    categories = get_categories()
    
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            button_type = "primary" if category == st.session_state.selected_category else "secondary"
            emoji = "🌟" if category == "All" else get_category_emoji(category)
            if st.button(f"{emoji} {category}", key=f"cat_{category}", type=button_type, use_container_width=True):
                set_category(category)
    
    # Filter data
    filtered_data = st.session_state.items_data.copy()
    
    # Filter by category
    if st.session_state.selected_category != 'All':
        filtered_data = filtered_data[filtered_data['category'] == st.session_state.selected_category]
    
    # Filter by search
    if search_query:
        mask = (
            filtered_data['name'].str.contains(search_query, case=False, na=False) | 
            filtered_data['location'].str.contains(search_query, case=False, na=False) |
            filtered_data['description'].str.contains(search_query, case=False, na=False)
        )
        filtered_data = filtered_data[mask]
    
    st.subheader(f"🛍️ Available Items ({len(filtered_data)})")
    
    if len(filtered_data) == 0:
        st.info("🔍 No items found. Try a different category or search term.")
    else:
        for idx, item in filtered_data.iterrows():
            emoji = get_category_emoji(item['category'])
            remaining = int(item['remaining_quantity'])
            total_qty = int(item['quantity'])
            is_reserved = remaining < total_qty
            is_fully_reserved = remaining == 0
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    title_html = f"**{emoji} {item['name']}**"
                    if is_fully_reserved:
                        title_html += ' <span class="fully-reserved-badge">RESERVED</span>'
                    elif is_reserved:
                        title_html += ' <span class="reserved-badge">Partially Reserved</span>'
                    st.markdown(title_html, unsafe_allow_html=True)
                    
                    if is_fully_reserved:
                        st.caption(f"{item['category']} • All Reserved")
                    else:
                        st.caption(f"{item['category']} • {remaining} of {total_qty} Available")
                
                with col2:
                    if item.get('image_url') and str(item['image_url']).strip():
                        st.link_button("📸", item['image_url'], use_container_width=True)
                
                st.write(f"📍 **Location:** {item['location']}")
                if item.get('pickup_date') and str(item['pickup_date']).strip():
                    st.write(f"📅 **Ready by:** {item['pickup_date']}")
                
                description = str(item.get('description', 'Contact for more details'))
                if len(description) > 120:
                    st.write(f"💬 {description[:120]}...")
                else:
                    st.write(f"💬 {description}")
                
                # Action buttons
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"View Details", key=f"view_{item['id']}", use_container_width=True):
                        navigate_to_item_details(item['id'])
                with col_btn2:
                    if not is_fully_reserved:
                        if st.button(f"🎯 Reserve", key=f"reserve_home_{item['id']}", use_container_width=True, type="primary"):
                            show_reservation_dialog(item['id'])
                    else:
                        st.button(f"Reserved", key=f"reserved_home_{item['id']}", use_container_width=True, disabled=True)
                
                st.markdown("---")

# Enhanced item details page with reservation
def show_item_details():
    try:
        item = st.session_state.items_data[st.session_state.items_data['id'] == st.session_state.selected_item_id].iloc[0]
        
        if st.button("← Back to Marketplace", key="back_button", type="primary"):
            back_to_home()
        
        emoji = get_category_emoji(item['category'])
        remaining = int(item['remaining_quantity'])
        total_qty = int(item['quantity'])
        is_reserved = remaining < total_qty
        is_fully_reserved = remaining == 0
        
        title_html = f"{emoji} {item['name']}"
        if is_fully_reserved:
            availability = "All Reserved"
        elif is_reserved:
            availability = f"{remaining} of {total_qty} Available"
        else:
            availability = f"{remaining} Available"
        
        st.markdown(f"""
        <div class="hero-header">
            <div class="hero-title">{title_html}</div>
            <div class="hero-subtitle">{item['location']} • {availability}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show reservation status if partially or fully reserved
        if is_reserved:
            reserved_qty = total_qty - remaining
            if is_fully_reserved:
                st.markdown("""
                <div class="reservation-info">
                    <strong>⚠️ This item is fully reserved</strong>
                    <p>All available items have been reserved. Check back later for new items!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="reservation-info">
                    <strong>📊 Reservation Status</strong>
                    <p>{reserved_qty} out of {total_qty} items have been reserved. {remaining} still available!</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Image section
        if item.get('image_url') and str(item['image_url']).strip():
            st.markdown('<div class="photo-available">📸 Photo Available</div>', unsafe_allow_html=True)
            st.link_button("View Full Photo", item['image_url'], use_container_width=True)
        else:
            st.markdown('<div class="photo-not-available">📷 No Photo Available</div>', unsafe_allow_html=True)
        
        # Item details
        st.subheader("📋 Item Details")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"🏷️ **Category:** {item['category']}")
            st.write(f"📦 **Total Quantity:** {total_qty}")
            st.write(f"✅ **Available:** {remaining}")
        
        with col2:
            st.write(f"📍 **Location:** {item['location']}")
            st.write(f"🏨 **Hotel:** {item.get('hotel', item['location'])}")
            if item.get('pickup_date') and str(item['pickup_date']).strip():
                st.write(f"📅 **Ready by:** {item['pickup_date']}")
        
        # Description
        st.subheader("📝 Description")
        st.markdown(f'<div class="item-description-box">{item.get("description", "Contact for more details")}</div>', unsafe_allow_html=True)
        
        # Reserve button - prominent placement
        if not is_fully_reserved:
            st.markdown("### 🎯 Reserve This Item")
            st.write("Click below to reserve this item for pickup")
            if st.button("Reserve Now", key="reserve_details", use_container_width=True, type="primary"):
                show_reservation_dialog(item['id'])
        
        st.markdown("---")
        
        # Donation section
        st.markdown("""
        <div class="donation-section">
            <h4>💝 Support Our Cause</h4>
            <p>Before claiming this item, please consider making a donation to help us continue reducing waste and supporting the community.</p>
            <p><strong>Every contribution makes a difference!</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.link_button("❤️ Donate to Great Ormond Street Hospital Children's Charity", 
                      "https://www.justgiving.com/page/4c-group-3?utm_medium=FR&utm_source=CL", 
                      use_container_width=True,
                      type="primary")
        
        st.markdown("---")
        
        # Contact section
        email_subject = f"Interested in: {item['name']} (Free Hotel Marketplace)"
        email_body = f"Hello,\n\nI am interested in the {item['name']} you have listed on the Free Hotel Marketplace.\n\nPlease let me know about availability and pickup arrangements.\n\nThank you!"
        email_link = create_email_link(item['contact_email'], email_subject, email_body)
        
        st.markdown(f"""
        <div class="contact-section">
            <h4>📞 Need More Information?</h4>
            <p><strong>📧 Email:</strong> {item['contact_email']}</p>
            {f'<p><strong>📱 Phone:</strong> {item["contact_phone"]}</p>' if item.get('contact_phone') else ''}
        </div>
        """, unsafe_allow_html=True)
        
        st.link_button("✉️ Contact for Questions", email_link, use_container_width=True)
        
        # Related items
        st.subheader("🔍 More from this category")
        related_items = st.session_state.items_data[
            (st.session_state.items_data['category'] == item['category']) & 
            (st.session_state.items_data['id'] != item['id']) &
            (st.session_state.items_data['remaining_quantity'] > 0)
        ].head(3)
        
        if not related_items.empty:
            for _, related_item in related_items.iterrows():
                related_emoji = get_category_emoji(related_item['category'])
                related_remaining = int(related_item['remaining_quantity'])
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{related_emoji} **{related_item['name']}**")
                    st.caption(f"📍 {related_item['location']} • {related_remaining} available")
                with col2:
                    if st.button("View", key=f"related_{related_item['id']}", use_container_width=True):
                        navigate_to_item_details(related_item['id'])
        else:
            st.info("No other available items in this category.")
            
        if item.get('timestamp'):
            st.caption(f"🕒 Listed on: {item['timestamp']}")
    
    except Exception as e:
        st.error(f"Error displaying item details: {e}")
        st.button("🏠 Go back to marketplace", on_click=back_to_home)

# Display the appropriate page
if st.session_state.current_page == 'home':
    show_home_page()
elif st.session_state.current_page == 'item_details':
    show_item_details()

# Footer
st.markdown("---")
st.markdown("**♻️ 4C Group - Marketplace**")
st.caption("© 2025 • Transforming waste into opportunity")