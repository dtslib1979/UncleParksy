# PARKSY Production Order System

## Overview

The PO (Production Order) system enables dispatching work orders from `parksy.kr` to the `studio-engine` repository for automated content production.

```
┌─────────────────┐         ┌─────────────────┐
│   parksy.kr     │  ──→    │  studio-engine  │
│   (Frontend)    │   PO    │  (PC Workflow)  │
│                 │         │                 │
│  • Create PO    │         │  • Process PO   │
│  • Queue        │         │  • Execute      │
│  • Dispatch     │         │  • Return       │
└─────────────────┘         └─────────────────┘
```

## Directory Structure

```
/po/
├── index.json      # Queue status and history
├── schema.json     # PO data schema
├── templates.json  # Pre-defined order templates
├── queue/          # Pending orders (JSON files)
└── README.md       # This file
```

## PO Types

| Type | Description | Icon |
|------|-------------|------|
| `content_transform` | Transform content via persona × merit | ⚡ |
| `video_render` | Render video for YouTube | 🎬 |
| `image_generate` | Generate images via AI | 🖼️ |
| `audio_process` | Process audio files | 🎵 |
| `document_compile` | Compile documents | 📄 |
| `batch_publish` | Publish across platforms | 📤 |
| `data_sync` | Sync data between services | 🔄 |

## PO Lifecycle

```
draft → queued → dispatched → processing → completed
                     ↓              ↓
                  failed        cancelled
```

## Integration

### From parksy.kr (Frontend)

1. User creates PO in Studio (B2)
2. PO saved to `/po/queue/PO-YYYYMMDD-XXXX.json`
3. GitHub Action dispatches to `studio-engine`

### From studio-engine (Backend)

1. Watches for new POs via webhook or polling
2. Processes order based on type
3. Updates status and returns result
4. Pushes output to designated destination

## API Endpoints (Future)

```
POST   /api/po/create     # Create new PO
GET    /api/po/queue      # List queued POs
POST   /api/po/dispatch   # Dispatch PO to engine
GET    /api/po/:id        # Get PO status
DELETE /api/po/:id        # Cancel PO
```

## Configuration

Target repository: `dtslib1979/studio-engine`

Environment variables needed:
- `STUDIO_ENGINE_TOKEN` - GitHub PAT for dispatch
- `WEBHOOK_SECRET` - Webhook verification

## Status

🚧 **System Status: PENDING SETUP**

The PO system is currently a placeholder. Full integration requires:

1. [ ] Create `studio-engine` repository
2. [ ] Set up GitHub Actions workflow
3. [ ] Configure webhook endpoints
4. [ ] Implement dispatch mechanism

---

*PARKSY Broadcasting — Production Order System v1.0*
