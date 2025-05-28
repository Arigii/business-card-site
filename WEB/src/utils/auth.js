export const decodeToken = (token) => {
    try {
        const base64Url = token.split('.')[1]
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
        const jsonPayload = decodeURIComponent(
            atob(base64)
                .split('')
                .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                .join('')
        )
        return JSON.parse(jsonPayload)
    } catch (error) {
        console.error('Ошибка декодирования токена:', error)
        return null
    }
}

export const getUserRole = () => {
    const token = localStorage.getItem('access_token')
    if (!token) return null

    const decoded = decodeToken(token)
    return decoded?.role || null
}



export const isAuthenticated = () => {
    return !!localStorage.getItem('access_token')
}


export const isAdmin = () => {
    return getUserRole() === 'admin'
}