# Network

Network is a production-grade, full-stack social networking application designed to model the core interaction patterns of modern discussion platforms. It enables users to create and edit posts in real time, follow other users, and engage with content through likes and dynamic feeds, all delivered through a clean, responsive interface with asynchronous updates.

The platform is built with a strong emphasis on scalability, security, and user experience. It uses Python Django on the backend to provide a robust, secure API and data layer, while a lightweight JavaScript frontend (Fetch API) enables seamless, real-time interactions without full page reloads. Bootstrap is used for responsive layout and consistent design across devices.

## Key Features

### Content Creation

- Authenticated users can publish text-based posts
- Server-side validation with client-side constraints
- Reverse-chronological feed (most recent first)

### Social Graph

- Follow/unfollow users
- Profile pages show follower & following counts
- Personalized feed showing posts from followed users only

### Engagement

- Like/unlike posts asynchronously
- Real-time like count updates (no page reloads)
- Optimistic UI with server confirmation

### Inline Editing

- Users can edit only their own posts
- Inline textarea editing with options to Save or Cancel
- Secure server-side authorization checks

### Pagination

- All feeds paginated (10 posts per page)
- Efficient database queries using Django’s Paginator
- Intuitive Next/Previous navigation

### Authentication & Security

- Secure login/logout/registration
- CSRF-protected API requests
- Permission-safe endpoints (no client-side trust)

## System Design Highlights

- **Normalized relational models** for posts, likes, and follows
- **Many-to-many relationships** via join tables for scalability
- **Asynchronous state updates** using fetch + JSON
- **Pagination at query level** to avoid over-fetching
- **Security-first design** with all mutations validated server-side

## Getting Started

### Clone & Setup
```
git clone https://github.com/niravkpatel36/Network.git
cd network
python -m venv venv
```
- **Windows**
```
venv\Scripts\activate
```
- **macOS/Linux**
```
source venv/bin/activate
```

### Install Dependencies
```
pip install django
```

### Database Setup
```
python manage.py makemigrations
python manage.py migrate
```

### Run Server
```
python manage.py runserver
```

The web application will be served at http://127.0.0.1:8000/

## Key Endpoints

| Endpoint                         | Method | Description                           |
|----------------------------------|--------|---------------------------------------|
| `/`                              | GET    | All posts                             |
| `/following`                     | GET    | Followed users feed                   |
| `/profile/<username>`            | GET    | User profile                          |
| `/post`                          | POST   | Create new post                       |
| `/post/<id>`                     | PUT    | Edit post                             |
| `/post/<id>/like`                | POST   | Like/Unlike                           |
| `/profile/<username>/follow`     | POST   | Follow/Unfollow                       |

## Manual Testing Checklist

- Create/edit posts without page reload
- Like/unlike updates count instantly
- Follow/unfollow updates profile counts
- Unauthorized edits return HTTP 403
- Pagination shows correct ordering
- CSRF protection enforced on all mutations

## Future Enhancements

- Notifications system
- Infinite scrolling
- PostgreSQL + Redis caching
- WebSocket real-time updates

## License
Network is licensed under the MIT License.