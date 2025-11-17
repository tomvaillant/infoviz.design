# Infoviz - AI-Powered Journalism Assistant

A full-stack application built with **SvelteKit** (frontend) and **FastAPI** (backend), designed to help journalists with data analysis, fact-checking, web scraping, and OSINT investigations.

## 🎯 Features

### 5 Journalism Modes

1. **SCRAPE** - Schedule automated web scrapers with customizable criteria
2. **DATA** - Query Swiss Parliament (OpenParlData) and BFS datasets
3. **INVESTIGATE** - Bellingcat-style OSINT tools (coming soon)
4. **FACT-CHECK** - AI-powered claim detection using Factiverse API
5. **GRAPHICS** - Data visualization (Hugging Face Space integration)

## 🏗️ Architecture

```
Infoviz-svelte/
├── frontend/          # SvelteKit app (TypeScript + Tailwind)
│   ├── src/
│   │   ├── routes/              # Pages (+layout, +page)
│   │   └── lib/
│   │       ├── components/      # Svelte components
│   │       ├── stores/          # State management
│   │       ├── types.ts         # TypeScript types
│   │       └── api-client.ts    # Backend API wrapper
│   └── package.json
│
├── backend/           # FastAPI app (Python 3.11)
│   ├── app/
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── parsers/             # Data parsers
│   │   ├── models/              # Pydantic schemas
│   │   └── main.py              # FastAPI entry point
│   └── requirements.txt
│
└── docker-compose.yml # Local development setup
```

## 🚀 Quick Start (Local Development)

### Prerequisites

- Docker & Docker Compose
- Supabase account (for authentication & database)
- Hugging Face API key
- Factiverse API token (optional, for FACT-CHECK mode)

### Setup

1. **Clone and configure**
   ```bash
   cd Infoviz-svelte
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials:**
   ```bash
   # Supabase (required)
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJxxx...
   SUPABASE_SERVICE_ROLE_KEY=eyJxxx...
   PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
   PUBLIC_SUPABASE_ANON_KEY=eyJxxx...

   # Hugging Face (required)
   HUGGINGFACE_API_KEY=hf_xxx

   # Factiverse (optional)
   FACTIVERSE_API_TOKEN=xxx
   ```

3. **Start the application**
   ```bash
   docker-compose up
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Database Setup (Supabase)

Create these tables in your Supabase database:

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    auth_user_id UUID UNIQUE REFERENCES auth.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scheduled scrapers table
CREATE TABLE scheduled_scrapers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    criteria TEXT,
    regularity TEXT CHECK (regularity IN ('weekly', 'monthly')),
    day_number INTEGER,
    time_utc TEXT,
    scraper_service TEXT,
    prompt_summary TEXT,
    monitoring BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduled_scrapers ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth_user_id = auth.uid());

CREATE POLICY "Users can view own scrapers" ON scheduled_scrapers
    FOR SELECT USING (user_id IN (SELECT id FROM users WHERE auth_user_id = auth.uid()));

CREATE POLICY "Users can insert own scrapers" ON scheduled_scrapers
    FOR INSERT WITH CHECK (user_id IN (SELECT id FROM users WHERE auth_user_id = auth.uid()));

CREATE POLICY "Users can delete own scrapers" ON scheduled_scrapers
    FOR DELETE USING (user_id IN (SELECT id FROM users WHERE auth_user_id = auth.uid()));
```

## 🛠️ Development

### Frontend (SvelteKit)

```bash
cd frontend
npm install
npm run dev
```

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📦 Tech Stack

### Frontend
- **SvelteKit** - Web framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Supabase Auth** - Authentication
- **Lucide Svelte** - Icons

### Backend
- **FastAPI** - API framework
- **Pydantic** - Data validation
- **Supabase Python** - Database & auth
- **gradio-client** - HF Spaces integration
- **LangChain** - LLM orchestration
- **Requests** - HTTP client

## 🔌 API Endpoints

### Chat
- `POST /api/chat` - Send message to AI (supports all modes)

### Scrapers
- `POST /api/scrapers` - Create scraper
- `GET /api/scrapers` - List user's scrapers
- `GET /api/scrapers/{id}` - Get scraper details
- `DELETE /api/scrapers/{id}` - Delete scraper

### Authentication
- `GET /api/auth/me` - Get current user
- `GET /api/auth/status` - Check auth status

## 🌐 Hugging Face Spaces Integration

The backend integrates with these HF Spaces:

- **DATA**: `tomvaillant/cojournalist-data` (Swiss Parliament + BFS)
- **GRAPHICS**: `Infoviz/cojournalist-graphics`
- **INVESTIGATE**: `Infoviz/cojournalist-investigate`
- **FACT-CHECK**: `Infoviz/Infoviz-Fact-Check`

## 📝 Environment Variables

### Backend (.env)
```bash
SUPABASE_URL                # Supabase project URL
SUPABASE_KEY                # Supabase anon key
SUPABASE_SERVICE_ROLE_KEY   # Supabase service role key
HUGGINGFACE_API_KEY         # HF API token
FACTIVERSE_API_TOKEN        # Factiverse API token (optional)
DEBUG                       # Debug mode (True/False)
```

### Frontend (.env)
```bash
PUBLIC_SUPABASE_URL         # Supabase project URL (public)
PUBLIC_SUPABASE_ANON_KEY    # Supabase anon key (public)
VITE_API_URL                # Backend API URL (default: http://localhost:8000)
```

## 🧪 Testing

```bash
# Backend tests (if implemented)
cd backend
pytest

# Frontend tests (if implemented)
cd frontend
npm run test
```

## 🚢 Deployment (Render.com)

### Prerequisites
- GitHub repository with your code
- Render.com account ([sign up here](https://render.com))
- All required API credentials ready:
  - Supabase URL and keys
  - HuggingFace API key
  - Factiverse API token (optional)

### Deployment Steps

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Create New Web Service on Render.com**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the `main` branch

3. **Configure Service Settings**
   - **Name**: `cojournalist` (or your preferred name)
   - **Region**: Choose closest to your users (e.g., Frankfurt, Oregon)
   - **Environment**: `Docker`
   - **Docker Command**: Leave empty (uses Dockerfile CMD)
   - **Plan**: Select your preferred tier (Free/Starter/Pro)

4. **Set Environment Variables**
   In the Render dashboard under "Environment", add these variables:

   ```bash
   # Supabase (required)
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJxxx...
   SUPABASE_SERVICE_ROLE_KEY=eyJxxx...
   PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
   PUBLIC_SUPABASE_ANON_KEY=eyJxxx...

   # Hugging Face (required)
   HUGGINGFACE_API_KEY=hf_xxx

   # n8n Webhook (pre-configured)
   PUBLIC_N8N_WEBHOOK_URL=https://n8n-service-oy4e.onrender.com/webhook/criteria-check

   # API Configuration
   VITE_API_URL=/api
   DEBUG=false

   # Factiverse (optional)
   FACTIVERSE_API_TOKEN=xxx
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application
   - Monitor the build logs for any issues
   - Once deployed, your app will be available at `https://your-app-name.onrender.com`

### Using render.yaml (Infrastructure as Code)

This repository includes a `render.yaml` blueprint for automated deployment:

```bash
# Deploy using Render Blueprint
# 1. Go to Render Dashboard
# 2. Click "New" → "Blueprint"
# 3. Connect your repository
# 4. Render will auto-detect render.yaml and configure everything
```

### Health Checks

Render automatically monitors your app's health using the `/api/health` endpoint.

### Auto-Deploy

Render automatically redeploys your app when you push to the `main` branch:

```bash
git push origin main  # Triggers automatic deployment
```

### Troubleshooting

**Build fails with "port already in use"**
- This shouldn't happen with Docker, but ensure `PORT` env var is set by Render

**Frontend not loading**
- Verify `VITE_API_URL=/api` is set in environment variables
- Check that frontend build completed in logs

**API calls failing**
- Verify all Supabase environment variables are correct
- Check CORS settings if using custom domain
- Ensure HuggingFace API key is valid

**Slow cold starts (Free tier)**
- Free tier services spin down after inactivity
- Upgrade to Starter tier for always-on service

### Monitoring

View logs in Render dashboard:
- Build logs: Shows Docker build process
- Deploy logs: Shows application startup
- Service logs: Real-time application logs

## 📄 License

[Your License Here]

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 🙏 Acknowledgments

- **OpenParlData** - Swiss Parliament data
- **Factiverse** - Claim detection AI
- **Hugging Face** - Model hosting & Spaces
- **Supabase** - Authentication & database
- **Bellingcat** - OSINT methodology inspiration
---
title: Infoviz
emoji: 🐳
colorFrom: purple
colorTo: gray
sdk: docker
app_port: 7860
---

# Infoviz - AI-Powered Journalism Assistant
