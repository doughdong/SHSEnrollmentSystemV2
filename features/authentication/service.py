class AuthenticationService:

    def __init__(self, database):
        self.database = database

    def login(self, username, password):
        connection = self.database.connect()
        try:
            row = connection.execute(
                """
                SELECT id
                FROM users
                WHERE username = ?
                AND password = ?
                """,
                (username.strip(), password)
            ).fetchone()
            return row is not None
        finally:
            connection.close()

    def signup(self, username, password):
        username = username.strip()
        if not username:
            raise ValueError("Username is required.")
        if not password:
            raise ValueError("Password is required.")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters.")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")

        connection = self.database.connect()
        try:
            existing = connection.execute(
                "SELECT id FROM users WHERE username = ?",
                (username,)
            ).fetchone()
            if existing:
                raise ValueError("Username already exists.")

            connection.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
