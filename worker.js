// Cloudflare Worker for URL Shortener
// This handles the actual redirects to make URLs as short as possible

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  const path = url.pathname.slice(1) // Remove leading slash

  // Home page - show simple info
  if (!path || path === '') {
    return new Response(getHomePage(), {
      headers: { 'content-type': 'text/html' }
    })
  }

  // API endpoint to sync links from Streamlit
  if (path === 'api/sync' && request.method === 'POST') {
    try {
      const data = await request.json()
      await LINKS.put('all_links', JSON.stringify(data))
      return new Response(JSON.stringify({ success: true }), {
        headers: { 'content-type': 'application/json' }
      })
    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), {
        status: 400,
        headers: { 'content-type': 'application/json' }
      })
    }
  }

  // Get all links from KV storage
  const linksData = await LINKS.get('all_links')
  const links = linksData ? JSON.parse(linksData) : {}

  // Check if short code exists
  if (links[path]) {
    const destinationUrl = links[path].url

    // Increment click counter
    links[path].clicks = (links[path].clicks || 0) + 1
    await LINKS.put('all_links', JSON.stringify(links))

    // Redirect to the destination URL
    return Response.redirect(destinationUrl, 301)
  }

  // Short code not found
  return new Response(getNotFoundPage(path), {
    status: 404,
    headers: { 'content-type': 'text/html' }
  })
}

function getHomePage() {
  return `
<!DOCTYPE html>
<html>
<head>
  <title>URL Shortener</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    .container {
      text-align: center;
      padding: 2rem;
    }
    h1 {
      font-size: 3rem;
      margin-bottom: 1rem;
    }
    p {
      font-size: 1.2rem;
      opacity: 0.9;
    }
    .emoji {
      font-size: 4rem;
      margin-bottom: 1rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="emoji">🔗</div>
    <h1>URL Shortener</h1>
    <p>Lightning-fast link redirects</p>
    <p style="font-size: 0.9rem; margin-top: 2rem;">Powered by Cloudflare Workers</p>
  </div>
</body>
</html>
  `
}

function getNotFoundPage(code) {
  return `
<!DOCTYPE html>
<html>
<head>
  <title>Link Not Found</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      color: white;
    }
    .container {
      text-align: center;
      padding: 2rem;
    }
    h1 {
      font-size: 3rem;
      margin-bottom: 1rem;
    }
    code {
      background: rgba(255,255,255,0.2);
      padding: 0.5rem 1rem;
      border-radius: 0.5rem;
      font-size: 1.2rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>404 - Link Not Found</h1>
    <p>The short code <code>${code}</code> doesn't exist.</p>
    <p style="font-size: 0.9rem; margin-top: 2rem;">Check the URL and try again</p>
  </div>
</body>
</html>
  `
}
