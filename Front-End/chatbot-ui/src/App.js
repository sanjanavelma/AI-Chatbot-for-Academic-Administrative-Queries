import React, { useState } from "react";
import "./App.css";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // Chat send
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      if (!res.ok) throw new Error("Chat request failed");

      const data = await res.json();
      const botMsg = { sender: "bot", text: data.reply };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error("Chat error:", err);
      alert("Chat failed — see console");
    }

    setLoading(false);
  };

  // PDF upload
  const uploadPDF = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data.error || "Upload failed");

      alert(data.message || "PDF uploaded successfully!");
    } catch (err) {
      console.error("Upload error:", err);
      alert("Upload failed — check backend terminal");
    }
  };

  return (
    <div className="app">

      {/* Sidebar */}
      <div className="sidebar">
        <h2 className="logo">Campus AI</h2>

        <button className="new-chat">+ New Chat</button>

        {/* Upload button */}
        <label className="upload-btn">
          Upload PDF
          <input
            type="file"
            accept=".pdf"
            hidden
            onChange={uploadPDF}
          />
        </label>
      </div>

      {/* Chat Area */}
      <div className="chat-area">

        <div className="chat-box">

          {messages.length === 0 && (
            <div className="welcome">
              <h1>AI Academic Assistant</h1>
              <p>Ask anything about syllabus, rules, exams…</p>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`message-row ${msg.sender}`}>
              <div className={`bubble ${msg.sender}`}>

                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    code({ inline, className, children }) {
                      const match = /language-(\w+)/.exec(className || "");
                      return !inline ? (
                        <SyntaxHighlighter
                          style={oneDark}
                          language={match?.[1]}
                          PreTag="div"
                        >
                          {String(children).replace(/\n$/, "")}
                        </SyntaxHighlighter>
                      ) : (
                        <code className="inline-code">{children}</code>
                      );
                    },
                  }}
                >
                  {msg.text}
                </ReactMarkdown>

              </div>
            </div>
          ))}

          {loading && (
            <div className="typing">AI is typing…</div>
          )}

        </div>

        {/* Input bar */}
        <div className="input-bar">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask something..."
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>

      </div>
    </div>
  );
}

export default App;
