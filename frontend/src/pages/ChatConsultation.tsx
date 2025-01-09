import React, { useState } from "react";
import axios from "../api/axios"; // Import the configured Axios instance
import { Send, User, Bot } from "lucide-react";

const ChatConsultation = () => {
  const [messages, setMessages] = useState([
    {
      type: "bot",
      content: "Hello! I'm your AI therapy assistant. How are you feeling today?",
    },
  ]);
  const [input, setInput] = useState("");

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;

    // Append user message to the chat
    setMessages([...messages, { type: "user", content: userMessage }]);
    setInput("");

    try {
      // Call Django API
      const response = await axios.post("/chat/", {
        message: userMessage,
      });

      // Append bot's response to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: "bot", content: response.data.response },
      ]);
    } catch (error) {
      console.error("Error communicating with the API", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: "bot", content: "Sorry, something went wrong. Please try again." },
      ]);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="p-4 bg-indigo-600">
          <h1 className="text-xl font-semibold text-white">Chat Therapy Session</h1>
        </div>

        <div className="h-[600px] flex flex-col">
          <div className="flex-1 p-4 overflow-y-auto space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex items-start space-x-2 ${
                  message.type === "user"
                    ? "flex-row-reverse space-x-reverse"
                    : ""
                }`}
              >
                <div
                  className={`p-2 rounded-lg max-w-[80%] ${
                    message.type === "user"
                      ? "bg-indigo-600 text-white"
                      : "bg-gray-100 text-gray-900"
                  }`}
                >
                  <div className="flex items-center space-x-2 mb-1">
                    {message.type === "user" ? (
                      <User className="w-4 h-4" />
                    ) : (
                      <Bot className="w-4 h-4" />
                    )}
                    <span className="font-medium">
                      {message.type === "user" ? "You" : "TherapyNest AI"}
                    </span>
                  </div>
                  <p>{message.content}</p>
                </div>
              </div>
            ))}
          </div>

          <form onSubmit={handleSend} className="p-4 border-t">
            <div className="flex space-x-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <button
                type="submit"
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatConsultation;
