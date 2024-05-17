import { useEffect, useState, useCallback, useMemo } from "react";
import { useNavigate } from 'react-router-dom';
import TournamentComponent from './TournamentComponent';
import securedFetch from './utils';
import CreateTournamentModal from './CreateTournamentModal';

const Home = () => {
    const [tournaments, setTournaments] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false); 
    const navigate = useNavigate();  // Хук для навигации
    const url = 'http://localhost:1234/api/v1/tournaments/';

    useEffect(() => {
        const fetchTournaments = async () => {
            try {
                const response = await securedFetch(url);  // Дожидаемся результата
                setTournaments(response.data);  // Обновляем состояние
            } catch (error) {
                console.error('Error fetching tournaments:', error);
            }
        };
        fetchTournaments();
    }, []);

    const handleCreateTournament = useCallback((response) => {
        setTournaments(prevTournaments => [...prevTournaments, response.data]);
        navigate(`/tournaments/${response.data.id}`);
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user_id');
        navigate('/login');
    };

    const renderedTournaments = useMemo(() => {
        return tournaments.length > 0 ? (
            tournaments.map(tournament => (
                <TournamentComponent key={tournament.id} s={tournament} />
            ))
        ) : (
            <tr>
                <td colSpan="5">Нет доступных турниров</td>
            </tr>
        );
    }, [tournaments]);

    return (
        <>
            <h1>Турниры</h1>
            <button className="logout-button" onClick={handleLogout}>Выйти</button>
            <button onClick={() => setIsModalOpen(true)}>Создать турнир</button>
            <button onClick={() => navigate('/leaderboard')}>Лидерборд</button>
            <table id="tournaments">
                <thead>
                    <tr>
                        <th>Название</th>
                        <th>Адрес</th>
                        <th>Дата начала</th>
                        <th>Победитель</th>
                        <th>Статус</th>
                    </tr>
                </thead>
                <tbody>
                    {renderedTournaments}
                </tbody>
            </table>
            {isModalOpen && <CreateTournamentModal onClose={() => setIsModalOpen(false)} onCreate={handleCreateTournament} />}
        </>
    );
}

export default Home;
