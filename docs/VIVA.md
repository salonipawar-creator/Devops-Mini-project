# Viva Questions and Answers

1. What is the project about?  
It is an academic prototype that analyzes urine strip pad colors using image processing, colorimetry, microservices, and demo ML.

2. Is it a medical diagnostic product?  
No. It is only an academic demonstration and must not be used for diagnosis or treatment.

3. What is colorimetry?  
Colorimetry is measuring and comparing colors quantitatively.

4. Why use RGB?  
RGB is the direct red, green, and blue channel representation captured from images.

5. Why use HSV?  
HSV separates hue from saturation and brightness, making color families easier to interpret.

6. Why use CIE Lab?  
Lab is more perceptually uniform, so numeric distance better approximates visible color difference.

7. What is Delta E?  
Delta E is a color distance measure in a perceptual color space. This prototype uses a simple Euclidean Lab distance.

8. Why use median color?  
Median central crop color reduces the effect of pad edges, glare, shadows, and outlier pixels.

9. How is the strip detected?  
The image service finds colored vertical regions and falls back to a configured demo layout for controlled samples.

10. Why is the layout configurable?  
Different strip brands have different pad orders and positions, so the layout must be replaceable.

11. What happens with a blurry image?  
The image service rejects it using a Laplacian blur score.

12. What happens with poor brightness?  
Images that are too dark or too bright are rejected to avoid false confidence.

13. Which parameters are included?  
Glucose, protein, pH, ketones, blood, leukocytes, nitrite, specific gravity, bilirubin, and urobilinogen.

14. Are the reference colors clinical?  
No. They are demonstration calibration values only.

15. What ML model is used?  
A Random Forest classifier.

16. Why Random Forest?  
It is simple, explainable enough for a college project, handles nonlinear boundaries, and gives class probabilities.

17. What data trains the model?  
Synthetic demonstration data generated from configured reference colors.

18. Does the service train on every request?  
No. `ml/train.py` trains separately and the AI service loads the saved model.

19. What is the primary classification method?  
Reference-color matching is primary; ML is only an academic assist.

20. What is a microservice?  
A small independent service with one responsibility, communicating through APIs.

21. Why use an API Gateway?  
It gives the frontend one entry point and coordinates calls to backend services.

22. What is Docker used for?  
Docker packages each service with its runtime and dependencies.

23. What is Docker Compose used for?  
Compose starts all services, networks, ports, and MongoDB together.

24. Why not hardcode Docker hostnames?  
Environment variables make the services configurable for local, Docker, and CI environments.

25. What is MongoDB storing?  
Complete analysis records with metadata, pad coordinates, color values, predictions, and final demo results.

26. Does the app store personal data?  
No unnecessary personal information is stored.

27. What is REST API?  
REST exposes resources through HTTP methods such as GET and POST.

28. What is a health check?  
An endpoint or command that reports whether a service is available.

29. How does service failure handling work?  
The gateway catches service errors and returns meaningful messages. If AI fails, reference classification still works.

30. What does CI/CD do here?  
GitHub Actions installs dependencies, runs tests, builds the frontend, and builds Docker images.

31. What is the difference between monolithic and microservices architecture?  
A monolith puts all modules in one deployable app; microservices split responsibilities into independently deployable services.

32. What is the biggest limitation?  
The system lacks clinical validation, standardized capture, and manufacturer-specific calibration.

33. What future improvements are possible?  
Camera calibration, multiple strip layouts, timed captures, validated datasets, and regulatory workflows.

34. How is explainability shown?  
The result table shows measured colors, closest reference match, distance, ML prediction, and confidence.

35. Why is the disclaimer prominent?  
To prevent users from interpreting demonstration output as medical advice.
