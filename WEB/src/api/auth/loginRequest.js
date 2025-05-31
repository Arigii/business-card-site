import axios from "axios";
import CONFIG from "../../core/config.js";

const loginUser = async (loginData) => {
    try {
        const response = await axios.post(`${CONFIG.BASE_URL}/auth/`, loginData, {
            withCredentials: true,
        });

        const { access_token, user_id } = response.data;

        return { access_token, user_id };
    } catch (error) {
        if (error.response?.status === 401) {
            throw new Error("Неверное имя пользователя или пароль");
        }

        throw new Error(error.message);
    }
};

export default loginUser;
