const express = require('express');
const cors = require('cors');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');

const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 8 * 1024 * 1024 } });
const app = express();
app.use(cors());
app.use(express.json({ limit: '2mb' }));

const services = {
  image: process.env.IMAGE_SERVICE_URL || 'http://localhost:8000',
  colorimetry: process.env.COLORIMETRY_SERVICE_URL || 'http://localhost:8001',
  ai: process.env.AI_SERVICE_URL || 'http://localhost:8002',
  result: process.env.RESULT_SERVICE_URL || 'http://localhost:8003'
};

const disclaimer = 'Academic demonstration only. Not intended for medical diagnosis or treatment. Results must not be used as a substitute for professional medical testing.';

function errorPayload(message, status = 502, details = undefined) {
  return { status, body: { error: message, details, disclaimer } };
}

async function postImage(url, file, extraFields = {}) {
  const form = new FormData();
  form.append('file', file.buffer, { filename: file.originalname, contentType: file.mimetype });
  Object.entries(extraFields).forEach(([key, value]) => form.append(key, value));
  return axios.post(url, form, { headers: form.getHeaders(), timeout: 15000 });
}

function mergeResults(measurements, predictions) {
  return measurements.map((measurement) => {
    const prediction = predictions.find((item) => item.parameter === measurement.parameter);
    const confidence = prediction ? prediction.confidence : 0;
    return {
      parameter: measurement.parameter,
      estimated_result: prediction && confidence >= 0.35 ? prediction.prediction : measurement.reference_match,
      confidence,
      reference_match: measurement.reference_match,
      color_distance: measurement.color_distance,
      ml_available: Boolean(prediction),
      note: prediction ? prediction.explanation : 'ML service unavailable; reference-color match used.'
    };
  });
}

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'api-gateway', services });
});

app.post('/api/analyze', upload.single('image'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'Upload an image file using field name image.', disclaimer });
  }
  try {
    console.log('analysis request received');
    const imageResponse = await postImage(`${services.image}/process-image`, req.file);
    const pads = imageResponse.data.pads;
    const colorResponse = await postImage(`${services.colorimetry}/analyze-colors`, req.file, {
      pads_json: JSON.stringify(pads)
    });
    const measurements = colorResponse.data.measurements;
    let predictions = [];
    let mlWarning = null;
    try {
      const mlResponse = await axios.post(`${services.ai}/predict`, measurements, { timeout: 10000 });
      predictions = mlResponse.data.predictions;
    } catch (error) {
      mlWarning = 'AI/ML service unavailable. Reference-color classification was used.';
      console.error('ML service failure', error.message);
    }
    const finalResults = mergeResults(measurements, predictions);
    const analysis = {
      image_metadata: {
        filename: req.file.originalname,
        mime_type: req.file.mimetype,
        size_bytes: req.file.size,
        quality: imageResponse.data.quality,
        layout: imageResponse.data.layout
      },
      detected_pads: pads,
      measurements,
      ml_predictions: predictions,
      final_results: finalResults,
      disclaimer
    };
    const saved = await axios.post(`${services.result}/results`, analysis, { timeout: 10000 });
    res.json({ ...saved.data, strip_detection: imageResponse.data, colorimetry_method: colorResponse.data.method, ml_warning: mlWarning });
  } catch (error) {
    const status = error.response?.status || 502;
    const details = error.response?.data || error.message;
    console.error('analysis failed', details);
    const payload = errorPayload('Analysis failed. Check image quality and service health.', status, details);
    res.status(payload.status).json(payload.body);
  }
});

app.get('/api/results', async (req, res) => {
  try {
    const response = await axios.get(`${services.result}/results`, { timeout: 10000 });
    res.json(response.data);
  } catch (error) {
    res.status(502).json(errorPayload('Could not retrieve results.', 502, error.message).body);
  }
});

app.get('/api/results/:id', async (req, res) => {
  try {
    const response = await axios.get(`${services.result}/results/${req.params.id}`, { timeout: 10000 });
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 502).json(errorPayload('Could not retrieve result.', error.response?.status || 502, error.message).body);
  }
});

if (require.main === module) {
  const port = process.env.PORT || 8080;
  app.listen(port, () => console.log(`api-gateway listening on ${port}`));
}

module.exports = app;
