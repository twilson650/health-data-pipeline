import express from 'express';
import cors from 'cors';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'clinical-measures' });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    service: 'clinical-measures',
    version: '0.1.0',
    description: 'FHIR clinical quality measures service'
  });
});

// Example endpoint for evaluating measures
app.post('/api/measures/evaluate', (req, res) => {
  // TODO: Implement measure evaluation logic
  res.json({
    message: 'Measure evaluation endpoint',
    body: req.body
  });
});

// Get available measures
app.get('/api/measures', (req, res) => {
  res.json({
    measures: [
      {
        id: 'monitor_depression_symptoms',
        name: 'Monitor Depression Symptoms',
        version: '6.2.012'
      }
    ]
  });
});

// Get specific measure
app.get('/api/measures/:measureId', (req, res) => {
  const { measureId } = req.params;
  res.json({
    id: measureId,
    message: 'Measure details endpoint',
    // TODO: Return measure details
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal server error',
    message: err.message
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    path: req.path
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Clinical Measures service listening on port ${PORT}`);
});

