# URL Shortener

A lightweight, self-hosted URL shortening service with a clean web interface and custom domain support.

## Overview

This application provides a simple solution for creating and managing shortened URLs. Built for personal or small-team use, it features password protection, automatic synchronization to edge infrastructure, and a minimalistic user interface.

## Features

- **Custom Short URLs**: Create memorable short links on your own domain
- **Password Protected**: Secure access with authentication
- **Auto-Sync**: Automatic synchronization to Cloudflare Workers for instant deployment
- **Clean Interface**: Minimalistic black and white UI
- **Link Management**: View, create, and delete short URLs from a single dashboard
- **Fast Redirects**: Edge-based routing via Cloudflare Workers for global performance

## Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Cloudflare Workers (Serverless edge computing)
- **Storage**: Cloudflare KV (Key-value store)
- **Deployment**: Streamlit Cloud + Cloudflare

## Prerequisites

- Python 3.8+
- Cloudflare account (free tier)
- Custom domain (optional but recommended)

## Installation

Clone the repository:

```bash
git clone https://github.com/asaikiranb/URL-Shortner.git
cd URL-Shortner
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Run Locally

```bash
streamlit run streamlit_app.py
```

Access the application at `http://localhost:8501` and log in with your credentials.

### Create Short URLs

1. Enter your desired short code (e.g., `docs`, `project`, `link`)
2. Paste the destination URL
3. Click "Create"
4. Your short URL is instantly available

### Deploy to Production

#### Streamlit Cloud

1. Push your code to GitHub
2. Get a Cloudflare API token:
   - Go to https://dash.cloudflare.com/profile/api-tokens
   - Create token with "Account.Workers KV Storage:Edit" permission
3. Visit [share.streamlit.io](https://share.streamlit.io)
4. Connect your repository
5. Deploy with main file: `streamlit_app.py`
6. In Streamlit Cloud settings, add secret:
   ```
   CLOUDFLARE_API_TOKEN = "your_token_here"
   ```

#### Cloudflare Workers

1. Install Wrangler CLI: `npm install -g wrangler`
2. Configure `wrangler.toml` with your domain
3. Deploy: `wrangler deploy`

## Configuration

Edit `streamlit_app.py` to customize:

- `DOMAIN`: Your custom domain
- `USERNAME`: Authentication username
- `PASSWORD`: Authentication password

## File Structure

```
.
├── streamlit_app.py     # Main application
├── worker.js            # Cloudflare Worker for redirects
├── wrangler.toml        # Cloudflare configuration
├── requirements.txt     # Python dependencies
├── sync_to_worker.py    # Sync utility
└── README.md           # Documentation
```

## How It Works

1. User creates a short URL via the Streamlit interface
2. Link is saved to local JSON storage
3. Automatically synced to Cloudflare KV storage
4. Cloudflare Worker handles redirect requests at the edge
5. Users accessing the short URL are instantly redirected to the destination

## Security

- Password-protected web interface
- Credentials hardcoded in application (update before deployment)
- HTTPS encryption via Cloudflare
- No public API endpoints

## License

MIT License - Feel free to use and modify for your needs.

## Contributing

This is a personal project, but suggestions and improvements are welcome via issues or pull requests.

---

**Note**: Update authentication credentials in `streamlit_app.py` before deploying to production.
