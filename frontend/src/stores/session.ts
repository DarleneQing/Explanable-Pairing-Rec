import { defineStore } from 'pinia';
import { ref } from 'vue';
import { Session } from '../types/Session';
import { sessionService } from '../services/sessionService';

export const useSessionStore = defineStore('session', () => {
    const session = ref<Session | null>(null);
    const storedSessionId = localStorage.getItem('sessionId');

    const initializeSession = async () => {
        if (session.value) {
            session.value.is_active = true;
            if (session.value.session_id) {
                localStorage.setItem('sessionId', session.value.session_id);
            }
        }
    }

    const createSession = async () => {
        try {
            session.value = await sessionService.createSession();
            await initializeSession();
            return session.value;
        } catch (error) {
            console.error('Failed to create session:', error);
            throw error;
        }
    }

    const loadStoredSession = () => {
        if (storedSessionId) {
            // You might want to validate this session with the backend later
            console.log('Found stored session ID:', storedSessionId);
        }
    }

    return {
        session,
        initializeSession,
        createSession,
        loadStoredSession,
    }
});
