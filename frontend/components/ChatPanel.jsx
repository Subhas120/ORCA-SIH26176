import React, { useState, useEffect, useRef } from 'react';

export default function ChatPanel({ situation }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'user',
      text: 'Is it safe to go fishing tomorrow morning near Kochi?',
      time: '10:28 IST'
    },
    {
      id: 2,
      role: 'orca',
      text: 'Tomorrow morning shows heightened wind gusts up to 22 km/h and moderate wave swell around 1.2 m near Kochi coast. Nearshore waters (within 5 nm) are viable with caution, but offshore operations past 12 nm carry moderate risk due to choppy conditions.',
      confidence: '88% Confidence',
      reasoning: [
        'Moderate sea swell (1.2m) driven by south-westerly offshore breeze.',
        'Wind gusts expected between 18-24 km/h peaking at 08:30 IST.',
        'No storm cyclone advisory or naval restriction in coastal Sector 4.'
      ],
      showReasoning: false,
      time: '10:29 IST'
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const isFirstMount = useRef(true);

  // Update scenario context when scenario is applied/updated
  useEffect(() => {
    if (isFirstMount.current) {
      isFirstMount.current = false;
      return;
    }

    if (!situation) return;

    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' IST';
    const newMsgId = Date.now();

    const scenarioUserMsg = {
      id: newMsgId,
      role: 'user',
      text: `Scenario Evaluation: ${situation.activity} near ${situation.location} departing at ${situation.time} (${situation.date}) for ${situation.duration} with ${situation.vesselType} (Crew: ${situation.crewSize}).`,
      time: currentTime
    };

    setMessages(prev => [...prev, scenarioUserMsg]);
    setIsTyping(true);

    const timer = setTimeout(() => {
      const scenarioAiMsg = {
        id: newMsgId + 1,
        role: 'orca',
        text: `[Scenario Evaluation - Demo Mode] Evaluated situation for ${situation.activity} departing ${situation.location} at ${situation.time}. Given the ${situation.vesselType} with crew of ${situation.crewSize}, planned for ${situation.duration}, navigation in the ${situation.preferredZone} is recommended. Swell (1.2m) and wind (22 km/h) suggest cautious speed along the recommended route.`,
        confidence: '86% Confidence',
        reasoning: [
          `Vessel Class: ${situation.vesselType} benchmarked against coastal wave tolerance.`,
          `Time Window: ${situation.time} departure on ${situation.date} for ${situation.duration}.`,
          `Zone Alignment: Evaluated safe transit corridor targeting ${situation.preferredZone}.`
        ],
        showReasoning: false,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' IST'
      };
      setMessages(prev => [...prev, scenarioAiMsg]);
      setIsTyping(false);
    }, 600);

    return () => clearTimeout(timer);
  }, [situation]);

  const toggleReasoning = (id) => {
    setMessages(prev =>
      prev.map(m => (m.id === id ? { ...m, showReasoning: !m.showReasoning } : m))
    );
  };

  const handleSend = (e) => {
    if (e) e.preventDefault();
    if (!input.trim() || isTyping) return;

    const userQuery = input.trim();
    const newMsgId = Date.now();
    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' IST';

    setMessages(prev => [
      ...prev,
      { id: newMsgId, role: 'user', text: userQuery, time: currentTime }
    ]);
    setInput('');
    setIsTyping(true);

    setTimeout(() => {
      setMessages(prev => [
        ...prev,
        {
          id: newMsgId + 1,
          role: 'orca',
          text: `[Mock Analysis] Evaluated situation for "${userQuery}" near ${situation?.location || 'Kochi'}. Moderate swell and local wind factors recommend staying within the inner suitable zone. Monitor live alerts before voyage.`,
          confidence: '85% Confidence',
          reasoning: [
            'Simulated spatial cross-check with coastal weather radar.',
            'Ocean state benchmarked against vessel operational thresholds.'
          ],
          showReasoning: false,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' IST'
        }
      ]);
      setIsTyping(false);
    }, 800);
  };

  return (
    <div className="panel-card chat-panel-container">
      <div className="panel-header">
        <div className="panel-title-group">
          <div className="panel-title-with-icon">
            <span className="icon-badge cyan">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
              </svg>
            </span>
            <h3>ASK ORCA</h3>
          </div>
          <p className="panel-subtitle">AI-assisted marine situation analysis</p>
        </div>
        <div className="panel-tag ai-tag">ORCA AGENT ACTIVE</div>
      </div>

      <div className="chat-messages-scroll">
        {messages.map((msg) => (
          <div key={msg.id} className={`chat-bubble-row ${msg.role}`}>
            {msg.role === 'orca' && (
              <div className="avatar orca-avatar">
                <span>AI</span>
              </div>
            )}
            <div className={`chat-bubble ${msg.role}`}>
              <div className="bubble-header">
                <span className="bubble-sender">{msg.role === 'user' ? 'Operator' : 'ORCA Reasoning Agent'}</span>
                <span className="bubble-time">{msg.time}</span>
              </div>
              <p className="bubble-text">{msg.text}</p>

              {msg.role === 'orca' && (
                <div className="ai-response-meta">
                  <span className="confidence-pill">{msg.confidence}</span>
                  {msg.reasoning && (
                    <button
                      type="button"
                      className="reasoning-toggle-btn"
                      onClick={() => toggleReasoning(msg.id)}
                    >
                      {msg.showReasoning ? 'Hide reasoning ▴' : 'View reasoning ▾'}
                    </button>
                  )}
                </div>
              )}

              {msg.showReasoning && msg.reasoning && (
                <div className="reasoning-drawer">
                  <div className="reasoning-title">Key Reasoning Factors:</div>
                  <ul>
                    {msg.reasoning.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
            {msg.role === 'user' && (
              <div className="avatar user-avatar">
                <span>OP</span>
              </div>
            )}
          </div>
        ))}

        {isTyping && (
          <div className="chat-bubble-row orca">
            <div className="avatar orca-avatar">
              <span>AI</span>
            </div>
            <div className="chat-bubble orca typing-indicator">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </div>
          </div>
        )}
      </div>

      <form className="chat-input-form" onSubmit={handleSend}>
        <div className="input-wrapper">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about marine conditions..."
            className="marine-input"
          />
          <button type="submit" className="marine-send-btn" disabled={!input.trim() || isTyping}>
            <span>Send</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </form>

      <div className="chat-disclaimer">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <span>AI explains conditions; deterministic safety rules determine final risk.</span>
      </div>
    </div>
  );
}
