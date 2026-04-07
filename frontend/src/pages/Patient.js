import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";

export default function Patient() {
  const { id } = useParams();

  const [data, setData] = useState(null);
  const [visitId, setVisitId] = useState("");
  const [folder, setFolder] = useState("");
  const [files, setFiles] = useState([]);
  const [concern, setConcern] = useState("");
  const [date, setDate] = useState("");

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    const res = await axios.get(`http://127.0.0.1:8000/patient/${id}`);
    setData(res.data);
  };

  const createVisit = async () => {
    const data = new FormData();
    data.append("concern", concern);
    data.append("date", date);

    const res = await axios.post(`http://127.0.0.1:8000/create-visit/${id}`, data);
    setVisitId(res.data.visit_id);
    alert("Visit created");
    load();
  };

  const upload = async () => {
    const data = new FormData();
    data.append("folder_name", folder);

    for (let i = 0; i < files.length; i++) {
      data.append("files", files[i]);
    }

    await axios.post(`http://127.0.0.1:8000/upload/${id}/${visitId}`, data);
    alert("Uploaded");
  };

  if (!data) return <h2>Loading...</h2>;

  return (
    <>
      <div className="header">{data.name}</div>

      <div className="container">

        <div className="card">
          <h2>Create Visit</h2>
          <input placeholder="Concern" onChange={e => setConcern(e.target.value)} />
          <input type="date" onChange={e => setDate(e.target.value)} />
          <button onClick={createVisit}>Create Visit</button>
        </div>

        <div className="card">
          <h2>Visit History</h2>
          {data.visits.map(v => (
            <div key={v.visit_id}>
              {v.date} - {v.concern}
            </div>
          ))}
        </div>

        <div className="card">
          <h2>Upload Files</h2>
          <input placeholder="Folder Name (Pre / After)" onChange={e => setFolder(e.target.value)} />
          <input type="file" multiple onChange={e => setFiles(e.target.files)} />
          <button onClick={upload}>Upload</button>
        </div>

      </div>
    </>
  );
}