import axios from 'axios'
import CONFIG from '@/core/config.js'

const updateTeam = async (team) => {
    try {
        const response = await axios.put(
            `${CONFIG.BASE_URL}/teams/${team.id}`,
            team,
            { withCredentials: true }
        )
        return response.data
    } catch (error) {
        throw new Error(error.response?.data?.detail || error.message)
    }
}

export default updateTeam
