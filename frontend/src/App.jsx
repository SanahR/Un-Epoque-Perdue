/* Simple front end with space for the input, the length slider, and the output */
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [openingLine, setOpeningLine] = useState("")
  const [length, setLength] = useState(100)
  const [output, setOutput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const generateClassicalProse = async (openingLine, wordCount) => {
    if (!openingLine.trim()) {
      setError("Pray, provide an opening line for the scribe.");
      return;
    }
    setIsLoading(true);
    setError("");
    setOutput("");
    try {
      const response = await fetch("http://localhost:5001/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: openingLine,
          length: wordCount, // User-selected length
        }),
      });

      if (!response.ok) throw new Error("The manuscript was lost in transit.");

      const data = await response.json();
      setOutput(data.text);
    } catch (error) {
      console.error("Back-end error:", error);
      setError("A blot upon the page... please check your server connection.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <img src="/emblem.svg" className="logo" alt="Emblem Logo" />
      <div className="main_functioning">
        <div className="prompt_select">
          <h1 className="im-fell-dw-pica-sc-regular">Prompt and Select</h1>
          <p className="im-fell-dw-pica-regular-paragraph">Enter a prompt and select the length of the output.</p>
          <label className="opening-line-label">Opening Line:</label>
          <textarea className="opening-line-area" value={openingLine} onChange={(e) => setOpeningLine(e.target.value)} placeholder="Type your opening line here..."></textarea>
          <label className="opening-line-label">Length:</label>
          <input type="range" className="length-slider" min={50} max={1000} value={length} onChange={(e) => setLength(e.target.value)}></input>
          <p1 className="im-fell-dw-pica-regular-paragraph">{length}</p1>
          <br />
          <button
            className="generate-button"
            onClick={() => generateClassicalProse(openingLine, length)}
            disabled={isLoading}
          >
            {isLoading ? "The scribe is at work..." : "Generate Prose"}
          </button>
          {error && <p className="error-message">{error}</p>}
        </div>
        <div className="output">
          <h1 className="im-fell-dw-pica-sc-regular">The Manuscript</h1>
          <div className="output-content">
            {isLoading ? (
              <div className="scribe-loader">
                <div className="quill"></div>
                <p className="im-fell-dw-pica-regular-italic">Writing...</p>
              </div>
            ) : (
              <p className="im-fell-dw-pica-regular-paragraph manuscript-text">{openingLine} {output}</p>
            )}
          </div>
        </div>
      </div>
    </>
  )
}

export default App
