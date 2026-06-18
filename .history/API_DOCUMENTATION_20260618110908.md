# API Documentation

## Authentication

### POST /login

- Description: Authenticate user and create session.
- Request:
  - `email` (string)
  - `password` (string)
  - `remember` (optional boolean)
- Response: Redirect to dashboard.

### GET /logout

- Description: Log out the user.

### POST /register

- Description: Create a new citizen account.
- Request:
  - `name` (string)
  - `email` (string)
  - `password` (string)
  - `confirm_password` (string)

## User Module

### GET /user/dashboard
- Description: View citizen dashboard.

### GET /user/report
- Description: Display complaint report form.

### POST /user/report
- Description: Submit a new complaint.
- Request:
  - `category_id` (integer)
  - `description` (string)
  - `latitude` (float)
  - `longitude` (float)
  - `image` (file)

### GET /user/complaints
- Description: View list of citizen complaints.

### GET /user/profile
- Description: View profile update form.

### POST /user/profile
- Description: Update citizen profile.
- Request:
  - `name` (string)
  - `phone` (string)
  - `address` (string)

### GET /user/nearby
- Description: Show nearby complaints by location query.
- Query Parameters:
  - `lat` (float)
  - `lng` (float)

## Officer Module

### GET /officer/dashboard
- Description: Officer work dashboard.

### GET /officer/assigned
- Description: List assigned complaints.

### GET /officer/assign/<complaint_id>
- Description: Claim assignment for a complaint.

### GET /officer/complaint/<complaint_id>
- Description: View complaint details.

### POST /officer/complaint/<complaint_id>
- Description: Update complaint status and resolution info.
- Request:
  - `status_id` (integer)
  - `remark` (string)
  - `resolution_image` (file)

## Admin Module

### GET /admin/dashboard
- Description: Admin overview and analytics.

### GET /admin/users
- Description: Manage citizen accounts.

### GET /admin/officers
- Description: Manage officer accounts.

### POST /admin/officers
- Description: Create a new officer.
- Request:
  - `name` (string)
  - `email` (string)
  - `password` (string)
  - `department` (string)
  - `assigned_area` (string)

### GET /admin/complaints
- Description: View all complaints.

### POST /admin/complaints/update/<complaint_id>
- Description: Update complaint assignment or status.
- Request:
  - `status_id` (integer)
  - `officer_id` (integer)

### GET /admin/categories
- Description: View category list.

### POST /admin/categories
- Description: Add a new complaint category.
- Request:
  - `name` (string)
  - `description` (string)

### GET /admin/analytics
- Description: View analytics graphs and reports.
