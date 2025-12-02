# Clinical Measures Service

A Node.js REST API service for evaluating FHIR clinical quality measures using CQL (Clinical Quality Language).

## Development

### Prerequisites
- Node.js 18 or higher
- npm

### Setup
```bash
npm install
```

### Run
```bash
npm start
```

For development with auto-reload:
```bash
npm run dev
```

### API Endpoints

- `GET /health` - Health check
- `GET /` - Service information
- `GET /api/measures` - List available measures
- `GET /api/measures/:measureId` - Get measure details
- `POST /api/measures/evaluate` - Evaluate a measure

## Docker

Build and run:
```bash
docker build -t clinical-measures .
docker run -p 3000:3000 clinical-measures
```

