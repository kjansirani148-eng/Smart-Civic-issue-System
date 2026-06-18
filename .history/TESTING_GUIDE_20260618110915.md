# Testing Guide

## Local Smoke Tests

1. Start the application:
   ```powershell
   python run.py
   ```
2. Open browser at `http://127.0.0.1:5000`.
3. Register a new citizen account.
4. Submit a complaint with an image and auto location.
5. Log in as admin and verify the complaint appears under complaints.
6. Log in as an officer and update the status.

## Manual Verification

- Confirm login and role redirection work.
- Ensure complaint images upload and display correctly.
- Validate category management in the admin portal.
- Check that profile updates persist.
- Verify nearby complaints by allowing location access.

## Database Schema Validation

- Run `schema.sql` and verify tables: `users`, `officers`, `categories`, `complaint_status`, `complaints`, `notifications`.
- Seed sample data from `sample_data.sql`.

## Recommended Test Cases

- Register a new citizen with mismatched passwords.
- Submit a complaint without selecting a category.
- Submit a complaint with unsupported file type.
- Officer attempts to access admin routes.
- Admin assigns a complaint to an officer.
- Officer uploads a resolution image.

## Notes

- Use environment variables from `.env` for local database and S3 settings.
- If using AWS credentials, keep them out of source control.
