// src/services/chatService.js

/**
 * Service for handling communication with the knowledge-assistant-service API
 */
export class ChatService {
  /**
   * @param {string} baseUrl - Base URL of the API (no trailing slash)
   */
  constructor(baseUrl = 'http://localhost:8000') {
    // Ensure no trailing slash on the base URL
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.endpoints = {
      chat: '/api/chat',
      history: '/api/chat/history',
    };
  }

  /**
   * Send a message to the knowledge assistant service
   * @param {string} message - User message
   * @param {string} [sessionId] - Optional session ID for conversation context
   * @returns {Promise<object>} - Parsed JSON response from the API
   * @throws {Error} - If the network request fails or returns a non-OK status
   */
  async sendMessage(message, sessionId = null) {
    const endpoint = this.endpoints.chat;
    // Only spread the session_id field if sessionId is truthy
    const payload = {
      message,
      ...(sessionId ? { session_id: sessionId } : {})
    };

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to send message');
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  /**
   * Get chat history for a session
   * @param {string} sessionId - Session ID
   * @returns {Promise<object[]>} - Array of chat messages
   * @throws {Error} - If the network request fails or returns a non-OK status
   */
  async getChatHistory(sessionId) {
    const endpoint = this.endpoints.history;
    const url = `${this.baseUrl}${endpoint}?session_id=${encodeURIComponent(sessionId)}`;

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to fetch chat history');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching chat history:', error);
      throw error;
    }
  }
}

// Export a singleton instance for easy import
const chatService = new ChatService();
export default chatService;