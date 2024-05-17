const securedFetch = async (url, options = {}) => {
    const token = localStorage.getItem('token'); // Получаем токен из хранилища
    const refreshToken = localStorage.getItem('refreshToken'); // Получаем refresh token из хранилища

    // Функция для получения нового access token с использованием refresh token
    const getNewAccessToken = async () => {
        try {
            const response = await fetch('http://localhost:1234/api/v1/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh_token: refreshToken }),
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to refresh token');
            }
            localStorage.setItem('token', data.access_token); // Сохраняем новый access token
            localStorage.setItem('refreshToken', data.refresh_token);
            return data.access_token;
        } catch (error) {
            console.error('Error refreshing token:', error);
            throw error;
        }
    };

    // Обновляем заголовки запроса для включения access token
    const headers = new Headers(options.headers || {});
    if (token) {
        headers.append('Authorization', `Bearer ${token}`);
    }

    // Дополняем переданные опции новыми заголовками
    let updatedOptions = { ...options, headers };

    try {
        // Делаем запрос с текущим access token
        let response = await fetch(url, updatedOptions);
        if (response.status === 401) {
            // Если получили 401 ошибку, пытаемся обновить access token
            try {
                const newAccessToken = await getNewAccessToken();
                headers.set('Authorization', `Bearer ${newAccessToken}`);
                updatedOptions = { ...options, headers };
                response = await fetch(url, updatedOptions); // Повторяем запрос с новым токеном
            } catch (refreshError) {
                // Если обновление токена не удалось, перенаправляем на страницу логина
                window.location.href = '/login';
                throw refreshError;
            }
        }
        const data = await response.json();
        return { ok: response.ok, status: response.status, data };
    } catch (error) {
        console.error('Error making secured fetch:', error);
        throw error; // Перебрасываем ошибку для обработки в вызывающем коде
    }
};

export default securedFetch;