import axios from "axios";
import CONFIG from "@/core/config.js";

const fetchProjects = async () => {
    try {
        const response = await axios.get(`${CONFIG.BASE_URL}/projects`, {
            withCredentials: true,
        });
        return response.data;
    } catch (error) {
        if (error.response?.status === 401) {
            throw new Error("Нет доступа к проектам (401)");
        }
        throw new Error(error.message);
    }
};

export default fetchProjects;
