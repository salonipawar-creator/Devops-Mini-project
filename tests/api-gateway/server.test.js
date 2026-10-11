process.env.IMAGE_SERVICE_URL = 'http://image.test';
process.env.COLORIMETRY_SERVICE_URL = 'http://color.test';
process.env.AI_SERVICE_URL = 'http://ai.test';
process.env.RESULT_SERVICE_URL = 'http://result.test';

const request = require('../../api-gateway/node_modules/supertest');
const nock = require('../../api-gateway/node_modules/nock');
const app = require('../../api-gateway/server');

describe('api gateway', () => {
  afterEach(() => nock.cleanAll());

  test('health endpoint', async () => {
    const response = await request(app).get('/health');
    expect(response.status).toBe(200);
    expect(response.body.service).toBe('api-gateway');
  });

  test('successful analysis', async () => {
    nock('http://image.test').post('/process-image').reply(200, {
      quality: { quality: 'good' },
      layout: 'demo',
      pads: [{ parameter: 'glucose', x: 1, y: 1, width: 10, height: 10 }]
    });
    nock('http://color.test').post('/analyze-colors').reply(200, {
      method: 'median',
      measurements: [{ parameter: 'glucose', rgb: { r: 1, g: 2, b: 3 }, hsv: { h: 1, s: 2, v: 3 }, lab: { l: 1, a: 2, b: 3 }, reference_match: 'negative', color_distance: 1 }]
    });
    nock('http://ai.test').post('/predict').reply(200, {
      predictions: [{ parameter: 'glucose', prediction: 'negative', confidence: 0.9, explanation: 'demo' }]
    });
    nock('http://result.test').post('/results').reply(200, { id: 'abc', final_results: [] });
    const response = await request(app).post('/api/analyze').attach('image', Buffer.from('fake'), 'demo.png');
    expect(response.status).toBe(200);
    expect(response.body.id).toBe('abc');
  });

  test('service failure is meaningful', async () => {
    nock('http://image.test').post('/process-image').reply(503, { detail: 'down' });
    const response = await request(app).post('/api/analyze').attach('image', Buffer.from('fake'), 'demo.png');
    expect(response.status).toBe(503);
    expect(response.body.error).toContain('Analysis failed');
  });
});
