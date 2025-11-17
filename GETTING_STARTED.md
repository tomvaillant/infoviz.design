# Getting Started with Infoviz.design

This guide will help you set up and run the Infoviz.design visual inspiration gallery locally.

## Prerequisites

Before you start, ensure you have:

1. **Docker Desktop** installed and running
2. **HuggingFace account** with API token ([get one here](https://huggingface.co/settings/tokens))

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/tomvaillant/infoviz.design.git
cd infoviz.design
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your HuggingFace API key:

```bash
# Required
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx

# Optional
DEBUG=false
ENVIRONMENT=development
VITE_API_URL=http://localhost:8000
```

### 3. Start the Application

```bash
# Start with the convenience script
./start.sh

# Or use docker-compose directly
docker-compose up --build
```

The first build will take a few minutes to download and install dependencies.

### 4. Access the Application

Once started, open your browser:

- **Frontend**: http://localhost:5173
- **Backend API docs**: http://localhost:8000/docs

## How to Use

### Search for Visual Stories

1. Enter a topic in the search box (e.g., "climate change", "election graphics", "data visualization")
2. Click "Find visuals"
3. Browse the results with images, sources, and publication dates
4. Click any card to open the original story
5. Use "Load more results" to see additional examples

### Daily Features

When you first load the page, you'll see 2 featured visual stories published recently. These update automatically based on the latest content.

## Development

### Project Structure

```
infoviz.design/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI application
│   │   ├── config.py                  # Configuration
│   │   ├── routers/
│   │   │   └── graphics.py            # Graphics search endpoint
│   │   └── services/
│   │       └── hf_spaces_client.py    # HuggingFace integration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── routes/
│   │   │   ├── +page.svelte           # Main page
│   │   │   └── +layout.svelte         # Root layout
│   │   ├── lib/
│   │   │   ├── api-client.ts          # API client
│   │   │   └── components/
│   │   │       └── graphics/
│   │   │           └── GraphicsView.svelte
│   │   ├── app.css                    # Global styles
│   │   └── app.html                   # HTML template
│   └── package.json
├── docker-compose.yml                 # Local development
├── Dockerfile                         # Production build
└── render.yaml                        # Render deployment config
```

### Frontend Development

The frontend uses:
- **SvelteKit** for the framework
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Fraunces** (display serif) and **Inter** (sans-serif) fonts
- Custom animations and green gradient scrollbar

Hot reload is enabled - changes to files in `frontend/src` will automatically refresh the browser.

### Backend Development

The backend uses:
- **FastAPI** for the web framework
- **gradio-client** to connect to HuggingFace Spaces
- **BeautifulSoup4** for HTML parsing

Hot reload is enabled - changes to files in `backend/app` will automatically restart the server.

### API Endpoint

**POST /api/graphics/examples**

Request:
```json
{
  "query": "climate change visualizations"
}
```

Response:
```json
{
  "query": "climate change visualizations",
  "items": [
    {
      "title": "Story title",
      "source": "Publication name",
      "date": "2024-01-15",
      "url": "https://...",
      "image": "https://..."
    }
  ]
}
```

## Troubleshooting

### Docker Issues

**"Cannot connect to Docker daemon"**
```bash
# Make sure Docker Desktop is running
# On Mac: Check menu bar for Docker icon
# On Windows: Check system tray
```

**"Port already in use"**
```bash
# Stop existing services
docker-compose down

# Or kill processes on ports 8000/5173:
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### Backend Issues

**"HuggingFace connection failed"**
- Check your `HUGGINGFACE_API_KEY` in `.env` is valid
- Verify the key has read permissions
- HuggingFace Spaces can have cold starts (up to 30 seconds) - try again

**"API timeout"**
- The HuggingFace Space might be starting up (first request can be slow)
- Check backend logs: `docker-compose logs backend`

### Frontend Issues

**"Failed to fetch spotlights"**
- Ensure backend is running on http://localhost:8000
- Check backend logs for errors
- Verify your HuggingFace API key is valid

**"Blank page or loading forever"**
- Clear browser cache and reload
- Check browser console for errors (F12)
- View frontend logs: `docker-compose logs frontend`

## View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

## Restart Services

```bash
# Restart everything
docker-compose restart

# Rebuild after code changes
docker-compose up --build

# Stop services
docker-compose down

# Clean rebuild (removes volumes)
docker-compose down -v && docker-compose up --build
```

## Production Deployment

The application is deployed on Render.com using Docker. See the main README.md for deployment configuration details.

Required environment variables for production:
- `HUGGINGFACE_API_KEY` (required)
- `ENVIRONMENT=production`
- `DEBUG=false`

## Tips

1. **Hot Reload**: Changes in `frontend/src` and `backend/app` auto-reload
2. **API Docs**: Visit http://localhost:8000/docs for interactive API testing
3. **Debugging**: Add `console.log()` (frontend) or `print()` (backend) statements
4. **Pagination**: Results are paginated client-side (9 items per page)

## Getting Help

If you encounter issues:
1. Check the logs: `docker-compose logs -f`
2. Verify `HUGGINGFACE_API_KEY` is set correctly in `.env`
3. Ensure Docker Desktop is running
4. Try a clean rebuild: `docker-compose down -v && docker-compose up --build`

## Links

- **Newsletter**: [Buried Signals](https://buriedsignals.substack.com/)
- **YouTube**: [@buriedsignals](https://www.youtube.com/@buriedsignals)
- **GitHub**: [tomvaillant/infoviz.design](https://github.com/tomvaillant/infoviz.design)

Happy exploring! 🎨
