# WhatsApp Bot Creator

## Overview

WhatsApp Bot Creator is a full-stack Progressive Web App (PWA) that enables users to create and manage WhatsApp chatbots without coding. The system uses a Flask backend with SQLite for data persistence, a Bootstrap-based responsive frontend, and integrates with WhatsApp through WPPConnect (a Node.js gateway). Users can define keyword-based conversation rules, track analytics, and manage multiple bots through an intuitive dashboard.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Structure

**Backend Framework**: Python Flask with blueprint-based modular architecture
- Blueprints organize functionality into logical domains: authentication (`auth`), bot management (`bots`), API endpoints (`api`), and analytics (`analytics`)
- This separation enables clean code organization and makes the codebase easier to navigate and maintain

**Frontend Architecture**: Server-side rendered templates with Progressive Web App capabilities
- Uses Jinja2 templating with a base template (`base.html`) for consistent layout
- Bootstrap 5 provides responsive UI components without requiring custom JavaScript frameworks
- PWA features (service worker, manifest) enable offline support and mobile installation
- Choice rationale: Server-side rendering reduces frontend complexity while PWA features provide native app-like experience

**Database Design**: SQLAlchemy ORM with SQLite
- Four core models with clear relationships:
  - `User`: Authentication and bot ownership
  - `Bot`: Bot configuration and settings
  - `Rule`: Keyword-response pairs for bot logic
  - `MessageLog`: Conversation history and analytics data
- Uses cascading deletes to maintain referential integrity
- SQLite chosen for simplicity and Replit compatibility (no external database service needed)

### Authentication System

**Session-based authentication** using Flask sessions
- Passwords hashed with Werkzeug's `generate_password_hash` (PBKDF2-based)
- Login decorator pattern (`login_required`) protects authenticated routes
- No password reset or email features (simplified by design per requirements)
- Session data stores `user_id` and `username` for identifying logged-in users

### Bot Response Logic

**Keyword matching system** implemented in `/api/get_response` endpoint
- Linear search through rules for keyword matches (case-insensitive)
- First matching rule wins; falls back to bot's default message if no match
- Simple but effective for small-to-medium rule sets
- Future optimization opportunity: implement trie or more sophisticated NLP if scale demands

**Message logging**: All incoming/outgoing messages stored in `MessageLog`
- Enables analytics dashboard
- Tracks conversation history per bot
- Direction field distinguishes between incoming and outgoing messages

### Progressive Web App Features

**Service Worker**: Implements cache-first strategy
- Caches static assets (CSS, JS, manifest)
- Falls back to network for dynamic content
- Improves load times and enables basic offline functionality

**Manifest**: Defines app metadata for installation
- Enables "Add to Home Screen" on mobile devices
- Provides app icons and theme colors
- Makes the web app feel like a native application

## External Dependencies

### Third-Party Services

**WPPConnect** (Node.js gateway in `bot_gateway/`)
- Purpose: Bridges WhatsApp Web protocol with the Flask backend
- Communication: Posts incoming WhatsApp messages to Flask's `/api/get_response` endpoint via HTTP
- Authentication: QR code scanning links the gateway to a WhatsApp account
- Alternative considered: Official WhatsApp Business API (rejected due to cost and complexity)
- Limitation: Requires Node.js runtime alongside Python

### Python Packages

**Flask**: Web framework (v2.x or later)
- SQLAlchemy integration via Flask-SQLAlchemy
- Session management and template rendering

**Werkzeug**: Password hashing and security utilities
- Bundled with Flask
- PBKDF2 algorithm for password hashing

**SQLAlchemy**: ORM and database toolkit
- Abstracts database operations
- Provides model relationships and query interface

### Node.js Packages

**@wppconnect-team/wppconnect**: WhatsApp Web client
- Handles WhatsApp protocol communication
- Provides QR code for authentication
- Manages message sending/receiving

**axios**: HTTP client for API communication
- Posts messages from WhatsApp to Flask backend
- Handles JSON request/response

### Frontend Dependencies

**Bootstrap 5**: CSS framework (CDN-delivered)
- Responsive grid system and components
- No build process required
- Reduces custom CSS needs

### Environment Configuration

**Environment variables**:
- `SESSION_SECRET`: Flask session encryption key (defaults to dev key)
- `FLASK_API_URL`: URL for Node.js gateway to reach Flask API (defaults to localhost:5000)

**Database**: SQLite file (`whatsapp_bot.db`)
- Auto-created on first run via `db.create_all()`
- Single-file deployment simplifies backup and migration
- No external database service required

### Deployment Considerations

**Port Configuration**: 
- Flask runs on port 5000
- Node.js gateway connects to Flask via configurable URL
- Both services must run simultaneously for full functionality

**Replit Compatibility**:
- SQLite works natively without configuration
- Static file serving handled by Flask
- PWA features require HTTPS (Replit provides this automatically)