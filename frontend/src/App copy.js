import { useState } from "react"
import { useCookies } from 'react-cookie';
import User from './User'

const Registration = () => {
    const [cookies, setCookie] = useCookies(['token']);
    const setJwtToken = (token) => {
        setCookie('token', token, { expires: 7 }); // 7 дней
    };
    const getJwtToken = () => {
        return cookies.token;
    };
    const [formdata, setFormdata] = useState({
        username: 'sadfas',
        password: 'asfafsasadsf',
        email: 'sdfdsgs@gmail.com',
        role: 'PLAYER',
    })
    const handleSubmit = () => {
        const url = 'http://213.171.3.136/api/v1/auth/register';
        const getFormDataAsJson = () => {
            const { username, password, email, role } = formdata;
            return ({ username, password, email, role });
            // return JSON.stringify({ username, password, email, role });
        };
        const jsonData = getFormDataAsJson();
        // const jsonData = JSON.stringify(formdata);
        // let a = JSON.stringify({ username: "sss33ss@gmail.com", email: "sss33ss@gmail.com", password: "sssss@gmail.com", role: "PLAYER" })
        // alert(a);

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData,
        })
            .then((response) => {
                if (response.ok) {
                    alert(response.body)
                    console.log(response.body)
                    // const token = response.body.get('access_token');
                    // if (token) {
                    //     setJwtToken(token);
                    // return <User username = {formdata.username} />
                    window.location.href = '/home';
                    // }
                }
            })
            .catch((error) => {
                alert('lox')
                window.location.href = '/home';
                console.error('Ошибка:', error.message);
            });


    };
    return (
        <>
            <div class="login-page">
                <div class="form">
                    <form class="register-form" action=' http://213.171.3.136/api/v1/auth/register' method='post'>
                        <input type="text" placeholder="имя пользователя" value={formdata.username} onChange={(e) => setFormdata({ ...formdata, username: e.target.value })} />
                        <input type="password" placeholder="пароль (не менее 6 символов)" value={formdata.password} onChange={(e) => setFormdata({ ...formdata, password: e.target.value })} />
                        <input type="email" placeholder="электронная почта" value={formdata.email} onChange={(e) => setFormdata({ ...formdata, email: e.target.value })} />
                        <input type="text" placeholder="роль" value={formdata.role} onChange={(e) => setFormdata({ ...formdata, role: e.target.value })} />
                        <button onClick={handleSubmit}>create</button>
                        <p class="message">Already registered? <a href="/Login">Sign In</a></p>
                    </form>
                </div>
            </div >
        </>
    )
}

export default Registration