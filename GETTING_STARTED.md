# 🚀 Getting Started with Infoviz

This guide will help you set up and test your newly migrated Infoviz application.

## ✅ What's Been Completed

### Backend (FastAPI) - 100% Complete
- ✅ Full project structure with routers, services, parsers
- ✅ All Python business logic ported (factiverse, parsers, prompt builders)
- ✅ Supabase authentication & authorization
- ✅ HF Spaces integration with gradio-client
- ✅ All 5 mode endpoints (SCRAPE, DATA, INVESTIGATE, FACT-CHECK, GRAPHICS)
- ✅ Complete API with health checks and error handling

### Frontend (SvelteKit) - 100% Complete
- ✅ Full TypeScript + Tailwind setup
- ✅ Svelte stores (auth, chat, app, scraper)
- ✅ Authentication flow with login/signup
- ✅ All chat components with message rendering
- ✅ DATA mode cards (Votes, Parliamentarians, Motions)
- ✅ FACT-CHECK mode cards (Claims with confidence badges)
- ✅ SCRAPE sidebar (Setup, Active Jobs, Notifications)
- ✅ DATA & INVESTIGATE sidebars
- ✅ Main app page with mode switching

### Development Tools
- ✅ Docker Compose for local development
- ✅ Development Dockerfiles (hot reload enabled)
- ✅ Comprehensive README and documentation

## 📋 Prerequisites

Before you start, ensure you have:

1. **Docker Desktop** installed and running
2. **Supabase account** (free tier is fine)
3. **Hugging Face account** with API token
4. **(Optional)** Factiverse API token for FACT-CHECK mode

## 🛠️ Step-by-Step Setup

### 1. Configure Supabase

#### Create a Supabase Project
1. Go to https://supabase.com
2. Create a new project
3. Wait for the database to provision (~2 minutes)

#### Run Database Migration
In your Supabase SQL Editor, run this SQL:

```sql
-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    auth_user_id UUID UNIQUE REFERENCES auth.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create scheduled scrapers table
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

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduled_scrapers ENABLE ROW LEVEL SECURITY;

-- RLS Policies for users table
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth_user_id = auth.uid());

CREATE POLICY "Users can insert own data" ON users
    FOR INSERT WITH CHECK (auth_user_id = auth.uid());

-- RLS Policies for scrapers table
CREATE POLICY "Users can view own scrapers" ON scheduled_scrapers
    FOR SELECT USING (user_id IN (SELECT id FROM users WHERE auth_user_id = auth.uid()));

CREATE POLICY "Users can insert own scrapers" ON scheduled_scrapers
    FOR INSERT WITH CHECK (user_id IN (SELECT id FROM users WHERE auth_user_id = auth.uid()));

CREATE POLICY "Users can delete own scrapers" ON scheduled_scrapers
    FOR DELETE USING (user_id IN (SELECT id FROM users WHERE auth_user_id = auth.uid()));

-- Create a function to auto-create user record on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.users (auth_user_id)
    VALUES (NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to call the function
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();
```

#### Get Supabase Credentials
1. Go to **Project Settings** > **API**
2. Copy these values:
   - Project URL (e.g., `https://xxxxx.supabase.co`)
   - `anon` `public` key (starts with `eyJ...`)
   - `service_role` `secret` key (starts with `eyJ...`)

### 2. Get API Keys

#### Hugging Face
1. Go to https://huggingface.co/settings/tokens
2. Create a new token (Read permission is enough)
3. Copy the token (starts with `hf_...`)

#### Factiverse (Optional)
1. Go to https://factiverse.ai
2. Sign up for an account
3. Get your API token from the dashboard

### 3. Configure Environment

```bash
cd Infoviz-svelte
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
# Supabase (REQUIRED)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Hugging Face (REQUIRED)
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx

# Factiverse (OPTIONAL - only needed for FACT-CHECK mode)
FACTIVERSE_API_TOKEN=your-factiverse-token
```

### 4. Start the Application

```bash
# Option 1: Use the startup script
./start.sh

# Option 2: Use docker-compose directly
docker-compose up --build
```

The first build will take a few minutes to download and install dependencies.

### 5. Create Your First Account

1. Open http://localhost:5173 in your browser
2. Click "Don't have an account? Sign Up"
3. Enter an email and password (min 6 characters)
4. Click "Sign Up"
5. Check your email for verification link (from Supabase)
6. Click the verification link
7. Return to http://localhost:5173 and sign in

## 🧪 Testing Each Mode

### 1. SCRAPE Mode
1. Click the **SCRAPE** button
2. Go to "Scraper Setup" tab
3. Fill in the form:
   - URL: `https://example.com`
   - Criteria: `Monitor for changes`
   - Frequency: `Weekly`
   - Day: `Monday`
   - Time: `12:00`
   - Notification: `Email`
4. Click "Create Scraper"
5. Switch to "Active Jobs" tab to see your scraper
6. Try deleting it with the trash icon

### 2. DATA Mode
1. Click the **DATA** button
2. Try these questions:
   - "Who are the parliamentarians from Zurich?"
   - "Show me votes about climate change"
   - "Find motions from 2024"
3. Observe the parsed vote/parliamentarian cards
4. Try switching datasets in the sidebar (Swiss Parliament ↔ BFS)

### 3. FACT-CHECK Mode
1. Click the **FACT-CHECK** button
2. Paste this test text:
   ```
   Switzerland has 26 cantons. The capital of Switzerland is Bern.
   The Swiss Alps cover approximately 60% of the country.
   ```
3. Click "Send"
4. Observe the detected claims with confidence badges
5. Note: This requires a valid Factiverse API token

### 4. INVESTIGATE Mode
1. Click the **INVESTIGATE** button
2. See the placeholder Bellingcat tools in the sidebar
3. This mode is a placeholder for future OSINT tools

### 5. GRAPHICS Mode
1. Click the **GRAPHICS** button
2. Ask: "Create a bar chart of Swiss canton populations"
3. This mode connects to the GRAPHICS HF Space

## 🐛 Troubleshooting

### Docker Issues

**"Cannot connect to Docker daemon"**
```bash
# Make sure Docker Desktop is running
# On Mac: Check menu bar for Docker icon
# On Windows: Check system tray
```

**"Port already in use"**
```bash
# Stop any existing services on ports 8000 or 5173
docker-compose down
# or kill the processes:
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### Backend Issues

**"Supabase connection failed"**
- Check your `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` in `.env`
- Verify your Supabase project is active

**"HF Space timeout"**
- HF Spaces can have cold starts (up to 30 seconds)
- Try again after waiting a moment
- Check your `HUGGINGFACE_API_KEY` is valid

### Frontend Issues

**"Authentication failed"**
- Clear browser cookies and try again
- Check `PUBLIC_SUPABASE_URL` and `PUBLIC_SUPABASE_ANON_KEY` match your backend values
- Verify email is confirmed in Supabase Auth dashboard

**"API request failed"**
- Check backend is running on http://localhost:8000
- View backend logs: `docker-compose logs backend`

## 📊 View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

## 🔄 Restart Services

```bash
# Restart everything
docker-compose restart

# Rebuild after code changes
docker-compose up --build

# Stop services
docker-compose down
```

## 📝 Next Steps

### For Testing
1. Test all 5 modes with various inputs
2. Verify scraper CRUD operations
3. Check authentication flow (signup, login, logout)
4. Test responsive design on mobile

### For Deployment
See the main README.md for:
- HF Spaces deployment instructions
- Production Dockerfile
- nginx configuration
- Environment variable setup

## 💡 Tips

1. **Hot Reload**: Code changes in `frontend/src` and `backend/app` will auto-reload
2. **API Docs**: Visit http://localhost:8000/docs for interactive API testing
3. **Database**: Use Supabase dashboard to view/edit database directly
4. **Logs**: Add `console.log()` (frontend) or `logger.info()` (backend) for debugging

## 🆘 Getting Help

If you encounter issues:
1. Check the logs: `docker-compose logs -f`
2. Verify all environment variables are set correctly
3. Ensure Supabase database migration was successful
4. Try rebuilding: `docker-compose down && docker-compose up --build`

Happy testing! 🎉
