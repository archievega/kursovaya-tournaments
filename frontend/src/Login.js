import { useState } from "react";
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [formData, setFormData] = useState({ username: 'user@example.com', password: 'stringstring' });
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        const url = 'http://localhost:1234/api/v1/auth/login';

        const formBody = Object.keys(formData).map(key => {
            const encodedKey = encodeURIComponent(key);
            const encodedValue = encodeURIComponent(formData[key]);
            return `${encodedKey}=${encodedValue}`;
        }).join("&");

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formBody,
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
                }
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Something went wrong');
            }
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('refreshToken', data.refresh_token);
            localStorage.setItem('user_id', data.user_id);
            navigate('/tournaments');
        } catch (error) {
            console.error('Login Error:', error.message);
        }
    };

    return (
        <div className="login-page">
            <div className="form">
                <form className="login-form" onSubmit={handleSubmit}>
                    <input
                        type="email"
                        placeholder="электронная почта"
                        value={formData.username}
                        onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    />
                    <input
                        type="password"
                        placeholder="пароль (не менее 8символов)"
                        value={formData.password}
                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    />
                    <button type="submit">login</button>
                    <p className="message">
                        Не зарегистрированы? <a href="/registration">Создать аккаунт</a>
                    </p>
                </form>
            </div>
        </div>
    );
};

export default Login;