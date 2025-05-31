import axios from 'axios'
import CONFIG from '../../core/config.js'

const getUserProfile = async (user_id, token) => {
    try {
        const response = await axios.get(`${CONFIG.BASE_URL}/profiles/${user_id}/`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        return response.data
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Ошибка получения профиля')
    }
}

export default getUserProfile
