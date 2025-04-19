// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ChatProvider } from './context/ChatContext';
import ChatPage from './pages/ChatPage';
import Layout from './components/Layout/Layout';
import NotFoundPage from './pages/NotFoundPage';

function App() {
  return (
    <Router>
      <ChatProvider>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<ChatPage />} />
            <Route path="/chat/:sessionId?" element={<ChatPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </ChatProvider>
    </Router>
  );
}

export default App;