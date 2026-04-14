import { useParams } from "react-router-dom";
import { useState } from "react";
import axios from "axios";

export default function Patient() {
  const { id } = useParams();

  const [visitId, setVisitId] = useState("");
  const [files, setFiles] = useState([]);
  const [concern, setConcern] = useState("");
  const [date, setDate] = useState("");
  const [folder, setFolder] = useState("");

  // 📅 CREATE VISIT
  const createVisit = async () => {

    // 🔥 VALIDATION ADD
    if (!concern || !date) {
      alert("Please fill concern and date ❌");
      return;
    }

    const data = new FormData();

    const name = localStorage.getItem("name");
    const mobile = localStorage.getItem("mobile");

    data.append("patient_id", id);
    data.append("name", name || "unknown");
    data.append("mobile", mobile || "0000000000");
    data.append("concern", concern);
    data.append("date", date);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/create-visit",
        data
      );

      setVisitId(res.data.visit_id);
      alert("Visit Created ✅");

      // 🔥 RESET INPUTS
      setConcern("");
      setDate("");

    } catch (err) {
      console.log(err);
      alert("Error creating visit");
    }
  };

  // 📤 UPLOAD FILES
  const upload = async () => {
    const folder_id = localStorage.getItem("folder_id");

    if (!folder_id) {
      alert("❌ Folder ID missing (create patient first)");
      return;
    }

    if (!folder) {
      alert("Enter folder name (before / after)");
      return;
    }

    const data = new FormData();

    data.append("folder_id", folder_id);
    data.append("subfolder_name", folder);

    for (let i = 0; i < files.length; i++) {
      data.append("files", files[i]);
    }

    try {
      await axios.post("http://127.0.0.1:8000/upload", data);
      alert("Uploaded Successfully 🚀");
    } catch (err) {
      console.log(err);
      alert("Upload failed");
    }
  };

  return (
    <>
      <div className="header">Patient ID: {id}</div>

      <div className="container">

        {/* CREATE VISIT */}
        <div className="card">
          <h2>Create Visit</h2>

          <input
            placeholder="Concern"
            value={concern}   // 🔥 IMPORTANT
            onChange={(e) => setConcern(e.target.value)}
          />

          <input
            type="date"
            value={date}     // 🔥 IMPORTANT
            onChange={(e) => setDate(e.target.value)}
          />

          <button onClick={createVisit}>
            Create Visit
          </button>
        </div>

        {/* UPLOAD */}
        <div className="card">
          <h2>Upload Photos / Videos</h2>

          <input
            placeholder="Folder Name (before / after)"
            value={folder}
            onChange={(e) => setFolder(e.target.value)}
          />

          <input
            type="file"
            multiple
            onChange={(e) => setFiles([...e.target.files])}
          />

          <button onClick={upload}>
            Upload
          </button>
        </div>

      </div>
    </>
  );
}