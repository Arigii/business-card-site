import axios from "axios";
import CONFIG from "@/core/config.js";

const fetchTeams = async () => {
    try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(`${CONFIG.BASE_URL}/teams`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        return response.data;
    } catch (error) {
        if (error.response?.status === 401) {
            throw new Error("Нет доступа к командам (401)");
        } else if (error.response?.status === 403) {
            throw new Error("Доступ запрещён (403)");
        }
        throw new Error(error.message);
    }
};

export default fetchTeams;
