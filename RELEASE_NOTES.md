### Release Notes

**Title:** `feat(auth): Database User Authentication System`

**Date:** `2025-08-26`

**Summary:**
This release introduces a brand new user authentication system, migrating from hardcoded admin credentials to a database-backed store. This significantly enhances security and future scalability.

**Key Changes:**
*   **Database Storage**: A new `users` table has been added to store usernames and hashed passwords.
*   **Dynamic Authentication**: The login logic now queries the database to verify user credentials.
*   **Default User**: On first startup, the system automatically creates a default admin user. The credentials can be configured via environment variables, improving deployment flexibility.
*   **Password Management**: A new API endpoint, `PUT /api/admin/password`, has been added to allow logged-in administrators to change their own password.