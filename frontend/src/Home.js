import { useEffect, useState } from "react"
import Match from './Match';

const Home = () => {
    const [name, setName] = useState([]);
    const url = 'http://213.171.3.136/api/v1/tournament'
    useEffect(() => {
        fetch(url, {
            method: "GET"
        }).then(response => response.json())
            .then(data => {
                setName(data);
            })
    }, [])
    return (
        <>
            <h1>
                Результаты матчей
            </h1>
            <table id="tournaments">
                {
                    name.map(r => (
                        <Match s={r} />
                    ))
                }
            </table>
        </>
    )
}

export default Home