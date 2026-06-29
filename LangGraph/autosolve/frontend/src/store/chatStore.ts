import { create } from 'zustand';

export interface ChatMessage {
  id: string;
  role: 'user' | 'agent' | 'tool' | 'system';
  content: string;
  toolName?: string;
  toolOutput?: string;
}

interface ChatState {
  messages: ChatMessage[];
  isTyping: boolean;
  addMessage: (msg: ChatMessage) => void;
  appendToken: (id: string, token: string) => void;
  setTyping: (typing: boolean) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isTyping: false,
  addMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),
  appendToken: (id, token) => set((state) => ({
    messages: state.messages.map(m => 
      m.id === id ? { ...m, content: m.content + token } : m
    )
  })),
  setTyping: (typing) => set({ isTyping: typing }),
}));
