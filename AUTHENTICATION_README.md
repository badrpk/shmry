# Shmry Platform Authentication System

## Overview
The Shmry Platform now includes a comprehensive authentication system supporting Google OAuth, GitHub OAuth, and Phone OTP authentication methods.

## Features
- **Google OAuth**: Sign in with Google account
- **GitHub OAuth**: Sign in with GitHub account  
- **Phone OTP**: Sign in with phone number and one-time password
- **JWT-based sessions**: Secure HTTP-only cookies
- **Protected routes**: Authentication middleware for API endpoints
- **User management**: User profiles, plans, and session handling

## Architecture

### Backend Components
- `deployment/auth.js` - Core authentication logic and user management
- `deployment/auth-api.js` - HTTP API endpoints for authentication
- `deployment/server.js` - Express server with authentication routes
- `package.json` - Dependencies (express, cookie-parser, jsonwebtoken)

### Frontend Components
- `dashboard/index.html` - Authentication page with login options
- `dashboard/app.html` - Protected dashboard for authenticated users
- `website/shmry-website.html` - Updated with "Sign in" button

## Authentication Flow

### 1. Google OAuth
```
User clicks "Continue with Google" 
→ Redirects to Google OAuth
→ Google returns authorization code
→ Backend exchanges code for user info
→ Creates/updates user account
→ Sets JWT cookie
→ Redirects to dashboard
```

### 2. GitHub OAuth
```
User clicks "Continue with GitHub"
→ Redirects to GitHub OAuth
→ GitHub returns authorization code
→ Backend exchanges code for user info
→ Creates/updates user account
→ Sets JWT cookie
→ Redirects to dashboard
```

### 3. Phone OTP
```
User enters phone number
→ Backend generates 6-digit OTP
→ OTP sent via SMS (simulated for demo)
→ User enters OTP code
→ Backend verifies OTP
→ Creates/updates user account
→ Sets JWT cookie
→ Shows success message
```

## API Endpoints

### Authentication
- `GET /api/auth/google/callback` - Google OAuth callback
- `GET /api/auth/github/callback` - GitHub OAuth callback
- `POST /api/auth/phone/send-otp` - Send phone OTP
- `POST /api/auth/phone/verify-otp` - Verify phone OTP
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user profile

### Protected Routes
- `GET /api/dashboard` - Dashboard data (requires auth)
- `GET /api/auth/health` - Authentication service health

## Security Features

### JWT Tokens
- HTTP-only cookies for security
- 7-day expiration
- Secure in production (HTTPS required)
- SameSite lax policy

### Session Management
- Server-side session tracking
- Automatic cleanup of expired sessions
- Activity monitoring

### OTP Security
- 6-digit codes
- 10-minute expiration
- Maximum 3 attempts
- Rate limiting (implemented in backend)

## User Data Model

```javascript
class User {
    id: string           // Unique identifier
    email: string        // Email address (null for phone users)
    name: string         // Display name
    avatar: string       // Profile picture URL
    provider: string     // 'google', 'github', or 'phone'
    phone: string        // Phone number (for phone users)
    createdAt: Date      // Account creation timestamp
    lastLogin: Date      // Last login timestamp
    isActive: boolean    // Account status
    plan: string         // 'free', 'builder', 'scale', 'enterprise'
    apiKeys: Array      // API keys array
    projects: Array     // User projects
}
```

## Frontend Integration

### Sign In Button
Added to main website header, links to `/dashboard` for authentication.

### Authentication Page
Located at `/dashboard`, shows login options and handles authentication flow.

### Protected Dashboard
Located at `/dashboard/app`, requires valid authentication token.

## Configuration

### Environment Variables
```bash
JWT_SECRET=your-secret-key-here
NODE_ENV=production
```

### OAuth Setup (Production)
1. Create Google OAuth app in Google Cloud Console
2. Create GitHub OAuth app in GitHub Settings
3. Update callback URLs in OAuth apps
4. Set environment variables for client IDs and secrets

### SMS Service (Production)
Replace console.log OTP with actual SMS service:
- Twilio
- MessageBird
- Google Identity Toolkit

## Development vs Production

### Development
- Simulated OAuth flows
- Console.log OTP codes
- In-memory user storage
- HTTP cookies allowed

### Production
- Real OAuth integrations
- SMS OTP delivery
- Database user storage
- HTTPS cookies required

## Next Steps

### Immediate
- [x] Basic authentication system
- [x] Protected dashboard
- [x] User session management

### Short Term
- [ ] Real OAuth integrations
- [ ] Database backend (PostgreSQL)
- [ ] SMS service integration
- [ ] Password-based authentication

### Long Term
- [ ] Multi-factor authentication
- [ ] Role-based access control
- [ ] SSO integration
- [ ] Audit logging

## Testing

### Local Development
```bash
npm install
npm run dev
```

### Authentication Testing
1. Visit `/dashboard`
2. Try phone OTP flow (check console for codes)
3. Test protected routes
4. Verify session persistence

## Security Considerations

### Current Implementation
- JWT tokens in HTTP-only cookies
- Server-side session validation
- OTP rate limiting
- Secure cookie settings

### Production Requirements
- HTTPS enforcement
- Environment variable secrets
- Database security
- Input validation
- Rate limiting
- CORS configuration

## Support

For authentication issues or questions:
- Check browser console for errors
- Verify API endpoint responses
- Review server logs
- Ensure cookies are enabled
