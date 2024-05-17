import { useEffect, useState } from "react";
import securedFetch from './utils';

const Leaderboard = () => {
    const [leaderboard, setLeaderboard] = useState([]);

    useEffect(() => {
        const fetchLeaderboard = async () => {
            try {
                const response = await securedFetch('http://localhost:1234/api/v1/tournaments/leaderboard');
                setLeaderboard(response.data);
            } catch (error) {
                console.error('Error fetching leaderboard:', error);
            }
        };

        fetchLeaderboard();
    }, []);

    return (
        <>
            <h1>Лидерборд</h1>
            <table>
                <thead>
                    <tr>
                        <th>Место</th>
                        <th>Имя пользователя</th>
                        <th>Очки</th>
                    </tr>
                </thead>
                <tbody>
                    {leaderboard.length > 0 ? (
                        leaderboard.map((user, index) => (
                            <tr key={user.id}>
                                <td>{index + 1}</td>
                                <td>{user.username}</td>
                                <td>{user.scores}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="3">Нет данных для отображения</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </>
    );
};

export default Leaderboard;
