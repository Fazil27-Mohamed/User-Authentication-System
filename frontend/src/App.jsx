import { useState } from "react";

const API_URL = "http://127.0.0.1:5000/api";

function App() {
  const [mode, setMode] = useState("login");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState(null);

  const clearMessages = () => {
    setMessage("");
    setError("");
  };

  const handleRegister = async (event) => {
    event.preventDefault();
    clearMessages();

    if (!username || !email || !password) {
      setError("Please fill all fields");
      return;
    }

    if (password.length < 6) {
      setError("Password must contain at least 6 characters");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, email, password })
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || "Registration failed");
        return;
      }

      setMessage(data.message);
      setMode("login");
      setPassword("");
    } catch {
      setError("Unable to connect to the server");
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (event) => {
    event.preventDefault();
    clearMessages();

    if (!username || !password) {
      setError("Please enter username and password");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || "Login failed");
        return;
      }

      setUser(data.user);
      setMessage(data.message);
    } catch {
      setError("Unable to connect to the server");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setUser(null);
    setUsername("");
    setEmail("");
    setPassword("");
    setMessage("Logged out successfully");
    setError("");
  };

  if (user) {
    return (
      <main className="page">
        <section className="card dashboard">
          <div className="brand">AUTH SYSTEM</div>
          <h1>Welcome, {user.username}</h1>
          <p className="subtitle">You are successfully authenticated.</p>

          <div className="user-box">
            <span>Username</span>
            <strong>{user.username}</strong>
            <span>Email</span>
            <strong>{user.email}</strong>
          </div>

          <button className="primary-button" onClick={handleLogout}>
            Logout
          </button>

          {message && <p className="success">{message}</p>}
        </section>
      </main>
    );
  }

  return (
    <main className="page">
      <section className="card">
        <div className="brand">AUTH SYSTEM</div>

        <h1>{mode === "login" ? "Welcome back" : "Create account"}</h1>
        <p className="subtitle">
          {mode === "login"
            ? "Login to access your account"
            : "Register to create your account"}
        </p>

        <div className="tabs">
          <button
            className={mode === "login" ? "tab active" : "tab"}
            onClick={() => {
              setMode("login");
              clearMessages();
            }}
          >
            Login
          </button>
          <button
            className={mode === "register" ? "tab active" : "tab"}
            onClick={() => {
              setMode("register");
              clearMessages();
            }}
          >
            Register
          </button>
        </div>

        <form onSubmit={mode === "login" ? handleLogin : handleRegister}>
          <label>Username</label>
          <input
            type="text"
            placeholder="Enter username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />

          {mode === "register" && (
            <>
              <label>Email</label>
              <input
                type="email"
                placeholder="Enter email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
            </>
          )}

          <label>Password</label>
          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />

          {error && <p className="error">{error}</p>}
          {message && <p className="success">{message}</p>}

          <button className="primary-button" type="submit" disabled={loading}>
            {loading
              ? "Please wait..."
              : mode === "login"
              ? "Login"
              : "Create Account"}
          </button>
        </form>
      </section>
    </main>
  );
}

export default App;
