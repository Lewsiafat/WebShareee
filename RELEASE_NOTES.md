### `feat(backend): Comprehensive Logging and Stability`

**Date:** `2025-08-27`

**Summary:**
This update introduces a robust logging framework to the backend application, providing better visibility into application behavior and errors. It also includes several stability improvements and configuration updates to enhance the development experience.

**Key Changes:**
*   **Comprehensive Logging**: Integrated Python's `logging` module throughout the FastAPI application. All major events, API calls, and errors are now logged to the console for easier debugging and monitoring.
*   **Improved Dev Experience**: The development start script (`start.sh`) has been modified to stream backend server logs directly to the console.
*   **Configuration Update**: The `pyproject.toml` file has been updated to correctly identify the `app` package, ensuring proper package discovery.
*   **Dependency Management**: The `markdown` dependency is now explicitly managed.
*   **Bug Fix**: Corrected the file path resolution for served pages to use the path stored in the database, improving reliability.

---

### `feat(upload): Markdown Support`

**Date:** `2025-08-26`

**Summary:**
The application now fully supports Markdown. Users can upload Markdown files or paste Markdown code directly, which will be automatically converted and rendered as HTML.

**Key Changes:**
*   **Markdown Upload**: The upload page now features a dedicated "Markdown" tab.
*   **File & Code Support**: Supports both `.md`/`.markdown` file uploads and direct code pasting.
*   **Automatic Conversion**: The backend automatically converts all Markdown submissions to HTML before saving, ensuring they render correctly when viewed.
*   **Dependency Management**: The new `markdown` package is now managed via `pyproject.toml` and locked with `uv.lock`.

---

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