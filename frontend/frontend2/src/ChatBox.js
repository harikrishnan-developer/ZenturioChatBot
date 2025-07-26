import axios from 'axios';
import { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './ChatBox.css';
import { FaUser, FaRobot, FaDownload } from 'react-icons/fa';
import jsPDF from 'jspdf';

// Helper to convert Markdown to plain text for PDF
function markdownToPlain(text) {
  return text
    .replace(/^#+\s?/gm, '') // Remove headings
    .replace(/\*\*(.*?)\*\*/g, '$1') // Bold
    .replace(/\*(.*?)\*/g, '$1') // Italic
    .replace(/\[(.*?)\]\((.*?)\)/g, '$1 ($2)') // Links
    .replace(/^- /gm, '\u2022 ') // Bullet points
    .replace(/\r?\n/g, '\n'); // Normalize line breaks
}

// Add this helper function before the ChatBox component
function extractServiceName(botText) {
  const match = botText.match(/Service:\s*(.*)/i);
  return match ? match[1].split('\n')[0] : "";
}

// Add this helper function before the ChatBox component
function getLastUserMessage(messages) {
  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i].sender === "You") {
      return messages[i].text;
    }
  }
  return "";
}

export default function ChatBox() {
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem('chatHistory');
    return saved ? JSON.parse(saved) : [];
  });
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [showComplaint, setShowComplaint] = useState(false);
  const [complaint, setComplaint] = useState({ name: '', contact: '', service: '', complaint_text: '', email: '' });
  const [complaintStatus, setComplaintStatus] = useState(null);
  const [showTrack, setShowTrack] = useState(false);
  const [trackInput, setTrackInput] = useState({ complaint_id: '', contact: '' });
  const [trackResult, setTrackResult] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  const toggleDarkMode = () => setDarkMode(d => !d);
  const chatEndRef = useRef(null);

  // Save chat history to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('chatHistory', JSON.stringify(messages));
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "You", text: input };
    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);

    const res = await axios.post(
      "https://zenturiochatbot.onrender.com/ask",
      { message: input },
      { headers: { 'X-Frontend': 'web' } }
    );
    const botText = res.data.reply;
    const lines = botText.split(/\r?\n/).filter(line => line.trim() !== "");
    let currentText = "";
    let lineIdx = 0;
    const showNextLine = () => {
      if (lineIdx < lines.length) {
        currentText += (currentText ? "\n" : "") + lines[lineIdx];
        setMessages(prev => {
          // Remove the last bot message if it's still being built
          const last = prev[prev.length - 1];
          if (last && last.sender === "Bot" && last.incomplete) {
            return [...prev.slice(0, -1), { sender: "Bot", text: currentText, incomplete: true }];
          } else {
            return [...prev, { sender: "Bot", text: currentText, incomplete: true }];
          }
        });
        lineIdx++;
        setTimeout(showNextLine, 150); // 150ms per line (was 400ms)
      } else {
        // Mark the last bot message as complete
        setMessages(prev => {
          const last = prev[prev.length - 1];
          if (last && last.sender === "Bot" && last.incomplete) {
            return [...prev.slice(0, -1), { sender: "Bot", text: currentText }];
          }
          return prev;
        });
        setIsTyping(false);
      }
    };
    showNextLine();
    setInput("");
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleComplaintChange = e => {
    setComplaint({ ...complaint, [e.target.name]: e.target.value });
  };

  const submitComplaint = async e => {
    e.preventDefault();
    setComplaintStatus(null);
    try {
      const res = await axios.post('https://zenturiochatbot.onrender.com/register_complaint', complaint);
      setComplaintStatus(res.data.message + (res.data.complaint_id ? `\nYour Complaint ID: ${res.data.complaint_id}` : ''));
      if (res.data.success) {
        setComplaint({ name: '', contact: '', service: '', complaint_text: '', email: '' });
        setShowComplaint(false);
        // Show complaint ID in chat as bot message
        setMessages(prev => [...prev, { sender: "Bot", text: `Your complaint has been registered.\nComplaint ID: ${res.data.complaint_id}` }]);
      }
    } catch (err) {
      setComplaintStatus('Error submitting complaint.');
    }
  };

  const handleTrackChange = e => {
    setTrackInput({ ...trackInput, [e.target.name]: e.target.value });
  };

  const submitTrack = async e => {
    e.preventDefault();
    setTrackResult(null);
    try {
      const res = await axios.post('https://zenturiochatbot.onrender.com/track_complaint', trackInput);
      setTrackResult(res.data);
    } catch (err) {
      setTrackResult({ success: false, message: 'Error tracking complaint.' });
    }
  };

  const downloadPdf = (msg, idx) => {
    const doc = new jsPDF();
    doc.setFontSize(14);
    doc.text(`Bot:`, 10, 20);
    doc.setFont('helvetica', 'normal');
    const plain = markdownToPlain(msg.text);
    doc.text(plain, 10, 35, { maxWidth: 180 });
    doc.save(`chat-reply-${idx + 1}.pdf`);
  };

  // Find the last bot message
  const getLastBotMessage = () => {
    for (let i = messages.length - 1; i >= 0; i--) {
      if (messages[i].sender === "Bot") {
        return messages[i].text;
      }
    }
    return "";
  };

  // Open complaint modal and pre-fill service field with last user question
  const handleOpenComplaint = () => {
    // Try to extract service name from the last bot message
    const lastBotMsg = getLastBotMessage();
    let serviceName = "";
    if (lastBotMsg) {
      serviceName = extractServiceName(lastBotMsg);
    }
    // Fallback: try to extract from last user message
    if (!serviceName) {
      let lastUserMsg = getLastUserMessage(messages);
      // Try to extract a likely service name from the user message
      serviceName = lastUserMsg
        .replace(/how to apply for /i, "")
        .replace(/how to get /i, "")
        .replace(/i want to apply for /i, "")
        .replace(/application for /i, "")
        .replace(/apply for /i, "")
        .replace(/register for /i, "")
        .replace(/registration for /i, "")
        .replace(/\?$/, "") // remove trailing question mark
        .trim();
      // If still empty, use the full last user message
      if (!serviceName) {
        serviceName = lastUserMsg;
      }
    }
    setComplaint({
      ...complaint,
      service: serviceName
    });
    setShowComplaint(true);
  };

  return (
    <div className={`chat-container${darkMode ? ' dark' : ''}`}>
      <div className="chat-header">
        {/* <img src="/favicon.ico" alt="Kerala Icon" className="chat-logo" /> */}
        <span className="chat-title">Kerala Services Chat</span>
        <div className="mode-switch">
          <span
            className={`mode-dot${!darkMode ? ' active' : ''}`}
            title="Light Mode"
            onClick={() => setDarkMode(false)}
            style={{ cursor: 'pointer', marginRight: 8 }}
          >
            &#9679;
          </span>
          <span
            className={`mode-dot${darkMode ? ' active' : ''}`}
            title="Dark Mode"
            onClick={() => setDarkMode(true)}
            style={{ cursor: 'pointer' }}
          >
            &#9679;
          </span>
        </div>
        <button className="complaint-btn" onClick={handleOpenComplaint}>Register Complaint</button>
        <button className="track-btn" onClick={() => setShowTrack(true)}>Track Complaint</button>
      </div>
      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.sender === "You" ? 'user' : 'bot'}`}>
            <span className="avatar">
              {msg.sender === "You" ? <FaUser /> : <FaRobot />}
            </span>
            <div className="message-content">
              <b>{msg.sender}:</b>{" "}
              {msg.sender === "Bot"
                ? <ReactMarkdown>{msg.text}</ReactMarkdown>
                : msg.text}
            </div>
            {msg.sender === "Bot" && (
              <button className="download-btn" title="Download as PDF" onClick={() => downloadPdf(msg, i)}>
                <FaDownload />
              </button>
            )}
          </div>
        ))}
        {isTyping && <div className="typing-indicator">Bot is typing...</div>}
        <div ref={chatEndRef} />
      </div>
      <div className="input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyDown={e => {
            if (e.key === 'Enter') sendMessage();
          }}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
      {/* Complaint Modal */}
      {showComplaint && (
        <div className="complaint-modal">
          <div className="complaint-modal-content">
            <h2>Register Complaint</h2>
            <form onSubmit={submitComplaint}>
              <input name="name" value={complaint.name} onChange={handleComplaintChange} placeholder="Your Name" />
              <input name="contact" value={complaint.contact} onChange={handleComplaintChange} placeholder="Contact" />
              <input name="service" value={complaint.service} onChange={handleComplaintChange} placeholder="Service" required />
              <input name="email" value={complaint.email} onChange={handleComplaintChange} placeholder="Your Email (optional)" type="email" />
              <textarea name="complaint_text" value={complaint.complaint_text} onChange={handleComplaintChange} placeholder="Complaint" required />
              <button type="submit">Submit</button>
              <button type="button" onClick={() => { setShowComplaint(false); setComplaintStatus(null); }}>Cancel</button>
            </form>
            {complaintStatus && <div className="complaint-status">{complaintStatus}</div>}
          </div>
        </div>
      )}
      {/* Track Complaint Modal */}
      {showTrack && (
        <div className="complaint-modal">
          <div className="complaint-modal-content">
            <h2>Track Complaint</h2>
            <form onSubmit={submitTrack}>
              <input name="complaint_id" value={trackInput.complaint_id} onChange={handleTrackChange} placeholder="Complaint ID" />
              <input name="contact" value={trackInput.contact} onChange={handleTrackChange} placeholder="Contact (optional)" />
              <button type="submit">Track</button>
              <button type="button" onClick={() => { setShowTrack(false); setTrackResult(null); }}>Cancel</button>
            </form>
            {trackResult && (
              <div className="complaint-status">
                {trackResult.success ? (
                  <div>
                    <b>Status:</b> Complaint found<br/>
                    <b>ID:</b> {trackResult.complaint._id}<br/>
                    <b>Name:</b> {trackResult.complaint.name}<br/>
                    <b>Contact:</b> {trackResult.complaint.contact}<br/>
                    <b>Service:</b> {trackResult.complaint.service}<br/>
                    <b>Complaint:</b> {trackResult.complaint.complaint_text}
                  </div>
                ) : (
                  <div>{trackResult.message}</div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
