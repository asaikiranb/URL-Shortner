"""
Custom URL Shortener for saikiranb.com
Simple interface to create and manage short URLs
"""

import streamlit as st
import json
import subprocess
from datetime import datetime

# Configuration
LINKS_FILE = "links.json"
DOMAIN = "saikiranb.com"
USERNAME = "Annangi"
PASSWORD = "Annangi"


def authenticate():
    """Simple password protection"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("Login")
        st.markdown(f"URL Shortener for {DOMAIN}")
        st.markdown("---")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", type="primary", use_container_width=True):
            if username == USERNAME and password == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        return False
    return True


def load_links_from_cloudflare():
    """Load links from Cloudflare KV"""
    try:
        result = subprocess.run(
            ['wrangler', 'kv', 'key', 'get', '--binding=LINKS', 'all_links', '--remote'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
        return {}
    except Exception:
        return {}


def load_links():
    """Load links from local file or Cloudflare"""
    # Try Cloudflare first (for cloud deployment)
    cloudflare_links = load_links_from_cloudflare()
    if cloudflare_links:
        return cloudflare_links

    # Fallback to local file
    try:
        with open(LINKS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_links(links):
    """Save links to both local file and Cloudflare"""
    # Save to local file
    with open(LINKS_FILE, 'w') as f:
        json.dump(links, f, indent=2)

    # Save to Cloudflare
    sync_to_cloudflare(links)


def sync_to_cloudflare(links):
    """Sync links to Cloudflare KV storage"""
    try:
        links_json = json.dumps(links)
        result = subprocess.run(
            ['wrangler', 'kv', 'key', 'put', '--binding=LINKS', 'all_links', links_json, '--remote'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False


# Page config
st.set_page_config(
    page_title="URL Shortener",
    layout="centered"
)

# Authentication check
if not authenticate():
    st.stop()

# Main app
st.title("URL Shortener")
st.markdown(f"**Domain:** {DOMAIN}")
st.markdown("---")

# Load links (always from Cloudflare if available)
links = load_links()

# Show success message if just created
if "just_created" in st.session_state and st.session_state.just_created:
    created_code = st.session_state.created_code
    created_url = st.session_state.created_url
    st.success(f"Short URL created!")
    st.markdown("**Your Short URL is Ready**")
    st.code(f"https://{DOMAIN}/{created_code}", language=None)
    st.markdown(f"Redirects to: {created_url}")
    st.markdown("---")
    st.session_state.just_created = False

# Create new short URL
st.subheader("Create Short URL")

short_code = st.text_input(
    "Short Code",
    placeholder=f"Enter code (e.g., 'resume' for {DOMAIN}/resume)",
    key="short_code_input"
)

destination_url = st.text_input(
    "Destination URL",
    placeholder="https://drive.google.com/...",
    key="destination_url_input"
)

if st.button("Create Short URL", type="primary", use_container_width=True):
    if not short_code:
        st.error("Please enter a short code")
    elif not short_code.replace("-", "").replace("_", "").isalnum():
        st.error("Short code can only contain letters, numbers, hyphens, and underscores")
    elif not destination_url:
        st.error("Please enter a destination URL")
    elif not destination_url.startswith("http"):
        st.error("Please enter a valid URL starting with http:// or https://")
    elif short_code in links:
        st.error(f"Short code '{short_code}' already exists")
    else:
        # Create link
        links[short_code] = {
            "url": destination_url,
            "created": datetime.now().isoformat(),
            "clicks": 0
        }

        # Save to both local and Cloudflare
        save_links(links)

        # Store in session state for success message
        st.session_state.just_created = True
        st.session_state.created_code = short_code
        st.session_state.created_url = destination_url

        st.rerun()

# Display existing links (always show from loaded data)
if links:
    st.markdown("---")
    st.subheader("Your Short URLs")

    for code, data in sorted(links.items()):
        col1, col2, col3 = st.columns([2, 6, 1])

        with col1:
            st.markdown(f"`{code}`")

        with col2:
            # Make the destination URL clickable
            url_display = data['url'][:60] + "..." if len(data['url']) > 60 else data['url']
            st.markdown(f"[{DOMAIN}/{code}]({data['url']}) → {url_display}")

        with col3:
            if st.button("Delete", key=f"delete_{code}", type="secondary"):
                del links[code]
                save_links(links)
                st.rerun()
else:
    st.info("No short URLs created yet. Create your first one above!")

# Footer
st.markdown("---")
col1, col2 = st.columns([4, 1])
with col1:
    st.caption(f"{len(links)} short URL(s) • Synced to Cloudflare")
with col2:
    if st.button("Logout", type="secondary"):
        st.session_state.authenticated = False
        st.rerun()
