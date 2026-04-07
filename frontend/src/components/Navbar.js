import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div style={{ padding: 15, background: "#111", color: "#fff" }}>
      <h3>Healthcare</h3>
      <Link to="/" style={{ color: "#fff" }}>Dashboard</Link>
    </div>
  );
}