import { useEffect, useState } from "react";

function Logs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/logs")
      .then((res) => res.json())
      .then((data) => setLogs(data));
  }, []);

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h2>Query Logs</h2>

      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>ID</th>
            <th>User</th>
            <th>Question</th>
            <th>Answer</th>
            <th>Action</th>
            <th>Confidence</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log) => (
            <tr key={log.id}>
              <td>{log.id}</td>
              <td>{log.user_id}</td>
              <td>{log.query}</td>
              <td>{log.answer}</td>
              <td>{log.action}</td>
              <td>{log.confidence}</td>
              <td>{new Date(log.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Logs;
