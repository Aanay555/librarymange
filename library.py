# library_manager.py
import streamlit as st
import json
import os
from datetime import datetime

# ======================================
# ENHANCED CSS WITH 3D ANIMATIONS
# ======================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');


:root {
    --primary: #00ff88;  /* Changed to green */
    --secondary: blue;
    --glass: rgba(255, 255, 255, 0.1);
    --menu-text: #00ff88; /* New green text variable */
}

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: #a0ffdd;
    color: black;
    animation: appEntry 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

@keyframes appEntry {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

.sidebar .sidebar-content {
    background: var(--glass) !important;
    backdrop-filter: blur(15px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 5px 0 25px rgba(0,0,0,0.3) !important;
}

/* 3D Menu Styling */
div[data-baseweb="select"] > div:first-child {
    background: var(--glass) !important;
    border: 2px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 15px !important;
    padding: 12px 20px !important;
    color: white !important;
    transition: all 0.3s ease !important;
    transform-style: preserve-3d;
}

div[data-baseweb="select"] > div:first-child:hover {
    transform: rotateX(10deg) translateZ(20px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
}

/* 3D Card Animation */
.card {
    background: var(--glass) !important;
    border-radius: 20px !important;
    padding: 25px;
    margin: 15px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transform-style: preserve-3d;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    position: relative;
}

.card:hover {
    transform: perspective(1000px) rotateX(5deg) rotateY(5deg) translateY(-10px);
    box-shadow: 0 25px 50px rgba(0,0,0,0.3);
}

/* Glowing Button */
.stButton>button {
    background: linear-gradient(45deg, var(--primary), var(--secondary));
    border: none !important;
    border-radius: 15px !important;
    padding: 12px 30px !important;
    font-weight: 700 !important;
    transition: all 0.3s ease !important;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 30px rgba(106, 17, 255, 0.5);
}

/* Input Fields */
.stTextInput>div>div>input {
    background: var(--glass) !important;
    border: 2px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 15px !important;
    color: white !important;
    padding: 12px 20px !important;
}

/* Metrics */
.metric-box {
    background: var(--glass) !important;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 25px;
    margin: 15px;
    text-align: center;
    transition: all 0.3s ease;
}

h1 {
    text-align: center;
    background: linear-gradient(45deg, #00b4d8, #90e0ef);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: float 4s ease-in-out infinite;
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}
</style>
"""

# ======================================
# DATA HANDLING FUNCTIONS
# ======================================
def load_data():
    if os.path.exists("library.json"):
        with open("library.json", "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open("library.json", "w") as f:
        json.dump(data, f)

# ======================================
# CORE FEATURES
# ======================================
def add_book():
    st.subheader("📖 Add New Book")
    with st.form("add_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1800, max_value=datetime.now().year)
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Mystery", "Romance", "Other"])
        read = st.checkbox("Read Status")
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            new_book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read
            }
            st.session_state.library.append(new_book)
            save_data(st.session_state.library)
            st.success("Book added successfully! 🎉")

def remove_book():
    st.subheader("🗑️ Remove Book")
    titles = [book["title"] for book in st.session_state.library]
    selected = st.selectbox("Select Book to Remove", titles)
    
    if st.button("Remove"):
        st.session_state.library = [book for book in st.session_state.library if book["title"] != selected]
        save_data(st.session_state.library)
        st.success("Book removed successfully! ✅")

def search_books():
    st.subheader("🔍 Search Books")
    search_term = st.text_input("Search by Title, Author, or Genre")
    
    if search_term:
        results = []
        for book in st.session_state.library:
            if (search_term.lower() in book["title"].lower() or 
                search_term.lower() in book["author"].lower() or 
                search_term.lower() in book["genre"].lower()):
                results.append(book)
        
        if results:
            st.write(f"📚 Found {len(results)} results:")
            for book in results:
                st.markdown(f"""
                <div class="card">
                    <h3>{book['title']}</h3>
                    <p>👤 {book['author']}</p>
                    <p>📅 {book['year']} | 🎭 {book['genre']} | 📖 {'✅ Read' if book['read'] else '❌ Unread'}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No books found matching your search 😞")

def display_books():
    st.subheader("📚 All Books")
    if not st.session_state.library:
        st.warning("Your library is empty! Add some books first.")
        return
    
    for book in st.session_state.library:
        st.markdown(f"""
        <div class="card">
            <h3>{book['title']}</h3>
            <p>👤 {book['author']}</p>
            <p>📅 {book['year']} | 🎭 {book['genre']} | 📖 {'✅ Read' if book['read'] else '❌ Unread'}</p>
        </div>
        """, unsafe_allow_html=True)

def show_stats():
    st.subheader("📊 Library Statistics")
    if not st.session_state.library:
        st.warning("Your library is empty! Add some books first.")
        return
    
    total = len(st.session_state.library)
    read = sum(1 for b in st.session_state.library if b['read'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-box'><h3>📚 Total Books</h3><h2>{total}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box'><h3>✅ Read</h3><h2>{read}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box'><h3>📖 Unread</h3><h2>{total - read}</h2></div>", unsafe_allow_html=True)
    
    genres = [b['genre'] for b in st.session_state.library]
    st.bar_chart({g: genres.count(g) for g in set(genres)})

def export_library():
    st.subheader("📤 Export Library")
    if st.session_state.library:
        json_data = json.dumps(st.session_state.library, indent=2)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="library.json",
            mime="application/json"
        )
    else:
        st.warning("Library is empty!")

def import_library():
    st.subheader("📥 Import Library")
    uploaded_file = st.file_uploader("Upload JSON", type=["json"])
    
    if uploaded_file:
        try:
            data = json.load(uploaded_file)
            mode = st.radio("Import Mode:", ["Replace", "Merge"])
            
            if st.button("Confirm Import"):
                if mode == "Replace":
                    st.session_state.library = data
                else:
                    existing = {(b['title'], b['author']) for b in st.session_state.library}
                    for book in data:
                        if (book['title'], book['author']) not in existing:
                            st.session_state.library.append(book)
                
                save_data(st.session_state.library)
                st.success(f"Imported {len(data)} books!")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ======================================
# MAIN APP
# ======================================
def main():
    st.set_page_config(
        page_title="Personal Library Management System",
        page_icon="📚",
        layout="wide"
    )
    st.markdown(CSS, unsafe_allow_html=True)
    
    if "library" not in st.session_state:
        st.session_state.library = load_data()
    
    # SIDEBAR
    with st.sidebar:
        st.header("Navigation Portal")
        st.markdown("---")
        
        # Statistics
        total = len(st.session_state.library)
        read = sum(1 for b in st.session_state.library if b['read'])
        
        st.markdown(f"**📚 Total Books:** {total}")
        st.markdown(f"**✅ Read Books:** {read}")
        st.markdown(f"**📖 Unread Books:** {total - read}")
        st.markdown("---")
        
        # Navigation
        menu = [
            "🏠 Home", "➕ Add Book", "🗑️ Remove Book",
            "🔍 Search Books", "📚 View All", "📊 Statistics",
            "📤 Export", "📥 Import", "🚪 Exit"
        ]
        choice = st.selectbox("Menu", menu, label_visibility="collapsed")
    
    # MAIN CONTENT
    if choice == "🏠 Home":
        st.title("✨ Personal Library Management System!")
        st.image("https://cdn.pixabay.com/photo/2015/11/19/21/11/book-1052014_1280.jpg", 
                use_container_width=True)
        st.markdown("""
        ## Our Digital Library Manager
        Manage your book collection with these features:
        - Add new books with detailed metadata
        - Track reading progress
        - Search and filter your collection
        - Import/export your library
        - View detailed statistics
        """)
        
    elif choice == "➕ Add Book":
        add_book()
    elif choice == "🗑️ Remove Book":
        remove_book()
    elif choice == "🔍 Search Books":
        search_books()
    elif choice == "📚 View All":
        display_books()
    elif choice == "📊 Statistics":
        show_stats()
    elif choice == "📤 Export":
        export_library()
    elif choice == "📥 Import":
        import_library()
    elif choice == "🚪 Exit":
        st.sidebar.success("Thank you for using Digital Library Manager! 👋")
        st.stop()

if __name__ == "__main__":
    main()