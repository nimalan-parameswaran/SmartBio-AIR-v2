import React, { useState, useRef, useEffect } from "react";
import { MessageSquare, Send, Sparkles, User, Bot, X } from "lucide-react";
import { apiService } from "../services/api";

interface Message {
  role: "user" | "model";
  content: string;
}

export default function ChatWindow() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "model",
      content: "Hello! I am your Bioreactor AI Research Assistant. You can ask me questions about the current algae culture density, water temperature ranges, motor load states, or gas filtration rates."
    }
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (open) scrollToBottom();
  }, [messages, open]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    try {
      // Map message roles for backend matching
      const historyFormatted = messages.map((m) => ({
        role: m.role === "model" ? "model" : "user",
        content: m.content
      }));

      const reply = await apiService.askAI(userMsg, historyFormatted);
      setMessages((prev) => [...prev, { role: "model", content: reply }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "model", content: "Error communicating with AI services. Check that the backend server is running." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-40 p-4 bg-emerald-500 hover:bg-emerald-600 text-black font-semibold rounded-full shadow-lg hover:shadow-emerald-500/25 flex items-center justify-center gap-2 border border-emerald-400/20 active:scale-95 transition-all cursor-pointer"
      >
        <MessageSquare className="w-5 h-5 fill-black" />
        <span className="text-xs uppercase tracking-wider hidden md:inline">Ask AI Assistant</span>
        <span className="absolute top-0 right-0 w-2.5 h-2.5 bg-cyan-400 rounded-full border border-black animate-ping"></span>
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 z-50 w-96 max-w-[calc(100vw-3rem)] h-[480px] bg-[#0c120e]/95 border border-[#1e3226] shadow-2xl rounded-2xl flex flex-col backdrop-blur-xl overflow-hidden">
      {/* Header */}
      <div className="bg-[#121c16] border-b border-[#1e3226] p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-emerald-400 animate-pulse" />
          <div>
            <h3 className="font-bold text-xs text-emerald-400 tracking-wider uppercase">AI Research Assistant</h3>
            <span className="text-[9px] text-[#7ea18b] uppercase tracking-widest font-mono">Gemini-Powered</span>
          </div>
        </div>
        <button 
          onClick={() => setOpen(false)}
          className="p-1 hover:bg-[#1c2920] rounded-md text-[#7ea18b] hover:text-white transition-colors cursor-pointer"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 p-4 overflow-y-auto space-y-3.5 scrollbar">
        {messages.map((m, i) => {
          const isModel = m.role === "model";
          return (
            <div key={i} className={`flex gap-2.5 items-start ${isModel ? "" : "flex-row-reverse"}`}>
              {/* Avatar */}
              <div className={`w-6 h-6 rounded-md flex items-center justify-center flex-shrink-0 border ${
                isModel 
                  ? "bg-emerald-950/20 border-emerald-900/30 text-emerald-400" 
                  : "bg-cyan-950/20 border-cyan-900/30 text-cyan-400"
              }`}>
                {isModel ? <Bot className="w-3.5 h-3.5" /> : <User className="w-3.5 h-3.5" />}
              </div>
              
              {/* Message text */}
              <div className={`p-2.5 rounded-lg text-xs leading-normal max-w-[75%] border ${
                isModel
                  ? "bg-[#121c16]/30 border-[#1e3226] text-[#e2f0e7]"
                  : "bg-cyan-950/10 border-cyan-900/30 text-cyan-200"
              }`}>
                <p className="whitespace-pre-wrap">{m.content}</p>
              </div>
            </div>
          );
        })}
        {loading && (
          <div className="flex gap-2.5 items-start">
            <div className="w-6 h-6 rounded-md bg-emerald-950/20 border border-emerald-900/30 text-emerald-400 flex items-center justify-center flex-shrink-0 animate-pulse">
              <Bot className="w-3.5 h-3.5" />
            </div>
            <div className="bg-[#121c16]/30 border border-[#1e3226] p-2.5 rounded-lg text-xs flex gap-1 items-center text-[#7ea18b]">
              <span className="w-1.5 h-1.5 bg-[#7ea18b] rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-1.5 h-1.5 bg-[#7ea18b] rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-1.5 h-1.5 bg-[#7ea18b] rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSend} className="p-3 border-t border-[#1e3226] bg-[#0c120e] flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          className="flex-1 bg-[#121c16] border border-[#1e3226] rounded-lg px-3 py-2 text-xs text-[#e2f0e7] placeholder-[#7ea18b]/60 focus:outline-none focus:border-emerald-500/50"
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="p-2 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-black rounded-lg flex items-center justify-center transition-colors cursor-pointer"
        >
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
}
