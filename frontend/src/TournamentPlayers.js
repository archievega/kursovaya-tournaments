import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const TournamentPlayers = () => {
    const { tournamentId } = useParams();
    const [datas, setDatas] = useState(
        {
            players: [],
            title: ''
        }
    );
    const url = 'http://213.171.3.136/api/v1/tournament/' + tournamentId + '/players'
    useEffect(() => {
        fetch(url, {
            method: 'GET'
        }).then(response => response.json())
            .then(data => {
                setDatas(data);
                // console.log(data.players[1].username)
            })
    }, [])
    return (
        <>
            <h1>Турнир: {datas.title}</h1>
            <h2>Список игроков:</h2>
            <table>
                {datas.players.map((m) => <td> {m.username} </td>)}
            </table>
        </>
    )
}

export default TournamentPlayers;