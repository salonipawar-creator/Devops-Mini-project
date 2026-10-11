# Demonstration Guide

Academic demonstration only. Not intended for medical diagnosis or treatment. Results must not be used as a substitute for professional medical testing.

## 5-10 Minute Flow

1. Introduce the problem: reagent strips are interpreted by color comparison.
2. Explain that this project measures colors; it does not diagnose disease.
3. Show `config/color_reference.json` and the configurable ten-pad demo layout.
4. Start the system:

```bash
docker compose up --build
```

5. Show containers:

```bash
docker compose ps
```

6. Open `http://localhost:5173`.
7. Upload `sample_data/synthetic_demo_strip.png`.
8. Click Analyze Image.
9. Show the image preview and red pad bounding boxes.
10. Show strip quality, layout, and pad count.
11. Explain RGB, HSV, and CIE Lab values in the result table.
12. Explain reference-color matching using Lab distance.
13. Explain the Random Forest result and confidence as a synthetic academic ML assist.
14. Open `http://localhost:8088/api/results` (or configured API Gateway port) to show stored analyses.
15. Show MongoDB container logs or query the database if desired.
16. Show service health endpoints:

```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8088/health
```

## Microservice Failure Demo

Stop the AI service:

```bash
docker compose stop ai-service
```

Upload the demo image again. The gateway should still complete the analysis using reference-color classification and show a meaningful ML warning instead of crashing.

Restart it:

```bash
docker compose start ai-service
```

Run another analysis and confirm ML predictions return.

## Replace Demo Image

The included `sample_data/synthetic_demo_strip.png` is synthetic and labelled. To test with a real strip photo, place a PNG/JPEG in `sample_data/`, ensure it follows the configured layout, and upload it through the dashboard. Real work requires standardized lighting, calibrated imaging, manufacturer-specific charts, clinically validated datasets, and regulatory review.
