# Feature: User Authentication

## User Stories
- As a new user, I can sign up with email and password
- As a registered user, I can sign in with my credentials
- As a logged-in user, my session persists across page reloads
- As a user, I can sign out
- As a user, my tasks are private and only visible to me

## Technical Requirements

### Better Auth Configuration
- Install Better Auth in Next.js frontend
- Enable JWT plugin for token generation
- Configure shared secret between frontend and backend
- Set token expiry (7 days recommended)

### Backend JWT Verification
- FastAPI middleware to verify JWT tokens
- Extract user information from token payload
- Match user_id in token with user_id in URL path
- Return 401 Unauthorized for invalid/missing tokens

### API Security
- All `/api/{user_id}/*` endpoints require valid JWT
- User can only access their own data (user_id must match token)
- Return 403 Forbidden if user_id mismatch

## Acceptance Criteria

### Sign Up
- Email validation (valid format)
- Password requirements (min 8 characters)
- Unique email constraint
- Success returns user object and JWT token
- Error handling for duplicate email

### Sign In
- Verify email exists
- Verify password matches
- Success returns user object and JWT token
- Error handling for invalid credentials
