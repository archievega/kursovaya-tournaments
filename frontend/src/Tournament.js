import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const Tournament = () => {
    const { tournamentId } = useParams();
    const [datas, setDatas] = useState({
        address: '',
        title: '',
        winner: '',
        status: '',
        members_count: '',
        description: '',
    })
    const url = 'http://213.171.3.136/api/v1/tournament/' + tournamentId
    useEffect(() => {
        fetch(url, {
            method: 'GET'
        }).then(response => response.json())
            .then(data => {
                setDatas(data);
                // console.log(data)
            })
    }, [])
    if (datas.winner) {
        datas.winner = datas.winner.username
    }
    else {
        datas.winner = "определяется..."
    }
    return (
        <>
            <div>
                <h1>Турнир {datas.title}</h1>
                <h2>Место проведения: {datas.address}</h2>
                <h2>Описание: {datas.description}</h2>
                <h2>Количество игроков: <a href={"/tournaments/" + tournamentId + "/players"}>{datas.players_count}</a></h2>
                <h2>Статус: {datas.status}</h2>
                <h2>Победитель: {datas.winner}</h2>
            </div>
            <button>Вступить</button>
        </>
    )
}

export default Tournament