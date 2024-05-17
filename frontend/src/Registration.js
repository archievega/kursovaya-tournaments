import { useState } from "react";
import { useNavigate } from 'react-router-dom';

const Registration = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: ''
    });

    const handleSubmit = async () => {
        const url = 'http://127.0.0.1:1234/api/v1/auth/register';

        const jsonData = JSON.stringify({
            email: formData.email,
            password: formData.password,
            username: formData.username
        });

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: jsonData
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail);
            }
            
            navigate('/login');

        } catch (error) {
            alert('Registration failed: ' + error.message);
        }
    };

    return (
        <div className="login-page">
            <div className="form">
                <form className="register-form">
                    <input
                        type="text"
                        placeholder="имя пользователя"
                        value={formData.username}
                        onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    />
                    <input
                        type="email"
                        placeholder="электронная почта"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    />
                    <input
                        type="password"
                        placeholder="пароль (не менее 6 символов)"
                        value={formData.password}
                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    />
                    <button type="button" onClick={handleSubmit}>create</button>
                    <p className="message">Already registered? <a href="/Login">Sign In</a></p>
                </form>
            </div>
        </div>
    );
}

export default Registration;