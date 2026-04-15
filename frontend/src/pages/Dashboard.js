import { useState } from "react";
import axios from "axios";

const API = "https://healthcare-system-1x18.onrender.com";

export default function Dashboard() {

  const [search, setSearch] = useState("");
  const [results, setResults] = useState([]);

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

  const searchPatient = async (value) => {
    setSearch(value);

    if (!value) return setResults([]);

    try {
      const res = await axios.get(`${API}/search-patient?query=${value}`);
      setResults(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  const createFull = async () => {
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
      alert("Saved 🚀");
    } catch (err) {
      console.log(err);
      alert("Error ❌");
    }
  };

  return (
    <div className="main">

      {/* 🔍 SEARCH */}
      <div className="card">
        <h3>🔍 Search Patient</h3>

        <input
          className="input"
          placeholder="Search name / mobile"
          value={search}
          onChange={(e) => searchPatient(e.target.value)}
        />

        {results.map((p, i) => (
          <div key={i} className="result">
            <div>
              <b>{p.name}</b>
              <p>{p.mobile}</p>
            </div>

            <a href={p.patient_link} target="_blank">
              Open →
            </a>
          </div>
        ))}
      </div>

      {/* 🧾 FORM */}
      <div className="card">
        <h3>Patient Entry</h3>

        <div className="grid">

          <input className="input" name="name" placeholder="Name" onChange={handleChange}/>
          <input className="input" name="mobile" placeholder="Mobile" onChange={handleChange}/>
          <input className="input" name="age" placeholder="Age" onChange={handleChange}/>
          <input className="input" name="location" placeholder="Location" onChange={handleChange}/>
          <input className="input" name="photoshoot_by" placeholder="Photoshoot By" onChange={handleChange}/>

          <select className="input" name="clinic" onChange={handleChange}>
            <option value="">Clinic</option>
            <option>Gurugram</option>
            <option>Pitampura</option>
          </select>

          <input className="input" name="concern" placeholder="Concern" onChange={handleChange}/>
          <input className="input" type="date" name="date" onChange={handleChange}/>

          <input className="input" name="subfolder_name" placeholder="Folder (PRE / AFTER)" onChange={handleChange}/>

        </div>

        <input className="file" type="file" multiple onChange={handleFile}/>

        <button className="btn" onClick={createFull}>
          Save Patient
        </button>
      </div>

    </div>
  );
}