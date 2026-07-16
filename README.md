# Michael Jeffreys — Code Portfolio

**Front-End Engineer · React/TypeScript · PWAs & Real-Time UIs**

[mjcj1022@gmail.com](mailto:mjcj1022@gmail.com) · [LinkedIn](https://linkedin.com/in/michaeljeffreys) · [GitHub](https://github.com/mjcj1022-collab)

---

## About this repository

These are standalone code samples pulled from production projects I've built at LightSett. Most of the source repos are private — they're active business tools — so what's here are the patterns, architecture decisions, and problem-solving from applications that engineering teams use every day.

```
react-hooks/          Custom TypeScript React hooks (WebSocket, IndexedDB, API fetch)
react-components/     Reusable UI components (data tables, role-based views)
python-arcgis/        ArcGIS Pro Python toolbox automation
django-api/           Django REST Framework models, serializers, views
```

---

## Featured projects

### 1. ODEN PWA — React / TypeScript / Firebase

A 19,000+ line progressive web app used daily by 60+ field engineers. Full-featured GIS and permit tracking, built from scratch. Engineers use it on mobile in the field for real-time job coordination.

- GIS mapping via ArcGIS REST API with live pole/structure overlays
- Permit tracking integrated with the Katapult Pro API
- Firebase Realtime Database for instant field-note sync across devices
- Role-based access control (Admin / Engineer / Viewer)
- Full PWA — service workers, offline support, install prompts

**Stack:** React · Vite · TypeScript · Tailwind CSS · Firebase RTDB · ArcGIS REST API · Katapult Pro API · Service Workers

**Samples here:** [`react-hooks/useWebSocket.ts`](react-hooks/useWebSocket.ts) · [`react-hooks/useIndexedDB.ts`](react-hooks/useIndexedDB.ts) · [`react-components/RoleGate.tsx`](react-components/RoleGate.tsx)

---

### 2. Make-Ready Workstation — React / TypeScript / APIs

A 13-tab engineering browser tool for fiber optic make-ready analysis. It centralizes everything an OSP engineer needs during make-ready design, pulling live data from multiple external APIs and applying NESC clearance logic in-browser.

- Katapult Pro API integration (pole data, attachment heights, job management)
- NESC 235C clearance calculation engine written in TypeScript
- SPIDAcalc results parsing and display
- 29-gate PNM Joint-Use Permit Checker with pass/fail logic
- Custom hooks for caching API responses across tabs

**Stack:** React · TypeScript · Custom Hooks · REST APIs · Vite · Tailwind CSS

**Samples here:** [`react-hooks/useApiFetch.ts`](react-hooks/useApiFetch.ts) · [`react-components/DataTable.tsx`](react-components/DataTable.tsx)

---

### 3. REDLINE — Django / React / TypeScript

A contractor and PM coordination platform for fiber construction, with a Django REST Framework API backend and a Vite + React frontend.

- Django REST Framework API with JWT authentication
- Contractor work order creation, assignment, and status tracking
- React frontend consuming the DRF API, with React Query for data sync
- PostgreSQL data model for projects, contractors, and milestones

**Stack:** Python · Django · Django REST Framework · PostgreSQL · React · TypeScript · Vite · React Query

**Samples here:** [`django-api/models.py`](django-api/models.py) · [`django-api/serializers.py`](django-api/serializers.py) · [`django-api/views.py`](django-api/views.py)

---

### 4. EzeeFiber OSP Design Toolbox — Python / ArcGIS Pro

An ArcGIS Python Toolbox automating fiber OSP design workflows — turning hours of manual GIS work into seconds.

- Cabinet-to-address conduit routing with automatic feature creation
- Vault and structure placement at standardized intervals along routes
- Automatic naming conventions and depth specification labeling
- BEAD/UHLD template generation for funding applications
- Vitruvi import template generation from ArcGIS data

**Stack:** Python · ArcGIS Pro SDK · arcpy · GeoJSON

**Samples here:** [`python-arcgis/conduit_router.py`](python-arcgis/conduit_router.py)

---

### 5. LightBeam — Python / Tkinter

An internal desktop app giving the team PDF markup and management without BlueBeam licenses.

**Stack:** Python · Tkinter (TTK) · PyMuPDF

---

## Technical skills

### Front-end

| Category | Technologies |
|---|---|
| Languages | TypeScript, JavaScript (ES6+), HTML5, CSS3 |
| Frameworks | React, Vite, Next.js |
| State management | Redux Toolkit, React Query, Context API, custom hooks |
| Styling | Tailwind CSS, CSS Modules, responsive design |
| Real-time | WebSockets, BroadcastChannel API, Service Workers, Firebase RTDB |
| PWA | Service Workers, Web App Manifest, offline strategies, IndexedDB |

### Backend & APIs

| Category | Technologies |
|---|---|
| Languages | Python, JavaScript |
| Frameworks | Django, Django REST Framework |
| Databases | PostgreSQL, Firebase Realtime Database |
| API integration | ArcGIS REST API, Katapult Pro API, SPIDAcalc, RESTful design |

### DevOps & tooling

| Category | Technologies |
|---|---|
| Version control | Git, GitHub, GitHub Actions |
| CI/CD | GitHub Actions, Netlify |
| Build tools | Vite, npm/yarn |

### GIS & engineering domain

| Category | Technologies |
|---|---|
| GIS | ArcGIS Pro, arcpy, ArcGIS REST API |
| OSP tools | Katapult Pro, SPIDAcalc, AutoCAD OSP |
| Standards | NESC 235C, BEAD/UHLD specs, joint-use permitting |

### AI & automation

| Category | Technologies |
|---|---|
| AI APIs | Anthropic Claude API, GPT-4o Vision |
| Automation | AI-assisted design workflows, prompt engineering |

---

## Background

I started as a Fiber OSP Engineer designing outside plant networks, and realized I could build the tools my team needed faster and better than anything we could buy. That led to ODEN, the Make-Ready Workstation, and a suite of ArcGIS automation tools — all in active daily use.

I'm now focused on front-end engineering: fast, scalable React/TypeScript applications with clean architecture and good UX.

**Open to:** remote front-end engineering roles, contract or full-time.

---

## Contact

| | |
|---|---|
| Email | [mjcj1022@gmail.com](mailto:mjcj1022@gmail.com) |
| LinkedIn | [linkedin.com/in/michaeljeffreys](https://linkedin.com/in/michaeljeffreys) |
| GitHub | [@mjcj1022-collab](https://github.com/mjcj1022-collab) |
| Book a call | [calendar.app.google/hqWCTTNQaBzD2V747](https://calendar.app.google/hqWCTTNQaBzD2V747) |
