import api from './axios';
import { Session } from '@/types/Session';

export const sessionService = {
    async createSession(): Promise<Session> {
        const response = await api.post('/session');
        return Session.fromApiResponse(response.data);
    }
}

