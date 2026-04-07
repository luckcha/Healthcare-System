import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const [form, setForm] = useState({
    name: "",
    mobile: "",
    age: "",
    location: "",
    photoshoot_by: "",
    clinic: ""
  });

  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  // 🔍 LIVE SEARCH
  const handleSearch = async (value) => {
    setForm({ ...form, name: value });

    if (!value) {
      setResults([]);
      return;
    }

    try {
      const res = await axios.get(
        `http://127.0.0.1:8000/search?name=${value}`
      );
      setResults(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  // 👤 CREATE PATIENT
  const createPatient = async () => {
    const data = new FormData();

    Object.keys(form).forEach((key) => {
      data.append(key, form[key]);
    });

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/create-patient",
        data
      );

      navigate(`/patient/${res.data.patient_id}`);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <>
      <div className="header">Healthcare System</div>

      <div className="container">

        {/* 🔍 SEARCH SECTION */}
        <div className="card">
          <h2>Search Patient</h2>

          <input
            placeholder="Search Patient..."
            value={form.name}
            onChange={(e) => handleSearch(e.target.value)}
          />

          {/* 🔥 SUGGESTION DROPDOWN */}
          {results.length > 0 && (
            <div
              style={{
                background: "#fff",
                border: "1px solid #ccc",
                borderRadius: "8px",
                marginTop: "5px"
              }}
            >
              {results.map((r) => (
                <div
                  key={r.patient_id}
                  style={{
                    padding: "10px",
                    cursor: "pointer",
                    borderBottom: "1px solid #eee"
                  }}
                  onClick={() => {
                    navigate(`/patient/${r.patient_id}`);
                    setResults([]);
                  }}
                >
                  {r.name} ({r.mobile})
                </div>
              ))}
            </div>
          )}
        </div>

        {/* ➕ CREATE PATIENT */}
        <div className="card">
          <h2>Create New Patient</h2>

          <input
            placeholder="Name"
            onChange={(e) =>
              setForm({ ...form, name: e.target.value })
            }
          />

          <input
            placeholder="Mobile"
            onChange={(e) =>
              setForm({ ...form, mobile: e.target.value })
            }
          />

          <input
            placeholder="Age"
            onChange={(e) =>
              setForm({ ...form, age: e.target.value })
            }
          />

          <input
            placeholder="Location"
            onChange={(e) =>
              setForm({ ...form, location: e.target.value })
            }
          />

          <input
            placeholder="Photoshoot Done By"
            onChange={(e) =>
              setForm({ ...form, photoshoot_by: e.target.value })
            }
          />

          {/* 🔽 DROPDOWN */}
          <select
            onChange={(e) =>
              setForm({ ...form, clinic: e.target.value })
            }
            style={{
              width: "100%",
              padding: "10px",
              marginTop: "10px",
              borderRadius: "8px"
            }}
          >
            <option value="">Select Clinic</option>
            <option value="Gurugram">Gurugram</option>
            <option value="Pitampura">Pitampura</option>
          </select>

          <button onClick={createPatient}>
            Create Patient
          </button>
        </div>

      </div>
    </>
  );
}