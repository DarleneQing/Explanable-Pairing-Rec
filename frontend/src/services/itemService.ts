import api from './axios';

export const itemService = {
    async getItemMetadata(itemId: string) {
        await api.get(`/items/${itemId}`, {

        }).then(async (response) => {
            return response.data;
        }).catch((error) => {
            console.error('Error fetching item metadata:', error);
            throw error;
        });
    }
}
