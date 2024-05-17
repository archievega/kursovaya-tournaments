import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import securedFetch from "./utils";

const TournamentMatches = () => {
    const navigate = useNavigate();
    const { tournamentId } = useParams();
    const currentUserId = localStorage.getItem('user_id');
    const [isManager, setIsManager] = useState(false);
    const [matchesByRound, setMatchesByRound] = useState({});

    const url = `http://localhost:1234/api/v1/tournaments/${tournamentId}/matches`;

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await securedFetch(url);
                if (response.status === 404) {
                    navigate('/not-found');
                    return;
                }
                const data = response.data;
                setIsManager(data.manager.id === currentUserId);

                // Группируем матчи по раундам
                const groupedMatches = data.matches.reduce((acc, match) => {
                    const round = match.round;
                    if (!acc[round]) {
                        acc[round] = [];
                    }
                    acc[round].push(match);
                    return acc;
                }, {});

                setMatchesByRound(groupedMatches);
            } catch (error) {
                console.error('Error fetching matches data:', error);
            }
        };
        fetchData();
    }, [navigate, url, currentUserId]);

    const handleSetScores = async (matchId, player1Scores, player2Scores) => {
        try {
            const setScoresUrl = `http://localhost:1234/api/v1/tournaments/${tournamentId}/matches/${matchId}/set`;
            const response = await securedFetch(setScoresUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    player_1_scores: player1Scores,
                    player_2_scores: player2Scores
                })
            });
            if (!response.ok) {
                throw new Error('Failed to set scores');
            }
            const updatedMatch = response.data;
            setMatchesByRound(prevMatchesByRound => {
                const updatedMatches = { ...prevMatchesByRound };
                const roundMatches = updatedMatches[updatedMatch.round].map(match =>
                    match.id === updatedMatch.id ? updatedMatch : match
                );
                updatedMatches[updatedMatch.round] = roundMatches;
                return updatedMatches;
            });
            alert('Scores updated!');
        } catch (error) {
            console.error('Error setting scores:', error);
            alert('Failed to set scores: ' + error.message);
        }
    };

    return (
        <>
            <h1>Матчи турнира</h1>
            {Object.keys(matchesByRound).length === 0 ? (
                <p>Нет матчей для отображения</p>
            ) : (
                Object.keys(matchesByRound).sort().map(round => (
                    <div key={round} className="round">
                        <h2>Раунд {parseInt(round)+1}</h2>
                        <div className="matches">
                            {matchesByRound[round].map(match => (
                                <div key={match.id} className="match">
                                    <div className="match-info">
                                        <p>Игрок 1: {match.player_1.username} ({match.player_1_scores})</p>
                                        {match.player_2 && (
                                            <p>Игрок 2: {match.player_2.username} ({match.player_2_scores})</p>
                                        )}
                                        <p>Победитель: {match.winner ? match.winner.username : "Еще не определен"}</p>
                                    </div>
                                    {isManager && match.player_2 && !(match.winner) && (
                                        <div className="match-scores">
                                            <input
                                                type="number"
                                                placeholder="Очки игрока 1"
                                                defaultValue={match.player_1_scores}
                                                onChange={(e) => match.player_1_scores = parseInt(e.target.value)}
                                            />
                                            <input
                                                type="number"
                                                placeholder="Очки игрока 2"
                                                defaultValue={match.player_2_scores}
                                                onChange={(e) => match.player_2_scores = parseInt(e.target.value)}
                                            />
                                            <button
                                                onClick={() => handleSetScores(match.id, match.player_1_scores, match.player_2 ? match.player_2_scores : 0)}
                                                disabled={!match.player_2}
                                            >
                                                Обновить очки
                                            </button>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                ))
            )}
        </>
    );
}

export default TournamentMatches;
