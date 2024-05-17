import { useEffect, useState } from "react";
import { parseISO, format } from 'date-fns';
import { useParams, useNavigate } from "react-router-dom";
import securedFetch from "./utils";

const Tournament = () => {
    const formatDateTime = (date) => {
        try {
            const parsedDate = parseISO(date);
            return format(parsedDate, 'dd.MM.yyyy');
        } catch {}
    };

    const navigate = useNavigate();
    const currentUserId = localStorage.getItem('user_id');
    const { tournamentId } = useParams();
    const [isParticipating, setIsParticipating] = useState(false);
    const [isManager, setIsManager] = useState(false);
    const [datas, setDatas] = useState({
        address: '',
        title: '',
        starts_at: '',
        winner: '',
        status: '',
        players_count: '',
        description: '',
        players: [],
    });
    const url = 'http://localhost:1234/api/v1/tournaments/' + tournamentId;

    useEffect(() => {
        const fetchData = async () => {
            const response = await securedFetch(url);
            if (response.status === 404) {
                navigate('/not-found');
                return;
            }
            const data = response.data;
            setDatas(data);
            const userIsParticipating = data.players.some(player => player.id === currentUserId);
            setIsManager(data.manager.id === currentUserId);
            setIsParticipating(userIsParticipating);
        };
        fetchData();
    }, [navigate, url, currentUserId]);

    const handleViewMatches = () => {
        navigate(`/tournaments/${tournamentId}/matches`);
    };

    const handleJoinTournament = async () => {
        try {
            const joinUrl = `http://localhost:1234/api/v1/tournaments/${tournamentId}/join`;
            const response = await securedFetch(joinUrl, { method: 'POST' });
            if (!response.ok) {
                throw new Error(response.data.detail);
            }
            const updatedData = response.data;
            const userIsParticipating = updatedData.players.some(player => player.id === currentUserId);
            setIsParticipating(userIsParticipating);
            setDatas(updatedData);
        } catch (error) {
            console.error('Error joining tournament:', error);
            alert('Failed to join the tournament: ' + error.message);
        }
    };

    const handleStartTournament = async () => {
        try {
            const startUrl = `http://localhost:1234/api/v1/tournaments/${tournamentId}/start`;
            const response = await securedFetch(startUrl, { method: 'POST' });
            if (!response.ok) {
                throw new Error(response.data.detail);
            }
            const updatedData = response.data;
            setDatas(updatedData);
            alert('Tournament has started!');
        } catch (error) {
            console.error('Error starting tournament:', error);
            alert('Failed to start the tournament: ' + error);
        }
    };

    if (datas.winner) {
        datas.winner = datas.winner.username;
    } else {
        datas.winner = "Еще не определен";
    }

    return (
        <>
            <div>
                <h1>Турнир {datas.title}</h1>
                <h2>Место проведения: {datas.address}</h2>
                <h2>Дата начала: {formatDateTime(datas.starts_at)}</h2>
                <h2>Описание: {datas.description}</h2>
                <h2>Количество игроков: {datas.players_count}</h2>
                <h2>Статус: {datas.status}</h2>
                <h2>Победитель: {datas.winner}</h2>
            </div>
            <div className="button-container">
                <button className="tour_buttons" onClick={handleJoinTournament} disabled={isParticipating}>
                    {isParticipating ? "Вы участвуете" : "Вступить"}
                </button>
                {isManager && datas.status === "WAITING" && (
                    <button className="tour_buttons" onClick={handleStartTournament}>
                        Начать турнир
                    </button>
                )}
                <button className="tour_buttons" onClick={handleViewMatches}>
                    Смотреть матчи
                </button>
            </div>
            <div>
                <h3>Список игроков:</h3>
                <ol>
                    {datas.players.map((player, index) => (
                        <li key={player.id}>{index+1}.{player.username}</li>
                    ))}
                </ol>
            </div>
        </>
    );
}

export default Tournament;
