import { useState } from "react";
import axios from "axios";

// 🔥 LIVE BACKEND
const API = "https://healthcare-system-1x18.onrender.com";

export default function Dashboard() {

  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    name: "",
    mobile: "",
    age: "",
    location: "",
    photoshoot_by: "",
    clinic: "",
    concern: "",
    date: "",
    subfolder_name: "",
    files: []
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleFile = (e) => {
    setForm({ ...form, files: e.target.files });
  };

  const createFull = async () => {

    if (!form.name || !form.mobile || !form.date || !form.concern) {
      alert("Please fill required fields ❌");
      return;
    }

    if (form.files.length === 0) {
      alert("Please upload at least one file ❌");
      return;
    }

    setLoading(true);

    const data = new FormData();

    Object.keys(form).forEach((key) => {
      if (key === "files") {
        for (let i = 0; i < form.files.length; i++) {
          data.append("files", form.files[i]);
        }
      } else {
        data.append(key, form[key]);
      }
    });

    try {
      await axios.post(`${API}/create-full`, data);

      alert("Saved Successfully 🚀");

      setForm({
        name: "",
        mobile: "",
        age: "",
        location: "",
        photoshoot_by: "",
        clinic: "",
        concern: "",
        date: "",
        subfolder_name: "",
        files: []
      });

    } catch (err) {
      console.log(err);

      if (err.response) {
        alert(err.response.data.detail || "Server Error ❌");
      } else {
        alert("Network Error ❌");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="header">
        <div className="logo">
          <img src="/logo.png" alt="Satya Logo" />
          <span>Satya Skin & Hair</span>
        </div>
      </div>

      <div className="container">

        <div className="card premium">
          <h2>Patient Entry</h2>

          <div className="grid">

            <input name="name" placeholder="Patient Name" value={form.name} onChange={handleChange} />
            <input name="mobile" placeholder="Mobile Number" value={form.mobile} onChange={handleChange} />
            <input name="age" placeholder="Age" value={form.age} onChange={handleChange} />
            <input name="location" placeholder="Location" value={form.location} onChange={handleChange} />

            <input name="photoshoot_by" placeholder="Photoshoot By" value={form.photoshoot_by} onChange={handleChange} />

            <select name="clinic" value={form.clinic} onChange={handleChange}>
              <option value="">Select Clinic</option>
              <option value="Gurugram">Gurugram</option>
              <option value="Pitampura">Pitampura</option>
            </select>

            <input name="concern" placeholder="Concern" value={form.concern} onChange={handleChange} />
            <input type="date" name="date" value={form.date} onChange={handleChange} />

            <input
              name="subfolder_name"
              placeholder="Folder Name (PRE / AFTER / BEFORE)"
              value={form.subfolder_name}
              onChange={handleChange}
            />

          </div>

          <div className="upload-box">
            <input type="file" multiple onChange={handleFile} />
          </div>

          <button
            className="premium-btn"
            onClick={createFull}
            disabled={loading}
          >
            {loading ? "Saving..." : "Save Patient & Visit"}
          </button>

        </div>

      </div>
    </>
  );
}