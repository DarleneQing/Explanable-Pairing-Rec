import { defineStore } from 'pinia';
import { ref } from 'vue';
import { Session } from '../types/Session';
import { sessionService } from '../services/sessionService';

export const useSessionStore = defineStore('session', () => {
    const session = ref<Session | null>(null);

    const initializeSession = async () => {
        if (session.value) {
            session.value.is_active = true;
            if (session.value.session_id) {
                localStorage.setItem('sessionId', session.value.session_id);
                // Store the entire session data in localStorage for persistence
                localStorage.setItem('sessionData', JSON.stringify(session.value.toApiData()));
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

    const updateSessionData = async (userData: { name: string, section: string, garment_group: string }) => {
        if (!session.value) {
            throw new Error('No active session found');
        }

        try {
            // Update session on backend
            session.value = await sessionService.updateSession(session.value.session_id, {
                name: userData.name,
                section: userData.section,
                garment_group: userData.garment_group
            });

            // Persist updated data to localStorage
            localStorage.setItem('sessionData', JSON.stringify(session.value.toApiData()));
            
            return session.value;
        } catch (error) {
            console.error('Failed to update session:', error);
            throw error;
        }
    }

    const updateProductType = async (productType: string) => {
        if (!session.value) {
            throw new Error('No active session found');
        }

        try {
            // Update session on backend
            session.value = await sessionService.updateSession(session.value.session_id, {
                name: session.value.name,
                section: session.value.section,
                garment_group: session.value.garment_group,
                product_type: productType
            });

            // Persist updated data to localStorage
            localStorage.setItem('sessionData', JSON.stringify(session.value.toApiData()));
            
            return session.value;
        } catch (error) {
            console.error('Failed to update product type:', error);
            throw error;
        }
    }

    const updateColor = async (color: string) => {
        if (!session.value) {
            throw new Error('No active session found');
        }

        try {
            // Update session on backend
            session.value = await sessionService.updateSession(session.value.session_id, {
                name: session.value.name,
                section: session.value.section,
                garment_group: session.value.garment_group,
                product_type: session.value.product_type,
                color: color
            });

            // Persist updated data to localStorage
            localStorage.setItem('sessionData', JSON.stringify(session.value.toApiData()));
            
            return session.value;
        } catch (error) {
            console.error('Failed to update color:', error);
            throw error;
        }
    }

    const updateGraphicAppearance = async (graphicAppearance: string) => {
        if (!session.value) {
            throw new Error('No active session found');
        }

        try {
            // Update session on backend
            session.value = await sessionService.updateSession(session.value.session_id, {
                name: session.value.name,
                section: session.value.section,
                garment_group: session.value.garment_group,
                product_type: session.value.product_type,
                color: session.value.color,
                graphic_appearance: graphicAppearance
            });

            // Persist updated data to localStorage
            localStorage.setItem('sessionData', JSON.stringify(session.value.toApiData()));
            
            return session.value;
        } catch (error) {
            console.error('Failed to update graphic appearance:', error);
            throw error;
        }
    }

    const loadStoredSession = async () => {
        const storedSessionId = localStorage.getItem('sessionId');
        
        if (storedSessionId) {
            try {
                // Try to fetch the latest session data from backend first
                session.value = await sessionService.getSession(storedSessionId);
                console.log('Loaded session from backend:', session.value);
                
                // Update localStorage with latest data
                localStorage.setItem('sessionData', JSON.stringify(session.value.toApiData()));
                
            } catch (error) {
                console.warn('Failed to load session from backend, trying localStorage:', error);
                
                // Fallback to localStorage if backend fails
                const storedSessionData = localStorage.getItem('sessionData');
                if (storedSessionData) {
                    try {
                        const sessionData = JSON.parse(storedSessionData);
                        session.value = Session.fromApiResponse(sessionData);
                        console.log('Loaded stored session from localStorage:', session.value);
                    } catch (parseError) {
                        console.error('Failed to parse stored session data:', parseError);
                        // Clear invalid data
                        localStorage.removeItem('sessionData');
                        localStorage.removeItem('sessionId');
                    }
                }
            }
        }
    }

    const clearSession = () => {
        session.value = null;
        localStorage.removeItem('sessionId');
        localStorage.removeItem('sessionData');
    }

    return {
        session,
        initializeSession,
        createSession,
        updateSessionData,
        updateProductType,
        updateColor,
        updateGraphicAppearance,
        loadStoredSession,
        clearSession,
    }
});
