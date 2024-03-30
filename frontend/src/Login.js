import { useState } from "react"
import { useCookies } from 'react-cookie';


const Login = () => {
    const [token, setToken] = useState();
    const [cookies, setCookie] = useCookies(['token']);
    const [formdata, setFormdata] = useState({
        password: 'asfa21213fsasadsf',
        username: 'sdfdsdads11c1sgs@gmail.com',
    })
    const handleSubmit = () => {
        const url = 'http://213.171.3.136/api/v1/auth/login';

        // const jsonData = JSON.stringify(formdata);
        // let a = JSON.stringify({ username: "sss33ss@gmail.com", email: "sss33ss@gmail.com", password: "sssss@gmail.com", role: "PLAYER" })
        // alert(a);
        var formBody = [];
        for (var property in formdata) {
            var encodedKey = encodeURIComponent(property);
            console.log(encodedKey);
            var encodedValue = encodeURIComponent(formdata[property]);
            formBody.push(encodedKey + "=" + encodedValue);
        }
        console.log(formdata);
        formBody = formBody.join("&");
        fetch(url, {
            method: 'POST',
            body: formBody,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            }
        })
            .then(response => response.json())
            .then(data => {
                // setToken(JSON.stringify(data['access_token']));
                localStorage.setItem('token', JSON.stringify(data['access_token']))
                window.location.href = '/tournaments'
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
                    <form class="login-form" id="login-form">
                        <input type="email" placeholder="электронная почта" value={formdata.username} onChange={(e) => setFormdata({ ...formdata, email: e.target.value })} />
                        <input type="password" placeholder="пароль (не менее 6 символов)" value={formdata.password} onChange={(e) => setFormdata({ ...formdata, password: e.target.value })} />
                        <button type="button" onClick={handleSubmit}>login</button>
                        <p class="message">Not registered? <a href="/registration">Create an account</a></p>
                    </form>
                </div>
            </div >
        </>
    )
}

export default Login