# Infoviz.design

Visual inspiration gallery for journalists - discover exceptional visual stories from newsrooms around the world.

## Overview

Infoviz.design helps journalists find visual inspiration by searching curated examples of data-driven visual journalism. Browse by topic to spark ideas for your own storytelling.

## Features

- 🔍 **Search by topic** - Find visual stories about climate, elections, data, and more
- 📰 **Global newsrooms** - Examples from leading publications worldwide
- 🖼️ **Rich previews** - See images, sources, and publication dates
- 🔗 **Direct links** - Jump straight to the original story
- 📄 **Smart pagination** - Load more results as you explore

## Tech Stack

**Frontend:**
- SvelteKit + TypeScript
- Tailwind CSS with custom animations
- Fraunces & Inter fonts

**Backend:**
- FastAPI (Python 3.11)
- gradio-client (HuggingFace Spaces integration)
- BeautifulSoup4 (HTML parsing)

**Data Source:**
- Hugging Face Space: `Infoviz/cojournalist-graphics`

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Hugging Face API key ([get one here](https://huggingface.co/settings/tokens))

### Local Development

1. **Clone and setup:**
```bash
git clone https://github.com/tomvaillant/infoviz.design.git
cd infoviz.design
cp .env.example .env
```

2. **Add your HuggingFace API key to `.env`:**
```bash
HUGGINGFACE_API_KEY=hf_your_key_here
```

3. **Start with Docker:**
```bash
./start.sh
```

4. **Open your browser:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs

## Development (without Docker)

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API

### `POST /api/graphics/examples`

Fetch visual journalism examples by topic.

**Request:**
```json
{
  "query": "climate change visualizations"
}
```

**Response:**
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

## Environment Variables

### Required
- `HUGGINGFACE_API_KEY` - Your HuggingFace API key for Spaces access

### Optional
- `DEBUG` - Enable debug logging (default: false)
- `ENVIRONMENT` - Set to "production" for production (default: development)
- `VITE_API_URL` - Frontend API URL (default: http://localhost:8000)

## Production Deployment

Deployed on Render.com using Docker.

**Environment variables to set in Render:**
- `HUGGINGFACE_API_KEY` (required)
- `ENVIRONMENT=production`
- `DEBUG=false`

See `render.yaml` for complete configuration.

## Project Structure

```
infoviz.design/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── routers/
│   │   │   └── graphics.py      # Graphics API endpoint
│   │   └── services/
│   │       └── hf_spaces_client.py  # HF integration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── routes/
│   │   │   └── +page.svelte     # Main page
│   │   └── lib/
│   │       └── components/
│   │           └── graphics/
│   │               └── GraphicsView.svelte
│   └── package.json
├── Dockerfile                   # Production build
├── docker-compose.yml           # Local development
└── render.yaml                  # Render deployment config
```

## Team

Developed by **Tom Vaillant** and **Remy Dumas**.

## Links

- 📧 Newsletter: [Buried Signals](https://buriedsignals.substack.com/)
- 🎥 YouTube: [@buriedsignals](https://www.youtube.com/@buriedsignals)
- 💼 LinkedIn: [Tom Vaillant](https://www.linkedin.com/in/tomvaillant/)
- 🤗 Hugging Face: [@tomvaillant](https://huggingface.co/tomvaillant)

## License

MIT License - see LICENSE file for details
