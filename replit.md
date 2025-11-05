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

**WhatsApp Integration** (Python-based)
- Purpose: Enables bots to send and receive WhatsApp messages
- Providers supported: Twilio API and Meta WhatsApp Cloud API
- Communication: Webhooks receive incoming messages at `/webhook/twilio` and `/webhook/meta` endpoints
- Security: Signature validation for both Twilio (X-Twilio-Signature) and Meta (X-Hub-Signature-256)
- Message sending: Python service layer (`services/whatsapp_service.py`) handles API calls to Twilio or Meta
- Alternative considered: WPPConnect (rejected due to Node.js dependency and unofficial protocol)
- Limitation: Requires environment configuration (API keys, auth tokens, webhook secrets)

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

### Python WhatsApp Packages

**twilio**: Official Twilio SDK for Python
- Handles Twilio API authentication and message sending
- Provides webhook request validation utilities
- Used for both sending messages and validating incoming webhooks

**requests**: HTTP client for Meta API communication
- Makes HTTP requests to Meta WhatsApp Cloud API
- Handles JSON request/response for sending messages via Meta

### Frontend Dependencies

**Bootstrap 5**: CSS framework (CDN-delivered)
- Responsive grid system and components
- No build process required
- Reduces custom CSS needs

### API Key Management

**User-Specific API Keys** (NEW - November 2025):
- Users can now configure their Meta Cloud API or Twilio API keys directly in the dashboard
- API keys are encrypted using Fernet (symmetric encryption) before storage in the database
- Encryption key derived from `ENCRYPTION_SECRET` environment variable using PBKDF2-HMAC
- Each user can have their own WhatsApp provider and credentials
- Credentials are never displayed in plaintext - UI shows masked placeholders
- WhatsAppService automatically uses user-specific credentials for webhook responses

**Security Features**:
- AES-128 encryption via Fernet for all stored API keys
- PBKDF2-HMAC key derivation (100,000 iterations) from `ENCRYPTION_SECRET`
- Password-type input fields prevent credential exposure
- Credentials validated before provider switching to prevent runtime errors
- User model includes methods: `set_meta_credentials()`, `set_twilio_credentials()`, `get_meta_credentials()`, `get_twilio_credentials()`

### Environment Configuration

**Required Environment Variables**:
- `ENCRYPTION_SECRET`: **REQUIRED** - Encryption key for securing API credentials in database. Must be set before starting the application.
- `SESSION_SECRET`: Flask session encryption key (defaults to dev key in development)

**Optional Environment Variables** (for backward compatibility or webhook validation):
- **Meta Configuration** (optional - users can configure in dashboard):
  - `META_VERIFY_TOKEN`: Token for webhook subscription verification
  - `META_APP_SECRET`: App secret for webhook signature validation
- **Legacy Twilio/Meta Configuration**: Environment variables still supported as fallback when user has no credentials configured

**Database**: SQLite file (`whatsapp_bot.db`)
- Auto-created on first run via `db.create_all()`
- Stores encrypted user credentials in `users` table
- Single-file deployment simplifies backup and migration
- No external database service required

### Deployment Considerations

**Port Configuration**: 
- Flask runs on port 5000
- Webhook URLs must be publicly accessible (Replit provides automatic HTTPS)
- Environment variables must be configured before webhooks can function
- Webhook signature validation ensures security (required for production)

**Replit Compatibility**:
- SQLite works natively without configuration
- Static file serving handled by Flask
- PWA features require HTTPS (Replit provides this automatically)