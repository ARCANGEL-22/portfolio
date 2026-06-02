# Michael Jeffreys — Code Portfolio

**Front-End Engineer · React/TypeScript Specialist · PWA & Real-Time UI Builder**

📧 mjcj1022@gmail.com · 📱 (828) 417-8915 · [LinkedIn](https://linkedin.com/in/michaeljeffreys) · [GitHub @ARCANGEL-22](https://github.com/ARCANGEL-22)

---

## About This Repository

This repository contains **standalone code samples** extracted from production projects I've built at LightSett. Since most source repos are private (active business tools), these examples demonstrate real patterns, architecture decisions, and problem-solving from live applications used daily by engineering teams.

---

## 📁 Repository Structure

```
portfolio/
├── react-hooks/          # Custom TypeScript React hooks (WebSocket, IndexedDB, API fetch)
├── react-components/     # Reusable UI components (data tables, role-based views, modals)
├── python-arcgis/        # ArcGIS Pro Python toolbox automation scripts
├── django-api/           # Django REST Framework models, serializers, views
└── README.md             # This file
```

---

## 🚀 Featured Projects

### 1. ODEN PWA — React / TypeScript / Firebase
> **19,000+ line Progressive Web App** used daily by 60+ field engineers
>
> A full-featured GIS and permit tracking PWA built from scratch. Engineers use it in the field on mobile for real-time job coordination.
>
> **Key capabilities:**
> - GIS mapping via ArcGIS REST API with live pole/structure overlays
> - - Permit tracking integrated with Katapult Pro API
>   - - Firebase Realtime Database for instant field note sync across devices
>     - - Role-Based Access Control (Admin / Engineer / Viewer)
>       - - Full PWA with Service Workers, offline support, and install prompts
>        
>         - **Tech stack:** React · Vite · TypeScript · Tailwind CSS · Firebase RTDB · ArcGIS REST API · Katapult Pro API · Service Workers
>        
>         - **Code samples in this repo:** `react-hooks/useWebSocket.ts` · `react-hooks/useIndexedDB.ts` · `react-components/RoleGate.tsx`
>        
>         - ---
>
> ### 2. Make-Ready Workstation — React / TypeScript / APIs
> > **13-tab engineering browser tool** for fiber optic make-ready analysis
> >
> > A complex multi-tab workspace that centralizes all data an OSP engineer needs during make-ready design — pulling live data from multiple external APIs and applying NESC clearance logic in-browser.
> >
> > **Key capabilities:**
> > - Katapult Pro API integration (pole data, attachment heights, job management)
> > - - NESC 235C clearance calculation engine built in TypeScript
> >   - - SPIDAcalc results parsing and display
> >     - - 29-gate PNM Joint-Use Permit Checker with pass/fail logic
> >       - - Custom hooks for caching API responses across tabs
> >        
> >         - **Tech stack:** React · TypeScript · Custom Hooks · REST APIs · Vite · Tailwind CSS
> >        
> >         - **Code samples in this repo:** `react-hooks/useApiFetch.ts` · `react-components/DataTable.tsx`
> >        
> >         - ---
> >
> > ### 3. REDLINE — Django / React / TypeScript
> > > **Contractor & PM coordination platform** with full REST API backend
> > >
> > > A project management web app built for fiber construction contractor coordination. Features a Django REST Framework API backend and a Vite + React frontend.
> > >
> > > **Key capabilities:**
> > > - Django REST Framework API with JWT authentication
> > > - - Contractor work order creation, assignment, and status tracking
> > >   - - React frontend consuming DRF API with React Query for data sync
> > >     - - PostgreSQL data model for projects, contractors, and milestones
> > >      
> > >       - **Tech stack:** Python · Django · Django REST Framework · PostgreSQL · React · TypeScript · Vite · React Query
> > >      
> > >       - **Code samples in this repo:** `django-api/models.py` · `django-api/serializers.py` · `django-api/views.py`
> > >      
> > >       - ---
> > > 
### 4. EzeeFiber OSP Design Toolbox — Python / ArcGIS Pro
> **ArcGIS Python Toolbox** automating fiber OSP design workflows
>
> A collection of Python tools that automate the most time-consuming parts of outside plant fiber design in ArcGIS Pro — reducing hours of manual GIS work to seconds.
>
> **Key capabilities:**
> - Cabinet-to-address conduit routing with automatic feature creation
> - - Vault and structure placement at standardized intervals along routes
>   - - Automatic naming conventions and depth specification labeling
>     - - BEAD/UHLD template generation for funding applications
>       - - Vitruvi import template generation from ArcGIS data
>        
>         - **Tech stack:** Python · ArcGIS Pro SDK · arcpy · GeoJSON
>        
>         - **Code samples in this repo:** `python-arcgis/conduit_router.py` · `python-arcgis/structure_placer.py`
>        
>         - ---
> 
### 5. LightBeam — Python / Tkinter
> **Grassroots PDF tool** replacing expensive BlueBeam subscriptions
>
> An internal desktop app built to give the team PDF markup and management capabilities without paying for BlueBeam licenses.
>
> **Tech stack:** Python · Tkinter (TTK) · PyMuPDF
>
> ---
>
> ## 🛠️ Technical Skills
>
> ### Front-End
> | Category | Technologies |
> |---|---|
> | Languages | TypeScript, JavaScript (ES6+), HTML5, CSS3 |
> | Frameworks | React, Vite, Next.js |
> | State Management | Redux Toolkit, React Query, Context API, Custom Hooks |
> | Styling | Tailwind CSS, CSS Modules, Responsive Design |
> | Real-Time | WebSockets, BroadcastChannel API, Service Workers, Firebase RTDB |
> | PWA | Service Workers, Web App Manifest, Offline Strategies, IndexedDB |
>
> ### Backend & APIs
> | Category | Technologies |
> |---|---|
> | Languages | Python, JavaScript |
> | Frameworks | Django, Django REST Framework |
> | Databases | PostgreSQL, Firebase Realtime Database |
> | API Integration | ArcGIS REST API, Katapult Pro API, SPIDAcalc, RESTful design |
>
> ### DevOps & Tooling
> | Category | Technologies |
> |---|---|
> | Version Control | Git, GitHub, GitHub Actions |
> | CI/CD | GitHub Actions, Netlify |
> | Testing | Automated testing pipelines |
> | Build Tools | Vite, npm/yarn |
>
> ### GIS & Engineering Domain
> | Category | Technologies |
> |---|---|
> | GIS | ArcGIS Pro, arcpy, ArcGIS REST API |
> | OSP Tools | Katapult Pro, SPIDAcalc, AutoCAD OSP |
> | Standards | NESC 235C, BEAD/UHLD specs, Joint-Use permitting |
>
> ### AI & Automation
> | Category | Technologies |
> |---|---|
> | AI APIs | Anthropic Claude API, GPT-4o Vision |
> | Automation | AI-assisted design workflows, prompt engineering |
>
> ---
>
> ## 💡 Background
>
> I started as a **Fiber OSP Engineer** designing outside plant networks, and realized I could build the tools my team needed faster and better than anything we could buy. That path led me to build ODEN (a 19,000-line PWA), the Make-Ready Workstation, and a suite of ArcGIS automation tools — all of which are in active daily use.
>
> I'm now **100% focused on front-end engineering**: building fast, scalable, real-world React/TypeScript applications with clean architecture and excellent UX.
>
> **Open to:** Remote Front-End Engineer roles · Contract or Full-Time
>
> ---
>
> ## 📬 Contact
>
> | | |
> |---|---|
> | 📧 Email | mjcj1022@gmail.com |
> | 📱 Phone | (828) 417-8915 |
> | 💼 LinkedIn | [linkedin.com/in/michaeljeffreys](https://linkedin.com/in/michaeljeffreys) |
> | 🐙 GitHub | [@ARCANGEL-22](https://github.com/ARCANGEL-22) |
