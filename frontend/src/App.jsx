import { useState } from "react";
import Logs from "./Logs";

function App() {
  // ✅ All hooks first
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState("chat");
  const isAdmin = false; // change to true when you want to see logs


  const askAgent = async () => {
    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_id: 1,
          question: question
        })
      });

      const data = await response.json();
      console.log("Backend response:", data);

      setAnswer(data.answer || "No answer returned.");

    } catch (error) {
      console.error("Error:", error);
      setAnswer("Something went wrong.");

    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "40px", textAlign: "left" }}>
      
      {isAdmin && <button onClick={() => setView("logs")}>Logs</button>}

      
        <>
          <h1>Clinical Intelligence Agent</h1>
          <textarea
            rows="4"
            cols="60"
            placeholder="Ask a question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <br /><br />
          <button onClick={askAgent} disabled={loading}>
            {loading ? "Thinking..." : "Ask"}
          </button>

          {answer && <p><b>Answer:</b> {answer}</p>}
        </>
     

      {view === "logs" && <Logs />}
    </div>
  );
}

export default App;
