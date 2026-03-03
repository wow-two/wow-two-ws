# Air Pollutant Timeline Map — Research & Feasibility Analysis

*Last updated: 2026-02-24 10:30 PM*

## 1. Concept Overview

**Idea:** Build a web-based timeline map that uses AI to detect and visualize the movement of air pollutants from satellite/space imagery over time.

**Core value proposition:** Transform raw satellite atmospheric data into an animated, interactive map showing how pollutant plumes (NO₂, SO₂, CO, PM2.5, aerosols) form, move, and dissipate — with AI-powered detection and prediction.

### Feasibility Verdict: ✅ Highly Feasible

The field is mature enough — Sentinel-5P has been producing daily global atmospheric data since 2018, Google Earth Engine provides free cloud processing, and proven deep learning architectures (U-Net, CNN-LSTM) exist for this exact use case. Multiple research papers have demonstrated working prototypes.

---

## 2. Data Sources

### Tier 1 — Satellite (Primary)

| Source | Pollutants | Resolution | Frequency | Cost |
|---|---|---|---|---|
| **Sentinel-5P TROPOMI** | NO₂, SO₂, CO, O₃, CH₄, HCHO, aerosols | 7×3.5 km | Daily | Free |
| **NASA TEMPO** | NO₂, O₃, HCHO | ~2 km | Hourly (North America) | Free |
| **GEMS (South Korea)** | NO₂, SO₂, O₃, HCHO, aerosols | 3.5×8 km | Hourly (Asia) | Free |
| **MODIS (Terra/Aqua)** | AOD (Aerosol Optical Depth) | 3–10 km | 1–2x daily | Free |
| **Sentinel-4** (upcoming) | NO₂, SO₂, O₃ | 8 km | Hourly (Europe) | Free |

**Best starting point:** Sentinel-5P via Google Earth Engine — richest pollutant set, global coverage, already in GEE catalog.

### Tier 2 — Wind & Transport

| Source | Data | Resolution | Access |
|---|---|---|---|
| **NASA MERRA-2** | Wind fields (u, v at multiple levels), aerosol reanalysis | 0.5°×0.625°, hourly | GES DISC API, GEE |
| **NOAA HYSPLIT** | Air mass trajectory modeling | Configurable | Web API / standalone |
| **ERA5 (ECMWF)** | Wind, pressure, temperature | 0.25°, hourly | Copernicus CDS API |
| **GFS (NOAA)** | Wind forecast | 0.25°, 6-hourly | Free API |

**Key insight:** Combining satellite pollutant concentrations with wind field data (MERRA-2/ERA5) enables trajectory modeling — predicting *where* pollutants will move.

### Tier 3 — Ground Truth & Validation

| Source | Coverage | API |
|---|---|---|
| **OpenAQ** | Global, 300+ cities | Free (300 calls/5 min) |
| **OpenWeatherMap Air Pollution** | Global | Free (1M calls/month) |
| **AirNow (US EPA)** | USA | Free |
| **Open-Meteo** | Global forecast | Free (non-commercial) |
| **AQICN** | 100+ countries | Free |

### Data Pipeline Architecture

```
Sentinel-5P (TROPOMI) ──┐
MODIS AOD ──────────────┤──→ GEE / Cloud Processing ──→ Gridded pollutant maps
TEMPO / GEMS ───────────┘                                      │
                                                                ▼
MERRA-2 / ERA5 wind ──→ Trajectory Engine ──→ Movement vectors overlay
                                                                │
OpenAQ / AirNow ──→ Ground validation ──→ Calibration layer    │
                                                                ▼
                                                    Timeline Map Frontend
```

---

## 3. Mapping & Overlay Architecture

### Recommended Stack

| Layer | Technology | Why |
|---|---|---|
| **Base map** | MapLibre GL JS | Open-source, WebGL, vector tiles, free |
| **Data overlays** | deck.gl (HeatmapLayer, GridLayer) | GPU-accelerated, handles large datasets |
| **Timeline control** | Custom slider + deck.gl animation | Frame-by-frame pollutant movement |
| **Alternative** | Leaflet + heatmap plugin | Simpler, good for MVP |

### Overlay Types

1. **Concentration heatmap** — Color-coded pollutant density per grid cell (deck.gl HeatmapLayer)
2. **Wind vector field** — Arrows showing air mass direction/speed (deck.gl IconLayer or custom WebGL)
3. **Trajectory lines** — HYSPLIT-derived paths showing pollutant transport routes
4. **Point markers** — Ground station readings for validation
5. **Plume contours** — AI-detected plume boundaries as GeoJSON polygons

### Timeline Animation Approach

```
For each time step (e.g., hourly or daily):
  1. Load pre-computed pollutant grid (GeoJSON/GeoTIFF → tiles)
  2. Load wind vectors for same timestep
  3. Render heatmap overlay + wind arrows
  4. Interpolate between frames for smooth animation
  5. User controls: play/pause, speed, date picker, pollutant selector
```

### Map Tile Strategy

- **Pre-rendered tiles** (Cloud Optimized GeoTIFF → raster tiles via TiTiler) for historical data
- **Dynamic rendering** (deck.gl from GeoJSON API) for recent/real-time data
- **Vector tiles** (Mapbox Vector Tiles) for infrastructure/boundary context

---

## 4. AI/ML Models for Pollutant Detection

### Task Breakdown

| Task | Model Architecture | Maturity |
|---|---|---|
| **Pollutant concentration estimation** from satellite imagery | CNN, U-Net, AQNet (multimodal) | High — production-ready |
| **Spatial downscaling** (7km → 1km resolution) | U-Net, Super-Resolution CNNs | High — ESA challenge winner |
| **Plume detection & segmentation** | U-Net, DeepLabV3+, SAM 2 | Medium-High |
| **Temporal prediction** (where will plume move) | LSTM, ConvLSTM, Transformer | Medium |
| **Source attribution** (which factory/area caused it) | CNN + spectral indices (NDVI, AOD, LST) | Medium |
| **Anomaly detection** (unusual pollution events) | Autoencoders, Isolation Forest | Medium |

### Frontier Models Applicable

| Model | Type | Use Case |
|---|---|---|
| **AQNet** | Multimodal (satellite + ground + metadata) | End-to-end air quality prediction |
| **U-Net** | Segmentation | Plume boundary detection, downscaling |
| **DeepLabV3+** | Semantic segmentation | Land use classification affecting pollution |
| **SAM 2 (Meta)** | Foundation model, zero-shot segmentation | Plume segmentation without training |
| **ConvLSTM** | Spatiotemporal | Predicting pollutant movement over time |
| **DINOv2** | Self-supervised vision backbone | Feature extraction from satellite imagery |
| **RF-DETR** | Object detection | Detecting emission sources in aerial imagery |
| **MobileSAM** | Lightweight segmentation | Edge/real-time plume detection |

### Recommended Model Pipeline

```
Stage 1: Feature Extraction
  Satellite image → DINOv2 / ResNet backbone → Feature maps

Stage 2: Pollutant Detection
  Feature maps + spectral bands → U-Net → Concentration grid + plume masks

Stage 3: Temporal Modeling
  Sequence of concentration grids → ConvLSTM → Next-frame prediction

Stage 4: Trajectory Fusion
  AI prediction + HYSPLIT/wind data → Fused movement forecast
```

---

## 5. Cloud vs Local Models — The Real Trade-off

### Your Intuition Check

> "Local models lack reasoning level of cloud models — is it the same for image detection?"

**Short answer: No — for image segmentation/detection, fine-tuned local models *outperform* cloud general-purpose models.** This is the opposite of the LLM reasoning domain.

### Why Image Detection Differs from LLM Reasoning

| Dimension | LLM Reasoning | Image Detection/Segmentation |
|---|---|---|
| **Task nature** | Open-ended, requires world knowledge | Narrow, well-defined spatial patterns |
| **Cloud advantage** | Massive parameter count → better reasoning | Generic features, not domain-optimized |
| **Local advantage** | Limited by model size | Fine-tuned on domain data → learns exact patterns |
| **Data specificity** | General text works | Satellite imagery is VERY different from natural photos |
| **Benchmark reality** | Cloud models dominate | Fine-tuned DeepLabV3+ hits 82-92% on satellite benchmarks |

### Detailed Comparison

| Approach | Pros | Cons | Best For |
|---|---|---|---|
| **Cloud General (GPT-4V, Claude Vision, Gemini)** | Zero-shot, no training, reasoning about what's in image | Not trained on satellite spectral bands, can't process raw .nc/.tif, expensive per-image | Quick prototyping, natural language queries about imagery |
| **Cloud Specialized (Google Vertex AI, AWS SageMaker)** | Scalable, managed training, GPU access | Cost at scale, vendor lock-in | Training custom models without own hardware |
| **Fine-tuned Local (U-Net, DeepLabV3+, HRNet)** | Highest accuracy on domain data, full control, one-time training cost | Needs labeled data, training expertise | Production pollutant detection pipeline |
| **Foundation + Fine-tune (SAM 2, DINOv2)** | Pre-trained features + domain adaptation, less labeled data needed | Still needs some fine-tuning, larger models | Best of both worlds |
| **Hybrid Cloud-Edge** | Real-time edge inference + cloud precision | Architecture complexity | Operational monitoring systems |

### Recommendation for This Project

```
Phase 1 (MVP): Cloud-hosted inference
  - Use Google Earth Engine for data processing (free for research)
  - Deploy fine-tuned U-Net on Cloud Run / Vertex AI
  - Reason: Skip hardware investment, validate concept

Phase 2 (Scale): Hybrid
  - Train specialized models on satellite data
  - Host on cloud with auto-scaling
  - Cache/pre-compute historical analysis

Phase 3 (Optimize): Cloud with pre-trained backbones
  - DINOv2 backbone → fine-tuned segmentation head
  - ConvLSTM for temporal prediction
  - Serve via optimized cloud endpoints
```

### Key Insight

For satellite imagery specifically, **the winning formula is:**
1. **Cloud infrastructure** for compute (training + serving) ✅
2. **Specialized/fine-tuned architectures** for the actual model ✅
3. **NOT general-purpose cloud vision APIs** (GPT-4V, etc.) ❌

Cloud LLM vision models excel at *understanding* images (describing what they see), but they cannot process multi-spectral satellite data, handle raw geospatial formats, or match the pixel-level accuracy of fine-tuned segmentation models.

---

## 6. Architecture Summary

```
┌─────────────────────────────────────────────────────┐
│                    DATA INGESTION                     │
│  Sentinel-5P → GEE API                               │
│  MERRA-2 → NASA GES DISC API                         │
│  OpenAQ → REST API                                    │
│  ERA5 → Copernicus CDS                                │
└──────────────────┬──────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────┐
│                  AI PROCESSING (Cloud)                 │
│  U-Net (pollutant segmentation)                       │
│  ConvLSTM (temporal prediction)                       │
│  HYSPLIT (trajectory modeling)                        │
│  DINOv2 backbone (feature extraction)                 │
└──────────────────┬──────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────┐
│                  TILE GENERATION                      │
│  TiTiler (Cloud Optimized GeoTIFF → map tiles)       │
│  Pre-computed frames per timestep                     │
│  GeoJSON for vector overlays                          │
└──────────────────┬──────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────┐
│                  FRONTEND                             │
│  MapLibre GL JS (base map)                            │
│  deck.gl (heatmap + vector overlays)                  │
│  Timeline slider (animation control)                  │
│  Pollutant selector (NO₂, SO₂, CO, PM2.5, O₃)      │
│  Region picker + zoom                                 │
└─────────────────────────────────────────────────────┘
```

---

## 7. Risk & Challenges

| Risk | Impact | Mitigation |
|---|---|---|
| Cloud cover gaps in satellite data | Missing data in timeline | Interpolation + multi-source fusion (MODIS + S5P) |
| 7km resolution too coarse for city-level | Low granularity | AI downscaling (U-Net proved effective at ESA challenge) |
| Labeling satellite data is expensive | Training bottleneck | Self-supervised (DINOv2) + transfer learning + SAM 2 |
| Real-time wind data latency | Delayed movement prediction | Use forecast data (GFS) for near-real-time |
| Compute costs for global processing | Budget | Start regional, expand; GEE free tier for research |

---

## 8. Existing Competitors / Inspiration

| Product | What It Does |
|---|---|
| **S5P-PAL Mapping Portal** (maps.s5p-pal.com) | Official Sentinel-5P visualization, 14-day average |
| **Windy.com** | Beautiful wind/weather animation, includes some AQ layers |
| **Google Earth Engine Timelapse** | Historical satellite imagery animation |
| **Plume Labs (now part of AccuWeather)** | AQ forecasting with visualization |
| **BreezoMeter** | Hyperlocal AQ with street-level mapping |

**Gap:** None of these combine AI-powered plume detection + trajectory prediction + interactive timeline in a single tool.

---

## 9. Next Steps (if proceeding)

1. **Prototype (2-4 weeks):** GEE script → export Sentinel-5P NO₂ frames → MapLibre + deck.gl timeline viewer
2. **AI Layer (4-8 weeks):** Train U-Net on S5P data for plume segmentation, integrate MERRA-2 wind
3. **Prediction (8-12 weeks):** ConvLSTM for temporal forecasting, HYSPLIT integration
4. **Product (12+ weeks):** Full stack, multiple pollutants, global regions, real-time updates
