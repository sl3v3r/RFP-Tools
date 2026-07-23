# Frontend Setup Guide

## Overview

The RFP Tools dashboard is a modern React TypeScript application built with:
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **React Query** - Data fetching & caching
- **Recharts** - Data visualization
- **React Router** - Client-side routing

---

## Quick Start

### Development

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`

### Production Build

```bash
cd frontend
npm install
npm run build
npm run preview
```

### Docker

```bash
cd frontend
docker build -f docker/Dockerfile -t rfp-tools-frontend .
docker run -p 3000:3000 rfp-tools-frontend
```

---

## Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Dashboard.tsx       # Main dashboard
│   │   ├── Analyzer.tsx        # RFP analysis
│   │   ├── Evaluator.tsx       # Response evaluation
│   │   ├── Products.tsx        # Product management
│   │   └── BatchProcessor.tsx  # Batch operations
│   ├── components/
│   │   ├── Navigation.tsx      # Top navigation
│   │   ├── Card.tsx            # Card layout
│   │   ├── Button.tsx          # Button component
│   │   └── Badge.tsx           # Badge component
│   ├── services/
│   │   └── api.ts              # API client
│   ├── App.tsx                 # Root component
│   ├── main.tsx                # Entry point
│   └── index.css               # Global styles
├── index.html                  # HTML template
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── tailwind.config.js          # Tailwind config
└── vite.config.ts              # Vite config
```

---

## Features

### 🏠 Dashboard
- System status overview
- API metrics and statistics
- Knowledge base status
- System health visualization
- Real-time monitoring

### 📋 Analyzer
- RFP document input (text or file)
- Multi-agent toggle
- Response generation
- Response preview
- Download functionality

### ⭐ Evaluator
- RFP and response input
- Quality scoring
- Metric visualization
- Strengths/weaknesses analysis
- Improvement recommendations

### 🛍️ Products
- Product listing
- Product search
- Add new products
- Product details viewing
- Inline editing (future)

### 📦 Batch Processor
- Start batch jobs
- Monitor progress
- Track job status
- View completion

---

## API Integration

The frontend connects to the backend API at:
- Development: `http://localhost:8000`
- Production: Set via `REACT_APP_API_URL` environment variable

### Environment Variables

Create `.env.local`:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_DEBUG=true
```

---

## Development

### Adding New Pages

```typescript
// frontend/src/pages/MyPage.tsx
import React from 'react';
import Card from '../components/Card';

function MyPage() {
  return (
    <div className="space-y-8">
      <h1>My Page</h1>
      <Card>
        <p>Content here</p>
      </Card>
    </div>
  );
}

export default MyPage;
```

Then add to `App.tsx`:

```typescript
import MyPage from './pages/MyPage';

<Route path="/mypage" element={<MyPage />} />
```

### Adding New Components

```typescript
// frontend/src/components/MyComponent.tsx
import React from 'react';

interface MyComponentProps {
  title: string;
}

function MyComponent({ title }: MyComponentProps) {
  return <div>{title}</div>;
}

export default MyComponent;
```

### Styling with Tailwind

The project uses Tailwind CSS with dark mode support:

```typescript
// Light mode
<div className="bg-white text-gray-900">

// Dark mode
<div className="dark:bg-gray-800 dark:text-white">
```

---

## API Endpoints Used

### Health & Status
- `GET /health` - System health
- `GET /status` - System status
- `GET /metrics` - API metrics

### Analysis
- `POST /analyze` - Analyze RFP
- `POST /analyze/file` - Upload RFP file

### Evaluation
- `POST /evaluate` - Evaluate response

### Products
- `GET /products` - List products
- `POST /products/add` - Add product
- `POST /products/search` - Search products

### Batch
- `POST /batch/analyze` - Start batch job
- `GET /batch/status/{job_id}` - Check status

---

## Deployment

### Docker Compose

```bash
# Automatically builds frontend when you run:
docker-compose up
```

### Vercel

```bash
vercel deploy
```

### Netlify

```bash
netlify deploy --prod --dir=dist
```

### GitHub Pages

Update `vite.config.ts`:
```typescript
export default {
  base: '/rfp-tools/',
}
```

Then:
```bash
npm run build
```

---

## Performance Tips

1. **Code Splitting**: React Router automatically splits routes
2. **Lazy Loading**: Components are loaded on demand
3. **Image Optimization**: Compress images before use
4. **API Caching**: React Query caches API responses
5. **Production Build**: Run `npm run build` for optimized bundle

---

## Troubleshooting

### API Connection Issues

Check that backend is running:
```bash
curl http://localhost:8000/health
```

### Dark Mode Not Working

Ensure Tailwind config includes dark mode:
```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  // ...
}
```

### Build Fails

```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

---

## Future Enhancements

- [ ] WebSocket for real-time updates
- [ ] User authentication
- [ ] Response history/versioning
- [ ] Custom themes
- [ ] Export to PDF
- [ ] Email integration
- [ ] Slack notifications
- [ ] Advanced filtering
- [ ] Multi-language support
- [ ] Mobile app (React Native)

---

## Support

For frontend issues:
1. Check browser console (F12)
2. Verify backend is running
3. Check network tab for API errors
4. Review React Query DevTools: http://localhost:5173/#/

---

## License

MIT
