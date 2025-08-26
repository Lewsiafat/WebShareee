### `feat(account): Account Settings Page`

**Date:** `2025-08-26`

**Summary:**
This update introduces a new "Account Settings" page, allowing users to manage their credentials directly within the application. It also includes a necessary fix for the frontend development environment.

**Key Changes:**
*   **Account Settings Page**: A new page at `/account` is now available from the user dropdown menu.
*   **Change Username**: Users can now change their username after verifying their current password.
*   **Change Password**: The form for changing the password is now implemented on this page.
*   **Backend API**: A new endpoint `PUT /api/admin/username` was added to support this functionality.
*   **Bug Fix**: Corrected the Vite configuration (`vite.config.js`) to properly resolve the `@` path alias, fixing import errors in the frontend.

---

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