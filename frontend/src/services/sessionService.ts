import api from './axios';
import { Session } from '@/types/Session';

export const sessionService = {
    async createSession(): Promise<Session> {
        const response = await api.post('/session');
        return Session.fromApiResponse(response.data);
    },

    async updateSession(sessionId: string, sessionData: { name?: string, section?: string, garment_group?: string, product_type?: string, color?: string, graphic_appearance?: string }): Promise<Session> {
        const response = await api.put(`/session/${sessionId}`, sessionData);
        return Session.fromApiResponse(response.data);
    },

    async getSession(sessionId: string): Promise<Session> {
        const response = await api.get(`/session/${sessionId}`);
        return Session.fromApiResponse(response.data);
    }
}

