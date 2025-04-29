import axios from "axios";
import CONFIG from "../../core/config.js";

const loginUser = async (loginData) => {
    try {
        const response = await axios.post(`${CONFIG.BASE_URL}/auth/`, loginData, {
            withCredentials: true,
        });
        return response.data.access_token;
    } catch (error) {
        if (error.status === 401) {
            throw new Error("Неверное имя пользователя или пароль")
        }

        throw new Error(error.message);
    }
};

export default loginUser;
