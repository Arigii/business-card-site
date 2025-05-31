import axios from "axios";
import CONFIG from "@/core/config.js";

const fetchUsers = async () => {
    try {
        const response = await axios.get(`${CONFIG.BASE_URL}/users`, {
            withCredentials: true,
        });
        return response.data;
    } catch (error) {
        if (error.response?.status === 401) {
            throw new Error("Нет доступа к пользователям (401)");
        }
        throw new Error(error.message);
    }
};

export default fetchUsers;
