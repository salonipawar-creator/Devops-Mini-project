import os
import sys
from reportlab.lib.pagesizes import A3
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas

def draw_poster():
    pdf_path = "DevOps_Mini_Project_Poster.pdf"
    width, height = A3 # 841.89 x 1190.55
    c = canvas.Canvas(pdf_path, pagesize=A3)

    # Background
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.rect(0, 0, width, height, fill=True, stroke=False)

    # ------------------ TOP INSTITUTION HEADER ------------------
    top_h = 75
    c.setFillColor(colors.HexColor("#0f1e36"))
    c.rect(0, height - top_h, width, top_h, fill=True, stroke=False)

    # University & College text
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#ffffff"))
    c.drawCentredString(width / 2.0, height - 26, "Somaiya Vidyavihar University")

    c.setFont("Helvetica-Bold", 19)
    c.setFillColor(colors.HexColor("#f2c94c"))
    c.drawCentredString(width / 2.0, height - 48, "K J Somaiya School of Engineering")

    c.setFont("Helvetica", 13)
    c.setFillColor(colors.HexColor("#e2e8f0"))
    c.drawCentredString(width / 2.0, height - 66, "Department of Information Technology")

    # Left & Right Brand Badges
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor("#dc2626"))
    c.drawString(35, height - 38, "SOMAIYA")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#cbd5e1"))
    c.drawString(35, height - 54, "VIDYAVIHAR UNIVERSITY")

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#ffffff"))
    c.drawRightString(width - 35, height - 38, "Somaiya")
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#f2c94c"))
    c.drawRightString(width - 35, height - 54, "T R U S T")

    # ------------------ POSTER TITLE BOX ------------------
    title_box_top = height - top_h - 15
    title_box_h = 75
    margin_x = 30
    box_w = width - (2 * margin_x)

    c.setStrokeColor(colors.HexColor("#1e3a8a"))
    c.setLineWidth(1.5)
    c.setFillColor(colors.HexColor("#ffffff"))
    c.roundRect(margin_x, title_box_top - title_box_h, box_w, title_box_h, 6, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor("#0f1e36"))
    c.drawCentredString(width / 2.0, title_box_top - 32, "Urine Test Strip Analysis Using Colorimetry and DevOps Microservices")

    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.HexColor("#4338ca"))
    c.drawCentredString(width / 2.0, title_box_top - 58, "Course : DevOps Lab Mini Project Poster Presentation")

    # ------------------ METADATA BAR ------------------
    meta_top = title_box_top - title_box_h - 12
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#0f1e36"))
    c.drawString(margin_x + 5, meta_top - 12, "Student Name: Saloni Pawar (Roll No. ___)")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawString(margin_x + 5, meta_top - 26, "Class: Information Technology  |  Div: ___  |  Batch: ___")

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#0f1e36"))
    c.drawRightString(width - margin_x - 5, meta_top - 12, "Guide / Faculty In-charge: Dr. Seema Redekar")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawRightString(width - margin_x - 5, meta_top - 26, "Academic Year: 2026-27 | K J Somaiya School of Engineering")

    # ------------------ FOOTER ------------------
    footer_h = 28
    c.setFillColor(colors.HexColor("#0f1e36"))
    c.rect(0, 0, width, footer_h, fill=True, stroke=False)
    c.setFont("Helvetica", 9.5)
    c.setFillColor(colors.HexColor("#e2e8f0"))
    c.drawCentredString(width / 2.0, 9, "Department of Information Technology  |  K J Somaiya School of Engineering  |  Somaiya Vidyavihar University")

    # ------------------ 3-COLUMN LAYOUT SETUP ------------------
    content_top = meta_top - 38
    content_bottom = footer_h + 12

    col_gap = 14
    col_w = (box_w - (2 * col_gap)) / 3.0
    col1_x = margin_x
    col2_x = col1_x + col_w + col_gap
    col3_x = col2_x + col_w + col_gap

    styles = getSampleStyleSheet()
    bullet_style = ParagraphStyle(
        'PosterBullet',
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=10,
        firstLineIndent=-7
    )

    def draw_section_card(x, y, w, h, title, paragraphs, is_diagram=False, is_results=False):
        head_h = 20
        c.setFillColor(colors.HexColor("#1e293b"))
        c.roundRect(x, y + h - head_h, w, head_h, 3, fill=True, stroke=False)
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(colors.HexColor("#ffffff"))
        c.drawString(x + 10, y + h - 14, title)

        c.setFillColor(colors.HexColor("#ffffff"))
        c.setStrokeColor(colors.HexColor("#cbd5e1"))
        c.setLineWidth(1)
        c.roundRect(x, y, w, h - head_h, 3, fill=True, stroke=True)

        cur_y = y + h - head_h - 10
        inner_w = w - 16
        inner_x = x + 8

        if is_diagram:
            draw_architecture_diagram(inner_x, cur_y, inner_w)
            return

        if is_results:
            draw_results_box(inner_x, cur_y, inner_w)
            return

        for p_text in paragraphs:
            p = Paragraph(p_text, bullet_style)
            pw, ph = p.wrap(inner_w, h)
            cur_y -= ph
            if cur_y >= y + 5:
                p.drawOn(c, inner_x, cur_y)
            cur_y -= 4

    def draw_architecture_diagram(ix, iy, iw):
        # Layer 1: React Frontend & Client
        c.setFillColor(colors.HexColor("#e0e7ff"))
        c.setStrokeColor(colors.HexColor("#4338ca"))
        c.setLineWidth(1)
        c.roundRect(ix + 10, iy - 26, iw - 20, 24, 4, fill=True, stroke=True)
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(colors.HexColor("#312e81"))
        c.drawCentredString(ix + iw/2.0, iy - 17, "React 18 Dashboard (Vite 5)  [Port 5173]")

        c.setStrokeColor(colors.HexColor("#64748b"))
        c.setLineWidth(1.5)
        c.line(ix + iw/2.0, iy - 26, ix + iw/2.0, iy - 36)

        # Layer 2: API Gateway
        c.setFillColor(colors.HexColor("#fee2e2"))
        c.setStrokeColor(colors.HexColor("#b91c1c"))
        c.roundRect(ix + 10, iy - 62, iw - 20, 24, 4, fill=True, stroke=True)
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(colors.HexColor("#7f1d1d"))
        c.drawCentredString(ix + iw/2.0, iy - 53, "Node.js Express API Gateway  [Port 8088 / 8080]")

        c.line(ix + iw/2.0, iy - 62, ix + iw/2.0, iy - 72)
        c.line(ix + 40, iy - 72, ix + iw - 40, iy - 72)
        c.line(ix + 40, iy - 72, ix + 40, iy - 78)
        c.line(ix + iw/2.0, iy - 72, ix + iw/2.0, iy - 78)
        c.line(ix + iw - 40, iy - 72, ix + iw - 40, iy - 78)

        # Layer 3: Microservices row
        sw = (iw - 16) / 3.0
        c.setFillColor(colors.HexColor("#ecfdf5"))
        c.setStrokeColor(colors.HexColor("#059669"))
        c.roundRect(ix, iy - 118, sw, 38, 3, fill=True, stroke=True)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#065f46"))
        c.drawCentredString(ix + sw/2.0, iy - 93, "Image Service")
        c.setFont("Helvetica", 6.8)
        c.setFillColor(colors.HexColor("#047857"))
        c.drawCentredString(ix + sw/2.0, iy - 105, "OpenCV / Crop / Blur")
        c.drawCentredString(ix + sw/2.0, iy - 115, "FastAPI [8000]")

        c.setFillColor(colors.HexColor("#eff6ff"))
        c.setStrokeColor(colors.HexColor("#2563eb"))
        c.roundRect(ix + sw + 8, iy - 118, sw, 38, 3, fill=True, stroke=True)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#1e40af"))
        c.drawCentredString(ix + sw + 8 + sw/2.0, iy - 93, "Colorimetry")
        c.setFont("Helvetica", 6.8)
        c.setFillColor(colors.HexColor("#1d4ed8"))
        c.drawCentredString(ix + sw + 8 + sw/2.0, iy - 105, "RGB / Lab / Delta-E")
        c.drawCentredString(ix + sw + 8 + sw/2.0, iy - 115, "FastAPI [8001]")

        c.setFillColor(colors.HexColor("#fef3c7"))
        c.setStrokeColor(colors.HexColor("#d97706"))
        c.roundRect(ix + 2*sw + 16, iy - 118, sw, 38, 3, fill=True, stroke=True)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#92400e"))
        c.drawCentredString(ix + 2*sw + 16 + sw/2.0, iy - 93, "AI / ML Service")
        c.setFont("Helvetica", 6.8)
        c.setFillColor(colors.HexColor("#b45309"))
        c.drawCentredString(ix + 2*sw + 16 + sw/2.0, iy - 105, "Random Forest")
        c.drawCentredString(ix + 2*sw + 16 + sw/2.0, iy - 115, "FastAPI [8002]")

        # Layer 4: Result Service & MongoDB
        c.setStrokeColor(colors.HexColor("#64748b"))
        c.line(ix + sw + 8 + sw/2.0, iy - 118, ix + sw + 8 + sw/2.0, iy - 128)

        rw = (iw - 12) / 2.0
        c.setFillColor(colors.HexColor("#f1f5f9"))
        c.setStrokeColor(colors.HexColor("#475569"))
        c.roundRect(ix + 6, iy - 158, rw - 12, 28, 3, fill=True, stroke=True)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#334155"))
        c.drawCentredString(ix + 6 + (rw - 12)/2.0, iy - 142, "Result Service (FastAPI 8003)")
        c.setFont("Helvetica", 6.8)
        c.drawCentredString(ix + 6 + (rw - 12)/2.0, iy - 152, "Persistence & Queries")

        c.setFillColor(colors.HexColor("#dcfce7"))
        c.setStrokeColor(colors.HexColor("#16a34a"))
        c.roundRect(ix + rw + 6, iy - 158, rw - 12, 28, 3, fill=True, stroke=True)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#14532d"))
        c.drawCentredString(ix + rw + 6 + (rw - 12)/2.0, iy - 142, "MongoDB 7.0 [Port 27017]")
        c.setFont("Helvetica", 6.8)
        c.drawCentredString(ix + rw + 6 + (rw - 12)/2.0, iy - 152, "Analyses Collection")

        # Layer 5: DevOps Pipeline banner
        c.setFillColor(colors.HexColor("#f8fafc"))
        c.setStrokeColor(colors.HexColor("#0284c7"))
        c.setLineWidth(1)
        c.roundRect(ix, iy - 212, iw, 44, 4, fill=True, stroke=True)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#0369a1"))
        c.drawString(ix + 8, iy - 173, "DevOps CI/CD Automation Pipeline (Jenkins & GitHub Actions):")
        c.setFont("Helvetica", 7.2)
        c.setFillColor(colors.HexColor("#0f172a"))
        c.drawString(ix + 8, iy - 187, "1. Env Setup -> 2. Train ML -> 3. Python Tests -> 4. Gateway Tests ->")
        c.drawString(ix + 8, iy - 199, "5. Frontend Build -> 6. Docker Compose Build -> 7. Stack Health Deploy")
        c.setFont("Helvetica-Bold", 7.2)
        c.setFillColor(colors.HexColor("#16a34a"))
        c.drawString(ix + 8, iy - 209, "Status: 100% Automated | All 7 Stages Passed (Build #6 SUCCESS)")
        return iy - 215

    def draw_results_box(ix, iy, iw):
        c.setFont("Helvetica-Bold", 8.2)
        c.setFillColor(colors.HexColor("#0f172a"))
        c.drawString(ix, iy - 2, "Test & Build Validation Summary:")

        ty = iy - 18
        th = 15
        c.setFillColor(colors.HexColor("#e2e8f0"))
        c.rect(ix, ty, iw, th, fill=True, stroke=False)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#1e293b"))
        c.drawString(ix + 6, ty + 4, "Component / Test Suite")
        c.drawString(ix + 120, ty + 4, "Test Tool")
        c.drawRightString(ix + iw - 6, ty + 4, "Outcome")

        rows = [
            ("Python Microservices", "Pytest 8.3", "14 / 14 Passed (100%)", colors.HexColor("#16a34a")),
            ("Node.js API Gateway", "Jest 29", "3 / 3 Passed (100%)", colors.HexColor("#16a34a")),
            ("React Frontend Dashboard", "Vitest 2.1", "1 / 1 Passed (100%)", colors.HexColor("#16a34a")),
            ("Production Bundle Build", "Vite 5", "Compiled (147 kB)", colors.HexColor("#0284c7")),
            ("Multi-Container Build", "Docker Compose", "6 / 6 Images Built", colors.HexColor("#0284c7")),
            ("Jenkins Automated Pipeline", "Jenkins 2.568", "7 / 7 Stages Green (5m 57s)", colors.HexColor("#16a34a")),
            ("Fault Fallback Simulation", "Stop AI Container", "Graceful Degradation Verified", colors.HexColor("#d97706")),
        ]

        row_y = ty
        for comp, tool, outcome, col in rows:
            row_y -= 13
            c.setFont("Helvetica", 7.2)
            c.setFillColor(colors.HexColor("#334155"))
            c.drawString(ix + 6, row_y + 3, comp)
            c.drawString(ix + 120, row_y + 3, tool)
            c.setFont("Helvetica-Bold", 7.2)
            c.setFillColor(col)
            c.drawRightString(ix + iw - 6, row_y + 3, outcome)
            c.setStrokeColor(colors.HexColor("#f1f5f9"))
            c.setLineWidth(0.5)
            c.line(ix, row_y, ix + iw, row_y)

        cy = row_y - 8
        ch = 44
        c.setFillColor(colors.HexColor("#fef3c7"))
        c.setStrokeColor(colors.HexColor("#f59e0b"))
        c.roundRect(ix, cy - ch, iw, ch, 3, fill=True, stroke=True)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#92400e"))
        c.drawString(ix + 6, cy - 11, "Demonstrated Microservices Fault Resilience:")
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#78350f"))
        c.drawString(ix + 6, cy - 23, "- Executed 'docker compose stop ai-service' during live strip analysis.")
        c.drawString(ix + 6, cy - 33, "- API Gateway automatically fell back to reference color matching.")
        c.drawString(ix + 6, cy - 42, "- User receives analysis + warning; zero crashes; MongoDB retains record.")
        return cy - ch - 4

    # Column 1
    c1_h1 = 175
    c1_h2 = 140
    c1_h3 = 190
    gap = 12

    y1_1 = content_top - c1_h1
    draw_section_card(
        col1_x, y1_1, col_w, c1_h1,
        "1. INTRODUCTION",
        [
            "<b>• Clinical Reagent Strips:</b> Multistix / 10-SG urine test strips provide point-of-care screening for 10 key biochemical parameters (Glucose, Protein, pH, Ketones, etc.).",
            "<b>• Human Subjectivity Challenge:</b> Traditional visual inspection against printed color charts is compromised by ambient lighting variations, visual perception bias, and delayed readings.",
            "<b>• Engineering Solution:</b> An automated, containerized microservices platform combining computer vision, quantitative CIE Lab colorimetry, and Machine Learning.",
            "<b>• DevOps Foundation:</b> Incorporates continuous integration, multi-stage Docker packaging, and automated Jenkins pipelines for reproducible deployment."
        ]
    )

    y1_2 = y1_1 - gap - c1_h2
    draw_section_card(
        col1_x, y1_2, col_w, c1_h2,
        "2. PROBLEM STATEMENT",
        [
            "<b>• Problem:</b> Manual color comparison across 10 reagent pads simultaneously is error-prone, lacks audit trails, and suffers from colorimetric inaccuracy under non-standard light sources.",
            "<b>• Architectural Dilemma:</b> Monolithic health apps lack fault resilience; a single ML or vision failure crashes the entire clinical dashboard.",
            "<b>• Scope & Boundaries:</b> Focuses on automated processing of 10-pad vertical strips with modular calibration. Strictly an academic prototype for DevOps demonstration, not for medical diagnosis."
        ]
    )

    y1_3 = y1_2 - gap - c1_h3
    draw_section_card(
        col1_x, y1_3, col_w, c1_h3,
        "3. OBJECTIVES",
        [
            "<b>• Computer Vision Pipeline:</b> Detect urine strips, validate image quality (Laplacian blur & brightness thresholds), and extract precise pad coordinates.",
            "<b>• Perceptual Colorimetry:</b> Sample central median pad pixels to eliminate edge glare; convert RGB to HSV and CIE Lab for Delta-E distance matching.",
            "<b>• Explainable AI Assist:</b> Train an offline Random Forest classifier on synthetic reference swatches to output estimated categories and confidence scores.",
            "<b>• Microservice Architecture:</b> Decouple image processing, colorimetry, AI, and storage into independent FastAPI containers behind an Express Gateway.",
            "<b>• DevOps Automation:</b> Implement automated testing, Docker Compose orchestration, and an end-to-end 7-stage Jenkins CI/CD pipeline."
        ]
    )

    y1_4 = content_bottom
    c1_h4 = y1_3 - gap - y1_4
    draw_section_card(
        col1_x, y1_4, col_w, c1_h4,
        "4. LITERATURE REVIEW",
        [
            "<b>• Shen et al. (2012):</b> Developed smartphone-based colorimetric detection for biochemical test strips; proved feasibility but highlighted sensitivity to variable lighting conditions.",
            "<b>• Yetisen et al. (2014):</b> Evaluated color spaces for medical diagnostics; demonstrated that perceptual CIE Lab color space drastically minimizes visual variance compared to RGB.",
            "<b>• Jalal et al. (2017):</b> Built mobile paper-based diagnostic readers; recommended central crop median filtering to prevent pad border reagent leakage artifacts.",
            "<b>• Newman (2021) - Microservices:</b> Established architectural principles for distributed systems; recommended API gateways for request aggregation and circuit breaking.",
            "<b>• Research Gap Identified:</b> Existing point-of-care projects are tightly-coupled monoliths lacking enterprise DevOps workflows, containerized isolation, and automated failure fallback mechanisms."
        ]
    )

    # Column 2
    c2_h1 = 280
    c2_h2 = 230
    y2_1 = content_top - c2_h1
    draw_section_card(
        col2_x, y2_1, col_w, c2_h1,
        "5. METHODOLOGY / SYSTEM DESIGN",
        [],
        is_diagram=True
    )

    y2_2 = y2_1 - gap - c2_h2
    draw_section_card(
        col2_x, y2_2, col_w, c2_h2,
        "6. IMPLEMENTATION DETAILS",
        [
            "<b>• Frontend Dashboard:</b> React 18 with Vite 5, interactive pad overlay boxes, real-time RGB/HSV/Lab colorimetric tables, and MongoDB historical query cards.",
            "<b>• API Gateway:</b> Node.js Express server orchestrating multipart image forwarding, service aggregation, and graceful error recovery.",
            "<b>• Image Service (CV):</b> OpenCV-based Laplacian variance calculation (rejects blur < 80); brightness check (35-245); bounding box generation for 10 vertical pads.",
            "<b>• Colorimetry Service:</b> Extracts central 50% median color; converts RGB -> HSV -> CIE Lab; computes Euclidean Delta-E distance to reference chart colors.",
            "<b>• AI/ML Service:</b> Scikit-Learn Random Forest (100 trees, 6 features [R,G,B,L,a,b]) loaded from joblib; outputs class probabilities.",
            "<b>• Result Service & DB:</b> FastAPI CRUD service connected to MongoDB 7.0 storing complete analysis documents without collecting personal patient data."
        ]
    )

    y2_3 = content_bottom
    c2_h3 = y2_2 - gap - y2_3
    draw_section_card(
        col2_x, y2_3, col_w, c2_h3,
        "7. RESULTS & DISCUSSION",
        [],
        is_results=True
    )

    # Column 3
    c3_h1 = 150
    c3_h2 = 140
    c3_h3 = 170
    c3_h4 = 175
    y3_1 = content_top - c3_h1
    draw_section_card(
        col3_x, y3_1, col_w, c3_h1,
        "8. KEY FINDINGS",
        [
            "<b>• CIE Lab Perceptual Superiority:</b> Euclidean distance in CIE Lab space correctly identified demonstration color swatches with minimal error (Delta-E < 3.3).",
            "<b>• Median Crop Noise Immunity:</b> 50% central median cropping successfully filtered out border shadows, reflections, and pad margin bleeding.",
            "<b>• Fault Resilience Confirmed:</b> Disabling the AI service triggered instant gateway fallback to reference-matching with 0% downtime and explicit UI warnings.",
            "<b>• Jenkins CI/CD Speed:</b> End-to-end automated testing, Docker building, and deployment succeeded in 5m 57s across 7 isolated stages."
        ]
    )

    y3_2 = y3_1 - gap - c3_h2
    draw_section_card(
        col3_x, y3_2, col_w, c3_h2,
        "9. CONCLUSION",
        [
            "<b>• Complete DevOps Solution:</b> Engineered an end-to-end multi-language microservices application successfully bridging Computer Vision, Colorimetry, and DevOps.",
            "<b>• High Reliability & Maintainability:</b> Independent Docker containers ensure individual services can be scaled, updated, or restarted without impacting others.",
            "<b>• Automated Pipeline Success:</b> Integrated dual CI/CD pipelines (GitHub Actions + Jenkins) that enforce 100% test passing before container image publication.",
            "<b>• Academic Impact:</b> Demonstrates how complex medical-instrument analysis workflows can be prototyped using modern open-source software engineering practices."
        ]
    )

    y3_3 = y3_2 - gap - c3_h3
    draw_section_card(
        col3_x, y3_3, col_w, c3_h3,
        "10. FUTURE SCOPE",
        [
            "<b>• Standardized Color Calibration:</b> Integrate 24-color Macbeth/ColorChecker target boards in strip photos for automatic white-balance correction.",
            "<b>• Multi-Brand Layout Recognition:</b> Use Deep Learning (YOLOv8) for dynamic multi-manufacturer strip detection (Siemens, Roche, Mission).",
            "<b>• Time-Resolved Kinetic Capture:</b> Implement mobile camera timer alerts to measure specific reagent pad reactions at 30s, 60s, and 120s intervals.",
            "<b>• Kubernetes & Cloud Native:</b> Transition Docker Compose to Kubernetes manifests with Helm charts and Horizontal Pod Autoscaling (HPA)."
        ]
    )

    y3_4 = y3_3 - gap - c3_h4
    draw_section_card(
        col3_x, y3_4, col_w, c3_h4,
        "11. REFERENCES",
        [
            "<b>[1]</b> Shen, L., et al., 'Point-of-care colorimetric diagnostics using smartphone cameras,' <i>Lab on a Chip</i>, 12(15), 2012.",
            "<b>[2]</b> Yetisen, A. K., et al., 'Smartphone-based colorimetric algorithms,' <i>Biosensors and Bioelectronics</i>, 54, 2014.",
            "<b>[3]</b> Newman, S., <i>Building Microservices: Designing Fine-Grained Systems</i>, 2nd ed., O'Reilly Media, 2021.",
            "<b>[4]</b> Smart, J. F., <i>Jenkins: The Definitive Guide</i>, O'Reilly Media, 2011.",
            "<b>[5]</b> International Commission on Illumination, 'Colorimetry Technical Report CIE 15:2004,' 2004."
        ]
    )

    y3_5 = content_bottom
    c3_h5 = y3_4 - gap - y3_5
    draw_section_card(
        col3_x, y3_5, col_w, c3_h5,
        "ACKNOWLEDGEMENT",
        [
            "<b>• Institutional Guidance:</b> Sincere gratitude to <b>Dr. Seema Redekar</b> for her continuous mentorship, invaluable insights, and technical direction.",
            "<b>• Department of Information Technology:</b> Thanks to <b>K J Somaiya School of Engineering</b> and <b>Somaiya Vidyavihar University</b> for providing the laboratory facilities and academic environment."
        ]
    )

    c.save()
    print("Successfully generated:", pdf_path)

if __name__ == "__main__":
    draw_poster()
