import { useState } from "react"
import { useCookies } from 'react-cookie';
import User from './User'


const Registration = () => {
    const [token, setToken] = useState();
    const [cookies, setCookie] = useCookies(['token']);
    const [formdata, setFormdata] = useState({
        username: 'sadf122casasd',
        password: 'asfa21213fsasadsf',
        email: 'sdfdsdads11c1sgs@gmail.com',
        role: 'PLAYER',
    })
    const handleSubmit = () => {
        const url = 'http://213.171.3.136/api/v1/auth/register';
        const getFormDataAsJson = () => {
            const { username, password, email, role } = formdata;
            // return ({ username, password, email, role });
            return JSON.stringify({ username, password, email, role });
        };
        const jsonData = getFormDataAsJson();
        // const jsonData = JSON.stringify(formdata);
        // let a = JSON.stringify({ username: "sss33ss@gmail.com", email: "sss33ss@gmail.com", password: "sssss@gmail.com", role: "PLAYER" })
        // alert(a);
        console.log(jsonData);
        fetch(url, {
            method: 'POST',
            body: jsonData,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                // setToken(JSON.stringify(data['access_token']));
                localStorage.setItem('token', JSON.stringify(data['access_token']))
                alert('token saved');
                alert(localStorage.getItem('token'))

            })
            .catch((error) => {
                console.error('Error:', error.message);
                // Handle other errors (e.g., network issues)
            })

    }

    return (
        <>
            <div class="login-page">
                <div class="form">
                    <form class="register-form">
                        <input type="text" placeholder="имя пользователя" value={formdata.username} onChange={(e) => setFormdata({ ...formdata, username: e.target.value })} />
                        <input type="password" placeholder="пароль (не менее 6 символов)" value={formdata.password} onChange={(e) => setFormdata({ ...formdata, password: e.target.value })} />
                        <input type="email" placeholder="электронная почта" value={formdata.email} onChange={(e) => setFormdata({ ...formdata, email: e.target.value })} />
                        <input type="text" placeholder="роль" value={formdata.role} onChange={(e) => setFormdata({ ...formdata, role: e.target.value })} />
                        <button type="button" onClick={handleSubmit}>create</button>
                        <p class="message">Already registered? <a href="/Login">Sign In</a></p>
                    </form>
                </div>
            </div >
        </>
    )
}

export default Registration